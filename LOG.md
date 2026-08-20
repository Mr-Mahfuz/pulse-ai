# SmartTriage — Build Log

> Running log of decisions, progress, and issues. Updated after every meaningful step.

---

## Session 1 — 2026-08-17 (Day 1 of 3 Prep Days)

### 18:00 — Project Kickoff & Research

**Actions:**
- Read `Launchpad-Rulebook-1.pdf` (11 pages, image-based PDF — extracted to PNGs for reading)
- Read `LaunchPad AI Hackathon participants - AI hackathon.pdf` (73 teams)
- Read `LaunchPad AI Hackathon participants - Research.pdf` (19 research teams)

**Key Findings:**
1. **Hackathon duration is 5 hours** (9:30 AM – 2:30 PM), not multi-day
2. **"AI Emergency Triage"** is explicitly listed as a Track 2 problem statement — perfect fit
3. **73 teams** registered for AI Hackathon segment, ~24 in Healthcare AI track
4. **19 additional teams** in Research segment (separate from us)
5. All our proposed tech (Python, FastAPI, Next.js, React, PostgreSQL, HuggingFace) is explicitly allowed
6. Pre-built UI templates allowed; core AI must be developed by team
7. Pre-trained models explicitly encouraged

**Critical Decision — Architecture Simplification:**
The original architecture (from prior AI discussion) assumed multi-day build time. With only 5 hours on hackathon day, I made these changes:

| Changed | From | To | Reason |
|---|---|---|---|
| Database | PostgreSQL + pgvector | SQLite | Zero setup, portable, demo-sufficient |
| Real-time | Redis + WebSockets | REST + 3s polling | Same UX, 90% less complexity |
| NLP | Bio_ClinicalBERT | Keyword-based + LLM extraction | BERT download/setup too slow |
| Deployment | Docker Compose | Direct run (uvicorn + npm) | No container overhead for demo |
| Auth | Keycloak/OIDC | None (demo mode) | Zero demo value |
| TypeScript | Yes | No (JavaScript) | Faster iteration, fewer type-error blockers |

**Rationale:** The goal is to **maximize visible impressiveness per hour of build time**. Every simplification above trades invisible infrastructure for more time on visible AI features and UI polish.

### 18:08 — Planning Documents Created

- `00-overview.md` — Project overview, architecture, competitive analysis
- `phase-1-setup-data-model.md` — Backend/frontend setup, data model, synthetic data, ML training
- `phase-2-triage-engine.md` — Three-layer AI pipeline
- `phase-3-frontend-dashboard.md` — Dashboard UI, patient detail, wireframes
- `phase-4-polish-demo-prep.md` — Demo script, README, disclosure, Q&A prep
- `LOG.md` — This file
- `FEATURES.md` — Feature tracker

**Status:** Waiting for user review and approval before starting Phase 1 implementation.

---

## Open Issues

| # | Issue | Priority | Status |
|---|---|---|---|
| 1 | Need Gemini API key from user | High | ⏳ Waiting |
| 2 | Confirm Python 3.10+ installed | Medium | ⏳ Waiting |
| 3 | Confirm Node.js 18+ installed | Medium | ⏳ Waiting |
| 4 | Team member names for README | Low | ⏳ Later |
| 5 | Determine if presentation slides needed | Low | ⏳ Later |

---

## Session Post-Audit Hardening — 2026-08-20

### Tier 0 Fixes (Demo-Breaking Issues) Completed

**Actions:**
1. **GCS field mismatch**: Changed `gcs` to `gcs_score` in `PatientFormModal.vue` (`vitalConfig` and `form`) to match the backend `PatientCreate` schema, preventing GCS values from being silently dropped and ignored by the red flag layer.
2. **`/api/triage/batch` route shadowing**: Reordered `backend/routes/triage.py` to declare `@router.post("/batch")` before `@router.post("/{patient_id}")`, fixing the 404 shadowing bug.
3. **Gemini SDK dependency mismatch**: Updated `backend/requirements.txt` from `google-generativeai` to `google-genai` to match the actual code imports.
4. **`speech.py` unconditional Gemini import**: Wrapped `from google import genai` in `speech.py` in a try/except block, catching `ImportError` and returning 503 if unavailable, to prevent catastrophic failure on backend startup if the SDK isn't installed.
5. **`demo_sim.py` status code check**: Updated the HTTP check to `response.status_code in (200, 201)` because `POST /api/patients/` returns 201, fixing false-positive error logs during the demo simulation.

**Status**: Tier 0 complete. Moving to Tier 1.

### Tier 1 Fixes (Trust & Correctness) Completed

**Actions:**
1. **ESI color inconsistency**: Aligned `frontend/app/utils/esi.js` to match the standard colors defined in `main.css` and `phase-2-triage-engine.md` (Level 1: Red, Level 2: Orange, Level 3: Yellow, Level 4: Green, Level 5: Blue).
2. **Misleading confidence on red-flag overrides**: Modified `frontend/app/pages/index.vue` to display a "Safety Rule" badge instead of a potentially confusing ML confidence percentage when the triage decision was forced by a deterministic red flag.
3. **Docs vs. reality pass**: Updated `FEATURES.md`, `DOCUMENTATION.md`, `HACKATHON_PITCH.md`, and all four phase docs to accurately reflect the actual implementation: Nuxt/Vue instead of Next.js/React, SQLite instead of PostgreSQL, 10s polling instead of 3s, and explicitly documenting the rule+ML+LLM pipeline instead of Bio_ClinicalBERT.
4. **Root `README.md` + AI disclosure**: Created a root `README.md` containing accurate setup instructions, project architecture, and a strict AI disclosure clarifying the use of synthetic training data and the limited role of the LLM.

**Status**: Tier 1 complete. Moving to Tier 2.
