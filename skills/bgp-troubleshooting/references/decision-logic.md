# BGP Diagnostic Decision Logic

## Session State

| Evidence | Supported interpretation | Next read-only evidence |
| --- | --- | --- |
| Idle | Session is not progressing; cause is not yet established | Peer detail, interface, route to peer, logs |
| Connect or Active | TCP establishment is incomplete | Route to peer, source/update-source, interface, ACL counters if approved |
| OpenSent or OpenConfirm | Transport progressed; capability, ASN, timer, or authentication evidence may matter | Peer detail and logs |
| Established | Control session is up; route exchange can still be wrong | Prefix counts, received/advertised routes, policy evidence |
| Repeated transitions | A flap exists only when bounded historical evidence shows transitions | Logs or bounded telemetry plus current state |

Do not infer root cause from state alone. For example, Active plus a missing route
supports a reachability hypothesis, not proof of the exact faulty component.

## Missing Prefixes

1. Confirm the expected prefix, direction, address family, and peer.
2. Determine whether the device received or advertised it.
3. Compare relevant policy evidence when an approved read-only capability exists.
4. State whether the evidence localizes the issue to inbound policy, outbound
   policy, upstream behavior, or remains inconclusive.

## Confidence

- `high`: independent evidence directly establishes the conclusion.
- `medium`: evidence supports one leading explanation but a required check is absent.
- `low`: evidence is incomplete, conflicting, or only establishes symptoms.
