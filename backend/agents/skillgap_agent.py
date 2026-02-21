import json
import os


# ---------- LOAD DOMAIN VECTORS ----------
def load_domain_vectors():

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "domain_vectors.json"
    )

    with open(path) as f:
        return json.load(f)



# ---------- LOAD IMPROVEMENT TIPS ----------
def load_tips():

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "trait_tips.json"
    )

    with open(path) as f:
        return json.load(f)



# ---------- CALCULATE SKILL GAPS ----------
def calculate_gap(profile, domain):

    DOMAIN_VECTORS = load_domain_vectors()
    required = DOMAIN_VECTORS.get(domain, {})

    gaps = []

    for trait, required_value in required.items():

        user_value = profile.get(trait, 0)

        gap_value = round(required_value - user_value, 2)

        # dynamic threshold
        threshold = 0.15 if required_value < 0.7 else 0.1

        if gap_value > threshold:

            priority = gap_value * required_value

            gaps.append({
                "trait": trait,
                "your_score": user_value,
                "required": required_value,
                "gap": gap_value,
                "priority": round(priority,2)
            })

    return sorted(gaps, key=lambda x: x["priority"], reverse=True)



# ---------- GET IMPROVEMENT ADVICE ----------
def improvement_advice(trait):

    tips = load_tips()

    return tips.get(
        trait,
        "Practice real-world activities related to this skill."
    )



# ---------- MAIN ANALYSIS ----------
def skill_gap_analysis(profile, best_domain):

    domain = best_domain["domain"]

    gaps = calculate_gap(profile, domain)

    report = []

    for gap in gaps:
        report.append({
            "trait": gap["trait"],
            "gap": gap["gap"],
            "priority": gap["priority"],
            "advice": improvement_advice(gap["trait"])
        })

    return {
        "target_domain": domain,
        "total_gaps": len(report),
        "improvement_plan": report
    }