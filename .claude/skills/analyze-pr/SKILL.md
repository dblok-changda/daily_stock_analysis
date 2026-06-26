# Analyze PR

Use this skill when reviewing a GitHub pull request.

Follow `AGENTS.md` as the rule source.

## Workflow

1. Check the working tree.
2. Fetch all remote refs with prune.
3. Fast-forward the current branch only when the working tree is clean and the
   branch can move safely.
4. Inspect PR metadata, title, body, changed files, CI evidence, and the diff.
5. Read source, tests, docs, scripts, and workflow files affected by the same
   business contract.
6. Save review notes under `.claude/reviews/`.

## Review Order

1. Necessity
2. Relevance
3. Title recommendation
4. PR body completeness
5. Verification evidence
6. Implementation correctness
7. Merge decision

Lead with blockers. Put non-blocking style or evidence gaps under suggestions.
Do not treat CI success as proof that semantic review concerns are resolved.
