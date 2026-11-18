# MCP Deployment and Network Capability Plan

## Runtime Placement

`vm-mcp` (`192.168.0.117`) is the dedicated integration plane. MCP modules may
run as separate processes for dependency and failure isolation while remaining
one managed capability catalog for the coordinator and skills.

## Active Homelab Module

The central Streamable HTTP endpoint is:

```text
http://192.168.0.117:8765/mcp
```

Validated tools:

- `service_status`
- `worker_status`
- `recent_tasks`
- `task_status`
- `list_runbooks`
- `read_runbook`
- `metric`

A real MCP client successfully initialized, listed all seven tools, and called
service and worker status after migration.

## Arista EOS Module

Pinned implementation: `x86taka/arista-eos-mcp` v1.0.0. The release checksum
was verified before installation.

Supported read-only protocols and capabilities:

- EOS eAPI over HTTPS;
- gNMI Get and Capabilities;
- curated show datasets;
- interfaces and running-configuration retrieval;
- explicit guards against configuration mode, writes, reloads, clears, copies,
  shell access, and other state changes.

Installed path:

```text
/opt/yotoconn-mcp/bin/arista-eos-mcp
```

Systemd unit:

```text
yotoconn-arista-mcp.service
```

Planned internal endpoint:

```text
http://127.0.0.1:8766
```

The service is disabled until an authorized device inventory exists at
`/etc/yotoconn/arista-devices.json`. Dynamic/ad-hoc targets remain disabled.
Credentials must come from OpenBao and never from either skills repository.

## Protocol Policy

Add protocols because a managed system requires them, not to maximize protocol
count. Initial priorities are eAPI/HTTPS and gNMI for Arista, REST/OpenAPI for
approved services, SNMPv3 read-only for legacy telemetry, and SSH only through
curated command allowlists. NETCONF and RESTCONF are added when an identified
platform and tested skill require them.

## Relationship to Skills

MCP tools are reusable capabilities. Skills are tested operating procedures that
select and compose those tools. Twenty skills should not create twenty servers.
Role assignment and tool filtering prevent every agent from seeing every tool.

## Remaining Production Controls

1. Put MCP behind HTTPS on port 443.
2. Add client identity and scoped authorization.
3. Add namespaced tool discovery and per-agent filtering.
4. Export request, error, duration, and tool metrics to Prometheus.
5. Record skill version and tool calls in the PostgreSQL ledger.
6. Add approval gates before any future write-capable module.
7. Add rate limits, bounded outputs, timeouts, and circuit breakers.
