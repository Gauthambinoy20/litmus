# Litmus — Roadmap

Migration + hardening of the dual-axis resume scanner (formerly axiom-resume-scanner) into a clean, tested, fully-free production repo.

## Milestones

### 0. Migration baseline
- [x] 0.1 fresh-history snapshot, repo identity ............ 8%
- [x] 0.2 rebrand to Litmus (all strings, configs) ......... 15%
- [x] 0.3 working baseline verified (boot + e2e scan) ...... 22%

### 1. Repair & hardening
- [x] 1.1 offline-deterministic test suite (mock external HTTP) 30%
- [x] 1.2 stale tests realigned to current behavior ........ 36%
- [x] 1.3 fix: PDF report crash (duplicate reportlab style)  42%
- [x] 1.4 fix: React setState-in-effect (lazy initializers)  46%
- [x] 1.5 single-source app version from config ............ 50%
- [x] 1.6 trim 8 unused dependencies ....................... 55%

### 2. Quality gates
- [x] 2.1 gap-fill tests: validators · humanizer · export · pdf-parser · grammar (67 → 116 backend tests, 65% → 79% coverage) 65%
- [x] 2.2 ruff + mypy + bandit fully green ................. 72%
- [x] 2.3 CVE zero-out: fastapi/nltk/python-multipart/pdfplumber bumps, vitest 4 (0 vulns both stacks) 78%
- [x] 2.4 standard CI: lint/types/tests/build + gitleaks + Trivy + CodeQL + Dependabot 84%

### 3. Documentation & ship
- [x] 3.1 Mermaid diagrams (architecture · DFD · sequence) . 88%
- [x] 3.2 README rewrite ................................... 92%
- [ ] 3.3 4 real-run screenshots ........................... 96%
- [ ] 3.4 push to Gauthambinoy20/litmus, CI green on GitHub  100%

## Known issues
- Summaries module (`analytics_service.py`) has aggregate stats in memory only — resets on restart (by design, no DB).
- spaCy `en_core_web_sm` has no word vectors; ATS semantic-similarity dimension uses context tensors (W007 warning). A larger model would improve relevance scoring but breaks the free/fast constraint.
- `api/index.py` (Vercel serverless wrapper) retained but untested — the supported deploys are Docker/uvicorn.

## Next
- Optional: re-point the Vercel deployment to this repo under the Litmus name.

## ✍️ TODO: my words
<!-- Gautham: product positioning, lessons learned, what you'd do differently -->
