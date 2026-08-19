# SmartTriage Status Report

Audit date: 2026-08-19  
Repository root audited: `C:\workspace\Personal\smarttriage`

## TL;DR

- Overall completion estimate: about 70% for a local hackathon demo; much lower for anything production-like.
- Top 3 risks / blockers:
  1. Fresh install is likely broken or fragile: `backend/requirements.txt` lists `google-generativeai`, but the code imports `from google import genai`, which belongs to the newer `google-genai` SDK. It works on this machine only because `google.genai` is already installed globally.
  2. `POST /api/triage/batch` is effectively unreachable because `backend/routes/triage.py` registers `POST /api/triage/{patient_id}` before `POST /api/triage/batch`; a request to `/api/triage/batch` is treated as patient ID `batch` and returns `404`.
  3. The AI story is partly over-claimed in the docs: there is no Bio_ClinicalBERT or true clinical NLP layer, no real clinical data validation, no auth, and the model's 100% test accuracy is only on highly separable synthetic data.
- Top 3 recommended next steps:
  1. Fix demo-breaking backend/frontend mismatches: install dependency name, route ordering, GCS field name, and polling interval/documentation mismatch.
  2. Harden and verify the end-to-end demo path: create patient, auto-triage, edit vitals, re-triage, override, audit trail, print report.
  3. Update public-facing docs and pitch so the claims match the actual Nuxt/FastAPI/SQLite/synthetic-data implementation.

## 1. Project Snapshot

### Current title / pitch

The implemented project is still titled **SmartTriage: AI Emergency Patient Prioritization System**. The pitch has evolved from the original three-layer clinical NLP + ML + LLM idea into a practical ED dashboard:

- structured patient intake;
- deterministic red-flag rules;
- Random Forest triage classifier trained on synthetic data;
- Gemini or template-generated clinical rationale;
- clinician override and audit logging;
- bilingual English/Bengali UI;
- optional browser speech dictation plus Gemini transcript parsing.

### Stack actually in use vs. planned

| Area | Planned in docs | Actually present | Notes |
|---|---|---|---|
| Frontend | `00-overview.md` and phase docs mention Next.js + React/JavaScript | Nuxt 4.5.2, Vue 3.5.41, Tailwind, `@nuxtjs/i18n`, `@nuxtjs/google-fonts` | This is a real divergence. The current frontend lives under `frontend/app`, not `frontend/src/app`. |
| Backend | Python + FastAPI | FastAPI + SQLAlchemy + Pydantic | Present and starts via FastAPI TestClient. |
| Database | SQLite | SQLite file at root: `smarttriage.db` | `backend/database.py` uses `sqlite:///./smarttriage.db`, so the DB location depends on the working directory used to start the backend. |
| ML | scikit-learn Random Forest or Gradient Boosting on synthetic data | RandomForestClassifier saved at `backend/data/triage_model.pkl` | Present. Synthetic-only. |
| Clinical NLP | Original idea: Bio_ClinicalBERT; revised docs: keyword/rule-based + LLM extraction | No Bio_ClinicalBERT. Keyword features in `backend/ml_model.py`; speech transcript parsing in `backend/routes/speech.py` uses Gemini. | There is no separate clinical NLP inference layer for triage notes. |
| LLM | Gemini explanation layer | Gemini wired in `backend/llm_explainer.py`; fallback template works | In sandbox verification, socket access was blocked and fallback rationale was returned. |
| Real-time | REST + 3s polling per docs | REST + polling every 10 seconds in `frontend/app/pages/index.vue` | No WebSockets. Poll interval differs from plan. |
| Auth | Demo-mode/no auth | No auth | Audit actor values are hardcoded strings like `system` and `clinician`. |
| Deployment | Direct run | Direct run only | No Docker, hosting, CI, or deployment config. |

### Can it run end-to-end right now?

Likely yes for a local development demo on this machine, with caveats.

Verified:

- Backend imports and FastAPI health check worked via TestClient:
  - `GET /api/health` returned `{"status": "healthy"}`.
  - Startup initialized the DB, loaded `backend/data/triage_model.pkl`, and initialized Gemini client.
- Python available: `Python 3.14.0`.
- Node available: `v24.11.0`.
- `cmd /c npm --version` from `frontend` returned `11.12.1`.
- Current root DB contains 10 patients and 21 audit logs.

Not fully verified:

- Production frontend build did not finish within 120 seconds. It reached Nuxt build setup/app generation and then timed out; no final success or error was observed.
- Browser UI was not visually smoke-tested in this audit.
- Live Gemini calls were not verified. The local sandbox blocked socket access with `[WinError 10013]`, causing fallback rationale output.

Startup steps:

1. From repo root, install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
   But also install `google-genai` unless `from google import genai` is already available:
   ```bash
   pip install google-genai
   ```
2. Ensure `GEMINI_API_KEY` exists in `backend/.env` or root `.env`. Both files currently define that key name; values are intentionally not reproduced here.
3. Start backend from the repo root so it uses the existing root `smarttriage.db`:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
4. Start frontend from `frontend`. On this Windows machine, direct `npm` in PowerShell is blocked by execution policy, so use:
   ```bash
   cmd /c npm run dev
   ```
5. Optional seed data, after backend is running:
   ```bash
   python backend/data/seed_demo.py
   ```

## 2. Architecture As-Built

### High-level structure

```text
smarttriage/
  00-overview.md
  FEATURES.md
  LOG.md
  phase-1-setup-data-model.md
  phase-2-triage-engine.md
  phase-3-frontend-dashboard.md
  phase-4-polish-demo-prep.md
  DOCUMENTATION.md
  HACKATHON_PITCH.md
  .env
  smarttriage.db
  backend/
    main.py
    database.py
    models.py
    triage_engine.py
    ml_model.py
    llm_explainer.py
    demo_sim.py
    requirements.txt
    routes/
      patients.py
      triage.py
      audit.py
      speech.py
    data/
      generate_synthetic.py
      train_model.py
      seed_demo.py
      synthetic_patients.json
      triage_model.pkl
  frontend/
    package.json
    nuxt.config.ts
    app/
      pages/
        index.vue
        analytics.vue
        patient/[id].vue
      components/
        PatientFormModal.vue
        PatientCard.vue
        OverrideModal.vue
      composables/useApi.js
      utils/esi.js
      layouts/default.vue
      assets/css/main.css
    i18n/locales/
      en.json
      bn.json
```

Note: `frontend/node_modules` is present in the workspace and very large. That is convenient locally but not ideal for source control.

### Data flow today

1. User registers a patient in `frontend/app/components/PatientFormModal.vue`.
2. The frontend calls `POST /api/patients` via `frontend/app/composables/useApi.js`.
3. `backend/routes/patients.py` inserts a `PatientDB` row and an audit log action `patient_registered`.
4. The dashboard parent handler `onPatientCreated` then calls `POST /api/triage/{patient_id}`.
5. `backend/routes/triage.py` loads the patient and builds a patient-data dict.
6. `backend/triage_engine.py` runs `check_red_flags(...)`.
7. `backend/ml_model.py` extracts 24 features and predicts ESI probabilities using the Random Forest.
8. Red flags override the ML class if triggered; otherwise the ML class is final.
9. `backend/llm_explainer.py` tries Gemini, then falls back to a template if Gemini fails or no key/client is available.
10. `backend/routes/triage.py` persists triage fields on the patient row and logs `triage_computed`.
11. The dashboard polls `GET /api/patients` every 10 seconds and renders sorted queue rows.
12. Patient detail page can update vitals with `PUT /api/patients/{id}`, immediately call `POST /api/triage/{id}`, then refresh audit logs.

### Structural divergences from phase docs

- Frontend is Nuxt/Vue, not Next.js/React.
- There is no `src/app` frontend tree.
- Polling is 10 seconds, not the planned 3 seconds.
- The planned Bio_ClinicalBERT layer was not implemented.
- The planned "clinical NLP model extracts structured medical entities from free text" is only partially represented by Gemini speech parsing, not by the triage pipeline itself.
- Extra features not emphasized in early phase docs were added: bilingual UI, browser speech dictation, MCI display mode, analytics page, print-ready report.

## 3. Feature Status

`FEATURES.md` is stale: it still marks every feature as planned, but many are implemented. Honest current status:

| ID | Feature | Current status | Note |
|---|---|---|---|
| AI-1 | Red-Flag Rules Engine | Done | Implemented in `backend/triage_engine.py`; includes vitals thresholds, age-aware HR/RR thresholds, ESI-1 and ESI-2 keyword checks. |
| AI-2 | ML Triage Classifier | Done | RandomForest model exists at `backend/data/triage_model.pkl`; synthetic-only validation. |
| AI-3 | LLM Explanation Layer | Partial | Gemini is wired, but live API was not verified in this sandbox; fallback template worked. Dependency declaration is wrong for fresh installs. |
| AI-4 | Triage Engine Orchestrator | Done | `compute_triage` combines red flags, ML prediction, and explanation. Audit logging happens in the route, not inside the orchestrator. |
| AI-5 | Fallback Explanation | Done | Template fallback exists in `LLMExplainer._generate_template_explanation`. |
| DM-1 | Synthetic Patient Dataset | Done | `backend/data/synthetic_patients.json` has 250 patients, not just 200. Distribution: ESI-1 12, ESI-2 37, ESI-3 89, ESI-4 75, ESI-5 37. |
| DM-2 | Trained ML Model (.pkl) | Done | RandomForestClassifier, 200 estimators, 24 input features, classes `[1 2 3 4 5]`. |
| DM-3 | Demo Seed Data | Done | `backend/data/seed_demo.py` has 10 curated patients; current DB already has 10 patients. |
| BE-1 | Patient CRUD API | Done | `backend/routes/patients.py` supports create/list/get/update/delete/status. Create does not itself triage; frontend triggers triage after create. |
| BE-2 | Triage API | Partial | Single-patient triage works. Batch triage route is shadowed by `/{patient_id}` and returns 404. No `/history` route exists; audit route is used instead. |
| BE-3 | Clinician Override API | Done | `PUT /api/triage/{patient_id}/override` persists override and audit log. |
| BE-4 | Audit Log API | Done | `GET /api/audit/{patient_id}` and `GET /api/audit?limit=...` exist. |
| BE-5 | CORS Configuration | Done | Allows localhost/127.0.0.1 ports 3000 and 3001. |
| FE-1 | Triage Queue Dashboard | Done | Built in `frontend/app/pages/index.vue`; table, stats, sorting, tabs, search, MCI toggle. Polls every 10s, not 3s. |
| FE-2 | Patient Detail View | Done | Built in `frontend/app/pages/patient/[id].vue`; vitals, AI assessment, probabilities, rationale, audit, print view. |
| FE-3 | Add Patient Form | Partial | Modal works and parent runs triage. Bug: form uses `gcs`, backend expects `gcs_score`, so entered GCS is ignored and defaults to 15. |
| FE-4 | Override Modal | Done | `frontend/app/components/OverrideModal.vue` calls backend override API. |
| FE-5 | ESI Color System | Partial | Implemented, but not the planned/standard mapping. `frontend/app/utils/esi.js` maps ESI-1 to blue and ESI-2 to red. CSS variables in `main.css` still imply ESI-1 red, so the system is internally inconsistent. |
| FE-6 | Dark Theme | Partial | Light/dark toggle exists, but default is light via cookie default. Planned primary dark theme is not the default. |
| FE-7 | Animations | Partial | Fade/slide modals, confidence transitions, pulse border exist. No robust priority-change transitions. |
| FE-8 | Auto-Refresh (Polling) | Partial | Implemented as 10s polling in `index.vue`, not 3s. |
| UX-1 | Live Re-triage | Done | Patient detail save flow updates vitals, re-runs triage, refreshes patient and audit logs. It requires clicking save/re-run. |
| UX-2 | Probability Visualization | Done | Horizontal probability bars in patient detail. |
| UX-3 | Red Flag Badges | Done | Red flags display in queue/detail when `triage_source === "red_flag_override"` or flags exist. |
| UX-4 | Confidence Indicator | Done | Confidence bar and percentage shown in queue/detail. |
| UX-5 | Arrival Time Tracking | Done | Relative wait time and estimated wait are shown. |
| DOC-1 | README.md | Partial | No root `README.md`. There is `DOCUMENTATION.md` and `frontend/README.md`. |
| DOC-2 | AI Disclosure Document | Partial | Disclosure-like text exists in phase docs/DOCUMENTATION, but there is no final dedicated disclosure file and it does not fully match current implementation. |
| DOC-3 | Demo Script | Partial | `phase-4-polish-demo-prep.md` contains a demo script, but it is not updated for current Nuxt UI and extra features. |
| DOC-4 | Q&A Prep | Partial | Exists in `phase-4-polish-demo-prep.md`, but still reflects intended claims more than actual current limitations. |

## 4. AI Pipeline - Detailed Status

### 4.1 Deterministic rules / red-flag layer

Status: implemented.

Location: `backend/triage_engine.py`.

Core rule entry point:

```python
def check_red_flags(...):
    # returns {triggered: bool, level: int, matched_rules: list}
```

Implemented ESI-1 signals include:

- severe bradycardia/tachycardia with pediatric adjustment;
- SpO2 `<85%`;
- respiratory rate too high or too low with pediatric adjustment;
- systolic BP `<60`;
- GCS `<=8`;
- ESI-1 keywords including `unresponsive`, `not breathing`, `cardiac arrest`, `pulseless`, `active seizure`, `no pulse`, `agonal breathing`.

Implemented ESI-2 signals include:

- chest pain plus age over 40, tachycardia, or hypoxia;
- stroke phrases such as `sudden weakness`, `slurred speech`, `facial droop`, `sudden numbness`;
- systolic BP `<80`;
- temperature `>39.5`, with extra concern if GCS `<14`;
- severe pain plus tachycardia or SBP `>180`;
- SpO2 in `85-89%`;
- GCS `9-12`;
- ESI-2 keywords including `stroke`, `hematemesis`, `suicidal`, `overdose`, `anaphylaxis`, `gunshot`, `major trauma`, `severe bleeding`, `altered mental status`.

Important divergence: phase docs said ESI-1 shock threshold would be SBP `<70`; code uses `<60` for ESI-1 and `<80` for ESI-2.

### 4.2 Trained ML model

Status: implemented, but synthetic-only.

Locations:

- feature extraction runtime: `backend/ml_model.py`
- dataset generation: `backend/data/generate_synthetic.py`
- training script: `backend/data/train_model.py`
- saved model: `backend/data/triage_model.pkl`

Model details from the saved file:

- class: `RandomForestClassifier`
- estimators: `200`
- classes: `[1 2 3 4 5]`
- input features: `24`
- version string returned by runtime: `smarttriage-rf-v1.0`

Actual features:

- 8 vitals/demographic features: heart rate, systolic BP, diastolic BP, respiratory rate, temperature, SpO2, GCS, age.
- 6 derived features: pulse pressure, mean arterial pressure, tachycardic flag, hypoxic flag, febrile flag, altered-consciousness flag.
- 10 keyword group indicators: cardiac, respiratory, neurological, trauma, gastrointestinal, severe pain, infection, allergic, mental health, urinary.

Synthetic dataset:

- `backend/data/synthetic_patients.json`
- 250 generated patients.
- Labels generated directly from scenario templates, not clinical records.

Validation observed during audit:

- Holdout accuracy using the training script's same split logic: `1.0` / 100%.
- Confusion matrix on 50-patient holdout:
  ```text
  [[2, 0, 0, 0, 0],
   [0, 8, 0, 0, 0],
   [0, 0, 18, 0, 0],
   [0, 0, 0, 15, 0],
   [0, 0, 0, 0, 7]]
  ```
- Top saved model feature importances:
  - `spo2`: 0.1811
  - `gcs_score`: 0.1281
  - `diastolic_bp`: 0.1146
  - `systolic_bp`: 0.1109
  - `map`: 0.0792
  - `heart_rate`: 0.0690
  - `temperature`: 0.0654
  - `respiratory_rate`: 0.0574
  - `is_altered_consciousness`: 0.0516
  - `is_hypoxic`: 0.0489

Interpretation: the model is trained and technically functional, but its validation is not meaningful for real clinical performance because the data generator creates clean separations between ESI classes.

### 4.3 Clinical NLP / Bio_ClinicalBERT layer

Status: not implemented as originally described.

There is no Bio_ClinicalBERT, transformer embedding model, entity recognizer, or clinical NLP model in the triage path.

What exists instead:

- keyword-group feature extraction in `backend/ml_model.py`;
- deterministic keyword red flags in `backend/triage_engine.py`;
- speech transcript parsing in `backend/routes/speech.py`, which uses Gemini to convert a browser transcript into a `PatientCreate` schema.

The speech parser is useful and demo-friendly, but it is not the same as a clinical NLP layer feeding the triage classifier.

### 4.4 LLM explanation layer

Status: partially implemented.

Location: `backend/llm_explainer.py`.

Behavior:

- Loads `.env` from `backend/.env` and CWD.
- Reads `GEMINI_API_KEYS` or `GEMINI_API_KEY`.
- Imports `from google import genai`.
- Uses model name `gemini-3.6-flash`.
- Sends patient data, final ESI level, confidence, red flags, ML probabilities, and source into a prompt.
- If Gemini fails, returns a template rationale.
- Supports `language="bn"` fallback and prompt instruction for Bengali LLM output.

Input to LLM includes:

- demographics;
- chief complaint;
- vitals;
- medical history;
- final ESI level and name;
- model confidence;
- decision source;
- red flags;
- ML probability for the final ESI.

Output:

- A 2-3 sentence clinician-oriented rationale, if Gemini works.
- A deterministic fallback sentence/paragraph if Gemini fails.

Live API status:

- In this audit, Gemini client initialized, but generation failed due sandbox socket restriction:
  ```text
  [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions
  ```
- Fallback explanation then returned successfully.

### 4.5 Real sample input and actual output

Sample patient dict used in this audit:

```json
{
  "name": "Test Critical Chest Pain",
  "age": 58,
  "gender": "M",
  "chief_complaint": "Severe crushing chest pain radiating to left arm, shortness of breath, profuse sweating",
  "heart_rate": 135,
  "systolic_bp": 85,
  "diastolic_bp": 50,
  "respiratory_rate": 28,
  "temperature": 37.2,
  "spo2": 87,
  "gcs_score": 15,
  "medical_history": "Hypertension, type 2 diabetes, smoker"
}
```

Actual output from `compute_triage(patient, TriageClassifier(), LLMExplainer(), "en")` on this machine:

```json
{
  "level": 2,
  "level_name": "Emergent",
  "confidence": 0.49782142857142864,
  "rationale": "This 58-year-old M patient presenting with Severe crushing chest pain radiating to left arm, shortness of breath, profuse s has been classified as ESI-2 (Emergent) due to critical safety rules being triggered. Specifically: Chest pain in patient age 58 (>40); Chest pain with tachycardia (HR=135); Chest pain with hypoxia (SpO2=87%). Immediate clinical attention is recommended.",
  "source": "red_flag_override",
  "model_version": "smarttriage-rf-v1.0",
  "timestamp": "2026-08-19T10:28:38.839473",
  "red_flags": [
    "Chest pain in patient age 58 (>40)",
    "Chest pain with tachycardia (HR=135)",
    "Chest pain with hypoxia (SpO2=87%)",
    "Significant hypoxia (SpO2=87%, 85-89%)",
    "Emergent keyword: 'crushing chest'"
  ],
  "probabilities": {
    "ESI-1": 0.0037,
    "ESI-2": 0.4052,
    "ESI-3": 0.4978,
    "ESI-4": 0.0481,
    "ESI-5": 0.0451
  }
}
```

Notable: the ML model's highest probability was ESI-3, but the deterministic red-flag layer overrode the final level to ESI-2. Confidence remains the ML confidence (`~49.8%`), not the override confidence, so the displayed confidence can be confusing for red-flag decisions.

## 5. UI/UX Current State

### Built screens

- Triage queue dashboard: `frontend/app/pages/index.vue`
  - Functional and fairly polished.
  - Includes stats, queue table, priority badges, search, main ED / fast track tabs, MCI mode, estimated wait, SLA breach flag, manual refresh, and add-patient modal.
  - Polling works by interval in code, but every 10 seconds.
- Patient detail: `frontend/app/pages/patient/[id].vue`
  - Functional and demo-ready in scope.
  - Shows clinical presentation, editable vitals, AI triage assessment, red flags, probability bars, rationale, override state, audit trail, and print report layout.
- Add patient modal: `frontend/app/components/PatientFormModal.vue`
  - Functional, includes browser speech recognition and Gemini transcript extraction.
  - Bug: GCS field is stored as `gcs`, not `gcs_score`.
- Override modal: `frontend/app/components/OverrideModal.vue`
  - Functional; posts override level and reason.
- Analytics page: `frontend/app/pages/analytics.vue`
  - Mostly UI/demo analytics. It uses real patient counts and ESI distribution, but hardcodes KPIs such as "12% vs yesterday", average wait times, and 92% AI concordance.

### UI-only or weak-backend areas

- Staff Directory and Settings sidebar buttons in `frontend/app/layouts/default.vue` are non-functional buttons.
- Analytics KPIs are mostly hardcoded and should not be presented as measured system data.
- MCI mode is a frontend visualization that maps ESI into START-like categories; there is no separate backend MCI triage model.
- SLA breach and estimated wait are frontend heuristics only.

### Real-time / WebSocket status

- WebSockets are not implemented.
- Polling is implemented in the queue page:
  ```js
  refreshInterval = setInterval(() => { fetchPatients() }, 10000)
  ```
- Docs still say 3-second polling in multiple places. Current code uses 10 seconds.

## 6. Known Issues, Bugs, and Technical Debt

### Demo-breaking or likely-to-fail issues

- `POST /api/triage/batch` route bug:
  - Actual test result: `POST /api/triage/batch` returned `404 {"detail":"Patient not found"}`.
  - Cause: route order in `backend/routes/triage.py`.
- Dependency mismatch:
  - Code uses `from google import genai`.
  - `backend/requirements.txt` lists `google-generativeai>=0.8.0`, not `google-genai`.
  - Fresh backend installs can fail at `backend/routes/speech.py` import.
- `backend/routes/speech.py` imports Gemini SDK unconditionally:
  - If `google.genai` is absent, backend startup can fail.
  - `llm_explainer.py` handles missing import gracefully, but `speech.py` does not.
- Add-patient GCS bug:
  - `PatientFormModal.vue` sends `gcs`.
  - Backend schema expects `gcs_score`.
  - Pydantic ignores unknown `gcs`, so user-entered GCS from the add form is lost.
- `demo_sim.py` checks for HTTP status `200` after `POST /api/patients`, but the API returns `201`; it will falsely report errors even when patients are created.

### Modeling / AI debt

- No real clinical dataset.
- No external validation.
- No model calibration.
- No model card or limitations document.
- Confidence displayed for red-flag overrides is still ML confidence, even if the rule layer made the final decision.
- LLM output is not cached despite the phase doc claiming caching per triage computation.
- No timeout wrapper around Gemini generation beyond whatever the SDK/network does.
- `gemini-3.6-flash` is hardcoded in `llm_explainer.py`; availability was not verified because the sandbox blocked network before model validation.

### Backend/API debt

- No automated tests.
- SQLite DB path is relative to process CWD.
- No migrations.
- No pagination for patients.
- `list_patients` sorts in Python after querying all patients.
- No validation of status updates beyond a simple list.
- No optimistic locking or race protection for rapid re-triage clicks.
- No duplicate prevention, though UUIDs avoid identity collision.

### Frontend debt

- ESI color mapping diverges from the phase docs and from standard expectations:
  - `frontend/app/utils/esi.js`: ESI-1 blue, ESI-2 red, ESI-3 orange, ESI-4 lime, ESI-5 gray.
  - `frontend/app/assets/css/main.css`: CSS variables imply ESI-1 red, ESI-5 blue.
- Several SVG icons and emoji-like symbols are embedded manually rather than using an icon library.
- Production build was inconclusive due 120-second timeout.
- No browser E2E tests.
- Light mode is default despite dark theme being planned as the primary look.

### Security / audit gaps

- No authentication.
- No role enforcement.
- No real clinician identity; actors are hardcoded.
- Audit logs are normal editable database rows, not tamper-proof.
- No PHI/PII protection story beyond local SQLite.
- API key is stored in `.env` files in the workspace. Values were not printed here, but make sure they are not committed or shared.
- CORS is permissive for local frontend ports, which is fine for demo but not production.

## 7. Config, Environment & Deployment Status

### Already set up

- Local SQLite DB: `smarttriage.db`.
- Current DB contents:
  - 10 patients.
  - 21 audit logs.
  - triage distribution in DB: ESI-2 = 5, ESI-3 = 1, ESI-4 = 2, ESI-5 = 2, ESI-1 = 0.
- Synthetic dataset and trained model are present.
- Root `.env` and `backend/.env` both define `GEMINI_API_KEY`.
- Frontend dependencies are installed locally under `frontend/node_modules`.

### Not set up

- No Supabase project is used. The implemented storage is SQLite only.
- No deployment target or hosting config.
- No Docker.
- No CI.
- No committed git history available in this folder; `git log` reported `fatal: not a git repository`.

### Fresh-machine blockers

- Missing/incorrect Gemini SDK dependency in `backend/requirements.txt`.
- PowerShell execution policy may block direct `npm`; use `cmd /c npm ...` or adjust policy.
- Starting backend from the wrong directory can create/use the wrong SQLite DB.
- Gemini live features require a valid key and network access.
- Python 3.14 works on this machine, but many ML packages are safer on Python 3.10-3.12 for reproducibility.

## 8. Gap vs. Timeline

The planning docs and `LOG.md` frame this as a 5-hour hackathon build, with prep docs created on 2026-08-17. Against that scope:

- Phase 1 is mostly complete: backend, frontend, SQLite schema, synthetic data, trained model, demo DB exist.
- Phase 2 is mostly complete, but the "clinical NLP" claim is not complete and batch triage is broken.
- Phase 3 is substantially complete and has extra UI features beyond the plan.
- Phase 4 is partial: demo script and Q&A notes exist, but final README/disclosure and verified build/rehearsal are not done.

Status vs. timeline: good for a hackathon prototype, behind for a clean final submission package. The code has enough to demo, but the docs and setup are behind the implementation and there are a few small landmines.

Minimum safe demo if time runs short:

1. Do not rely on `/api/triage/batch`.
2. Start backend from repo root and frontend through `cmd /c npm run dev`.
3. Use the already seeded patients in `smarttriage.db`.
4. Demo one patient detail flow:
   - open queue;
   - open chest pain/stroke/asthma patient;
   - show red flags, probability bars, rationale, audit;
   - edit a vital and save/re-triage;
   - perform clinician override;
   - print report if needed.
5. If Gemini network/API fails, explicitly say fallback explanations guarantee a rationale and show that as resilience, not as a failure.

## 9. Recommendations

Highest-value use of remaining time: hardening, not new features. The app already has enough visible surface area. The biggest demo risk is a judge or teammate trying a planned endpoint/path and hitting a preventable bug.

Priority fixes:

1. Fix route order in `backend/routes/triage.py` so `/batch` is registered before `/{patient_id}`.
2. Replace or add the correct dependency in `backend/requirements.txt`: `google-genai`; make `speech.py` degrade gracefully if the SDK or key is missing.
3. Rename frontend add-patient form field `gcs` to `gcs_score`.
4. Align ESI colors with the intended standard and make CSS/util mappings consistent.
5. Update docs to say Nuxt/Vue, 10s polling or change code to 3s, SQLite only, synthetic-only model validation, no Bio_ClinicalBERT.
6. Create a final root `README.md` and dedicated AI disclosure that states exactly what was AI-assisted, what data is synthetic, and what Gemini is used for.

Biggest opportunity to stand out:

- The strongest existing differentiator is not adding another model; it is making the human-in-the-loop safety story crisp and demonstrable: red-flag override, ML probabilities, LLM rationale, clinician override, and audit trail all on one patient page.
- The bilingual dictation feature is also a strong judge-facing differentiator if it works live. It should be rehearsed with a short scripted English and Bengali/Banglish transcript.

Recent commit/activity summary:

- No git repository is available in this workspace, so no commit history can be summarized.
- File timestamps show planning docs were created on 2026-08-17, major backend/data artifacts around 2026-08-17 evening, frontend work around 2026-08-18, and Python cache files updated during 2026-08-19 audit commands.
