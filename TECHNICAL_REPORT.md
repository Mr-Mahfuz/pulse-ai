# Technical Report: SmartTriage Architecture & Methodology

**Project**: SmartTriage (AI Emergency Patient Prioritization System)  
**Track**: Healthcare AI (Track 2)  

---

## 1. Executive Summary

SmartTriage is an intelligent, bilingual emergency department triage assistant. Its primary objective is to transform unstructured patient intake data (symptoms, vitals, history) into a real-time, explainable, and color-coded prioritization dashboard (Emergency Severity Index 1-5). 

The system relies on a **Three-Layer AI Pipeline** that prioritizes patient safety above all else. Instead of relying purely on a generative language model to make high-stakes medical decisions, SmartTriage uses deterministic safety rules, machine learning classifiers, and LLMs in specialized roles to *assist* the human clinician, rather than replace them.

---

## 2. The 3-Layer AI Pipeline

Our architecture ensures safety, mathematical predictability, and human-readable explainability.

### Layer 1: Deterministic Red-Flag Engine
- **Technology**: Hardcoded Python logic (`triage_engine.py`)
- **How it works**: Evaluates vitals and chief complaints against strict physiological thresholds (e.g., SpO2 < 85%, HR > 180, GCS ≤ 8). 
- **Purpose**: Acts as an absolute safety net. If a patient meets life-threatening criteria, they are instantly flagged as ESI-1 or ESI-2. Machine learning is intentionally bypassed for these critical cases.

### Layer 2: Machine Learning Risk Classifier
- **Technology**: `scikit-learn` Random Forest Classifier (trained on synthetic ED data).
- **How it works**: Extracts 24 features (vitals, derived hemodynamics like mean arterial pressure, and NLP symptom keywords). It outputs a probability distribution across ESI levels.
- **Purpose**: Handles the vast majority of non-critical (ESI 3-5) patients by recognizing statistical patterns in vital signs and symptoms.

### Layer 3: LLM Explanation Generation
- **Technology**: Google Gemini 3.6 Flash (`google.genai` SDK)
- **How it works**: Takes the final triage assignment, the triggered red flags, the ML probabilities, and the patient context, then constructs a prompt asking the LLM to explain the decision based on standard ESI definitions.
- **Purpose**: Generates a 2-3 sentence, clinician-readable rationale. **The LLM explains the decision; it does not make the decision.**

---

## 3. Technology Stack

- **Frontend**: Nuxt 3 (Vue.js), Tailwind CSS. Provides a reactive, live-polling dashboard with auto-calculating SLA breaches and estimated wait times.
- **Backend API**: Python / FastAPI. Provides robust, async REST endpoints.
- **Database**: SQLite with SQLAlchemy. Chosen for zero-configuration portability during a hackathon environment while maintaining full ACID compliance and Audit Trails.
- **AI/ML Integration**: 
  - `gemini-2.5-flash`: Used with strict JSON Schema generation for parsing raw voice dictation into structured Pydantic models.
  - `gemini-3.6-flash`: Used for complex clinical reasoning and generating the final bilingual rationale.
  - `scikit-learn`: For the Random Forest triage classifier.

---

## 4. Methodology & Safety Mechanisms

1. **Human-in-the-Loop Override**: Any clinician can override an AI triage decision. This override is permanently recorded in the patient's audit log.
2. **Immutable Audit Trails**: Every action (registration, vital updates, triage computations, overrides) creates a time-stamped log. The system tracks exactly which model version made which decision and why.
3. **Live Re-Triage**: Updating a patient's vitals (e.g., SpO2 drops from 95% to 88%) triggers a real-time re-triage. The ML model runs instantly, the LLM generates a new rationale, and the dashboard updates without a page reload.
4. **LLM Fallback**: If the Gemini API rate-limits or times out, the system falls back to a template-based rationale engine. The system will *never* fail to provide a triage score due to an API outage.

---

## 5. Anticipated Judge Q&A

**Q: Why didn't you just use an LLM for the whole triage decision?**
**A:** Patient safety. LLMs are prone to hallucinations and lack mathematical predictability. By using a 3-layer approach, we guarantee that critical patients (e.g., SpO2 < 85%) are caught by deterministic rules (Layer 1). We use ML (Layer 2) for statistical probability, and strictly limit the LLM (Layer 3) to *explaining* the decision. This creates a safer, more auditable system.

**Q: How does your voice dictation handle messy input?**
**A:** We use the Web Speech API to capture raw audio, and then pass the messy transcript to `gemini-2.5-flash` using a **Strict JSON Schema**. This forces the LLM to output a valid JSON object matching our database schema, ensuring we never get unstructured chat responses, only clean data.

**Q: How did you train the machine learning model?**
**A:** We generated a synthetic dataset of 200+ realistic emergency room encounters, complete with vitals, symptoms, and ground-truth ESI labels. We extracted 24 features (including derived metrics like pulse pressure) and trained a Scikit-Learn Random Forest model. 

**Q: What happens if the internet goes down and the Gemini API fails?**
**A:** The core triage engine (Red Flags + Scikit-Learn) runs entirely locally on the backend. If the Gemini API fails, the system falls back to a local, template-based explanation generator. The patient will still receive their ESI level and priority instantly.

**Q: How are you ensuring clinician accountability?**
**A:** The `AuditLog` table records every state change. If a patient is downgraded from ESI-2 to ESI-3 by a human, we log the timestamp, the clinician's ID, the override reason, and the previous AI score. This makes the tool enterprise-ready for actual hospital liability tracking.
