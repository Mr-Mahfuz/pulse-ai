# SmartTriage: Comprehensive User Manual & Instructions

Welcome to the **SmartTriage** User Manual. This document provides a complete guide on how to set up, run, and use the AI-Powered Emergency Patient Prioritization System. 

---

## 📑 Table of Contents
1. [Overview](#1-overview)
2. [Prerequisites & Setup](#2-prerequisites--setup)
3. [Running the Application](#3-running-the-application)
4. [Using the Application (User Guide)](#4-using-the-application-user-guide)
5. [System Architecture](#5-system-architecture)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Overview
SmartTriage is an intelligent emergency department triage assistant designed to transform unstructured patient intake data into a real-time, color-coded prioritization dashboard. It uses a three-layer AI architecture (Clinical NLP, ML Classifier, LLM Rationale) to evaluate vitals and symptoms, and assign an **Emergency Severity Index (ESI)** level (1-5).

**The AI assists but never replaces the clinician.** Every decision is auditable, explainable, and can be overridden by a human professional.

---

## 2. Prerequisites & Setup

Before running the application, ensure your system has the following installed:
- **Python 3.9+** (For the FastAPI Backend)
- **Node.js 18+** (For the Nuxt/Vue Frontend)
- **Git** (For version control)

### Step-by-step Setup
1. **Clone or Download the Repository**
   Ensure you are in the root directory: `c:\workspace\Personal\smarttriage`

2. **Configure the Backend (Python)**
   Open a terminal in the root folder and run:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
   *Create your environment variables:*
   In the `backend/` folder, create a file named `.env`. Add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

3. **Configure the Frontend (Node.js)**
   Open a new terminal in the root folder and run:
   ```bash
   cd frontend
   npm install
   ```

---

## 3. Running the Application

### The Easy Way (Windows Only)
We have provided an automated batch script to launch both the frontend and backend simultaneously.
1. Navigate to the project root folder.
2. Double-click the **`run.bat`** file in File Explorer, OR run `.\run.bat` from your command prompt / PowerShell.
3. Two terminal windows will open automatically.

### The Manual Way (Mac/Linux/Windows)
If you prefer to start them manually or the batch file fails:

**Terminal 1 (Backend):**
```bash
cd backend
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
*API is accessible at http://127.0.0.1:8000*

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
*UI is accessible at http://localhost:3000*

---

## 4. Using the Application (User Guide)

### 4.1 The Triage Dashboard (Home Screen)
- **Summary Stats:** At the top of the dashboard, you will see a breakdown of patients per ESI Level (1 = Most Urgent, 5 = Least Urgent).
- **The Queue:** This table displays all patients in the system, automatically sorted by ESI level and wait time. It polls the backend automatically, so new patients appear in real-time.
- **Language Toggle:** In the top right, switch between English (EN) and Bengali (BN) instantly.

### 4.2 Registering a New Patient
1. Click the **"Register Patient"** button on the dashboard.
2. **Manual Entry:** You can type the patient's name, age, symptoms, and vitals manually.
3. **Voice Dictation (AI Feature):** 
   - Click the **"Dictate"** button.
   - Speak naturally (e.g., *"The patient is John Doe, 45 year old male, presenting with severe crushing chest pain, heart rate 135, oxygen 92%..."*).
   - Click the button again to stop. The AI will parse your speech and auto-fill the form perfectly.
4. Click **"Submit & Triage"**. The AI will evaluate the patient immediately.

### 4.3 Patient Detail View & AI Rationale
Click on any patient in the Queue to view their detailed record.
- **AI Assessment Card:** Displays the assigned ESI Level, any triggered "Red Flags" (e.g., *SpO2 < 90%*), the ML model's confidence score, and a plain-text rationale explaining exactly *why* the AI made this decision.
- **Vitals & Live Re-Triage:** You can edit the patient's vitals directly on this page. Clicking **"Save"** will update the record and *instantly re-run the AI triage*, recalculating priority based on the new data.

### 4.4 Clinician Overrides & Audit Log
- **Human-in-the-Loop Override:** If a clinician disagrees with the AI, they can click **"Override"** on the AI Assessment card. Select the new ESI level, provide a brief reason, and save. The queue updates instantly.
- **Audit Trail:** Located at the bottom of the patient page, this timeline records every single action taken on the patient—initial registration, AI scores, vitals updates, and human overrides—ensuring complete accountability.

### 4.5 Generating Reports
- Click **"Print Report"** on the patient detail page. The system will format the record into a clean, A4 hospital document with official letterheads, ready for physical printing or PDF saving.

---

## 5. System Architecture
SmartTriage uses a 3-layer pipeline to ensure safety and explainability:
1. **Red-Flag Rules Engine (Deterministic):** Instantly catches life-threatening conditions (SpO2 < 90%, HR > 130) and forces an ESI-1 or ESI-2 assignment.
2. **ML Classifier:** A trained Random Forest model that evaluates non-critical vitals and symptoms to predict ESI levels with mathematical confidence.
3. **LLM Explanation Layer (Gemini):** Takes the outputs of steps 1 and 2, and generates a clinician-friendly rationale. *The LLM explains the decision; it does not make the decision.*

---

## 6. Troubleshooting

**Q: The frontend says "Network Error" or "Backend Offline"**
- Ensure the FastAPI backend is running on `port 8000`. 
- Check the backend terminal for errors (e.g., a missing `.env` file or invalid Gemini API key).

**Q: The Voice Dictation isn't working**
- Voice dictation requires microphone permissions in your browser. Check your browser's address bar for a blocked microphone icon.
- Ensure you have a valid Internet connection (Web Speech API requires it in some browsers).

**Q: AI Rationale is failing or timing out**
- Check your `GEMINI_API_KEY` in the `backend/.env` file. Ensure you have not exceeded your quota.

---
*End of Document. Built for the LaunchPad AI Hackathon 2026.*
