#!/usr/bin/env python3
"""
AI code review script used by GitHub Actions PR Review workflow.
"""
import json
import os
import subprocess
import traceback


MAX_DIFF_LENGTH = 18000
REVIEW_PATHS = [
    '*.py',
    '*.md',
    'README.md',
    'AGENTS.md',
    'docs/**',
    '.github/PULL_REQUEST_TEMPLATE.md',
    'requirements.txt',
    '.github/requirements-ci.txt',
    'pyproject.toml',
    'setup.cfg',
    '.github/workflows/*.yml',
    '.github/scripts/*.py',
    'apps/dsa-web/**',
]


def run_git(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ git command failed: {' '.join(args)}")
        print(result.stderr.strip())
        return ''
    return result.stdout.strip()


def get_diff():
    """Get PR diff content for review-relevant files."""
    base_ref = os.environ.get('GITHUB_BASE_REF', 'main')
    diff = run_git(['git', 'diff', f'origin/{base_ref}...HEAD', '--', *REVIEW_PATHS])
    truncated = len(diff) > MAX_DIFF_LENGTH
    return diff[:MAX_DIFF_LENGTH], truncated


def get_changed_files():
    """Get changed file list for review-relevant files."""
    base_ref = os.environ.get('GITHUB_BASE_REF', 'main')
    output = run_git(['git', 'diff', '--name-only', f'origin/{base_ref}...HEAD', '--', *REVIEW_PATHS])
    return output.split('\n') if output else []


def get_pr_context():
    """Read PR title/body from GitHub event payload when available."""
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        return '', ''
    try:
        with open(event_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
        pr = payload.get('pull_request', {})
        return (pr.get('title') or '').strip(), (pr.get('body') or '').strip()
    except Exception:
        return '', ''


def classify_files(files):
    py_files = [f for f in files if f.endswith('.py')]
    doc_files = [f for f in files if f.endswith('.md') or f.startswith('docs/') or f in ('README.md', 'AGENTS.md')]
    frontend_files = [f for f in files if f.startswith('apps/dsa-web/') or f.endswith(('.tsx', '.ts'))]
    ci_files = [f for f in files if f.startswith('.github/workflows/')]
    config_files = [
        f for f in files if f in ('requirements.txt', '.github/requirements-ci.txt', 'pyproject.toml', 'setup.cfg', '.github/PULL_REQUEST_TEMPLATE.md')
    ]
    return py_files, doc_files, frontend_files, ci_files, config_files


def _build_ci_context():
    lines = ["## Static Check Context"]
    static_status = os.environ.get('STATIC_CHECK_STATUS', '').strip()
    syntax_status = os.environ.get('SYNTAX_CHECK_STATUS', '').strip()
    syntax_message = os.environ.get('SYNTAX_CHECK_MESSAGE', '').strip()
    has_backend_changes = os.environ.get('HAS_BACKEND_CHANGES', '').strip() == 'true'
    has_frontend_changes = os.environ.get('HAS_FRONTEND_CHANGES', '').strip() == 'true'
    has_workflow_changes = os.environ.get('HAS_WORKFLOW_CHANGES', '').strip() == 'true'

    if static_status:
        lines.append(f"- Overall static checks: **{static_status}**")
    if syntax_status:
        lines.append(f"- Python syntax checks: **{syntax_status}**")
    if syntax_message:
        lines.append(f"  - Details: {syntax_message}")
    else:
        lines.append("  - Details: no changed backend files; syntax check skipped")

    lines.append(
        f"- Change areas: backend={has_backend_changes}, frontend={has_frontend_changes}, workflow={has_workflow_changes}"
    )
    lines.append("")
    lines.append(
        "If these static checks passed, do not repeat their local output. Review semantics, contracts, compatibility, rollback, and test coverage instead."
    )
    return "\n".join(lines)


def build_prompt(diff_content, files, truncated, pr_title, pr_body):
    file_list = "\n".join(f"- {f}" for f in files[:80])
    if len(files) > 80:
        file_list += f"\n- ... {len(files) - 80} more files"

    truncation_note = (
        f"\n\nDiff content was truncated to {MAX_DIFF_CHARS} characters. Review only visible content and clearly mark uncertainty."
        if truncated else ""
    )

    ci_context = _build_ci_context()
    pr_body = pr_body or "(PR body unavailable)"
    pr_title = pr_title or "(PR title unavailable)"

    return f"""
You are the code review assistant for this repository.

Review only the visible PR diff and context. Do not assume CI passed unless the provided static-check context says so. If information is missing, write "cannot confirm" instead of guessing.

## Repository Review Rules

Block merge only for:
- Correctness or security bugs.
- Blocking CI/static checks failing.
- PR description materially contradicting the actual diff.
- Missing rollback plan.
- Clear contract drift that would break runtime, API, Web/Desktop, workflow, configuration, or notification behavior.

Put non-blocking issues under suggestions instead of blockers, including formatting issues, title style, minor PR body gaps, missing optional evidence, or unclear but non-fatal verification.

For backend changes, check whether `./scripts/ci_gate.sh` or equivalent targeted validation is reported. If static checks passed, do not require duplicate local command output. If validation is missing or insufficient, mark verification as "cannot confirm" and explain the gap.

## Required Output Structure

1. **Merge decision**: one of `pass`, `block`, or `cannot_confirm`.
2. **Blockers**: only issues matching the blocker criteria above. Include file paths when possible.
3. **Suggestions**: non-blocking review comments.
4. **Verification**: summarize what can and cannot be confirmed from the provided evidence.
5. **Compatibility and rollback**: note config/API/provider/model/Base URL/LiteLLM/workflow/report/notification compatibility risks and whether rollback is described.

## PR Title

{pr_title}

## PR Body

{pr_body}

{ci_context}

## Changed Files

{file_list}

## Diff

```diff
{diff_content}
```
{truncation_note}
""".strip()


def review_with_gemini(prompt):
    """Run review with Gemini API."""
    api_key = os.environ.get('GEMINI_API_KEY')
    model = os.environ.get('GEMINI_MODEL') or os.environ.get('GEMINI_MODEL_FALLBACK') or 'gemini-2.5-flash'

    if not api_key:
        print("❌ Gemini API Key not configured（check GitHub Secrets: GEMINI_API_KEY）")
        return None

    print(f"🤖 Using model: {model}")

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        print(f"✅ Gemini ({model}) review succeeded")
        return response.text
    except ImportError as e:
        print(f"❌ Gemini dependency is not installed: {e}")
        print("   ensure installed google-genai: pip install google-genai")
        return None
    except Exception as e:
        print(f"❌ Gemini review failed: {e}")
        traceback.print_exc()
        return None


def review_with_openai(prompt):
    """Run review with OpenAI-compatible API as fallback."""
    api_key = os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

    if not api_key:
        print("❌ OpenAI API Key not configured（check GitHub Secrets: OPENAI_API_KEY）")
        return None

    print(f"🌐 Base URL: {base_url}")
    print(f"🤖 Using model: {model}")

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.3
        )
        print(f"✅ OpenAI compatibility endpoint ({model}) review succeeded")
        return response.choices[0].message.content
    except ImportError as e:
        print(f"❌ OpenAI dependency is not installed: {e}")
        print("   ensure installed openai: pip install openai")
        return None
    except Exception as e:
        print(f"❌ OpenAI compatibility endpoint review failed: {e}")
        traceback.print_exc()
        return None


def ai_review(diff_content, files, truncated):
    """Run AI review: Gemini first, then OpenAI fallback."""
    pr_title, pr_body = get_pr_context()
    prompt = build_prompt(diff_content, files, truncated, pr_title, pr_body)

    result = review_with_gemini(prompt)
    if result:
        return result

    print("trying OpenAI compatibility endpoint...")
    result = review_with_openai(prompt)
    if result:
        return result

    return None


def main():
    diff, truncated = get_diff()
    files = get_changed_files()

    if not diff or not files:
        print("no reviewable code/docs/configuration changes，skipped AI review")
        summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
        if summary_file:
            with open(summary_file, 'a', encoding='utf-8') as f:
                f.write("## 🤖 AI code review\n\n✅ no reviewable changes\n")
        return

    print(f"review files: {files}")
    if truncated:
        print(f"⚠️ Diff content truncated to {MAX_DIFF_LENGTH} characters")

    review = ai_review(diff, files, truncated)

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')

    strict_mode = os.environ.get('AI_REVIEW_STRICT', 'false').lower() == 'true'

    if review:
        if summary_file:
            with open(summary_file, 'a', encoding='utf-8') as f:
                f.write(f"## 🤖 AI code review\n\n{review}\n")

        with open('ai_review_result.txt', 'w', encoding='utf-8') as f:
            f.write(review)

        print("AI review completed")
    else:
        print("⚠️ all AI APIs are unavailable")
        if summary_file:
            with open(summary_file, 'a', encoding='utf-8') as f:
                f.write("## 🤖 AI code review\n\n⚠️ AI API is unavailable，check configuration\n")
        if strict_mode:
            raise SystemExit("AI_REVIEW_STRICT=true and no AI review result is available")


if __name__ == '__main__':
    main()
