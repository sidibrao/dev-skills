# YoToConn Development Skills

`dev-skills` is the development and evaluation workspace for YoToConn Agent
Skills. Content in this repository is **not production-approved**.

## Purpose

- Draft and improve reusable skills for IT operations, networking, business,
  marketing, support, and platform administration.
- Keep deterministic helpers, references, fixtures, and behavioral evaluations
  beside each skill.
- Prove selection accuracy, output quality, safety, and tool boundaries before
  promotion.
- Submit approved releases to [`sidibrao/ag-skills`](https://github.com/sidibrao/ag-skills).

## Repository Layout

```text
skills/<skill-name>/
  SKILL.md                 Required portable entrypoint
  scripts/                 Optional deterministic helpers
  references/              Optional detail loaded only when needed
  assets/                  Optional output templates and static resources
  evals/evals.json         Required YoToConn behavioral evaluations
docs/                      Standards, architecture, security, and promotion
templates/                 Skill and evaluation starters
scripts/                   Repository validation
tests/                     Synthetic MCP contract tests
```

## Development Workflow

1. Create a branch from `main`.
2. Define the job, trigger boundary, inputs, evidence, tools, risk, and expected output.
3. Add the skill under `skills/<name>/` using the template.
4. Add realistic positive, negative, failure, and authorization evaluations.
5. Run `python3 scripts/validate_skills.py`.
6. Test against synthetic or explicitly authorized targets.
7. Open a pull request and attach test evidence.
8. Promote the reviewed commit using [docs/PROMOTION.md](docs/PROMOTION.md).

## Current Status

The development factory is initialized. No skill is production-approved yet.
Development pilots for `bgp-troubleshooting` and `arista-eos-health` have
deterministic synthetic coverage. See
[the pilot test record](docs/PILOT_NETWORK_SKILLS_V0.1.md). Live-device testing
requires separate approval.

## Principles

- One coherent, repeatable job per skill.
- Skills describe procedure; MCP servers provide capabilities.
- Read-only network observation is the default.
- A skill never grants infrastructure access or contains credentials.
- Evidence beats confident language.
- Every failure becomes a focused regression evaluation.
- Keep `SKILL.md` concise and load detailed references progressively.

See [docs/SKILLS_STANDARD.md](docs/SKILLS_STANDARD.md) for normative rules.
