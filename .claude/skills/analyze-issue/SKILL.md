# Analyze Issue

Use this skill when reviewing a GitHub issue for scope, reproducibility,
technical risk, and implementation readiness.

Follow `AGENTS.md` as the rule source.

## Workflow

1. Check the working tree.
2. Fetch the latest remote refs.
3. If the working tree is clean and the branch can fast-forward, update the local
   branch with `git pull --ff-only`.
4. Read the issue, related discussions, linked PRs, CI evidence, and relevant
   source/docs/tests.
5. Write the analysis under `.claude/reviews/`.

## Output

Include:

- issue summary
- suspected root cause or knowledge gap
- affected paths
- required verification
- implementation recommendation
- risks and rollback notes

Do not force checkout, stash, reset, push, or otherwise overwrite local work.
