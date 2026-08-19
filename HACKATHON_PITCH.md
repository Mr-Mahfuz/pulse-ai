# SmartTriage: The Future of Emergency Department Flow

Welcome to the SmartTriage project pitch. This document outlines the clinical problem we solve, our unique technological approach, and the ambitious roadmap we plan to execute next.

---

## The Problem: The "Orphaned Queue" & Triage Starvation

Modern Emergency Departments (EDs) are fundamentally broken at the point of entry. 
When a mass of patients arrive, triage nurses rely on static models (like standard ESI) to prioritize them. The flaw? **Queue Starvation.** 
If an ED is saturated with critical trauma cases (ESI 1 & 2), lower acuity patients (ESI 4 & 5) are infinitely delayed. They sit in the waiting room unmonitored for 6+ hours. Inevitably, they either leave without being seen (LWBS)—a massive liability—or they physically deteriorate in the waiting room until they become a critical ESI 2.

## Our Solution: SmartTriage

SmartTriage isn't just a categorization tool; it's an **Active Queue Management** engine.

### 1. Dual-Queue Processing (Fast Track)
We've architected a dual-queue system. By automatically splitting ESI 4 & 5 patients into a "Fast Track" queue, hospitals can dedicate a single Nurse Practitioner to rapidly clear the backlog of minor cases in parallel with the main trauma teams, dramatically reducing LWBS metrics.

### 2. Automated Re-Triage SLA Alerts
We enforce Wait Time SLAs. If a patient sits in the queue longer than their safe window (e.g., >120 mins for ESI 4), the system automatically flags them with a "Re-Triage Required" alert. This safety net ensures no patient deteriorates silently in the waiting room.

### 3. Mass Casualty Incident (MCI) Mode
In the event of a disaster (e.g., multi-car pileup), standard triage is too slow. With one click, SmartTriage strips away complex UI elements and switches to the international **START Triage Protocol** (Red/Yellow/Green/Black), instantly optimizing the hospital for mass casualty sorting.

### 4. Continuous Voice Parsing
Nurses shouldn't be typing during chaos. Our system uses advanced LLMs to continuously parse raw, natural language voice dictation—extracting hidden comorbidities, age, and vitals, and mathematically guaranteeing a structured JSON output for our ML models.

---

## The Future Roadmap (Post-Hackathon)

### 1. Hardware-in-the-Loop (IoT Vitals Stream)
**Vision:** Eliminate manual vital entry entirely.
**Implementation:** We will integrate ESP32 microcontrollers connected to MAX30102 pulse oximetry sensors. When clipped onto a patient's finger in the waiting room, these sensors will stream live SpO2 and Heart Rate data directly to our FastAPI backend via WebSockets. If a patient's oxygen drops while they are waiting, the SmartTriage dashboard will instantly upgrade their priority.

### 2. Multi-Tenant SaaS Architecture
**Vision:** A regional triage network.
**Implementation:** By upgrading our SQLAlchemy database to support `tenant_id`, SmartTriage becomes a centralized SaaS platform. Regional hospital administrators will have a "God View" dashboard, comparing triage throughput and SLA breaches across multiple clinics in real-time.

### 3. Intelligent Load Balancing & SMS Divert
**Vision:** Proactive congestion management.
**Implementation:** When SmartTriage detects that the Fast Track queue wait time exceeds 4 hours, it triggers a "Capacity Warning." The system will automatically interface with the Twilio API to text ESI 5 patients: *"Current wait is 4 hours. The affiliated Urgent Care 2 miles away has a 15-minute wait. Click here for directions."* This intelligently load-balances the city's medical infrastructure.
