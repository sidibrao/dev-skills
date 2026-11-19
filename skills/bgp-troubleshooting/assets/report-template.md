# BGP Diagnostic Report

- Target and authorization status
- Scope and stated expectation
- Current BGP state
- Observations, each linked to an evidence ID
- Hypotheses, each labeled and linked to supporting/contradicting evidence
- Conclusion and confidence (`high`, `medium`, or `low`)
- Unknowns and unavailable checks
- Safe read-only next checks
- Escalation or change-approval requirement
- Sanitized execution trace: timestamp, adapter, tool, target, result, evidence ID

Do not include credentials, full configurations, secret values, or unredacted
sensitive output in the report or trace.
