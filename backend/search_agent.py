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
        location_mask = (
            results["state"].str.lower().str.contains(location.lower(), na=False) |
            results["district"].str.lower().str.contains(location.lower(), na=False) |
            results["pincode"].str.contains(location, na=False)
        )
        location_results = results[location_mask]
        if len(location_results) > 0:
            results = location_results

    query_words = user_query.lower().split()
    def row_matches(row):
        row_text = " ".join(str(v).lower() for v in row.values)
        return any(word in row_text for word in query_words)

    keyword_results = results[results.apply(row_matches, axis=1)]
    if len(keyword_results) > 0:
        results = keyword_results

    return results.head(200), filters