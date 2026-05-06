from flask import Flask, request, jsonify
from flask_cors import CORS
from data_loader import load_data
from extractor import extract_from_notes
from trust_scorer import calculate_trust_score
from search_agent import smart_search

app = Flask(__name__)
CORS(app, origins="*", allow_headers="*", methods=["GET", "POST", "OPTIONS"])

print("Loading data...")
df = load_data()
print("Ready!")

CAPABILITY_KEYWORDS = {
    "has_icu": ["icu", "intensive care", "critical care"],
    "has_surgery": ["surgery", "surgical", "operation theatre", "ot "],
    "has_emergency": ["emergency", "casualty", "trauma"],
    "has_dialysis": ["dialysis", "nephrology", "kidney"],
    "has_oncology": ["oncology", "cancer", "chemotherapy"],
    "has_neonatal": ["neonatal", "nicu", "newborn", "paediatric"],
    "available_24_7": ["24/7", "24 hours", "round the clock", "always open"],
    "oxygen_supply": ["oxygen", "ventilator", "respiratory"],
    "has_anesthesiologist": ["anaesthesia", "anesthesia", "anesthesiologist"],
    "renovation_or_closed": ["closed", "renovation", "not operational", "shut"]
}

def fast_extract(notes_text):
    notes_lower = notes_text.lower()
    result = {}
    for cap, keywords in CAPABILITY_KEYWORDS.items():
        result[cap] = any(kw in notes_lower for kw in keywords)
    result["doctor_type"] = "fulltime" if any(
        w in notes_lower for w in ["fulltime", "full time", "full-time", "resident"]
    ) else "parttime"
    result["summary"] = notes_text[:120] + "..." if len(notes_text) > 120 else notes_text
    return result

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query"}), 400

    results, filters = smart_search(query, df)
    results = results.head(50)
    output = []

    for i, (_, row) in enumerate(results.iterrows()):
        parts = []
        for col in ["description", "specialties", "equipment", "procedure", "capability", "notes"]:
            val = str(row.get(col, ""))
            if val and val.lower() != "nan":
                parts.append(val)
        notes = " ".join(parts).strip()

        if i < 20 and notes:
            name = str(row.get("facility_name", ""))[:30]
            print("[Gemini] Extracting #" + str(i+1) + ": " + name)
            extracted = extract_from_notes(notes, str(row.get("facility_name", "")))
            if not extracted:
                print("[Fallback] Using keyword extraction for #" + str(i+1))
                extracted = fast_extract(notes)
        else:
            extracted = fast_extract(notes) if notes else {}

        trust = calculate_trust_score(extracted)

        validation = {
            "issues": [],
            "corrections": {},
            "ai_validation": {"is_consistent": True, "confidence": "low"},
            "is_valid": True
        }

        output.append({
            "name": str(row.get("facility_name", "Unknown")),
            "state": str(row.get("state", "")),
            "district": str(row.get("district", "")),
            "pincode": str(row.get("pincode", "")),
            "lat": float(row.get("latitude", 0) or 0),
            "lng": float(row.get("longitude", 0) or 0),
            "capabilities": extracted,
            "trust": trust,
            "validation": validation,
            "reasoning": filters.get("reasoning", "")
        })

    return jsonify(output)

@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "total": len(df),
        "states": int(df["state"].nunique()),
        "districts": int(df["district"].nunique())
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)