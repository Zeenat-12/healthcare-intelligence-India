def smart_search(user_query, df):
    filters = understand_query(user_query)
    results = df.copy()

    # Step 1 — Apply location filter FIRST
    location = filters.get("location", "")
    if location:
        location_mask = (
            results["state"].str.lower().str.contains(location.lower(), na=False) |
            results["district"].str.lower().str.contains(location.lower(), na=False) |
            results["pincode"].str.contains(location, na=False)
        )
        location_results = results[location_mask]
        if len(location_results) > 0:
            results = location_results  # Only use location filtered results

    # Step 2 — Apply capability filter WITHIN location results
    required_caps = filters.get("required_capabilities", [])
    if required_caps:
        def has_capability(row):
            row_text = " ".join(str(v).lower() for v in row.values)
            return any(cap.lower() in row_text for cap in required_caps)
        cap_results = results[results.apply(has_capability, axis=1)]
        if len(cap_results) > 0:
            results = cap_results

    return results.head(200), filters