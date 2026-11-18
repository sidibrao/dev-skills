# Approved Adapter Mapping

Logical names are stable policy-facing capabilities. Runtime configuration maps
them to a deployed MCP server and remains authoritative.

## Arista EOS MCP

| Logical capability | Arista MCP operation |
| --- | --- |
| `network.inventory.list` | `arista-eos.list_devices` |
| `network.bgp.summary` | `arista-eos.get_show_data(topic=bgp_summary)` |
| `network.bgp.neighbors` | `arista-eos.get_show_data(topic=bgp_neighbors)` |
| `network.interface.detail` | `arista-eos.get_interfaces` |
| `network.interface.counters` | `arista-eos.get_show_data(topic=interface_counters)` |
| `network.route.lookup` | `arista-eos.get_ip_route` |
| `network.bgp.received` | `arista-eos.get_bgp_received_routes` |
| `network.bgp.advertised` | `arista-eos.get_bgp_advertised_routes` |
| `network.logs.recent` | `arista-eos.get_show_data(topic=logging)` |

Use `arista-eos.run_show_command` only when no curated operation can provide the
required evidence and policy explicitly allows the exact read-only command.

## Non-Arista Platforms

No generic adapter is deployed by this skill. An approved adapter must expose the
same logical evidence contract, identify the target platform, enforce read-only
operations, and normalize evidence identifiers. Synthetic tests use a mock generic
adapter only to validate this contract; they do not prove a live integration.
