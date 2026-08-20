# SmartTriage: Technical Architecture & AI Methodology Report

## 1. Executive Summary
SmartTriage is a modern, decoupled web application built to streamline and prioritize emergency department admissions. It addresses the critical issue of "queue starvation" where lower-priority patients deteriorate silently while waiting for care. By combining deterministic clinical rules, machine learning, and large language models, the system actively categorizes patients and explains its rationale, ensuring transparent and auditable AI-assisted triage.

## 2. Technology Stack
- **Frontend:** Nuxt 4 (Vue.js 3), Tailwind CSS, Vite
- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Database:** SQLite with SQLAlchemy ORM
- **AI / ML:** 
  - `scikit-learn` (Random Forest Classifier)
  - Google GenAI SDK (`gemini-2.5-flash`)

## 3. The Three-Layer AI Pipeline

SmartTriage does not rely on a single AI model. It uses a cascading three-layer architecture to guarantee safety, accuracy, and explainability.

### Layer 1: Deterministic Red-Flag Rules Engine (`triage_engine.py`)
**Methodology:** Before any ML model evaluates the patient, their vitals are checked against hardcoded, universally accepted physiological thresholds (e.g., SpO2 < 85%, HR > 150).
- **Purpose:** Acts as a fail-safe. Life-threatening conditions automatically bypass the ML model and are immediately assigned ESI-1 or ESI-2.
- **Judge Q&A:** *"Why use hard rules if you have AI?"* -> "AI is probabilistic; emergency medicine requires guarantees. Our rules engine ensures that no matter what the ML predicts, critical physiological signs will always trigger an immediate, high-priority alert."

### Layer 2: Machine Learning Risk Classifier (`ml_model.py`)
**Methodology:** If no red flags are triggered, the patient data is vectorized and passed into a trained `RandomForestClassifier`.
- **Model Details:** 
  - **Algorithm:** Random Forest (an ensemble of decision trees).
  - **Features (24 total):** Includes normalized continuous vitals (HR, BP, SpO2, Temp, GCS) and boolean flags derived from keyword matching in the chief complaint (e.g., `has_cardiac_pain`, `has_stroke_signs`).
  - **Target:** ESI Level (1 to 5).
  - **Training Data:** Synthetically generated datasets modeling realistic triage distributions.
- **Output:** Returns a probability distribution across all 5 ESI levels and selects the highest-probability class.
- **Judge Q&A:** *"What parameters did you train on?"* -> "We trained on 24 features encompassing both physiological vitals and natural-language symptoms extracted via keyword mapping. We chose Random Forest because it is robust to non-linear clinical relationships and provides interpretable feature importances, unlike black-box deep learning."

### Layer 3: LLM Explainability Layer (`llm_explainer.py`)
**Methodology:** The final ESI decision (from Layer 1 or 2), the patient's vitals, and their chief complaint are structured into a prompt and sent to Google Gemini (`gemini-2.5-flash`).
- **Purpose:** To bridge the gap between algorithmic output and clinical trust. Gemini acts strictly as an explainer—it translates the *why* of the decision into a concise, 2-3 sentence clinical rationale based on standard ESI guidelines.
- **Bilingual Output:** Gemini translates this rationale into English or Bengali based on user preference.
- **Judge Q&A:** *"Is the LLM making the triage decision?"* -> "No. LLMs are prone to hallucination, which is dangerous in triage. Our deterministic rules and ML model make the decision; Gemini is only used to explain the clinical reasoning behind that pre-computed decision to the clinician."

## 4. Voice Parsing & Data Extraction (`speech.py`)
**Methodology:** Nurses can dictate patient information instead of typing.
- **Process:** The browser's Web Speech API streams text to the backend. The backend uses Google Gemini in **Structured Output Mode** (using a rigid JSON schema) to mathematically guarantee that the unstructured text is accurately parsed into demographic data, complaints, and discrete vitals.
- **Judge Q&A:** *"How do you prevent the AI from missing vitals in speech?"* -> "We enforce a strict JSON schema on the Gemini API response. If the LLM identifies a heart rate in the audio transcript, it is forced to map it to the `heart_rate` integer field. If it's missing, it returns `null`. This prevents parsing errors and hallucinations."

## 5. Security, Auditability, and Human-in-the-Loop
- **Clinician Override:** The AI is an assistant, not an autonomous agent. Clinicians can override any ESI level assigned by the AI.
- **Audit Trail:** Every state change—initial triage, vital updates, AI re-evaluations, and clinician overrides—is permanently logged in the SQLite database (`audit_logs` table). This ensures 100% retrospective transparency for hospital administration and legal compliance.

## 6. Mass Casualty Incident (MCI) Protocol
**Methodology:** In disaster scenarios, standard ESI triage is too slow. The system features a one-click toggle to enter MCI Mode, which maps patients to the international START protocol (Immediate/Red, Delayed/Yellow, Minor/Green).

## 7. Known Limitations & Future Work
- **Synthetic Data:** The current Random Forest model is trained on synthetic data. For production, it must be retrained on a de-identified, real-world clinical dataset (e.g., MIMIC-IV).
- **IoT Integration:** Future versions will integrate direct hardware telemetry (e.g., ESP32 pulse oximeters) to stream vitals directly into the system, bypassing manual entry entirely.
