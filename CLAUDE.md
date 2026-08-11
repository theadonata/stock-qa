# CLAUDE.md

This is the **QA/testing** repo for the Stock/HPP business-finance project.

## Project status

No test framework or tooling has been chosen yet and no test code exists.
Don't assume one — ask the user before scaffolding anything.

## Relationship to sibling repos

This project is split across independent repos, each buildable and
deployable on its own with no shared code or path dependency between them:

- `stock-frontend` — client-side UI
- `stock-backend` — API / business logic / data layer
- `stock-infrastructure` — CI/CD, deployment, IaC
- `stock-qa` (this repo) — test plans, test automation
- `stock-business-analyst` — requirements, specs, source material (incl. the original HPP/business-finance notes)

Tests here target the other repos' deployed/published outputs (API
endpoints, built UI), not their source trees directly, so this repo never
needs to be co-located with them.

## Working here

`.claude/` config (agents, hooks, skills, MCP) is kept identical across all
five repos on purpose, so any agent persona works the same way regardless of
which repo it's invoked in. Once a stack is chosen, update this file with
real test/run commands.
