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
        return {"required_capabilities": [], "location": "", "doctor_preference": "any", "reasoning": ""}

def extract_location_from_query(user_query):
    india_locations = [
        "bihar", "delhi", "mumbai", "bangalore", "chennai", "kolkata",
        "hyderabad", "pune", "ahmedabad", "jaipur", "lucknow", "patna",
        "ranchi", "bhopal", "kerala", "gujarat", "rajasthan", "maharashtra",
        "uttar pradesh", "madhya pradesh", "west bengal", "karnataka",
        "tamil nadu", "andhra pradesh", "telangana", "odisha", "assam",
        "punjab", "haryana", "uttarakhand", "jharkhand", "goa"
    ]
    query_lower = user_query.lower()
    for location in india_locations:
        if location in query_lower:
            return location
    return ""

def smart_search(user_query, df):
    filters = understand_query(user_query)
    results = df.copy()

    # Get location from Gemini or directly from query
    location = filters.get("location", "")
    if not location:
        location = extract_location_from_query(user_query)

    print(f"Location detected: {location}")

    # ✅ FIXED: Only filter by state/district/city columns, NOT all columns
    if location:
        location_cols = ["state", "district", "address_city", "address_stateorregion"]
        available_cols = [c for c in location_cols if c in results.columns]

        location_mask = results[available_cols].apply(
            lambda col: col.astype(str).str.lower().str.contains(location.lower(), na=False)
        ).any(axis=1)

        location_results = results[location_mask]
        print(f"Found {len(location_results)} results for location: {location}")

        if len(location_results) > 0:
            results = location_results

    return results.head(200), filters 