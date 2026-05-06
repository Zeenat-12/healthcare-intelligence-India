import sys
sys.path.insert(0, r"C:\Users\HP\Documents\Desktop\healthcare-intelligence-India\backend")
from google import genai
import json

GEMINI_KEY = "AIzaSyCfHQcMt4o4qoz3ePrxO_-wZbXSPyyZJkQ"
client = genai.Client(api_key=GEMINI_KEY)

def extract_from_notes(notes_text, facility_name=""):
    if not notes_text or notes_text.strip() == "":
        print(f"Skipping (empty notes): {facility_name[:30]}")
        return {}

    print(f"Extracting for: {facility_name[:30]}")

    prompt = f"""Read these hospital notes and return ONLY a JSON object. No extra text.
{{
  "has_icu": true,
  "has_emergency": true,
  "has_surgery": false,
  "has_anesthesiologist": false,
  "available_24_7": true,
  "doctor_type": "fulltime",
  "oxygen_supply": true,
  "renovation_or_closed": false,
  "summary": "one sentence"
}}
Hospital: {facility_name}
Notes: {notes_text}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        raw = response.text.strip()
        print(f"Gemini response: {raw[:100]}")
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception as e:
        print(f"Gemini error for {facility_name[:30]}: {e}")
        return {}