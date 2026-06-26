# Fix Issue

Use this skill when implementing a fix for a GitHub issue.

Follow `AGENTS.md` as the rule source.

## Workflow

1. Read the issue and related analysis.
2. Check the current working tree and fetch the latest remote refs.
3. Identify the minimal affected contract across runtime, API/Web, CLI,
   diagnostics, workflow, docs, and tests.
4. Implement the fix without unrelated refactors.
5. Add or update regression tests for the reported failure mode.
6. Run the closest verification commands.
7. Update docs and `docs/CHANGELOG.md` when behavior is user-visible.

## Delivery Notes

Explain:

- original problem
- root cause
- fix
- verification
- unverified gaps
- risk
- rollback path

Do not patch only the single line mentioned in review if the same semantic issue
exists in other entry points.
