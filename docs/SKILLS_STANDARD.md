# YoToConn Skills Standard v1.0

## Scope

This standard uses the portable Agent Skills folder format and adds YoToConn
quality and governance requirements. These additions are local policy, not fields
mandated by the upstream specification.

## Portable Contract

Every skill is one directory containing `SKILL.md`. Its YAML frontmatter must contain:

```yaml
---
name: lowercase-hyphenated-name
description: What the skill does and when it should activate.
---
```

The name must match its directory and contain no leading, trailing, or repeated
hyphens. Descriptions must identify the intended request and distinguish nearby
skills when confusion is likely.

## YoToConn Quality Contract

Each production candidate must define:

1. Objective and measurable outcome.
2. Required inputs and authorization prerequisites.
3. Ordered procedure and decision points.
4. Evidence required before conclusions.
5. Approved MCP tools or other capabilities.
6. Read/write classification and approval boundary.
7. Expected output structure.
8. Failure, timeout, partial-data, and escalation behavior.
9. At least five behavioral evaluations.
10. Owner, version, risk class, and review evidence in string-valued metadata.

Recommended metadata:

```yaml
metadata:
  version: "0.1.0"
  owner: "yotoconn-network"
  risk: "read-only"
  status: "development"
```

## Progressive Disclosure

- Put routing, essential workflow, and non-negotiable constraints in `SKILL.md`.
- Put substantial vendor procedures and decision trees in `references/`.
- Put repeatable deterministic operations in `scripts/` and test them directly.
- Put report templates or files copied into outputs in `assets/`.
- Link every supporting resource from `SKILL.md` and state when to use it.
- Avoid reference chains and copied product manuals.

## Skills and MCP

A skill is procedural knowledge. MCP is the controlled capability layer. Skills
refer to stable, namespaced tools such as:

```text
network.arista.get_interfaces
network.arista.get_bgp_neighbors
network.gnmi.get
homelab.worker_status
observability.query_metric
```

Skills must not embed credentials, implement an MCP server, or assume a tool is
authorized merely because it exists. Runtime policy remains authoritative.

## Evaluations

`evals/evals.json` must contain at least five cases covering normal success,
incomplete evidence, unauthorized operation, tool failure, and a near-miss that
should not trigger the skill. Assertions test observable behavior, not exact prose.

## Versioning

Use semantic versions. Development starts at `0.1.0`. Production content must
identify the exact development commit from which it was promoted.

## Sources

- Agent Skills specification: <https://agentskills.io/specification>
- Anthropic examples: <https://github.com/anthropics/skills>
- Superpowers evaluation workflow: <https://github.com/obra/superpowers>
- Greg Isenberg skills methodology: <https://www.gregisenberg.com/skills-suite>

Greg Isenberg's methodology informs reuse, Git distribution, continuous
improvement, and one-job-per-skill. Repository separation, security review,
approval records, and release gates are YoToConn production controls.
