import json
import os
from pathlib import Path

# Load domain vectors from data directory
current_dir = Path(__file__).parent.parent
vectors_path = current_dir / "data" / "domain_vectors.json"

with open(vectors_path) as f:
    DOMAIN_VECTORS = json.load(f)


def cosine_score(profile, domain_vector):
    score = 0
    total = 0

    for trait, value in domain_vector.items():
        if trait in profile:
            score += profile[trait] * value
            total += value

    return score / total if total else 0


def rank_domains(profile):
    results = []

    for domain, vector in DOMAIN_VECTORS.items():
        score = cosine_score(profile, vector)

        results.append({
            "domain": domain,
            "score": round(score,3)
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
