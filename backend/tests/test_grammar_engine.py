import pytest

from app.engines.grammar_engine import GrammarEngine, _split_sentences


@pytest.fixture
def engine():
    return GrammarEngine()


def test_clean_text_scores_high(engine):
    result = engine.analyze("Maintained the payment service in Python. Reviewed pull requests weekly.")
    assert result.overall_score >= 90
    assert result.error_count == 0


def test_empty_text_returns_perfect(engine):
    result = engine.analyze("")
    assert result.overall_score == 100
    assert result.issues == []


def test_double_spaces_flagged(engine):
    result = engine.analyze("Built the API.  Then shipped it to production.")
    assert any("Double" in i.message for i in result.issues)


def test_missing_capitalization_flagged(engine):
    result = engine.analyze("Shipped the feature. then fixed the bug right after.")
    assert any("capitalization" in i.message.lower() for i in result.issues)


def test_abbreviations_not_false_flagged(engine):
    result = engine.analyze("Worked with partners, e.g. vendors and suppliers.")
    assert not any("capitalization" in i.message.lower() for i in result.issues)


def test_repeated_words_flagged(engine):
    result = engine.analyze("Improved the the deployment pipeline significantly.")
    assert result.issue_count > 0


def test_score_decreases_with_issues(engine):
    clean = engine.analyze("Led the migration to PostgreSQL. Cut query times in half.")
    messy = engine.analyze("led the the migration.  then then it    broke. its fine.")
    assert messy.overall_score < clean.overall_score


def test_counts_are_consistent(engine):
    result = engine.analyze("Built the API.  then shipped the the release.")
    assert result.issue_count == len(result.issues)
    assert result.error_count + result.warning_count + result.suggestion_count == result.issue_count


def test_split_sentences():
    assert len(_split_sentences("One. Two! Three?")) == 3


def test_split_sentences_empty():
    assert _split_sentences("") == []
