# SmartTriage — AI Emergency Patient Prioritization System

> **Track 2: Healthcare AI** | **Problem Statement: AI Emergency Triage**
> LaunchPad AI Hackathon 2026 — Varendra University

---

## One-Paragraph Pitch

SmartTriage is an AI-powered emergency department triage assistant that transforms unstructured patient intake data — symptoms, vitals, medical history — into a real-time, color-coded prioritization dashboard. Unlike a simple chatbot wrapper, SmartTriage uses a **three-layer AI architecture**: (1) a clinical NLP model extracts structured medical entities from free text, (2) a trained ML classifier assigns urgency scores with confidence levels, and (3) an LLM generates plain-language rationale for every recommendation. The AI **assists** but never replaces the clinician — every decision is auditable, explainable, and overridable. The system updates live: change a patient's vitals and watch the priority, confidence, and explanation recalculate in real time.

---

## Architecture (5-Hour Build)

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Nuxt + Vue)                     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Triage Queue  │  │Patient Detail│  │  AI Rationale     │  │
│  │ (live, color- │  │  (vitals,    │  │  Panel ("Why AI   │  │
│  │  coded list)  │  │  symptoms,   │  │  flagged this")   │  │
│  │              │  │  history)    │  │                   │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────────┘  │
│         └────────────┬─────┘                  │              │
│                      ▼                        │              │
│              REST API Calls + Polling         │              │
└──────────────────────┬────────────────────────┘              │
                       │                                       │
┌──────────────────────▼───────────────────────────────────────┘
│                    BACKEND (Python + FastAPI)                 │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │                  Triage Engine                       │     │
│  │                                                     │     │
│  │  1. 🚩 Red-Flag Rules (deterministic)               │     │
│  │     → Cardiac arrest, stroke symptoms, etc.         │     │
│  │     → Instant ESI Level 1 override                  │     │
│  │                                                     │     │
│  │  2. 🧠 ML Risk Classifier                          │     │
│  │     → Pre-trained model on synthetic triage data    │     │
│  │     → Input: structured vitals + symptom features   │     │
│  │     → Output: ESI level (1-5) + confidence score    │     │
│  │                                                     │     │
│  │  3. 📝 LLM Explanation Layer (Gemini API)          │     │
│  │     → Takes ML output + patient context             │     │
│  │     → Generates clinician-readable rationale        │     │
│  │     → EXPLAINS decisions, doesn't MAKE them         │     │
│  │                                                     │     │
│  │  Output: { score, confidence, reasons,              │     │
│  │            model_version, timestamp }               │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Patient CRUD │  │  Audit Log   │  │  Synthetic Data   │  │
│  │  API          │  │  (every AI   │  │  Generator        │  │
│  │              │  │  decision)   │  │                   │  │
│  └──────────────┘  └──────────────┘  └───────────────────┘  │
│                                                              │
│  Storage: SQLite (single file, zero setup)                   │
└──────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions (vs. Original Plan)

| Original Plan | Revised for 5 Hours | Why |
|---|---|---|
| PostgreSQL + pgvector | **SQLite** | Zero setup, portable, sufficient for prototype |
| Redis + WebSockets | **REST + polling (10s interval)** | Same UX effect, 90% less setup time |
| Bio_ClinicalBERT embeddings | **Keyword/rule-based NLP + Gemini extraction** | BERT setup/download eats too much time; Gemini API handles NLP well enough |
| Train XGBoost from scratch | **Pre-trained scikit-learn model on synthetic data** (train during Phase 1) | Still "our own model" for judges, but trainable in minutes |
| Docker Compose | **Direct `npm run dev` + `uvicorn`** | No containers needed for demo day |
| Keycloak/OIDC auth | **Simple role-based header (demo mode)** | Auth adds zero demo value in 5 hours |
| Next.js + TypeScript | **Nuxt + Vue** | Faster to write, no type errors to debug under pressure |

---

## Why This Wins

### 1. Directly matches the listed problem statement
"AI Emergency Triage" is explicitly listed under Track 2. We're not shoehorning — we're the bulls-eye.

### 2. Three distinct, visible AI components (targets 20/20 on AI Implementation)
Judges reward **multiple AI techniques** over a single API call. We show:
- Rule-based clinical logic (deterministic safety net)
- A trained ML classifier (our own model, not a wrapper)
- LLM for explanation (innovative use — explaining, not deciding)

### 3. The "wow moment" is built into the architecture
Change a patient's vitals → watch the priority color, score, confidence, and plain-language explanation all update live. This is viscerally impressive in a 5-minute demo.

### 4. Audit trail & human-in-the-loop (targets 20/20 on Problem Solving)
Every AI decision is logged with score, confidence, reasons, model version, and timestamp. The clinician can override any recommendation. This shows mature thinking about real-world deployment — judges notice this.

### 5. Feasible in the actual time window
The original architecture was designed for a multi-day build. This revision is scoped for 5 hours with buffer, using SQLite, REST polling, and pre-built UI components.

---

## Competitive Landscape

- **~24 teams** in Track 2 (Healthcare AI) out of ~73 total
- **No team names explicitly reference triage** — but "AI Emergency Triage" is a listed problem, so expect 3-5 teams to attempt it
- **Differentiation strategy:** Most triage attempts will likely be either (a) a chatbot that asks symptoms and gives a priority, or (b) a form → ML model → result page. We differentiate with the **three-layer pipeline, real-time dashboard, audit log, and explainability panel**.
- The teams "MediBuZz", "MedVision AI", "Pulse AI", "MedialAlert" could be doing triage — our edge is the multi-model architecture and live-updating UX.

---

## Submission Checklist (from Rulebook)

- [x] Working prototype developed during hackathon
- [ ] Live demonstration ready
- [ ] Can explain architecture, AI approach, implementation in Q&A
- [ ] Disclose all AI tools, APIs, datasets used
- [ ] Original work (not previously completed)
