import pandas as pd
import os

def load_data():
    filepath = "VF_Hackathon_Dataset_India_Large.xlsx"
    
    if os.path.exists(filepath):
        print("Loading real dataset...")
        df = pd.read_excel(filepath)
        print(f"Columns found: {df.columns.tolist()}")
    else:
        print("Dataset not found! Using sample data...")
        data = {
            "facility_name": ["Patna Civil Hospital","PMCH Patna","Nalanda Medical","Gaya District Hospital","Ranchi RIMS","Muzaffarpur Hospital","Bhagalpur Medical","Darbhanga Hospital","Vaishali Clinic","Sitamarhi Health Center"],
            "state": ["Bihar","Bihar","Bihar","Bihar","Jharkhand","Bihar","Bihar","Bihar","Bihar","Bihar"],
            "district": ["Patna","Patna","Nalanda","Gaya","Ranchi","Muzaffarpur","Bhagalpur","Darbhanga","Vaishali","Sitamarhi"],
            "pincode": ["800001","800004","803101","823001","834001","842001","812001","846001","844101","843301"],
            "latitude": [25.5941,25.6093,25.1167,24.7955,23.3441,26.1197,25.2425,26.1542,25.7046,26.5921],
            "longitude": [85.1376,85.1314,85.4469,85.0077,85.3096,85.3910,86.9842,85.9000,85.4183,85.4872],
            "notes": [
                "Hospital has ICU with 10 beds, 24/7 emergency services, oxygen supply available, full-time doctors, surgery theatre operational",
                "Advanced surgery available, anesthesiologist on duty, neonatal care unit, dialysis center, 24/7 services",
                "Basic emergency care, part-time doctors available on weekdays, no ICU, oxygen available",
                "Claims advanced surgery but no anesthesiologist listed, emergency services, part-time staff only",
                "Full ICU facility, trauma center, oncology department, 24/7 emergency, oxygen supply",
                "Small clinic, part-time doctor visits twice a week, basic facilities only, under renovation",
                "Emergency services, ICU available but only 9am-5pm, oxygen supply, surgery available",
                "24/7 emergency, full-time staff, ICU operational, oxygen available, no surgery",
                "Basic health center, no ICU, part-time doctor, emergency referral only",
                "Community health center, basic facilities, 24/7 staff, oxygen available"
            ]
        }
        df = pd.DataFrame(data)

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df.dropna(how="all", inplace=True)

    # Find the notes column automatically
    notes_col = None
    for col in df.columns:
        if "note" in col or "description" in col or "detail" in col or "info" in col or "remark" in col:
            notes_col = col
            break

    if notes_col and notes_col != "notes":
        df["notes"] = df[notes_col]
    elif "notes" not in df.columns:
        df["notes"] = "No notes available"

    df["notes"] = df["notes"].fillna("No notes available")

    # Find facility name column
    name_col = None
    for col in df.columns:
        if "name" in col or "facility" in col or "hospital" in col:
            name_col = col
            break
    if name_col and name_col != "facility_name":
        df["facility_name"] = df[name_col]
    elif "facility_name" not in df.columns:
        df["facility_name"] = "Unknown"

    # Find state and district
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

    df["state"] = df["state"].astype(str).str.strip().str.title()
    df["district"] = df["district"].astype(str).str.strip().str.title()
    df = df.reset_index(drop=True)
    df["facility_id"] = df.index
    print(f"Loaded {len(df)} facilities!")
    return df