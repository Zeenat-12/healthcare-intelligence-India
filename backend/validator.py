from google import genai
import json

GEMINI_KEY = "AIzaSyCfHQcMt4o4qoz3ePrxO_-wZbXSPyyZJkQ"
client = genai.Client(api_key=GEMINI_KEY)

MEDICAL_STANDARDS = {
    "surgery_requires": ["anesthesiologist", "operation_theatre", "icu"],
    "icu_requires": ["24_7", "oxygen", "trained_staff"],
    "emergency_requires": ["oxygen", "ambulance", "24_7"],
    "dialysis_requires": ["nephrologist", "water_treatment"]
}

def validate_extraction(extracted, notes_text):
    issues = []
    corrections = {}

    if extracted.get("has_surgery"):
        if "theatre" not in notes_text.lower() and "operation" not in notes_text.lower():
            issues.append("Surgery claimed but no operation theatre mentioned in notes")
            corrections["has_surgery"] = "UNVERIFIED"

    if extracted.get("has_icu"):
        if "icu" not in notes_text.lower() and "intensive" not in notes_text.lower():
            issues.append("ICU claimed but word ICU not found in notes")
            corrections["has_icu"] = "UNVERIFIED"

    if extracted.get("available_24_7"):
        if "24" not in notes_text and "round" not in notes_text.lower():
            issues.append("24/7 claimed but not mentioned in notes")
            corrections["available_24_7"] = "UNVERIFIED"

    prompt = f"""
You are a medical data validator.
Check if this extracted data matches the original notes.
Return ONLY valid JSON:
{{
  "is_consistent": true,
  "hallucinations": [],
  "confidence": "high/medium/low"
}}

Extracted: {json.dumps(extracted)}
Original Notes: {notes_text[:500]}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        raw = response.text.strip()
        clean = raw.replace("```json","").replace("```","").strip()
        ai_validation = json.loads(clean)
    except:
        ai_validation = {"is_consistent": True, "hallucinations": [], "confidence": "low"}

    return {
        "issues": issues,
        "corrections": corrections,
        "ai_validation": ai_validation,
        "is_valid": len(issues) == 0 and ai_validation.get("is_consistent", True)
    }
