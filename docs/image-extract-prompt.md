# Image Stock Extraction Prompt

`src/services/image_stock_extractor.py` contains the prompt used to extract stock
symbols and names from uploaded images.

## Contract

- The prompt should ask the model to return structured stock candidates only.
- The extractor must keep enough context to distinguish code-like numbers from
  dates, prices, percentages, and ranks.
- The output must be conservative: uncertain candidates should be marked as low
  confidence instead of forced into a stock code.
- Changes to `EXTRACT_PROMPT` are user-visible because they affect image import
  behavior.

## Review Requirement

When a PR changes `EXTRACT_PROMPT`, include the full latest prompt in the PR
description. This keeps reviewers from needing to reconstruct prompt state from a
partial diff.

## Verification

Run the extractor tests after prompt changes:

```bash
python -m pytest tests/test_image_stock_extractor_litellm.py tests/test_import_parser.py
```

If the prompt change affects the web import flow, also run the relevant web tests
under `apps/dsa-web`.
