# SmartTriage User Manual

Welcome to the SmartTriage system. This manual provides complete instructions for nurses, triage officers, and clinicians on how to use the system effectively.

---

## 1. Dashboard Overview

The **Triage Queue Dashboard** is your primary workspace. It provides a real-time, color-coded overview of all waiting patients.

### Summary Statistics
At the top of the dashboard, you will see a breakdown of the current waiting room load:
- **Total In Queue:** Total number of patients waiting.
- **ESI 1 to ESI 5 Counts:** A count of patients in each triage category (Red to Blue).

### Triage Queue Table
The queue automatically sorts patients based on their clinical priority, ensuring the sickest patients are always at the top.
- **SLA Breach Alerts:** If a patient has been waiting longer than is safe for their assigned ESI level (e.g., >120 mins for ESI-4), the system will flash a red **"SLA Breach"** warning.
- **Queue Tabs:** You can switch between the **Main ED** queue (ESI 1-3) and the **Fast Track** queue (ESI 4-5) to better manage patient flow.
- **History (Cleared):** Click this tab to view patients who have been discharged, cleared, or moved to a doctor. You can restore patients back to the active queue from here.

---

## 2. Registering a New Patient (Voice Dictation)

SmartTriage allows you to dictate patient information hands-free.

1. Click the **Register Patient** button on the dashboard.
2. In the modal, click the **Dictate** button. The button will turn red and indicate that it is listening.
3. Speak clearly and naturally. For example: 
   *"The patient is an 80 year old male presenting with severe chest pain. Heart rate is 110, oxygen is 92 percent, temperature is 38 degrees."*
4. Click the red button again to stop listening.
5. The AI will parse your speech and automatically fill in the Name, Age, Gender, Complaint, and Vitals.
6. Review the extracted data. You can manually type or correct any fields as needed.
7. Click **Submit & Triage**. The AI will instantly compute the patient's ESI level and add them to the queue.

---

## 3. Reviewing Patient Details

Click on any patient in the dashboard queue to view their full medical record.

### Clinical Presentation & Vitals
- **Chief Complaint:** Displays the reason for the patient's visit.
- **Vitals:** Displays the patient's current vitals. 
- **Updating Vitals:** If you take a new set of vitals, enter them into the fields and click **Save**. The system will save the new vitals, log the time they were taken, and **automatically re-run the AI triage** to see if the patient's condition has worsened.

### AI Assessment
- **ESI Level & Red Flags:** Displays the calculated ESI level. If the patient triggered any critical safety rules (e.g., SpO2 < 85%), a red flag badge will appear.
- **ML Probability:** Shows the AI's confidence across all 5 ESI levels.
- **Clinical Rationale:** A plain-language explanation written by the AI explaining *why* it assigned the specific ESI level.
- **Translation:** You can click the **BN** (Bengali) or **EN** (English) buttons to translate the clinical rationale instantly.

### Audit Trail
- The right side of the screen shows a chronological log of every action taken on the patient (registration, vital updates, AI re-evaluations, and manual overrides). This ensures complete accountability.

---

## 4. Clinician Override

The AI is an assistant; the clinician is always in charge. If you disagree with the AI's triage decision:

1. Open the patient's detail page.
2. In the AI Assessment card, click the orange **Override** button.
3. Select the ESI level you believe is clinically appropriate.
4. Provide a brief reason for the override (e.g., "Patient appears more distressed than vitals indicate").
5. Click **Submit Override**.
6. The patient's priority will be instantly updated in the queue, and your override will be permanently recorded in the Audit Trail.

---

## 5. Clearing and Restoring Patients

When a patient is called in to see a doctor or leaves the ED:
1. Open their patient detail page.
2. Click the **Clear Patient** button at the top of the screen.
3. This removes them from the active triage queue.

**To undo a clear:**
1. On the main dashboard, click the **History (Cleared)** tab.
2. Click on the cleared patient's name.
3. Click the **Restore Patient** button at the top of the screen to place them back into the active queue.

---

## 6. Mass Casualty Incident (MCI) Mode

In the event of a disaster (e.g., multi-vehicle pileup, natural disaster):
1. On the main dashboard, click the **MCI Mode** toggle in the top right corner.
2. The complex UI will be stripped away.
3. The system switches to the international **START Triage Protocol** (Immediate, Delayed, Minor, Deceased).
4. Patients are displayed in massive, high-contrast cards for maximum visibility in chaotic environments.
5. Click the toggle again to return to standard ED operations.

---

## 7. Printing Reports

If a physical chart is required:
1. Open the patient's detail page.
2. Click the **Print Report** button at the top.
3. The system will format a clean, standardized A4 hospital document with an official letterhead and empty lines for physician notes and signatures. 
*(Tip: In your print settings, ensure "Headers and footers" is unchecked and "Background graphics" is checked for the best result).*
