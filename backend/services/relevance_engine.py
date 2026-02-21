
import json
import os


def load_keywords():

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "domain_keywords.json"
    )

    if not os.path.exists(path):
        return {}

    with open(path) as f:
        return json.load(f)



def rank_events(events, domain):

    keywords = load_keywords().get(domain, [])

    ranked = []

    for e in events:

        score = len(set(e["tags"]) & set(keywords))

        # fallback if no keyword file
        if not keywords and domain in e["tags"]:
            score = 1

        if score > 0:
            e["relevance"] = score
            ranked.append(e)

    return sorted(ranked, key=lambda x: x["relevance"], reverse=True)




# import json
# import os


# def load_keywords():

#     path = os.path.join(
#         os.path.dirname(__file__),
#         "..",
#         "data",
#         "domain_keywords.json"
#     )

#     with open(path) as f:
#         return json.load(f)



# def rank_events(events, domain):

#     keywords = load_keywords().get(domain, [])

#     ranked = []

#     for e in events:

#         score = len(set(e["tags"]) & set(keywords))

#         if score > 0:
#             e["relevance"] = score
#             ranked.append(e)

#     return sorted(ranked, key=lambda x: x["relevance"], reverse=True)