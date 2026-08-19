"""
LLM Explanation Layer — Layer 3 of the triage pipeline.
Uses Google Gemini API (google.genai SDK) to generate plain-language clinical rationale.
The LLM EXPLAINS decisions, it does NOT make them.
"""

import os
import asyncio
from typing import List, Dict, Optional

from dotenv import load_dotenv

# Load .env from backend dir and project root
_backend_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_backend_dir, ".env"))
load_dotenv()  # Also try CWD

GEMINI_AVAILABLE = False
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    pass

EXPLANATION_PROMPT = """You are a clinical decision-support assistant in an emergency department. A triage AI system has assessed a patient and assigned them a priority level. Your job is to explain WHY in plain language that a clinician would find useful.

STANDARD ESI DEFINITIONS:
- Level 1 (Resuscitation): Conditions that are considered threats to life or limb requiring immediate aggressive intervention.
- Level 2 (Emergent): Conditions that are considered threats to life or limb, or its function, requiring immediate intervention.
- Level 3 (Urgent): Conditions that could potentially progress to a serious problem requiring emergency intervention.
- Level 4 (Less Urgent): Conditions related to patient age, distress or potential for deterioration or complications.
- Level 5 (Non Urgent): Conditions that can be acute, but non urgent, or part of a chronic problem.

PATIENT DATA:
- Age: {age}, Gender: {gender}
- Chief Complaint: {chief_complaint}
- Vitals: HR {hr} bpm, BP {sbp}/{dbp} mmHg, RR {rr}/min, Temp {temp}°C, SpO2 {spo2}%, GCS {gcs}/15
- Medical History: {medical_history}

AI TRIAGE RESULT:
- Assigned Level: ESI-{level} ({level_name})
- Confidence: {confidence:.0%}
- Decision Source: {source}
- Red-flag rules triggered: {red_flags}
- ML Model probability for ESI-{level}: {ml_prob:.0%}

Generate a 2-3 sentence clinical rationale explaining this priority assignment. Focus on which specific findings drove the decision. Be concise, professional, and clinician-oriented. Do not use markdown formatting. Do not include disclaimers about being an AI.

CRITICAL INSTRUCTION FOR ESI 3, 4, AND 5:
If the assigned level is ESI-3, ESI-4, or ESI-5, you MUST explicitly predict the number and type of distinct hospital resources the patient is likely to need (e.g., "Requires 2+ resources: CBC lab, X-Ray", or "Requires 0 resources: prescription only")."""


class LLMExplainer:
    def __init__(self):
        self.client = None
        self.model_name = "gemini-3.6-flash"
        keys_str = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY")
        self.api_keys = [k.strip() for k in keys_str.split(',')] if keys_str else []
        self.current_key_idx = 0

        if self.api_keys and GEMINI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_keys[self.current_key_idx])
                print(f"✅ Gemini LLM explainer initialized (model: {self.model_name})")
            except Exception as e:
                print(f"⚠️ Gemini init failed: {e}")
                self.client = None
        else:
            if not GEMINI_AVAILABLE:
                print("⚠️ google-genai not installed — using template explanations")
            else:
                print("⚠️ No GEMINI_API_KEY set — using template explanations")

    def _get_client(self):
        if not GEMINI_AVAILABLE or not self.api_keys:
            return None
        return genai.Client(api_key=self.api_keys[self.current_key_idx])

    async def generate_explanation(
        self,
        patient_data: dict,
        level: int,
        level_name: str,
        confidence: float,
        red_flags: List[str],
        ml_probabilities: Dict[str, float],
        source: str,
        language: str = "en"
    ) -> str:
        """Generate a clinician-readable rationale for the triage decision."""

        # Try LLM first
        if self.api_keys:
            for attempt in range(len(self.api_keys) or 1):
                client = self._get_client()
                if client is not None:
                    try:
                        lang_instruction = ""
                        if language == "bn":
                            lang_instruction = "\n\nCRITICAL: You MUST write your rationale entirely in Bengali (বাংলা). Do NOT use English."
                        
                        prompt = EXPLANATION_PROMPT.format(
                            age=patient_data.get("age", "Unknown"),
                            gender=patient_data.get("gender", "Unknown"),
                            chief_complaint=patient_data.get("chief_complaint", "Not provided"),
                            hr=patient_data.get("heart_rate", "N/A"),
                            sbp=patient_data.get("systolic_bp", "N/A"),
                            dbp=patient_data.get("diastolic_bp", "N/A"),
                            rr=patient_data.get("respiratory_rate", "N/A"),
                            temp=patient_data.get("temperature", "N/A"),
                            spo2=patient_data.get("spo2", "N/A"),
                            gcs=patient_data.get("gcs_score", "N/A"),
                            medical_history=patient_data.get("medical_history", "None reported"),
                            level=level,
                            level_name=level_name,
                            confidence=confidence,
                            source="Red-flag safety rules" if source == "red_flag_override" else "ML risk classifier",
                            red_flags=", ".join(red_flags) if red_flags else "None",
                            ml_prob=ml_probabilities.get(f"ESI-{level}", 0)
                        ) + lang_instruction

                        # Run in thread to avoid blocking
                        response = await asyncio.to_thread(
                            client.models.generate_content,
                            model=self.model_name,
                            contents=prompt
                        )

                        if response and response.text:
                            return response.text.strip()
                    except Exception as e:
                        print(f"⚠️ Gemini API error (key index {self.current_key_idx}): {e}")
                        if "429" in str(e) or "quota" in str(e).lower() or len(self.api_keys) > 1:
                            self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
                            print(f"🔄 Rotating to next API key (index {self.current_key_idx})")
                            continue
                break

        # Fallback: template-based explanation
        return self._generate_template_explanation(
            patient_data, level, level_name, confidence,
            red_flags, ml_probabilities, source, language
        )

    def _generate_template_explanation(
        self,
        patient_data: dict,
        level: int,
        level_name: str,
        confidence: float,
        red_flags: List[str],
        ml_probabilities: Dict[str, float],
        source: str,
        language: str = "en"
    ) -> str:
        """Fallback template-based explanation when LLM is unavailable."""
        
        if language == "bn":
            if source == "red_flag_override":
                return f"রেড ফ্ল্যাগ নিয়মের কারণে রোগীকে ESI-{level} হিসাবে চিহ্নিত করা হয়েছে। অবিলম্বে মনোযোগ প্রয়োজন।"
            else:
                return f"এআই মডেলটি {confidence:.0%} আত্মবিশ্বাসের সাথে এই রোগীকে ESI-{level} হিসাবে মূল্যায়ন করেছে।"

        age = patient_data.get("age", "Unknown")
        gender = patient_data.get("gender", "")
        complaint = patient_data.get("chief_complaint", "symptoms")

        parts = []

        if source == "red_flag_override":
            parts.append(
                f"This {age}-year-old {gender} patient presenting with {complaint[:80]} "
                f"has been classified as ESI-{level} ({level_name}) due to critical safety rules being triggered."
            )
            if red_flags:
                flags_text = "; ".join(red_flags[:3])
                parts.append(f"Specifically: {flags_text}.")
            parts.append("Immediate clinical attention is recommended.")
        else:
            parts.append(
                f"The ML risk classifier assessed this {age}-year-old {gender} patient "
                f"presenting with {complaint[:80]} as ESI-{level} ({level_name}) "
                f"with {confidence:.0%} confidence."
            )

            # Highlight abnormal vitals
            abnormals = []
            hr = patient_data.get("heart_rate")
            if hr and (hr > 100 or hr < 60):
                abnormals.append(f"HR {hr}")
            sbp = patient_data.get("systolic_bp")
            if sbp and (sbp < 100 or sbp > 160):
                abnormals.append(f"BP {sbp}/{patient_data.get('diastolic_bp', '?')}")
            spo2 = patient_data.get("spo2")
            if spo2 and spo2 < 95:
                abnormals.append(f"SpO2 {spo2}%")
            temp = patient_data.get("temperature")
            if temp and temp > 38:
                abnormals.append(f"Temp {temp}°C")

            if abnormals:
                parts.append(f"Notable findings include: {', '.join(abnormals)}.")

            if level <= 2:
                parts.append("Prompt clinical evaluation is strongly recommended.")
            elif level == 3:
                parts.append("Multiple resources may be needed for evaluation.")
            else:
                parts.append("Standard evaluation pathway is appropriate.")

        return " ".join(parts)
