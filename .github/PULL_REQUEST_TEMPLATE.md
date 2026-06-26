## Summary

Describe the current problem, affected scope, and triggering scenario.

## Changes

List the actual files or areas changed. Include the file count when the diff is
large so docs, backend, API, frontend, and workflow changes stay aligned.

Recommended local context commands:

```bash
git status --short
git diff --stat
```

## Type

- [ ] fix
- [ ] feat
- [ ] refactor
- [ ] docs
- [ ] test
- [ ] ci
- [ ] chore

## Compatibility

Explain whether this changes any of the following:

- runtime configuration save, cleanup, migration, or backfill behavior
- provider, model, Base URL, LiteLLM, or fallback semantics
- API schemas or Web/Desktop contracts
- report structure, notification routing, or prompt behavior
- workflow, release, Docker, or deployment behavior

If compatibility is intentionally unchanged, state that explicitly.

## Verification

List the commands you actually ran and the key result. Do not write only
"tested".

```bash
# example
python -m pytest -m "not network"
```

For report rendering or Web UI changes, attach affected screenshots in the PR
description, PR comments, GitHub attachments, Actions artifacts, or another
reviewable evidence link. Do not commit temporary review screenshots.

## Third-Party Or Model Compatibility

If this PR changes third-party model fallback, provider behavior, model names, or
dependency windows such as LiteLLM, include official source links or
announcements and explain whether the constraint is long-term, runtime-only, or
a temporary compatibility workaround.

## Rollback

Describe the smallest rollback path. For compatibility fixes, include whether
old configuration is automatically rewritten, cleared, migrated, or preserved,
and how users can restore the old behavior.

## Checklist

- [ ] The PR scope is minimal for the stated problem.
- [ ] Tests or documented verification cover the changed behavior.
- [ ] Docs and `.env.example` are updated when configuration or user-visible
      behavior changes.
- [ ] `docs/CHANGELOG.md` is updated for user-visible changes.
- [ ] Secrets, account data, and private endpoints are not committed.
