import sys
import os
from pathlib import Path

# Add backend directory to path for imports
backend_path = str(Path(__file__).parent.parent)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from services.data_loader import load_weights

WEIGHTS = load_weights()


def evaluate_domain_fit(domain, profile):

    domain = domain.lower()
    weights = WEIGHTS.get(domain)

    if not weights:
        return {"error": f"{domain} not found"}

    score = 0
    strengths = []
    weaknesses = []

    total_weight = sum(weights.values()) or 1

    for skill, weight in weights.items():

        val = profile.get(skill, 0)
        score += val * weight

        if val >= 7:
            strengths.append(skill)
        elif val <= 4:
            weaknesses.append(skill)

    final_score = round(score / total_weight, 2)

    verdict = (
        "Excellent Fit" if final_score >= 7
        else "Moderate Fit" if final_score >= 4
        else "Low Fit"
    )

    confidence = round((len(strengths) / len(weights)) * 100, 2) if weights else 0

    return {
        "domain": domain,
        "score": final_score,
        "verdict": verdict,
        "confidence": confidence,
        "strengths": strengths,
        "weaknesses": weaknesses
    }









# from services.data_loader import load_weights

# WEIGHTS = load_weights()


# def evaluate_domain_fit(domain, profile):

#     domain = domain.lower()
#     weights = WEIGHTS.get(domain)

#     if not weights:
#         return {"error": f"{domain} not found"}

#     score = 0
#     strengths = []
#     weaknesses = []

#     for skill, weight in weights.items():

#         val = profile.get(skill, 0)
#         score += val * weight

#         if val >= 7:
#             strengths.append(skill)
#         elif val <= 4:
#             weaknesses.append(skill)

#     final_score = round(score / sum(weights.values()), 2)

#     verdict = (
#         "Excellent Fit" if final_score >= 7
#         else "Moderate Fit" if final_score >= 4
#         else "Low Fit"
#     )

#     confidence = round((len(strengths)/len(weights))*100,2)

#     return {
#         "domain": domain,
#         "score": final_score,
#         "verdict": verdict,
#         "confidence": confidence,
#         "strengths": strengths,
#         "weaknesses": weaknesses
#     }
