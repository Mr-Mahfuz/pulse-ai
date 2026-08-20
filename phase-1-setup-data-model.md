# Phase 1 — Project Setup, Data Model & Synthetic Dataset

> **Goal:** Get both frontend and backend running locally, define the data model, generate a synthetic patient dataset, and train the ML triage classifier.
> **Time Budget:** ~60 minutes (of 5 hours)

---

## Tasks (Ordered)

### 1.1 — Initialize Backend (Python + FastAPI)

```
smarttriage/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt     # Dependencies
│   ├── models.py            # Pydantic schemas
│   ├── database.py          # SQLite setup (SQLAlchemy)
│   ├── triage_engine.py     # Core triage logic (Phase 2)
│   ├── ml_model.py          # ML classifier (Phase 2)
│   ├── routes/
│   │   ├── patients.py      # Patient CRUD
│   │   ├── triage.py        # Triage endpoints
│   │   └── audit.py         # Audit log endpoints
│   ├── data/
│   │   ├── generate_synthetic.py  # Synthetic data generator
│   │   ├── train_model.py         # Model training script
│   │   └── synthetic_patients.json
│   └── smarttriage.db       # SQLite database (generated)
```

**Dependencies** (`requirements.txt`):
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0
pydantic>=2.0
scikit-learn>=1.3
pandas>=2.0
numpy>=1.24
google-generativeai>=0.8.0
python-dotenv>=1.0
```

### 1.2 — Initialize Frontend (Nuxt + Vue)

```
smarttriage/
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.js
│   │   │   ├── page.js        # Dashboard (triage queue)
│   │   │   └── patient/
│   │   │       └── [id]/
│   │   │           └── page.js  # Patient detail view
│   │   ├── components/
│   │   │   ├── TriageQueue.js
│   │   │   ├── PatientCard.js
│   │   │   ├── PatientForm.js
│   │   │   ├── VitalsPanel.js
│   │   │   ├── AIRationalePanel.js
│   │   │   └── AuditLog.js
│   │   └── lib/
│   │       └── api.js           # API client
│   └── public/
```

**Dependencies**: Nuxt (Vue), Tailwind CSS

### 1.3 — Define Data Model

#### Patient Table
| Column | Type | Description |
|---|---|---|
| id | UUID (string) | Primary key |
| name | string | Patient display name |
| age | int | Age in years |
| gender | string | M/F/Other |
| chief_complaint | text | Free-text symptom description |
| heart_rate | int | BPM |
| systolic_bp | int | mmHg |
| diastolic_bp | int | mmHg |
| respiratory_rate | int | breaths/min |
| temperature | float | °C |
| spo2 | int | % oxygen saturation |
| gcs_score | int | Glasgow Coma Scale (3-15) |
| medical_history | text | Free-text history |
| arrival_time | datetime | When patient arrived |
| triage_level | int (1-5) | AI-assigned ESI level |
| triage_confidence | float | Model confidence (0-1) |
| triage_rationale | text | LLM-generated explanation |
| triage_model_version | string | Model identifier |
| triage_timestamp | datetime | When triage was last computed |
| clinician_override | int (null) | Manual override ESI level |
| status | string | waiting / in-treatment / discharged |
| created_at | datetime | Record creation time |

#### Audit Log Table
| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| patient_id | UUID (FK) | Link to patient |
| action | string | triage_computed / override / vitals_updated |
| old_value | JSON | Previous state |
| new_value | JSON | New state |
| actor | string | system / clinician |
| timestamp | datetime | When action occurred |

### 1.4 — Generate Synthetic Patient Dataset

Create `generate_synthetic.py` that produces ~200 synthetic patients with realistic:
- Vital sign ranges (normal vs. abnormal)
- Chief complaints (text strings matching ESI triage guidelines)
- Medical histories
- Ground-truth ESI labels (1=Resuscitation through 5=Non-urgent)

Distribution: ESI-1 (5%), ESI-2 (15%), ESI-3 (35%), ESI-4 (30%), ESI-5 (15%)

### 1.5 — Train ML Triage Classifier

Using `train_model.py`:
1. Load synthetic dataset
2. Feature engineering: vitals (numeric) + symptom keyword indicators (binary)
3. Train a **Random Forest** or **Gradient Boosting** classifier (scikit-learn)
4. Evaluate with train/test split — report accuracy + confusion matrix
5. Save model as `triage_model.pkl` via joblib
6. This becomes our "own trained model" for the judges

### 1.6 — Verify Phase 1

- [ ] `uvicorn backend.main:app --reload` starts without errors
- [ ] `npm run dev` starts frontend without errors
- [ ] SQLite DB created with correct schema
- [ ] Synthetic dataset generated (200+ patients)
- [ ] ML model trained and saved (>70% accuracy on synthetic data)
- [ ] Basic CRUD: can create/read patients via API

---

## API Contracts Introduced

### `POST /api/patients`
Create a new patient record.
```json
// Request
{
  "name": "string",
  "age": 25,
  "gender": "M",
  "chief_complaint": "Severe chest pain radiating to left arm, shortness of breath",
  "heart_rate": 120,
  "systolic_bp": 90,
  "diastolic_bp": 60,
  "respiratory_rate": 28,
  "temperature": 37.2,
  "spo2": 88,
  "gcs_score": 15,
  "medical_history": "History of hypertension, smoking 10 years"
}

// Response: 201 Created
{
  "id": "uuid",
  "...all fields...",
  "triage_level": null,  // Not yet triaged
  "status": "waiting"
}
```

### `GET /api/patients`
List all patients, ordered by triage priority.

### `GET /api/patients/{id}`
Get single patient with full details.

### `PUT /api/patients/{id}`
Update patient (e.g., change vitals).

### `GET /api/audit/{patient_id}`
Get audit log for a patient.

---

## 🔴 USER ACTION REQUIRED

1. **Python virtual environment**: I'll create this for you, but confirm you have Python 3.10+ installed.
2. **Node.js**: Confirm you have Node.js 18+ installed (needed for Nuxt).
3. **Google Gemini API Key**: You'll need a free API key from [Google AI Studio](https://aistudio.google.com/apikey).
   - Go to the link → Click "Create API Key" → Copy it
   - You'll set it as `GEMINI_API_KEY` in a `.env` file (I'll tell you exactly when and where)
   - This is free-tier and sufficient for our demo
