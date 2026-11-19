# YoToConn AI Agent Lab Inventory

Last verified: 2026-11-18 (America/Toronto)

## Architecture

```text
Web / future Telegram
        |
        v
vm-admin-110: portal, coordinator, ledger, model gateway, queues
        |
        +---- Redis task streams ----> specialist workers .111-.115
        |
        +---- MCP requests ----------> vm-mcp .117
        |                                |-- homelab MCP
        |                                |-- Arista EOS MCP module
        |                                |-- ZeusCloud / Cartography
        |                                |-- Steampipe and audit reports
        |
        +---- metrics ----------------> vm-obs .116

vm-secrets .115 supplies runtime secrets through OpenBao.
.250 remains the human Codex and VS Code administration workstation.
```

## Virtual Machines

| IP | Hostname | Resources | Role | Primary services |
|---|---|---:|---|---|
| `192.168.0.110` | `vm-admin-110` | 4 vCPU, 16 GB, 55 GB | Control plane | Portal, agent console, PostgreSQL 16, Redis 7, LiteLLM, Nginx, metrics exporter |
| `192.168.0.111` | `vm-it` | 2 vCPU, 8 GB, 40 GB | IT worker | Worker daemon, node exporter |
| `192.168.0.112` | `vm-mkt` | 2 vCPU, 8 GB, 40 GB | Marketing worker | Worker daemon, node exporter |
| `192.168.0.113` | `vm-sup` | 2 vCPU, 8 GB, 40 GB | Support worker | Worker daemon, node exporter |
| `192.168.0.114` | `vm-worker-1` | 2 vCPU, 8 GB, 40 GB | General/reviewer | Worker daemon, node exporter |
| `192.168.0.115` | `vm-secrets` | 2 vCPU, 8 GB, 45 GB | Secrets and worker | OpenBao 2.7, worker daemon, node exporter |
| `192.168.0.116` | `vm-obs` | 2 vCPU, 8 GB, 40 GB | Observability | Prometheus, Grafana OSS, node exporter |
| `192.168.0.117` | `vm-mcp` | 2 vCPU, 8 GB, 40 GB | Integration and execution | Central MCP, Arista module, ZeusCloud, Steampipe, security reports |
| `192.168.0.250` | `SID-Linux-VM1` | 8 GB, 34 GB root + 42 GB data | Human administration | Codex, code-server, desktop, Nginx, SSH |

All AI service VMs are on ESXi `datastoreTB`. The `.250` administration VM
remains on `datastore1` because moving its storage requires shutting down the
machine running the administrative session.

## Service Endpoints

| Service | Endpoint | Status |
|---|---|---|
| Web portal | `https://192.168.0.110/` | Active |
| LiteLLM gateway | `http://192.168.0.110:4000` | Active |
| Redis | `192.168.0.110:6379` | Active |
| PostgreSQL ledger | `192.168.0.110:5432` | Active |
| OpenBao | `https://192.168.0.115:8200` | Active, initialized and unsealed |
| Grafana | `http://192.168.0.116:3000` | Active |
| Prometheus | `http://192.168.0.116:9090` | Active |
| Central homelab MCP | `http://192.168.0.117:8765/mcp` | Active |
| Arista EOS MCP | `127.0.0.1:8766` on `.117` | Installed; activation awaits target credentials |
| ZeusCloud | `http://192.168.0.117:9080` | Active, HTTP 200 |
| Security reports | `http://192.168.0.117:8099` | Active, HTTP 200 |
| Steampipe database | `127.0.0.1:9193` on `.117` | Active |
| Powerpipe | `192.168.0.117:9033` when enabled | Installed, disabled to preserve prior state |
| code-server | `https://192.168.0.250:8088` | Active |

## Migration Status

- Homelab MCP migrated from `.110` to `.117`; old service is disabled and retained for rollback.
- ZeusCloud code, PostgreSQL, Neo4j, Cartography, backend, frontend and proxy migrated from `.250` to `.117`.
- The inherited Neo4j health check was corrected from unavailable `curl` to `wget`; database and health status pass.
- ZeusCloud AWS credentials were placed in OpenBao KV at `secret/zeuscloud/aws` and materialized on `.117` with restricted permissions for compatibility.
- Steampipe, Powerpipe files, and security-audit reports migrated from `.250` to `.117`.
- Duplicate `.250` LiteLLM and Redis are stopped with restart disabled; canonical services remain on `.110`.
- All `.250` ZeusCloud containers are stopped with restart disabled. Source files and migration archives remain for rollback.
- `.250` user services for Steampipe, Powerpipe and security reports are disabled and stopped.

## Current Constraints

- MCP port `8765` is currently plain HTTP on the trusted lab LAN. HTTPS gateway and client authentication remain required before external exposure.
- Arista EOS MCP requires an authorized EOS management IP, read-only username and secret before activation.
- Powerpipe remains disabled because it was not active before migration.
- Source rollback data has not been deleted.
