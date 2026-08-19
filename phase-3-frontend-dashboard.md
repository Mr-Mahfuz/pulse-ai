# Phase 3 — Frontend Dashboard & UI

> **Goal:** Build the three key screens — triage queue, patient detail, and AI rationale panel — with a polished, real-product feel. Targets: UI/UX (10 marks) + Presentation & Demo (10 marks) + the visual "wow moment."
> **Time Budget:** ~90 minutes (of 5 hours)

---

## Pre-Hackathon Prep (During 3-Day Window)

- [x] Next.js project scaffolded with Tailwind + shadcn/ui
- [x] Design system tokens defined (colors, typography, spacing)
- [x] Component shells created (structure without business logic)
- [x] API client utility (`lib/api.js`) written
- [x] ESI level color mapping and labels defined

---

## Design System

### ESI Color Palette
| Level | Name | Color | Hex | Use |
|---|---|---|---|---|
| ESI-1 | Resuscitation | 🔴 Red | `#DC2626` | Immediate life threat |
| ESI-2 | Emergent | 🟠 Orange | `#EA580C` | High risk, time-sensitive |
| ESI-3 | Urgent | 🟡 Yellow | `#CA8A04` | Needs multiple resources |
| ESI-4 | Less Urgent | 🟢 Green | `#16A34A` | Single resource needed |
| ESI-5 | Non-Urgent | 🔵 Blue | `#2563EB` | Can wait |

### Typography
- **Headings:** Inter (Google Fonts)
- **Body:** Inter
- **Monospace (vitals):** JetBrains Mono

### Dark Mode
Primary theme is dark (clinical dashboard feel). Dark backgrounds with vivid ESI colors for maximum contrast and visual impact.

---

## Tasks (Ordered)

### 3.1 — Screen 1: Triage Queue Dashboard (Main Page)

The hero screen. A real-time, color-coded patient queue sorted by priority.

**Layout:**
```
┌────────────────────────────────────────────────────────┐
│  🏥 SmartTriage    [Add Patient]    ⏱ Live   🔄 3s    │
├────────────────────────────────────────────────────────┤
│  Summary Stats Bar                                     │
│  [🔴 2 Critical] [🟠 5 Emergent] [🟡 12 Urgent] ...  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 🔴 ESI-1  John D. (45M) • Chest pain, SOB       │  │
│  │ HR: 135  BP: 85/50  SpO2: 87%  • 98% confidence │  │
│  │ ⏱ Arrived 3 min ago          [View Details →]    │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 🟠 ESI-2  Sarah K. (67F) • Sudden left weakness │  │
│  │ HR: 92   BP: 170/95  SpO2: 96%  • 91% conf.    │  │
│  │ ⏱ Arrived 8 min ago          [View Details →]    │  │
│  └──────────────────────────────────────────────────┘  │
│  ...                                                   │
└────────────────────────────────────────────────────────┘
```

**Features:**
- Auto-refreshes every 3 seconds (polling)
- Sorted by ESI level (1 first), then by arrival time within same level
- Color-coded left border per ESI level
- Key vitals shown inline with abnormal values highlighted
- Click → navigates to patient detail
- Subtle pulse animation on ESI-1 cards (attention-grabbing)
- Summary bar at top shows count per ESI level

### 3.2 — Screen 2: Patient Detail View

Deep-dive into a single patient with editable vitals (the "wow moment" trigger).

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  ← Back to Queue    Patient: John Doe (45M)    ESI-1 🔴│
├───────────────────────┬─────────────────────────────────┤
│                       │                                  │
│   VITALS (editable)   │   AI TRIAGE RESULT              │
│   ┌───────────────┐   │   ┌────────────────────────┐    │
│   │ HR:  [135]    │   │   │ Level: ESI-1           │    │
│   │ BP:  [85/50]  │   │   │ Confidence: 98%        │    │
│   │ RR:  [28]     │   │   │ Source: Red-flag override│   │
│   │ Temp:[37.2]   │   │   │ Model: rf-v1.0         │    │
│   │ SpO2:[87]     │   │   │ ⏱ 2 sec ago            │    │
│   │ GCS: [15]     │   │   └────────────────────────┘    │
│   └───────────────┘   │                                  │
│                       │   🚩 RED FLAGS TRIGGERED         │
│   Chief Complaint     │   • SpO2 < 85% (critical)       │
│   ┌───────────────┐   │   • HR > 130 (tachycardia)      │
│   │ Severe chest  │   │                                  │
│   │ pain radiating│   │   📊 ML PROBABILITIES           │
│   │ to left arm,  │   │   ESI-1: ████████████ 72%       │
│   │ shortness of  │   │   ESI-2: ████          22%       │
│   │ breath        │   │   ESI-3: █              4%       │
│   └───────────────┘   │   ESI-4: ░              1%       │
│                       │   ESI-5: ░              1%       │
│   [🔄 Re-run Triage]  │                                  │
│   [✋ Override →]      │                                  │
├───────────────────────┴─────────────────────────────────┤
│                                                          │
│   🤖 AI RATIONALE                                       │
│   "This patient presents with severe chest pain and     │
│    hemodynamic instability (BP 85/50, HR 135). The      │
│    combination of hypotension, tachycardia, and SpO2    │
│    of 87% suggests possible acute coronary syndrome     │
│    with cardiogenic shock. Immediate intervention       │
│    required."                                            │
│                                                          │
├──────────────────────────────────────────────────────────┤
│   📋 AUDIT LOG                                          │
│   14:23:01 — Triage computed: ESI-1 (98% conf.)        │
│   14:22:45 — Patient registered                         │
│   14:23:15 — Vitals updated: HR 135→128                │
│   14:23:16 — Triage recomputed: ESI-1 (96% conf.)     │
└──────────────────────────────────────────────────────────┘
```

**The "Wow Moment" Flow:**
1. Edit a vital (e.g., change SpO2 from 87 → 96)
2. Click "Re-run Triage"
3. Watch: level changes, confidence updates, probability bars animate, rationale rewrites itself
4. Audit log shows the before/after

### 3.3 — Screen 3: Add Patient Modal/Form

Quick-entry form to register a new patient for triage.

**Fields:**
- Name, Age, Gender
- Chief Complaint (free text, textarea)
- Vitals: HR, BP (systolic/diastolic), RR, Temp, SpO2, GCS
- Medical History (free text, textarea)
- [Submit & Triage] button — creates patient AND runs triage in one step

### 3.4 — Override Modal

When clinician clicks "Override":
- Dropdown to select new ESI level (1-5)
- Required text field: reason for override
- Submit logs to audit trail with `actor: "clinician"`

### 3.5 — Responsive & Polish

- Animations: card entry, priority change, confidence bar transitions
- Loading states for API calls
- Error boundaries with user-friendly messages
- Mobile-responsive (though demo will be on laptop)

---

## Verify Phase 3

- [ ] Queue displays all patients sorted by priority
- [ ] Queue auto-refreshes (new patients appear without reload)
- [ ] Patient detail shows all vitals, triage result, rationale, and audit log
- [ ] Editing vitals + re-running triage updates everything live
- [ ] Add Patient form works end-to-end
- [ ] Override flow works with audit logging
- [ ] No visual glitches, smooth animations
- [ ] Dark theme renders correctly

---

## 🔴 USER ACTION REQUIRED

None for this phase — all frontend work.
