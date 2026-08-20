# SmartTriage

**AI Emergency Patient Prioritization System**

SmartTriage is an intelligent emergency department triage assistant designed to evaluate patient intake data (vitals and symptoms) in real-time, assigning an Emergency Severity Index (ESI) level (1-5) through a robust, auditable AI pipeline.

## System Architecture
SmartTriage uses a **three-layer architecture** for triage:
1. **Red-Flag Rules Engine (Safety Net):** Deterministic evaluation of extreme vitals (e.g., SpO2 < 85%) and critical symptoms (e.g., "cardiac arrest") that bypasses ML to assign ESI-1 or ESI-2.
2. **Machine Learning Classifier:** A Random Forest model trained on 24 features (including vitals and symptom indicators) to output a baseline ESI probability.
3. **LLM Explanation Layer:** Google Gemini generates a concise, plain-language clinical rationale explaining *why* the specific ESI level was recommended. 

The clinician remains the ultimate authority, with the ability to override any AI triage decision, all of which is permanently stored in the chronological audit log.

## Features
- **Intelligent Triage Pipeline:** Rules + ML + LLM.
- **Voice Dictation:** Browser speech-to-text with Gemini parsing structured clinical data.
- **Real-time Dashboard:** Live updating queue sorting patients by priority and SLAs.
- **Full Bilingual Support:** English and Bengali interface and rationale.
- **Mass Casualty Incident (MCI) Mode:** Stripped down UI prioritizing START triage protocols.

## Tech Stack
- **Frontend:** Nuxt 4, Vue 3, Tailwind CSS
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **AI Models:** Scikit-learn (Random Forest), Google GenAI (`gemini-2.5-flash`)

## Setup & Running Locally

### 1. Backend Setup
```bash
# Navigate to project root
cd smarttriage

# Install dependencies
pip install -r backend/requirements.txt

# Create .env and set your Google Gemini API key
echo "GEMINI_API_KEY=your_key_here" > backend/.env

# Start the FastAPI server
python -m uvicorn backend.main:app --reload
```
*The backend will run on `http://localhost:8000`.*

### 2. Frontend Setup
```bash
# Open a new terminal and navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the Nuxt development server
npm run dev
```
*The frontend will run on `http://localhost:3000`.*

## AI Disclosure & Limitations
- **Synthetic Training Data:** The ML classifier (Random Forest) was trained purely on synthetically generated patient records. It has **not** been validated on real clinical datasets and is intended solely for demonstration purposes as a prototype.
- **Clinical Validation:** SmartTriage is a decision-support prototype and should not be used in a real clinical setting without extensive validation, regulatory approval, and rigorous testing.
- **LLM Usage:** Google Gemini is used exclusively for (1) generating plain-text rationale for computed ESI levels, and (2) parsing speech-to-text dictation into structured JSON. It **does not** independently determine the triage level. If the API is unavailable, the system gracefully falls back to template-based explanations and manual form entry.
