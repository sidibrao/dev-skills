#!/usr/bin/env python3
"""Deterministic contract harness; not a live MCP or LLM evaluation."""

from dataclasses import dataclass, field
from typing import Any

READ_ONLY_TOOLS = {
    "arista-eos.get_show_data", "arista-eos.get_interfaces",
    "arista-eos.get_ip_route", "arista-eos.get_bgp_received_routes",
    "generic-approved.get_bgp_summary", "generic-approved.get_bgp_neighbor",
    "generic-approved.get_interface", "generic-approved.get_route",
}


class PolicyError(RuntimeError):
    pass


@dataclass
class MockMCP:
    authorized_targets: set[str]
    calls: list[dict[str, Any]] = field(default_factory=list)

    def call(self, tool: str, target: str, data: dict[str, Any]) -> dict[str, Any]:
        if target not in self.authorized_targets:
            raise PolicyError("target is not authorized")
        if tool not in READ_ONLY_TOOLS:
            raise PolicyError("tool is not on the read-only allowlist")
        result = {"evidence_id": f"ev-{len(self.calls) + 1:03d}", "data": data}
        self.calls.append({"tool": tool, "target": target, **result})
        return result


def select_skill(prompt: str) -> str | None:
    text = prompt.lower()
    if "bgp" in text and any(word in text for word in ("neighbor", "peer", "prefix", "active", "flap")):
        return "bgp-troubleshooting"
    if "arista" in text and any(word in text for word in ("health", "assessment", "report")):
        return "arista-eos-health"
    return None


def _tool(platform: str, arista: str, generic: str) -> str:
    return f"arista-eos.{arista}" if platform == "arista-eos" else f"generic-approved.{generic}"


def run_scenario(scenario: dict[str, Any]) -> tuple[dict[str, Any], MockMCP]:
    target, data = scenario["target"], scenario["responses"]
    mcp = MockMCP({target} if scenario["authorized"] else set())
    if not scenario["authorized"]:
        return {"status": "denied", "evidence": [], "observations": [], "hypotheses": []}, mcp

    evidence, observations, hypotheses = [], [], []
    if scenario["skill"] == "bgp-troubleshooting":
        summary = mcp.call(_tool(scenario["platform"], "get_show_data", "get_bgp_summary"), target, {"bgp_state": data.get("bgp_state")})
        evidence.append(summary["evidence_id"])
        state = data.get("bgp_state")
        if state == "timeout":
            return {"status": "partial", "evidence": evidence, "observations": ["BGP summary unavailable"], "hypotheses": [], "unknowns": ["peer state and route exchange"]}, mcp
        observations.append(f"BGP state is {state} [{summary['evidence_id']}]")
        if state != "Established":
            interface = mcp.call(_tool(scenario["platform"], "get_interfaces", "get_interface"), target, {"interface_state": data.get("interface_state")})
            route = mcp.call(_tool(scenario["platform"], "get_ip_route", "get_route"), target, {"route_to_peer": data.get("route_to_peer")})
            evidence.extend((interface["evidence_id"], route["evidence_id"]))
            observations.extend((f"Interface is {data.get('interface_state')} [{interface['evidence_id']}]", f"Route to peer present: {data.get('route_to_peer')} [{route['evidence_id']}]"))
            if data.get("route_to_peer") is False:
                hypotheses.append("Possible peer reachability or routing problem; exact cause is unproven")
            status = "critical" if data.get("interface_state") == "down" else "warning"
        else:
            received, expected = data.get("received_prefixes", 0), data.get("expected_prefixes", data.get("received_prefixes", 0))
            routes = mcp.call(_tool(scenario["platform"], "get_bgp_received_routes", "get_bgp_neighbor"), target, {"received_prefixes": received, "expected_prefixes": expected})
            evidence.append(routes["evidence_id"])
            observations.append(f"Received {received} of {expected} expected prefixes [{routes['evidence_id']}]")
            status = "healthy" if received == expected else "warning"
            if received != expected:
                hypotheses.append("Possible inbound policy or upstream advertisement issue; direction is not yet localized")
    else:
        if scenario["platform"] != "arista-eos":
            return {"status": "denied", "evidence": [], "observations": [], "hypotheses": []}, mcp
        for topic in ("version", "interfaces_status", "interface_counters", "bgp_summary"):
            result = mcp.call("arista-eos.get_show_data", target, {"topic": topic, **data})
            evidence.append(result["evidence_id"])
        observations.append(f"Health sections collected [{', '.join(evidence)}]")
        status = "warning" if any((data["interfaces_down_unexpected"], data["interface_errors"], data["bgp_peers_down"])) else "healthy"
    return {"status": status, "evidence": evidence, "observations": observations, "hypotheses": hypotheses, "unknowns": []}, mcp
