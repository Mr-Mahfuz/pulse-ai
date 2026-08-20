# SmartTriage: AI-Powered Emergency Patient Prioritization System

SmartTriage is an intelligent, bilingual (English/Bengali) emergency department triage system. It leverages large language models (Google Gemini) and strict clinical heuristics to assist triage nurses and clinicians in rapidly and accurately assigning Emergency Severity Index (ESI) levels (1-5) to incoming patients.

---

## 🌟 Key Features

1. **AI Voice Dictation & Parsing:** Nurses can dictate patient demographics, complaints, and vitals using continuous voice recognition. The AI strictly parses the natural language into structured clinical data.
2. **Intelligent Triage (ESI):** Automatically evaluates patient data against critical clinical red flags (e.g., hypoxia, tachycardia) and assigns a standardized ESI priority level (1 to 5).
3. **AI Clinical Rationale:** The system explains *why* a specific ESI level was chosen using plain, clinician-oriented language based on standard ESI definitions.
4. **Clinician Overrides & Audit Trail:** AI is a support tool, not a replacement. Clinicians can override the AI's triage decision. Every action (registration, vitals update, override) is permanently logged in a chronological audit trail.
5. **Print-Ready Reports:** Generate clean, standardized A4 hospital reports directly from the patient view.
6. **Full Bilingual Support:** Seamlessly switch between English and Bengali (Banglish/Bengali voice dictation is also supported).

---

## 🏗️ Technical Architecture

SmartTriage is a modern, decoupled web application.

### Tech Stack
*   **Frontend:** Nuxt 3 (Vue.js), Tailwind CSS, Vue i18n.
*   **Backend:** Python, FastAPI, SQLAlchemy (SQLite database).
*   **AI Integration:** Google GenAI SDK (`gemini-2.5-flash`).

### Core AI Pipelines
1.  **Speech-to-JSON Pipeline (`speech.py`):**
    *   Captures continuous Web Speech API transcripts.
    *   Uses Gemini with a **Strict JSON Schema (`response_schema`)** to mathematically guarantee the unstructured voice text is parsed into a valid Pydantic model (`PatientCreate`).
2.  **Triage Assessment Pipeline:**
    *   **Red-Flag Engine (`triage_engine.py`):** Evaluates vitals and symptoms against hardcoded physiological thresholds (e.g., SpO2 < 85% = Level 1).
    *   **ML Classifier (`ml_model.py`):** A Random Forest model that predicts the baseline ESI level and probabilities based on 24 features.
3.  **Rationale Generation Pipeline (`llm_explainer.py`):**
    *   Feeds the computed triage level, patient data, and triggered red flags back into Gemini.
    *   Prompts Gemini with standard ESI guidelines to generate a 2-3 sentence clinical explanation for the clinician.

---

## 📖 User Guide

### 1. Dashboard Overview
*   **Summary Stats:** View the total number of patients in the queue and a breakdown of patients per ESI level.
*   **Triage Queue:** A live-updating table of patients sorted strictly by Priority (ESI-1 first), then by wait time.
*   **Language Toggle:** Click the `EN / BN` switch in the top right to instantly translate the entire interface.

### 2. Registering a Patient (Voice Dictation)
1.  Click **"Register Patient"** on the dashboard.
2.  Click **"Dictate"**. The button will turn red and display *"Listening... (Click to Stop)"*.
3.  Speak naturally (e.g., *"The patient is Rahim, 58 year old male, presenting with severe crushing chest pain, heart rate 135..."*). You can pause while speaking; the system will continue listening.
4.  Click the red listening button again to stop.
5.  The AI will process your speech and automatically fill in the Name, Age, Gender, Complaint, and Vitals fields.
6.  Click **Submit & Triage**.

### 3. Reviewing Patient Details
*   Click on any patient row to open their detailed medical record.
*   **Clinical Presentation:** Displays the history and chief complaint.
*   **AI Assessment:** Displays the ESI Level, triggered Red Flags, confidence percentage, and the AI's plain-text clinical rationale.
*   **Vitals:** Editable input fields for HR, BP, RR, Temp, SpO2, and GCS.
*   **Audit Trail:** A timeline of every action taken on this patient.

### 4. Clinician Override & Updating Vitals
*   **Updating Vitals:** Change a number in the Vitals card and click **Save**. The system will save the new vitals, log the change in the audit trail, and automatically re-run the AI triage to see if the priority level needs to change.
*   **Overriding AI:** If you disagree with the AI's ESI level, click **Override** in the AI Assessment card. Select your professional ESI level, type a brief reason, and save. The patient's priority is instantly updated in the queue.

### 5. Printing Reports
*   From a patient's detail page, click **Print Report**.
*   The system strips away all UI elements (sidebars, buttons) and renders a clean, 3-column A4 hospital document with an official letterhead. *(Tip: Uncheck "Headers and footers" in your browser print dialog for the best result).*

---

## 💻 Running Locally

### Backend Setup
1. Open a terminal in the project root.
2. Ensure you have Python installed and your virtual environment activated.
3. Install dependencies (if not already done): `pip install -r requirements.txt` (or equivalent).
4. Create a `.env` file in the `backend/` directory containing your API key: `GEMINI_API_KEY=your_key_here`
5. Run the FastAPI server:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
   *The backend will run on `http://localhost:8000`.*

### Frontend Setup
1. Open a new terminal in the `frontend/` directory.
2. Install dependencies: `npm install`
3. Start the Nuxt development server:
   ```bash
   npm run dev
   ```
   *The frontend will be accessible at `http://localhost:3000` (or `3001` depending on port availability).*
