# Development-to-Production Promotion

`dev-skills` is the workshop. `ag-skills` is the approved release library.

## Required Gates

1. **Specification:** repository validator passes.
2. **Behavior:** realistic evaluations pass and evidence is attached.
3. **Security:** tools, scripts, dependencies, targets, and data handling are reviewed.
4. **Quality:** output is evidence-backed and within latency/cost targets.
5. **Approval:** a human approves the exact source commit and release version.

## Promotion Record

Every production pull request must state:

```text
Skill:
Version:
Development repository commit:
Evaluation artifact or run:
Security reviewer:
Approver:
Rollback version:
```

Copy only the approved skill directory. Set metadata `status` to `approved`, run
both validators, and create a release tag after merge. Never promote directly
from an uncommitted working tree.

## Rollback

Revert the production commit or restore the preceding release. Disable the skill
in the runtime catalog first when continued execution could cause harm. Add the
failure as a regression evaluation in `dev-skills`.
