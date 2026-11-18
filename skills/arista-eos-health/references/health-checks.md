# Arista EOS Health Checks

| Section | Preferred operation | Interpretation boundary |
| --- | --- | --- |
| Platform/software | `arista-eos.get_show_data(topic=version)` | Report current facts; require a baseline to assess compliance |
| Interface status | `arista-eos.get_show_data(topic=interfaces_status)` | Down can be expected; use inventory/baseline before assigning severity |
| Error counters | `arista-eos.get_show_data(topic=interface_counters)` | A snapshot shows totals, not rate; avoid claiming active degradation without trend/baseline |
| BGP | `arista-eos.get_show_data(topic=bgp_summary)` | Non-Established is actionable only for expected peers |
| Focused interface | `arista-eos.get_interfaces(interface=...)` | Use after summary identifies a relevant interface |
| Combined overview | `arista-eos.get_device_health` | Use as an initial overview, not a substitute for cited evidence |

Severity is contextual:

- `critical`: direct evidence of a service-impacting condition against an approved baseline.
- `warning`: abnormal evidence that needs investigation but lacks proven impact.
- `healthy`: checked evidence meets the supplied expectation.
- `unknown`: required evidence is absent, stale, conflicting, or failed.
- `not assessed`: the section was outside scope.
