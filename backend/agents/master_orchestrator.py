import sys
import os
from pathlib import Path

# Add backend directory to path for imports
backend_path = str(Path(__file__).parent.parent)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from agents.adaptive_agent import next_question
from agents.assessment_agent import evaluate_domain_fit
from agents.skillgap_agent import skill_gap_analysis
from agents.roadmap_agent import generate_roadmap
from agents.timeline_agent import generate_timeline
from agents.explanation_agent import explain
from agents.pace_customizer_agent import customize_pace
from agents.alternative_paths_agent import explore_alternative_paths
from agents.resource_recommender_agent import recommend_resources
from agents.market_intelligence_agent import analyze_market_intelligence

from services.data_loader import load_weights


CONFIDENCE_THRESHOLD = 2
STOP_THRESHOLD = 6.5
DOMAIN_GAP_THRESHOLD = 1.0
MAX_CLARIFY_QUESTIONS = 5


def should_continue(state):
    return any(c < CONFIDENCE_THRESHOLD for c in state["confidence"].values())


def evaluate_all_domains(profile):

    weights = load_weights()

    results = [
        evaluate_domain_fit(domain, profile)
        for domain in weights.keys()
    ]

    return sorted(results, key=lambda x: x["score"], reverse=True)


def need_domain_verification(results):

    if len(results) < 2:
        return False

    return abs(results[0]["score"] - results[1]["score"]) < DOMAIN_GAP_THRESHOLD


def build_full_report(best, results, profile):

    roadmap = generate_roadmap(best["domain"])
    skill_gaps = skill_gap_analysis(profile, best)
    
    # Transform skill gaps for resource recommender
    # Convert "improvement_plan" with "trait" keys to format expected by recommend_resources
    formatted_gaps = []
    for gap_item in skill_gaps.get("improvement_plan", []):
        formatted_gaps.append({
            "skill": gap_item.get("trait", ""),
            "gap_value": gap_item.get("gap", 0),
            "priority": gap_item.get("priority", "medium"),
            "learning_tip": gap_item.get("advice", "")
        })
    
    return {
        "best_domain": best,
        "top_5": results[:5],
        "explanation": explain(best, profile),
        "skill_gap": skill_gaps,
        "roadmap": roadmap,
        "timeline": generate_timeline(best),
        "pace_customization": customize_pace(profile, roadmap),
        "alternative_paths": explore_alternative_paths(None, best["domain"], profile),
        "resource_recommendations": recommend_resources(formatted_gaps, profile),
        "market_intelligence": analyze_market_intelligence(best["domain"], profile, formatted_gaps)
    }


def orchestrate(state, profile):

    if "clarify_count" not in state:
        state["clarify_count"] = 0

    # STEP 1
    if should_continue(state):
        return {
            "action": "ask_question",
            "data": next_question(state)
        }

    # STEP 2
    results = evaluate_all_domains(profile)
    best = results[0]

    # STEP 3
    if need_domain_verification(results):

        if state["clarify_count"] < MAX_CLARIFY_QUESTIONS:
            state["clarify_count"] += 1

            return {
                "action": "ask_question",
                "data": next_question(state),
                "note": f"Clarifying between {results[0]['domain']} and {results[1]['domain']}"
            }

        else:
            return {
                "action": "final_result",
                **build_full_report(best, results, profile),
                "note": "Decision made after clarification phase"
            }

    # STEP 4
    if best["score"] >= STOP_THRESHOLD:

        return {
            "action": "final_result",
            **build_full_report(best, results, profile)
        }

    # STEP 5
    return {
        "action": "ask_question",
        "data": next_question(state)
    }





# from agents.adaptive_agent import next_question
# from agents.assessment_agent import evaluate_domain_fit
# from agents.skillgap_agent import skill_gap_analysis
# from agents.roadmap_agent import generate_roadmap
# from agents.timeline_agent import generate_timeline
# from agents.explainabilityagent import explain

# from services.data_loader import load_weights


# CONFIDENCE_THRESHOLD = 2
# STOP_THRESHOLD = 6.5
# DOMAIN_GAP_THRESHOLD = 1.0
# MAX_CLARIFY_QUESTIONS = 5


# # -------------------------------
# # SHOULD CONTINUE ASKING?
# # -------------------------------
# def should_continue(state):
#     return any(c < CONFIDENCE_THRESHOLD for c in state["confidence"].values())


# # -------------------------------
# # EVALUATE ALL DOMAINS
# # -------------------------------
# def evaluate_all_domains(profile):

#     weights = load_weights()

#     results = [
#         evaluate_domain_fit(domain, profile)
#         for domain in weights.keys()
#     ]

#     return sorted(results, key=lambda x: x["score"], reverse=True)


# # -------------------------------
# # DOMAIN CONFUSION CHECK
# # -------------------------------
# def need_domain_verification(results):

#     if len(results) < 2:
#         return False

#     return abs(results[0]["score"] - results[1]["score"]) < DOMAIN_GAP_THRESHOLD


# # -------------------------------
# # GENERATE FULL AI REPORT
# # -------------------------------
# def build_full_report(best, results, profile):

#     # skill gaps
#     gaps = skill_gap_analysis(profile, best)

#     # roadmap
#     roadmap = generate_roadmap(best["domain"])

#     # timeline
#     timeline = generate_timeline(best)

#     # explanation
#     explanation = explain(best, profile)

#     return {
#         "best_domain": best,
#         "top_5": results[:5],
#         "explanation": explanation,
#         "skill_gap": gaps,
#         "roadmap": roadmap,
#         "timeline": timeline
#     }


# # -------------------------------
# # MASTER AI BRAIN
# # -------------------------------
# def orchestrate(state, profile):

#     # init clarify counter
#     if "clarify_count" not in state:
#         state["clarify_count"] = 0

#     # STEP 1 — keep assessment
#     if should_continue(state):
#         return {
#             "action": "ask_question",
#             "data": next_question(state)
#         }

#     # STEP 2 — evaluate domains
#     results = evaluate_all_domains(profile)
#     best = results[0]

#     # STEP 3 — unclear winner
#     if need_domain_verification(results):

#         if state["clarify_count"] < MAX_CLARIFY_QUESTIONS:
#             state["clarify_count"] += 1

#             return {
#                 "action": "ask_question",
#                 "data": next_question(state),
#                 "note": f"Clarifying between {results[0]['domain']} and {results[1]['domain']}"
#             }

#         # clarification finished → generate report anyway
#         else:
#             report = build_full_report(best, results, profile)

#             return {
#                 "action": "final_result",
#                 **report,
#                 "note": "Decision made after clarification phase"
#             }

#     # STEP 4 — confident result
#     if best["score"] >= STOP_THRESHOLD:

#         report = build_full_report(best, results, profile)

#         return {
#             "action": "final_result",
#             **report
#         }

#     # STEP 5 — fallback
#     return {
#         "action": "ask_question",
#         "data": next_question(state)
#     }

