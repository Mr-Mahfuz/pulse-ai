# SmartTriage: Business Model & Impact

## 1. The Problem: ED Starvation and Burnout
Emergency Departments (EDs) are at a breaking point globally.
- **Triage Delay:** Patients wait hours just to be seen by a triage nurse.
- **Silent Deterioration:** Patients in the waiting room often deteriorate unnoticed, leading to adverse outcomes.
- **Cognitive Overload:** Triage nurses suffer from severe decision fatigue, causing misclassification of patient acuity.

## 2. The Solution: AI-Powered Autonomous Triage
SmartTriage is a multi-layered AI triage engine designed to safely and autonomously categorize patients:
- **Instant Intake:** Voice-to-text processing for barrier-free patient enrollment.
- **Explainable AI:** Fuses deterministic safety rules, machine learning (Random Forest), and Generative AI (LLMs) to ensure 100% transparent and safe triage routing.
- **Continuous Monitoring:** Hardware IoT integration for continuous SpO2/HR monitoring while waiting.

## 3. Real-World Impact (High Social Return)
- **Zero Wait-to-Triage:** Eliminates the initial bottleneck. Every patient is triaged instantly upon arrival.
- **Equity in Care:** Bilingual generative AI rationale translates medical reasoning into the patient's native language, empowering them.
- **Preventing Adverse Events:** Dynamic SLA tracking ensures patients are escalated *before* they breach safe waiting thresholds.

## 4. Scalable Business Model
SmartTriage operates on a highly scalable B2B SaaS + Hardware model.

### Tier 1: Software Core (SaaS)
- **Target:** Urgent Care Clinics, Rural Hospitals.
- **Pricing:** $1,500 / month per facility.
- **Features:** Voice parsing, AI Triage Engine, Basic Dashboard.

### Tier 2: Enterprise + Hardware IoT
- **Target:** Large Urban Emergency Departments.
- **Pricing:** $8,000 / month per facility + hardware leasing.
- **Features:** Full Tier 1 + Wearable Oximeter integration for continuous waiting room monitoring, custom EHR integrations (Epic/Cerner), and Advanced Analytics.

## 5. Token Optimization & Cost Efficiency
We’ve engineered our pipeline to be exceptionally cost-effective:
- **Rules Bypassing:** Deterministic red flags (e.g., HR < 40 = ESI 1) bypass the LLM entirely, saving latency and API costs.
- **Cost per Triage:** We achieve a blended cost of **<$0.001 per patient** using Gemini 2.5 Flash for transcription and rationale generation.

## 6. The "Production-Grade" Advantage
- **Fully Dockerized:** SmartTriage ships with full containerization, ready to deploy to any hospital’s secure cloud or on-premise Kubernetes cluster.
- **HIPAA Compliant:** Built-in Privacy Mode for public waiting room monitors, ensuring PHI is strictly masked.
