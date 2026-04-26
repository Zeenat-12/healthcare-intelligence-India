from flask import Flask, request, jsonify
from flask_cors import CORS
from data_loader import load_data
from extractor import extract_from_notes
from trust_scorer import calculate_trust_score
from search_agent import smart_search
from validator import validate_extraction

app = Flask(__name__)
CORS(app)

print("Loading data...")
df = load_data()
print("Ready!")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query"}), 400

    results, filters = smart_search(query, df)
    output = []

    for _, row in results.iterrows():
        # Build notes from multiple columns
        notes = str(row.get("notes", ""))
        if str(row.get("description", "")) != "nan":
            notes = str(row.get("description", ""))
        if str(row.get("specialties", "")) != "nan":
            notes += " " + str(row.get("specialties", ""))
        if str(row.get("equipment", "")) != "nan":
            notes += " " + str(row.get("equipment", ""))
        if str(row.get("procedure", "")) != "nan":
            notes += " " + str(row.get("procedure", ""))
        if str(row.get("capability", "")) != "nan":
            notes += " " + str(row.get("capability", ""))

        extracted = extract_from_notes(notes, row.get("facility_name", ""))
        trust = calculate_trust_score(extracted)
        validation = validate_extraction(extracted, notes)

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