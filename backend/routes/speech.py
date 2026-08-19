import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from backend.models import PatientCreate
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api")

class SpeechRequest(BaseModel):
    transcript: str
    language: str = "en" # "en" or "bn"

# System instruction to force structured JSON output matching PatientCreate
SPEECH_PARSING_PROMPT = """You are an AI assistant in a busy emergency department.
Your task is to take a raw voice transcript from a triage nurse and extract structured patient data.
The transcript may be in English or Bengali.

Extract the following fields and format exactly as JSON matching this schema:
- name (string)
- age (integer)
- gender (string: "M", "F", or "Other")
- chief_complaint (string, translated to English if the input was Bengali)
- heart_rate (integer or null)
- systolic_bp (integer or null)
- diastolic_bp (integer or null)
- respiratory_rate (integer or null)
- temperature (float or null)
- spo2 (integer or null)
- gcs_score (integer or null, default 15)
- medical_history (string, translated to English if the input was Bengali. AGGRESSIVELY extract any mention of chronic conditions, past surgeries, comorbidities, or risk factors here (e.g., "diabetic", "history of bypass", "hypertension").)

If a value is not mentioned in the transcript, set it to null (or empty string for strings).
If age is not explicitly mentioned but implied (e.g. "middle aged"), estimate it or set to 30.
If gender is not explicitly mentioned but implied by name or pronouns, infer it.
If a blood pressure is given like "120 over 80", map 120 to systolic_bp and 80 to diastolic_bp.

Respond ONLY with valid JSON. Do not include markdown blocks like ```json."""

@router.post("/parse-speech", response_model=PatientCreate)
async def parse_speech(request: SpeechRequest):
    keys_str = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY")
    api_keys = [k.strip() for k in keys_str.split(',')] if keys_str else []
    
    if not api_keys:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured")

    last_error = None
    for api_key in api_keys:
        try:
            client = genai.Client(api_key=api_key)
            
            # Use gemini-3.6-flash or 2.5-flash with JSON schema enforcement
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=f"Transcript: {request.transcript}")]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SPEECH_PARSING_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.1,
                    response_schema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "integer"},
                            "gender": {"type": "string"},
                            "chief_complaint": {"type": "string"},
                            "heart_rate": {"type": "integer"},
                            "systolic_bp": {"type": "integer"},
                            "diastolic_bp": {"type": "integer"},
                            "respiratory_rate": {"type": "integer"},
                            "temperature": {"type": "number"},
                            "spo2": {"type": "integer"},
                            "gcs_score": {"type": "integer"},
                            "medical_history": {"type": "string"}
                        },
                        "required": ["name", "age", "gender", "chief_complaint"]
                    }
                )
            )
            
            if not response.text:
                raise HTTPException(status_code=500, detail="Empty response from LLM")
                
            parsed_data = json.loads(response.text)
            
            # Ensure fallback values for required fields
            if not parsed_data.get("name"):
                parsed_data["name"] = "Unknown Patient"
            if not parsed_data.get("age"):
                parsed_data["age"] = 30
            if not parsed_data.get("gender"):
                parsed_data["gender"] = "Other"
                
            return parsed_data

        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM JSON: {e}")
            raise HTTPException(status_code=500, detail="LLM returned invalid JSON structure")
        except Exception as e:
            print(f"⚠️ Speech parsing API error: {e}")
            last_error = e
            if "429" in str(e) or "quota" in str(e).lower() or len(api_keys) > 1:
                print("🔄 Rotating to next API key...")
                continue
            break
            
    print(f"Error parsing speech after trying all keys: {last_error}")
    raise HTTPException(status_code=500, detail=str(last_error))
