import json
import os

def load_careers():

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "careers.json"
    )

    with open(path) as f:
        return json.load(f)


def match_careers(profile):

    careers = load_careers()
    results = []

    for career in careers:

        score = 0
        for trait in career["traits"]:
            score += profile.get(trait,0)

        results.append({
            "career": career["career"],
            "domain": career["domain"],
            "score": round(score,2)
        })

    return sorted(results,key=lambda x:x["score"],reverse=True)[:10]