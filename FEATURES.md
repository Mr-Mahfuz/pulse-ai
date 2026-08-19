# SmartTriage — Feature Tracker

> Living list of every feature/component with status and description.
> Status: 📋 Planned | 🔨 In Progress | ✅ Done | ❌ Cut

---

## Core AI Pipeline

| # | Feature | Status | Description |
|---|---|---|---|
| AI-1 | Red-Flag Rules Engine | 📋 Planned | Deterministic rules that catch life-threatening conditions (cardiac arrest, respiratory failure, shock, unconscious). Auto-assigns ESI-1 or ESI-2. |
| AI-2 | ML Triage Classifier | 📋 Planned | Random Forest model trained on synthetic patient data. Takes vitals + symptom indicators, outputs ESI level (1-5) with confidence score. |
| AI-3 | LLM Explanation Layer | 📋 Planned | Google Gemini API generates plain-language clinical rationale for each triage decision. Explains but does not decide. |
| AI-4 | Triage Engine Orchestrator | 📋 Planned | Combines all three layers: red-flags → ML → LLM explanation. Outputs unified result with score, confidence, rationale, model version, timestamp. |
| AI-5 | Fallback Explanation | 📋 Planned | Template-based explanation when LLM is unavailable or times out. Ensures the system never returns without a rationale. |

## Data & Models

| # | Feature | Status | Description |
|---|---|---|---|
| DM-1 | Synthetic Patient Dataset | 📋 Planned | ~200 synthetic patients with realistic vitals, symptoms, histories, and ground-truth ESI labels. |
| DM-2 | Trained ML Model (.pkl) | 📋 Planned | Saved scikit-learn model file, trained on synthetic data. Target: >70% accuracy. |
| DM-3 | Demo Seed Data | 📋 Planned | 10 pre-built patients with diverse scenarios for the live demo (cardiac emergency, stroke, broken arm, sore throat, etc.) |

## Backend API

| # | Feature | Status | Description |
|---|---|---|---|
| BE-1 | Patient CRUD API | 📋 Planned | Create, read, update, list patients. SQLite + SQLAlchemy. |
| BE-2 | Triage API | 📋 Planned | Run triage on patient, batch triage, get triage history. |
| BE-3 | Clinician Override API | 📋 Planned | Allows clinician to override AI triage with a reason. Logged to audit trail. |
| BE-4 | Audit Log API | 📋 Planned | View audit history per patient — every triage computation, override, and vital change. |
| BE-5 | CORS Configuration | 📋 Planned | Allow frontend (localhost:3000) to call backend (localhost:8000). |

## Frontend UI

| # | Feature | Status | Description |
|---|---|---|---|
| FE-1 | Triage Queue Dashboard | 📋 Planned | Main screen: real-time, color-coded patient list sorted by priority. Auto-refreshes every 3s. Summary stats bar. |
| FE-2 | Patient Detail View | 📋 Planned | Deep-dive: editable vitals, AI triage result, red flags, ML probabilities, rationale, audit log. |
| FE-3 | Add Patient Form | 📋 Planned | Modal/page to register new patient with vitals and symptoms. Submit triggers immediate triage. |
| FE-4 | Override Modal | 📋 Planned | Clinician selects new ESI level + reason. Logged to audit trail. |
| FE-5 | ESI Color System | 📋 Planned | Consistent color-coding across all screens: Red(1), Orange(2), Yellow(3), Green(4), Blue(5). |
| FE-6 | Dark Theme | 📋 Planned | Clinical dashboard aesthetic — dark background, vivid ESI colors, high contrast. |
| FE-7 | Animations | 📋 Planned | Card entry, priority change transitions, confidence bar animations, pulse effect on ESI-1. |
| FE-8 | Auto-Refresh (Polling) | 📋 Planned | Queue page polls backend every 3 seconds for updates. |

## UX Features

| # | Feature | Status | Description |
|---|---|---|---|
| UX-1 | Live Re-triage | 📋 Planned | Edit vitals → re-run triage → see priority/confidence/rationale update in real time. The "wow moment." |
| UX-2 | Probability Visualization | 📋 Planned | Horizontal bar chart showing ML model's probability distribution across ESI levels. |
| UX-3 | Red Flag Badges | 📋 Planned | Visual badges showing which red-flag rules were triggered (e.g., "SpO2 < 85%", "HR > 180"). |
| UX-4 | Confidence Indicator | 📋 Planned | Visual representation of model confidence — color + percentage + textual label (High/Medium/Low). |
| UX-5 | Arrival Time Tracking | 📋 Planned | Shows "arrived X min ago" with time-since formatting. |

## Documentation & Submission

| # | Feature | Status | Description |
|---|---|---|---|
| DOC-1 | README.md | 📋 Planned | Project overview, setup instructions, architecture, screenshots. |
| DOC-2 | AI Disclosure Document | 📋 Planned | Required by rules: all AI tools, APIs, datasets, external resources used. |
| DOC-3 | Demo Script | 📋 Planned | Scripted 5-minute demo flow with timing. |
| DOC-4 | Q&A Prep | 📋 Planned | Anticipated judge questions with prepared answers. |

---

## Feature Count Summary

| Category | Planned | In Progress | Done | Cut | Total |
|---|---|---|---|---|---|
| Core AI | 5 | 0 | 0 | 0 | 5 |
| Data & Models | 3 | 0 | 0 | 0 | 3 |
| Backend API | 5 | 0 | 0 | 0 | 5 |
| Frontend UI | 8 | 0 | 0 | 0 | 8 |
| UX Features | 5 | 0 | 0 | 0 | 5 |
| Docs | 4 | 0 | 0 | 0 | 4 |
| **Total** | **30** | **0** | **0** | **0** | **30** |
