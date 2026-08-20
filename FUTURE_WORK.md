# SmartTriage AI: Future Work & Roadmap

While the current version of SmartTriage AI successfully demonstrates a highly functional, secure, and auditable AI-assisted emergency department workflow, several key features and integrations are planned for the next phases of development to make it ready for true enterprise clinical deployment.

## 1. Real-World Model Retraining (Clinical Validation)
- **Current State:** The Random Forest model is trained on a synthetic dataset designed to model triage distributions.
- **Future Work:** Partner with clinical institutions to retrain and validate the ML model against large-scale, de-identified real-world clinical datasets (e.g., MIMIC-IV), ensuring statistical robustness across diverse demographics and edge cases.

## 2. True IoT Hardware Integration
- **Current State:** Hardware telemetry is simulated in the UI using randomized intervals to mimic a live sensor.
- **Future Work:** Integrate physical IoT hardware (e.g., ESP32 microcontrollers connected to pulse oximeters and blood pressure cuffs). This will allow the system to ingest vitals directly via WebSockets or MQTT, entirely removing the need for manual data entry.

## 3. EHR / EMR Interoperability (HL7/FHIR)
- **Current State:** SmartTriage operates as a standalone decoupled database.
- **Future Work:** Implement HL7 and FHIR standards to allow seamless two-way data synchronization with existing hospital Electronic Health Records (like Epic or Cerner).

## 4. Advanced Computer Vision Trauma Assessment
- **Current State:** Triage relies on structured vitals and transcribed text (voice or typed).
- **Future Work:** Introduce a computer vision module to assess visual indicators of trauma, estimating blood loss, identifying severe burns, or recognizing stroke signs (e.g., facial drooping) directly from a camera feed at the triage desk.

## 5. Predictive Surge Analytics
- **Current State:** The system tracks the live queue and highlights SLA breaches.
- **Future Work:** Build a predictive analytics engine that analyzes historical hospital influx data, weather patterns, and local events to forecast ED surges hours in advance, allowing administrators to dynamically adjust staffing.

## 6. Patient Wearables & Real-Time Geofencing
- **Current State:** Patients track their status via a centralized public monitor.
- **Future Work:** Issue BLE (Bluetooth Low Energy) wristbands to waiting patients. This would allow the system to track exactly where a patient is in the hospital, and ping their wristband if their vitals suddenly drop while they are in the waiting room or restroom.

## 7. Multi-Agent Clinician Handoff
- **Current State:** The AI assists the initial triage nurse.
- **Future Work:** Expand the LLM to generate automated, structured "handoff summaries" for the attending physician, ensuring that zero context is lost when the patient is finally transferred from the waiting room to an ED bed.
