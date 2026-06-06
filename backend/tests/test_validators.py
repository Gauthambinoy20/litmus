import pytest

from app.config import get_settings
from app.utils.exceptions import (
    InputTooLongError,
    InputTooShortError,
    JDEmptyError,
    ResumeEmptyError,
)
from app.utils.validators import validate_jd_text, validate_resume_text

settings = get_settings()

VALID_RESUME = "x" * settings.min_resume_length
VALID_JD = "y" * settings.min_jd_length


# ── validate_resume_text ────────────────────────────────────────────────


def test_resume_valid_passes_through():
    assert validate_resume_text(VALID_RESUME) == VALID_RESUME


def test_resume_strips_whitespace():
    assert validate_resume_text(f"  {VALID_RESUME}\n\n") == VALID_RESUME


def test_resume_empty_raises():
    with pytest.raises(ResumeEmptyError):
        validate_resume_text("")


def test_resume_whitespace_only_raises():
    with pytest.raises(ResumeEmptyError):
        validate_resume_text("   \n\t  ")


def test_resume_too_short_raises_with_details():
    with pytest.raises(InputTooShortError) as exc:
        validate_resume_text("too short")
    assert exc.value.details["min_length"] == settings.min_resume_length
    assert exc.value.details["actual_length"] == len("too short")


def test_resume_too_long_raises_with_details():
    text = "x" * (settings.max_resume_length + 1)
    with pytest.raises(InputTooLongError) as exc:
        validate_resume_text(text)
    assert exc.value.details["max_length"] == settings.max_resume_length


def test_resume_exact_min_boundary_passes():
    assert validate_resume_text("x" * settings.min_resume_length)


def test_resume_exact_max_boundary_passes():
    assert validate_resume_text("x" * settings.max_resume_length)


# ── validate_jd_text ────────────────────────────────────────────────────


def test_jd_valid_passes_through():
    assert validate_jd_text(VALID_JD) == VALID_JD


def test_jd_empty_raises():
    with pytest.raises(JDEmptyError):
        validate_jd_text("")


def test_jd_too_short_raises():
    with pytest.raises(InputTooShortError):
        validate_jd_text("short")


def test_jd_too_long_raises():
    with pytest.raises(InputTooLongError):
        validate_jd_text("y" * (settings.max_jd_length + 1))


def test_jd_exact_boundaries_pass():
    assert validate_jd_text("y" * settings.min_jd_length)
    assert validate_jd_text("y" * settings.max_jd_length)
