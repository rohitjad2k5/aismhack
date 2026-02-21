# def explain(top_domain, profile):

#     strongest = sorted(profile, key=profile.get, reverse=True)[:3]

#     return f"""
# Best career match: {top_domain['domain']}

# Reason:
# Your strongest traits are {', '.join(strongest)}.
# These traits align strongly with this career’s requirements.

# Confidence Score: {top_domain['score']}/10
# """


def explain(top_career, profile):

    strongest = sorted(profile, key=profile.get, reverse=True)[:3]

    return f"""
Best career match: {top_career['domain']}

Reason:
Your strongest traits are {', '.join(strongest)}.
These traits strongly align with this career’s requirements.

Final Score: {top_career['score']} / 10
"""