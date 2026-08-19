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
