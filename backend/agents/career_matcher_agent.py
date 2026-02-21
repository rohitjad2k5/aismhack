import sys
import os
from pathlib import Path

# Add backend directory to path for imports
backend_path = str(Path(__file__).parent.parent)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from core.career_engine import rank_domains


def generate_careers(domain, profile):

    careers = []

    if profile.get("creative",0) >= 7:
        careers.append(f"Creative {domain.title()} Specialist")

    if profile.get("analytical",0) >= 7:
        careers.append(f"{domain.title()} Analyst")

    if profile.get("social",0) >= 7:
        careers.append(f"{domain.title()} Consultant")

    if profile.get("risk",0) >= 7:
        careers.append(f"{domain.title()} Entrepreneur")

    if not careers:
        careers.append(f"General {domain.title()} Professional")

    return careers


def match_careers(profile):

    ranked = rank_domains(profile)

    output = []

    for item in ranked[:5]:
        domain = item["domain"]

        careers = generate_careers(domain, profile)

        output.append({
            "domain": domain,
            "score": item["score"],
            "careers": careers
        })

    return output



# from core.career_engine import rank_domains


# def generate_careers(domain, profile):

#     careers = []

#     if profile.get("creative",0) > 0.7:
#         careers.append(f"Creative {domain.title()} Specialist")

#     if profile.get("analytical",0) > 0.7:
#         careers.append(f"{domain.title()} Analyst")

#     if profile.get("social",0) > 0.7:
#         careers.append(f"{domain.title()} Consultant")

#     if profile.get("risk",0) > 0.7:
#         careers.append(f"{domain.title()} Entrepreneur")

#     if not careers:
#         careers.append(f"General {domain.title()} Professional")

#     return careers


# def match_careers(profile):

#     ranked = rank_domains(profile)

#     output = []

#     for item in ranked[:5]:
#         domain = item["domain"]

#         careers = generate_careers(domain, profile)

#         output.append({
#             "domain": domain,
#             "score": item["score"],
#             "careers": careers
#         })

#     return output
