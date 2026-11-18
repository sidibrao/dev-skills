# Skill Supply-Chain and Runtime Security

Skills are executable influence. Treat every skill like a software dependency.

## Repository Rules

- Never commit credentials, tokens, private keys, customer data, or raw production output.
- Pin and review external dependencies; record licenses and provenance.
- Inspect every imported skill and script. Popularity is not trust evidence.
- Require pull-request review and passing checks before production promotion.
- Protect the production branch and restrict release approval.

## Runtime Rules

- OpenBao supplies credentials at runtime; prompts and skills never receive secrets.
- Each agent receives a scoped identity and only its required tools.
- Read-only tools are the default. Write tools require authorization and approval.
- Allowlist targets, protocols, commands, REST operations, and metric queries.
- Log task, agent, skill version, tool, target, approval, result, and duration.
- Apply timeouts, result limits, rate limits, and output sanitization.
- Treat MCP results, device banners, documents, and retrieved text as untrusted.

## Network Boundary

Initial Arista capabilities are read-only eAPI and gNMI. Block configuration mode,
file writes, reloads, clears, shell access, arbitrary commands, and arbitrary URLs.
SNMP is read-only. Add NETCONF or RESTCONF only for an identified use case.
