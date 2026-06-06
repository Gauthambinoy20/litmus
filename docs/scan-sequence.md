# Litmus — Scan Request Lifecycle

The core feature path: `POST /api/v1/scan` from click to rendered scores.

```mermaid
sequenceDiagram
    actor U as User
    participant FE as React app<br/>(useScan.ts)
    participant MW as middleware.py<br/>(rate limit · errors · logging)
    participant R as routes.py<br/>POST /api/v1/scan
    participant V as validators.py
    participant SS as scan_service.py
    participant SP as section_parser.py
    participant KX as keyword_extractor.py
    participant ATS as ats_engine.py
    participant AI as ai_detection_engine.py
    participant FG as fix_generator.py
    participant SCR as scoring.py

    U->>FE: Paste resume + JD, click Scan
    FE->>MW: POST /api/v1/scan {resume_text, jd_text, mode}
    MW->>MW: rate-limit check (per-hour / per-day)
    MW->>R: forward request
    R->>V: validate_resume_text / validate_jd_text
    alt input invalid
        V-->>FE: 4xx with typed error (empty / too short / too long)
    end
    R->>SS: scan(resume, jd, mode)
    SS->>SP: parse(resume) → sections, bullets, contact
    SS->>KX: extract(jd) → keyword sets
    par dual-axis scoring
        SS->>ATS: score(resume, sections, keywords)
        ATS-->>SS: ATS score (5 dimensions, matched/missing)
    and
        SS->>AI: analyze(resume, sections, bullets)
        Note over AI: 19 signals; the ML signal calls<br/>HuggingFace if available,<br/>else scores locally
        AI-->>SS: AI risk score + per-bullet heatmap
    end
    SS->>FG: generate(ats_result, ai_result)
    FG-->>SS: prioritized fixes
    SS->>SCR: combine(ats, ai)
    SCR-->>SS: interview-readiness verdict
    SS-->>R: ScanResponse
    R-->>FE: 200 JSON (scores, heatmap, fixes, readability, grammar)
    FE->>FE: render gauges + heatmap;<br/>save entry to localStorage history
    FE-->>U: Results dashboard
```

Failure behavior
- Engine exceptions degrade to partial results where possible (`metadata.degraded_mode = true`) rather than failing the whole scan.
- The ML classifier signal times out at 5s and contributes a zero-score signal offline — never an error.
