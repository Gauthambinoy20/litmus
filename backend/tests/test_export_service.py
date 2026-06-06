from app.services.export_service import _escape, generate_pdf_report

FULL_RESPONSE = {
    "ats_score": {
        "overall_score": 72,
        "grade": "B",
        "keyword_match_score": 80,
        "section_score": 60,
        "formatting_score": 100,
        "matched_keywords": [{"keyword": "python", "found_in_sections": ["skills"], "frequency_in_resume": 2}],
        "missing_keywords": ["kubernetes", "terraform"],
    },
    "ai_score": {
        "overall_score": 25,
        "risk_level": "LOW",
        "signals": [{"name": "Sentence Length Variance", "score": 3.0, "details": "ok"}],
        "heatmap": [{"text": "Built a thing", "risk": 0.1, "flags": [], "color": "green"}],
    },
    "combined": {"verdict": "GOOD", "summary": "Solid resume."},
    "fixes": [
        {
            "priority": "high",
            "category": "keywords",
            "title": "Add kubernetes",
            "description": "JD requires k8s",
            "example": "Deployed on Kubernetes",
        }
    ],
    "readability": {"flesch_score": 50.0, "grade_level": "10th"},
    "text_analytics": {"word_count": 300, "bullet_count": 12},
}


def test_generate_pdf_report_returns_valid_pdf():
    pdf = generate_pdf_report(FULL_RESPONSE)
    assert isinstance(pdf, bytes)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000


def test_generate_pdf_report_minimal_payload():
    # Service must not crash on a sparse/empty scan response
    pdf = generate_pdf_report({})
    assert pdf.startswith(b"%PDF")


def test_generate_pdf_report_handles_special_chars():
    resp = dict(FULL_RESPONSE)
    resp["combined"] = {"verdict": "OK", "summary": "Uses <tags> & “quotes” — fine."}
    pdf = generate_pdf_report(resp)
    assert pdf.startswith(b"%PDF")


def test_escape_neutralizes_markup():
    out = _escape("<b>bold</b> & co")
    assert "<b>" not in out
    assert "&amp;" in out
