





from services.event_collector import fetch_events, upcoming
from services.relevance_engine import rank_events


def generate_timeline(best_domain):
    """
    Generates upcoming relevant career events for the selected domain.
    Always returns safe structured output even if data sources fail.
    """

    # ----------------------------
    # Validate input
    # ----------------------------
    if not best_domain or "domain" not in best_domain:
        return {
            "domain": None,
            "total_events": 0,
            "timeline": ["Invalid domain input"]
        }

    domain = best_domain["domain"]

    # ----------------------------
    # Fetch events safely
    # ----------------------------
    try:
        events = fetch_events() or []
    except Exception as e:
        return {
            "domain": domain,
            "total_events": 0,
            "timeline": [f"Event service error: {str(e)}"]
        }

    # ----------------------------
    # Filter future events
    # ----------------------------
    try:
        future_events = upcoming(events) or []
    except Exception:
        future_events = []

    # ----------------------------
    # Rank by relevance
    # ----------------------------
    try:
        relevant = rank_events(future_events, domain) or []
    except Exception:
        relevant = []

    # ----------------------------
    # If no events found
    # ----------------------------
    if not relevant:
        return {
            "domain": domain,
            "total_events": 0,
            "timeline": ["No upcoming relevant events found"]
        }

    # ----------------------------
    # Success result
    # ----------------------------
    return {
        "domain": domain,
        "total_events": len(relevant),
        "timeline": relevant[:10]
    }





