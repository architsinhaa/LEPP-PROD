def score_lead(row, icp: dict) -> int:
    score = 0
    max_score = 0

    field_mapping = {
        "# Employees": "Company_Size",
        "Company Country": "Location"
    }

    for icp_field, config in icp.items():
        weight = config["weight"]
        max_score += weight

        column = field_mapping.get(icp_field, icp_field)
        value = row.get(column)

        if "values" in config:
            allowed = {str(v).lower() for v in config["values"]}
            if value and str(value).lower() in allowed:
                score += weight

        elif "min" in config and "max" in config:
            try:
                num = int(value)
                if config["min"] <= num <= config["max"]:
                    score += weight
            except Exception:
                pass

    return int((score / max_score) * 100) if max_score else 0


def segment(score: int) -> str:
    if score >= 80:
        return "High"
    if score >= 50:
        return "Medium"
    return "Low"
