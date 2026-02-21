import sys
import os
from pathlib import Path

# Add backend directory to path for imports
backend_path = str(Path(__file__).parent.parent)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from services.data_loader import load_careers

careers_db = load_careers()


def evaluate_all_domains(profile):

    results = []

    for career in careers_db:

        score = 0
        weights = career["traits"]

        for trait, weight in weights.items():
            score += profile.get(trait,0)*weight

        results.append({
            "career":career["career"],
            "domain":career["domain"],
            "score":round(score,2)
        })

    return sorted(results,key=lambda x:x["score"],reverse=True)
