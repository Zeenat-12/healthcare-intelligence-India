import pandas as pd
import os
def load_data():
    filepath = r"C:\Users\HP\Documents\Desktop\healthcare-intelligence-India\backend\VF_Hackathon_Dataset_India_Large.xlsx"

    if os.path.exists(filepath):
        print("Loading real dataset...")
        df = pd.read_excel(filepath)
        print(f"Columns found: {df.columns.tolist()}")
    else:
        print("Dataset not found!")
        return pd.DataFrame()

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df.dropna(how="all", inplace=True)

    # Map actual columns to expected column names
    if "name" in df.columns and "facility_name" not in df.columns:
        df["facility_name"] = df["name"]

    if "address_stateorregion" in df.columns and "state" not in df.columns:
        df["state"] = df["address_stateorregion"]

    if "address_city" in df.columns and "district" not in df.columns:
        df["district"] = df["address_city"]

    if "address_ziporpostcode" in df.columns and "pincode" not in df.columns:
        df["pincode"] = df["address_ziporpostcode"].astype(str)

    # Build notes from available text columns
    text_cols = ["description", "specialties", "procedure", "equipment", "capability"]
    def build_notes(row):
        parts = []
        for col in text_cols:
            val = str(row.get(col, ""))
            if val and val.lower() != "nan":
                parts.append(val)
        return " ".join(parts) if parts else "No notes available"

    df["notes"] = df.apply(build_notes, axis=1)

    # Fill missing columns
    if "state" not in df.columns:
        df["state"] = "Unknown"
    if "district" not in df.columns:
        df["district"] = "Unknown"
    if "pincode" not in df.columns:
        df["pincode"] = "000000"
    if "latitude" not in df.columns:
        df["latitude"] = 20.0
    if "longitude" not in df.columns:
        df["longitude"] = 78.0

    df["facility_name"] = df["facility_name"].fillna("Unknown")
    df["state"] = df["state"].astype(str).str.strip().str.title()
    df["district"] = df["district"].astype(str).str.strip().str.title()
    df["notes"] = df["notes"].fillna("No notes available")
    df["pincode"] = df["pincode"].astype(str)

    df = df.reset_index(drop=True)
    df["facility_id"] = df.index
    print(f"Loaded {len(df)} facilities!")
    return df