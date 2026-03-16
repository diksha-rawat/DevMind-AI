"""
AI Code Review Agent
====================
Fetches a GitHub PR diff, sends it to local Ollama (Mistral)
and posts the review back as a PR comment.

Usage:
    python review.py --repo yourname/repo --pr 1 --dry-run
    python review.py --repo yourname/repo --pr 1
"""

import os
import json
import argparse
import textwrap
import logging
from dataclasses import dataclass

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
# Ollama runs locally on port 11434
OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# GitHub token for API access
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API   = "https://api.github.com"

# Keep diff small enough to fit in model context window
MAX_DIFF_CHARS = 2000


# ---------------------------------------------------------------------------
# Data classes — simple containers for our data
# ---------------------------------------------------------------------------
@dataclass
class PRInfo:
    number: int
    title: str
    author: str
    base_branch: str
    head_branch: str
    diff: str


@dataclass
class ReviewResult:
    summary: str
    issues: list
    suggestions: list
    security_flags: list
    score: int
    recommendation: str


# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------
def gh_headers():
    """Returns headers for GitHub API requests."""
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def get_pr_info(repo, pr_number):
    """Fetch PR metadata and unified diff from GitHub."""
    logger.info(f"Fetching PR #{pr_number} from {repo}...")

    # Fetch PR metadata
    resp = requests.get(
        f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}",
        headers=gh_headers(),
        timeout=15,
    )
    resp.raise_for_status()
    pr = resp.json()

    # Fetch the actual code diff
    diff_resp = requests.get(
        f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}",
        headers={**gh_headers(), "Accept": "application/vnd.github.diff"},
        timeout=15,
    )
    diff_resp.raise_for_status()

    # Truncate diff if too large for model
    diff = diff_resp.text[:MAX_DIFF_CHARS]
    if len(diff_resp.text) > MAX_DIFF_CHARS:
        diff += f"\n\n... (diff truncated at {MAX_DIFF_CHARS} chars)"

    return PRInfo(
        number=pr_number,
        title=pr["title"],
        author=pr["user"]["login"],
        base_branch=pr["base"]["ref"],
        head_branch=pr["head"]["ref"],
        diff=diff,
    )


def post_pr_comment(repo, pr_number, body):
    """Post a review comment on the PR."""
    resp = requests.post(
        f"{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments",
        headers=gh_headers(),
        json={"body": body},
        timeout=15,
    )
    resp.raise_for_status()
    url = resp.json()["html_url"]
    logger.info(f"Comment posted: {url}")
    return url


# ---------------------------------------------------------------------------
# Ollama helpers
# ---------------------------------------------------------------------------
def check_ollama():
    """Check if Ollama is running and Mistral is available."""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = [m["name"] for m in resp.json().get("models", [])]
        available = any(OLLAMA_MODEL in m for m in models)
        if not available:
            logger.warning(f"Model '{OLLAMA_MODEL}' not found. Run: ollama pull {OLLAMA_MODEL}")
        return available
    except Exception as e:
        logger.error(f"Ollama not reachable: {e}")
        return False


def call_ollama(prompt, system):
    """Send prompt to local Ollama and return response."""
    logger.info(f"Calling Ollama ({OLLAMA_MODEL})...")
    payload = {
        "model":  OLLAMA_MODEL,
        "stream": False,
        "system": system,
        "prompt": prompt,
        "options": {
            "temperature": 0.2,   # low = consistent reviews
            "num_predict": 1024,
        },
    }
    resp = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=300,   # local LLM can be slow
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


# ---------------------------------------------------------------------------
# Review logic
# ---------------------------------------------------------------------------

# This is the instruction we give to the AI model
SYSTEM_PROMPT = """
You are a senior software engineer performing a code review.
Review the provided git diff and return ONLY valid JSON.

Focus on:
- Bugs and logic errors
- Security vulnerabilities
- Performance problems
- Code style and maintainability
- Missing error handling

Be specific and constructive.
Do NOT include markdown fences or any text outside the JSON.
""".strip()


def build_review_prompt(pr):
    """Build the prompt we send to Ollama."""
    return textwrap.dedent(f"""
        Review this pull request and respond with JSON only.

        PR Title: {pr.title}
        Author: {pr.author}
        Branch: {pr.head_branch} → {pr.base_branch}

        Git Diff:
        {pr.diff}

        Respond with this exact JSON schema:
        {{
          "summary": "<2-3 sentence overview>",
          "issues": ["<specific bug or problem>"],
          "suggestions": ["<improvement suggestion>"],
          "security_flags": ["<security concern or empty list>"],
          "score": <integer 1-10>,
          "recommendation": "<approve | request_changes | comment>"
        }}
    """).strip()


def parse_review(raw):
    """Parse LLM JSON response into ReviewResult."""
    # Strip accidental markdown fences
    clean = raw.strip()
    clean = clean.removeprefix("```json").removeprefix("```")
    clean = clean.removesuffix("```").strip()

    data = json.loads(clean)
    return ReviewResult(
        summary=data.get("summary", ""),
        issues=data.get("issues", []),
        suggestions=data.get("suggestions", []),
        security_flags=data.get("security_flags", []),
        score=int(data.get("score", 5)),
        recommendation=data.get("recommendation", "comment"),
    )


def format_comment(pr, review):
    """Format the review as a GitHub Markdown comment."""
    # Pick emoji based on recommendation
    emoji = {
        "approve": "✅",
        "request_changes": "🚨",
        "comment": "💬"
    }.get(review.recommendation, "💬")

    # Build score bar e.g. ████████░░ 8/10
    score_bar = "█" * review.score + "░" * (10 - review.score)

    # Format lists
    issues_md      = "\n".join(f"- {i}" for i in review.issues) or "_None found_"
    suggestions_md = "\n".join(f"- {s}" for s in review.suggestions) or "_None_"
    security_md    = "\n".join(f"- ⚠️ {s}" for s in review.security_flags) or "_None detected_"

    return textwrap.dedent(f"""
        ## {emoji} AI Code Review — PR #{pr.number}

        > Reviewed by **local Ollama ({OLLAMA_MODEL})** · No data left your machine 🔒

        ### 📋 Summary
        {review.summary}

        ### 🐛 Issues
        {issues_md}

        ### 💡 Suggestions
        {suggestions_md}

        ### 🔐 Security
        {security_md}

        ### 📊 Score
        `{score_bar}` **{review.score}/10**

        ### Recommendation: `{review.recommendation.upper()}`

        ---
        _Generated by [DevMind-AI](https://github.com/diksha-rawat/DevMind-AI)_
    """).strip()


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------
def run_review(repo, pr_number, dry_run=False):
    """Main function — fetch PR, review it, post comment."""

    # Step 1 — Check Ollama is running
    if not check_ollama():
        logger.error("Ollama is not ready. Run: ollama serve && ollama pull mistral")
        return None

    # Step 2 — Fetch PR from GitHub
    pr = get_pr_info(repo, pr_number)
    logger.info(f"Reviewing: '{pr.title}' by @{pr.author}")

    # Step 3 — Build prompt and call Ollama
    prompt = build_review_prompt(pr)
    raw    = call_ollama(prompt, SYSTEM_PROMPT)

    # Step 4 — Parse AI response
    review = parse_review(raw)
    logger.info(f"Score: {review.score}/10 | Recommendation: {review.recommendation}")

    # Step 5 — Post comment or print if dry run
    comment = format_comment(pr, review)
    if dry_run:
        print("\n" + "="*60)
        print(comment)
        print("="*60)
        print("\n[Dry run — comment not posted to GitHub]")
    else:
        post_pr_comment(repo, pr_number, comment)

    return review


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("--repo",    required=True, help="GitHub repo e.g. yourname/repo")
    parser.add_argument("--pr",      type=int,      help="PR number")
    parser.add_argument("--dry-run", action="store_true", help="Print review, don't post")
    args = parser.parse_args()

    run_review(args.repo, args.pr, dry_run=args.dry_run)
