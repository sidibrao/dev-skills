# Network Skills Offline Tests

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

This deterministic harness validates structure, basic selection, mock adapter
contracts, authorization order, read-only policy, partial results, and evidence
linkage. It does not validate live MCP transport, real devices, credentials, LLM
quality, or production readiness.
