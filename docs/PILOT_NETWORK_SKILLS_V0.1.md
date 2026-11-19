# Network Skills Pilot v0.1 Test Record

## Scope

This pilot adds development versions of `bgp-troubleshooting` and
`arista-eos-health`. Neither skill is production-approved.

## Implemented

- Portable `SKILL.md` entrypoints with YoToConn ownership and risk metadata.
- Progressive references for BGP decisions, adapter mapping, health checks, and provenance.
- Report templates that separate observations, hypotheses, unknowns, and evidence.
- Twelve behavioral evaluation definitions: six per skill.
- Nine deterministic synthetic scenarios, including Arista and mock non-Arista data.
- A mock MCP policy layer that authorizes the target before tool use and rejects
  operations outside a read-only allowlist.
- CI execution of structural validation and offline contract tests.

## Verification Results

Run on 2026-11-18:

| Check | Result |
| --- | --- |
| Repository structural validator | Pass |
| Nine fixture status/evidence checks | Pass |
| Skill selection boundaries | Pass |
| Unauthorized target blocked before tool call | Pass |
| Write operation blocked | Pass |
| Partial timeout does not claim BGP state | Pass |
| Active plus missing route retains uncertainty | Pass |

## Explicitly Not Tested

- Live device access, live MCP transport, or device credentials.
- An LLM selecting or executing the skills.
- Accuracy against real EOS output variants.
- A production non-Arista adapter.
- Portal, Redis worker, approval-ledger, or long-term trace integration.

## Next Approval Gates

1. Review and merge the skills-standard pull request on which this pilot depends.
2. Review this pilot's tool boundary, fixtures, and reports.
3. Run model-based evaluations against synthetic data and retain outputs.
4. Configure an approved test target and restricted MCP identity.
5. Request separate approval for a live read-only test.
6. Add failures as regression fixtures before any production promotion.
