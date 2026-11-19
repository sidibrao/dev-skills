#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

from mock_network_skill_runner import MockMCP, PolicyError, run_scenario, select_skill

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = json.loads((ROOT / "tests/fixtures/network_scenarios.json").read_text())["scenarios"]


class NetworkSkillContractTests(unittest.TestCase):
    def test_all_nine_scenarios(self):
        self.assertEqual(9, len(SCENARIOS))
        for scenario in SCENARIOS:
            with self.subTest(scenario=scenario["id"]):
                report, mcp = run_scenario(scenario)
                self.assertEqual(scenario["expected_status"], report["status"])
                if scenario["authorized"]:
                    self.assertTrue(report["evidence"])
                    self.assertTrue(all(any(eid == call["evidence_id"] for call in mcp.calls) for eid in report["evidence"]))
                else:
                    self.assertEqual([], mcp.calls)

    def test_active_missing_route_is_evidence_backed_and_uncertain(self):
        scenario = next(x for x in SCENARIOS if x["id"] == "bgp-active-missing-route")
        report, _ = run_scenario(scenario)
        self.assertTrue(any("Route to peer present: False" in x for x in report["observations"]))
        self.assertTrue(any("Possible" in x and "unproven" in x for x in report["hypotheses"]))

    def test_write_and_unauthorized_calls_are_blocked(self):
        allowed = MockMCP({"leaf1"})
        with self.assertRaisesRegex(PolicyError, "read-only"):
            allowed.call("arista-eos.configure", "leaf1", {"command": "clear ip bgp *"})
        denied = MockMCP(set())
        with self.assertRaisesRegex(PolicyError, "authorized"):
            denied.call("arista-eos.get_show_data", "unknown", {"topic": "bgp_summary"})
        self.assertEqual([], allowed.calls)
        self.assertEqual([], denied.calls)

    def test_skill_selection(self):
        self.assertEqual("bgp-troubleshooting", select_skill("Diagnose BGP peer 192.0.2.6 in Active"))
        self.assertEqual("arista-eos-health", select_skill("Create an Arista EOS health report"))
        self.assertIsNone(select_skill("Write a switch replacement business case"))

    def test_partial_result_does_not_claim_state(self):
        scenario = next(x for x in SCENARIOS if x["id"] == "bgp-partial-timeout")
        report, _ = run_scenario(scenario)
        self.assertEqual("partial", report["status"])
        self.assertIn("peer state and route exchange", report["unknowns"])
        self.assertFalse(any("BGP state is" in x for x in report["observations"]))


if __name__ == "__main__":
    unittest.main()
