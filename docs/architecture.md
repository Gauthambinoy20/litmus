# Litmus — Architecture

Component view of the system as implemented. Every node maps to a real module or directory in this repo.

```mermaid
flowchart TB
    subgraph Browser["Browser — React 18 + TypeScript (frontend/src)"]
        Landing["Landing<br/>components/Landing"]
        Scanner["Scanner<br/>components/Scanner"]
        ResultsUI["Results<br/>components/Results"]
        HistoryUI["History<br/>components/History"]
        Hooks["hooks/<br/>useScan · useFileUpload · useHistory"]
    end

    subgraph API["FastAPI backend (backend/app)"]
        Routes["api/routes.py<br/>/scan · /scan/file · /scan/bulk · /scan/quick<br/>/compare · /humanize · /export/pdf<br/>/keywords/extract · /health · /stats"]
        MW["api/middleware.py<br/>error handling · rate limit · logging"]

        subgraph Services["services/"]
            ScanSvc["scan_service.py<br/>orchestrates the scan pipeline"]
            ExportSvc["export_service.py<br/>PDF report (reportlab)"]
            HistorySvc["history_service.py"]
            AnalyticsSvc["analytics_service.py"]
        end

        subgraph Engines["engines/"]
            PDFParse["pdf_parser.py<br/>pdfplumber · python-docx"]
            SectionP["section_parser.py"]
            KeywordX["keyword_extractor.py<br/>spaCy"]
            ATS["ats_engine.py<br/>5 scoring dimensions"]
            AIDet["ai_detection_engine.py<br/>19 signals"]
            Readab["readability_engine.py"]
            Grammar["grammar_engine.py"]
            FixGen["fix_generator.py"]
            Humanizer["humanizer_engine.py<br/>rule-based + optional ML"]
            Scoring["scoring.py<br/>combined verdict"]
        end
    end

    HF["HuggingFace Inference API<br/>(optional — free tier;<br/>graceful fallback offline)"]

    Hooks -->|"REST /api/v1"| Routes
    Routes --> MW
    Routes --> ScanSvc
    Routes --> ExportSvc
    Routes --> Humanizer
    ScanSvc --> PDFParse
    ScanSvc --> SectionP
    ScanSvc --> KeywordX
    ScanSvc --> ATS
    ScanSvc --> AIDet
    ScanSvc --> Readab
    ScanSvc --> Grammar
    ScanSvc --> FixGen
    ScanSvc --> Scoring
    AIDet -.->|"ML classifier signal"| HF
    Humanizer -.->|"ML paraphrase layer"| HF
```

Notes
- The two dashed HuggingFace edges are **optional**: with no API key or no network, both engines fall back to fully local logic. The whole product works offline and free.
- Scan history is stored **client-side in localStorage** (`hooks/useHistory.ts`); the backend keeps only in-memory aggregate stats (`/stats`).
- No database: the backend is stateless, which is why it deploys free on any container host.
