import pytest

from app.engines.humanizer_engine import (
    HumanizerEngine,
    HumanizeRequest,
    _clean_up,
    _quick_score,
    _replace_banned_phrases,
    _replace_banned_words,
    _split_into_sentences,
    _to_gerund,
    apply_rule_based_transforms,
)

AI_TEXT = (
    "Passionate and results-driven professional with a proven track record of "
    "delivering innovative solutions. Developed a scalable microservice architecture "
    "using Docker, reducing deployment time by 50%. Implemented a comprehensive data "
    "pipeline leveraging Python, improving efficiency by 40%."
)


# ── pure helpers ────────────────────────────────────────────────────────


def test_replace_banned_phrases_removes_cliches():
    out = _replace_banned_phrases("I have a proven track record of success.")
    assert "proven track record" not in out.lower()


def test_replace_banned_phrases_keeps_clean_text():
    text = "Maintained the payment service and reviewed pull requests."
    assert _replace_banned_phrases(text) == text


def test_replace_banned_words_substitutes():
    out = _replace_banned_words("Utilized Docker and orchestrated deployments.")
    assert "Utilized" not in out and "utilized" not in out
    assert "orchestrated" not in out.lower()


def test_split_into_sentences_basic():
    sents = _split_into_sentences("First sentence. Second one! Third?")
    assert len(sents) == 3


def test_split_into_sentences_empty():
    # Empty input yields a single empty segment (blank-line structure is preserved)
    assert _split_into_sentences("") == [""]


def test_to_gerund_irregular_verb():
    # Returns capitalized gerunds — used to open rewritten sentences
    assert _to_gerund("built") == "Building"


def test_to_gerund_regular_past_tense():
    assert _to_gerund("managed") == "Managing"


def test_clean_up_collapses_spaces():
    assert "  " not in _clean_up("too  many   spaces here.")


def test_quick_score_higher_for_ai_text():
    human_text = (
        "Rewrote the payment pipeline after we kept losing transactions on Friday "
        "spikes; failures dropped from 12% to about 2%. Spent a month on-call "
        "untangling the order queue race condition."
    )
    assert _quick_score(AI_TEXT) > _quick_score(human_text)


# ── rule-based transform pipeline ───────────────────────────────────────


def test_apply_rule_based_transforms_changes_ai_text():
    out = apply_rule_based_transforms(AI_TEXT)
    assert out and out != AI_TEXT


def test_apply_rule_based_transforms_aggressive_mode():
    out = apply_rule_based_transforms(AI_TEXT, aggressive=True)
    assert out and out != AI_TEXT


def test_apply_rule_based_transforms_handles_empty():
    assert apply_rule_based_transforms("") == ""


# ── engine end-to-end (offline: HF mocked away by conftest) ─────────────


@pytest.mark.asyncio
async def test_humanize_returns_result_offline():
    engine = HumanizerEngine()
    result = await engine.humanize(HumanizeRequest(text=AI_TEXT, ai_score=80.0))
    assert result.original_text == AI_TEXT
    assert result.humanized_text
    assert result.humanized_text != AI_TEXT


@pytest.mark.asyncio
async def test_humanize_reduces_quick_score():
    engine = HumanizerEngine()
    result = await engine.humanize(HumanizeRequest(text=AI_TEXT, ai_score=80.0))
    assert _quick_score(result.humanized_text) <= _quick_score(AI_TEXT)
