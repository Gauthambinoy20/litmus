# Litmus — Data Flow Diagram

How a resume + job description move through the system, from input to scored report.

```mermaid
flowchart LR
    User(["User"])

    subgraph Inputs
        Paste["Pasted text"]
        Upload["PDF / DOCX upload"]
    end

    subgraph Extraction
        PDFP["pdf_parser.py<br/>bytes → text"]
        Valid["utils/validators.py<br/>length & emptiness gates"]
        SecP["section_parser.py<br/>text → sections + bullets<br/>(+ inference for headerless text)"]
    end

    subgraph Analysis
        KX["keyword_extractor.py<br/>JD → keyword sets"]
        ATSE["ats_engine.py<br/>keyword match · placement ·<br/>sections · formatting · relevance"]
        AIE["ai_detection_engine.py<br/>19 signals → risk score + heatmap"]
        RE["readability_engine.py"]
        GE["grammar_engine.py"]
    end

    subgraph Synthesis
        FG["fix_generator.py<br/>findings → actionable fixes"]
        SC["scoring.py<br/>ATS + AI → interview-readiness"]
    end

    subgraph Outputs
        JSON["ScanResponse (JSON)"]
        PDF["PDF report<br/>export_service.py"]
        LS[("Browser localStorage<br/>scan history")]
    end

    User --> Paste --> Valid
    User --> Upload --> PDFP --> Valid
    Valid --> SecP
    SecP --> ATSE
    SecP --> AIE
    SecP --> RE
    SecP --> GE
    KX --> ATSE
    Valid -->|"JD text"| KX
    ATSE --> FG
    AIE --> FG
    ATSE --> SC
    AIE --> SC
    FG --> JSON
    SC --> JSON
    RE --> JSON
    GE --> JSON
    JSON --> PDF
    JSON --> LS
    JSON --> User
```

Key properties
- **Nothing persists server-side.** The resume text lives only for the duration of the request; history is the browser's localStorage.
- The JD and resume take separate extraction paths and meet in `ats_engine.py`.
- The AI-detection heatmap is computed per-bullet, so the frontend can color individual lines.
