from google import genai
import json

GEMINI_KEY = "AIzaSyCfHQcMt4o4qoz3ePrxO_-wZbXSPyyZJkQ"
client = genai.Client(api_key=GEMINI_KEY)

def understand_query(user_query):
    prompt = f"""Break down this hospital search query into filters.
Return ONLY valid JSON no extra text:
{{
  "required_capabilities": [],
  "location": "",
  "doctor_preference": "any",
  "reasoning": ""
}}
Query: "{user_query}"
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        raw = response.text.strip()
        clean = raw.replace("```json","").replace("```","").strip()
        return json.loads(clean)
    except:
        return {}

def smart_search(user_query, df):
    filters = understand_query(user_query)
    results = df.copy()
    location = filters.get("location", "")
    if location:
        results = results[
            results["state"].str.lower().str.contains(location.lower(), na=False) |
            results["district"].str.lower().str.contains(location.lower(), na=False)
        ]
    return results.head(10), filters