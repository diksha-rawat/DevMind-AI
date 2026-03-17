"""
Tests for AI Code Review Agent
Run: pytest tests/ -v
"""

import json
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add agent folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from review import PRInfo, ReviewResult, parse_review, format_comment, build_review_prompt


# ---------------------------------------------------------------------------
# Fixtures — reusable test data
# ---------------------------------------------------------------------------
@pytest.fixture
def sample_pr():
    """A sample PR for testing."""
    return PRInfo(
        number=1,
        title="Add user authentication",
        author="diksha",
        base_branch="main",
        head_branch="feature/auth",
        diff="+def login(user, pwd):\n+    return user == 'admin'",
    )


@pytest.fixture
def sample_review():
    """A sample review result for testing."""
    return ReviewResult(
        summary="Adds a basic login function.",
        issues=["Hardcoded admin username"],
        suggestions=["Use proper authentication library"],
        security_flags=["Plain text password comparison"],
        score=3,
        recommendation="request_changes",
    )


# ---------------------------------------------------------------------------
# parse_review tests
# ---------------------------------------------------------------------------
class TestParseReview:

    def test_parses_valid_json(self):
        """Should correctly parse a valid JSON response."""
        raw = json.dumps({
            "summary": "Simple change.",
            "issues": ["Bug found"],
            "suggestions": ["Fix it"],
            "security_flags": [],
            "score": 5,
            "recommendation": "comment",
        })
        result = parse_review(raw)
        assert result.score == 5
        assert result.recommendation == "comment"
        assert "Bug found" in result.issues

    def test_strips_markdown_fences(self):
        """Should strip markdown fences from LLM response."""
        raw = "```json\n{\"summary\":\"ok\",\"issues\":[],\"suggestions\":[],\"security_flags\":[],\"score\":8,\"recommendation\":\"approve\"}\n```"
        result = parse_review(raw)
        assert result.score == 8

    def test_handles_empty_lists(self):
        """Should handle empty issues and suggestions."""
        raw = json.dumps({
            "summary": "Clean PR.",
            "issues": [],
            "suggestions": [],
            "security_flags": [],
            "score": 9,
            "recommendation": "approve",
        })
        result = parse_review(raw)
        assert result.issues == []
        assert result.score == 9


# ---------------------------------------------------------------------------
# format_comment tests
# ---------------------------------------------------------------------------
class TestFormatComment:

    def test_contains_pr_number(self, sample_pr, sample_review):
        """Comment should contain PR number."""
        comment = format_comment(sample_pr, sample_review)
        assert "#1" in comment

    def test_approve_shows_checkmark(self, sample_pr):
        """Approve recommendation should show green checkmark."""
        review = ReviewResult(
            summary="Looks good.",
            issues=[], suggestions=[], security_flags=[],
            score=9, recommendation="approve",
        )
        comment = format_comment(sample_pr, review)
        assert "✅" in comment

    def test_request_changes_shows_alarm(self, sample_pr, sample_review):
        """Request changes should show alarm emoji."""
        comment = format_comment(sample_pr, sample_review)
        assert "🚨" in comment

    def test_security_flags_appear(self, sample_pr, sample_review):
        """Security flags should appear in comment."""
        comment = format_comment(sample_pr, sample_review)
        assert "Plain text password" in comment

    def test_score_appears(self, sample_pr, sample_review):
        """Score should appear in comment."""
        comment = format_comment(sample_pr, sample_review)
        assert "3/10" in comment


# ---------------------------------------------------------------------------
# build_review_prompt tests
# ---------------------------------------------------------------------------
class TestBuildReviewPrompt:

    def test_includes_pr_title(self, sample_pr):
        """Prompt should include PR title."""
        prompt = build_review_prompt(sample_pr)
        assert sample_pr.title in prompt

    def test_includes_diff(self, sample_pr):
        """Prompt should include the code diff."""
        prompt = build_review_prompt(sample_pr)
        assert "login" in prompt

    def test_requests_json_response(self, sample_pr):
        """Prompt should ask for JSON response."""
        prompt = build_review_prompt(sample_pr)
        assert "JSON" in prompt or "json" in prompt
