# Skills Architecture

```text
dev-skills
  draft -> validate -> evaluate -> security review -> human approval
                                                    |
                                                    v
ag-skills
  approved release -> runtime catalog -> assigned agents
                                           |
                                           v
                              one logical MCP endpoint
                                           |
                       policy -> audit -> capability modules
```

The repositories do not contain MCP implementations. The centralized MCP service
on `vm-mcp` exposes approved capabilities; skills compose them into repeatable
jobs. This lets many skills reuse a smaller set of governed tools.

Only metadata is loaded for discovery. Full instructions load after a match, and
references load only when required.
