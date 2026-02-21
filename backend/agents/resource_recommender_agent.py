import json
import os


# ---------- LOAD RESOURCE CATALOG ----------
def load_resource_catalog():
    """
    Loads comprehensive catalog of learning resources.
    Includes courses, books, videos, certifications, projects.
    """
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "resource_catalog.json"
    )
    
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    
    return {
        "courses": {},
        "books": {},
        "videos": {},
        "certifications": {},
        "projects": {}
    }


# ---------- SKILL TO RESOURCE MAPPING ----------
def get_resources_for_skill(skill_name, resource_type="all"):
    """
    Gets all resources available for a specific skill.
    
    Args:
        skill_name: Skill to find resources for
        resource_type: "course", "book", "video", "cert", "project", "all"
    
    Returns:
        List of resources matching the skill
    """
    
    catalog = load_resource_catalog()
    resources = []
    
    # Search all resource types if "all"
    types_to_search = {
        "course": catalog.get("courses", {}),
        "book": catalog.get("books", {}),
        "video": catalog.get("videos", {}),
        "cert": catalog.get("certifications", {}),
        "project": catalog.get("projects", {})
    }
    
    if resource_type != "all":
        types_to_search = {resource_type: types_to_search.get(resource_type, {})}
    
    # Search for skill in each type
    for rtype, resources_dict in types_to_search.items():
        for resource_id, resource_data in resources_dict.items():
            if skill_name.lower() in resource_data.get("skills", []):
                resource_data["type"] = rtype
                resource_data["id"] = resource_id
                resources.append(resource_data)
    
    return resources


# ---------- RANK RESOURCES ----------
def rank_resources(resources, criteria=None):
    """
    Ranks resources by relevance, quality, and fit.
    
    Args:
        resources: List of resources to rank
        criteria: {
            "max_hours": 40,
            "budget": "free" or "paid" or "any",
            "learning_style": "visual" or "hands-on" or "reading" or "mixed",
            "difficulty": "beginner" or "intermediate" or "advanced" or "any"
        }
    
    Returns:
        Ranked list of resources
    """
    
    if criteria is None:
        criteria = {"max_hours": 100, "budget": "any", "learning_style": "any", "difficulty": "any"}
    
    scored_resources = []
    
    for resource in resources:
        score = 100  # Starting score
        
        # Budget filtering
        if criteria.get("budget") != "any":
            if criteria["budget"] == "free" and resource.get("price", 0) > 0:
                continue  # Skip paid if looking for free
            if criteria["budget"] == "paid" and resource.get("price", 0) == 0:
                continue  # Skip free if looking for paid
        
        # Hours constraint
        hours = resource.get("hours_to_complete", 50)
        if hours > criteria.get("max_hours", 100):
            score -= (hours - criteria.get("max_hours", 100)) / 10
        
        # Learning style match
        learning_style = criteria.get("learning_style", "any")
        if learning_style != "any":
            resource_style = resource.get("learning_style", [])
            if learning_style in resource_style:
                score += 15
            else:
                score -= 10
        
        # Difficulty match
        difficulty = criteria.get("difficulty", "any")
        if difficulty != "any":
            if resource.get("difficulty") == difficulty:
                score += 10
        
        # Quality rating
        rating = resource.get("rating", 4.0)
        score += (rating - 3.0) * 10  # Convert 1-5 rating to score bonus/penalty
        
        # Popularity (more reviews = trusted)
        reviews = resource.get("reviews", 0)
        popularity_bonus = min((reviews / 1000) * 5, 20)  # Cap at 20 points
        score += popularity_bonus
        
        # Recency bonus (newer = better source)
        year = resource.get("updated_year", 2024)
        recency_bonus = max((year - 2020) * 2, 0)  # More recent = higher score
        score += recency_bonus
        
        resource["score"] = max(0, round(score, 1))
        scored_resources.append(resource)
    
    # Sort by score
    scored_resources.sort(key=lambda x: x["score"], reverse=True)
    
    return scored_resources


# ---------- GENERATE LEARNING PATH ----------
def generate_learning_path(skill_gaps, profile=None):
    """
    Creates an ordered learning path from skill gaps.
    Prioritizes gaps by severity and recommends resources for each.
    
    Args:
        skill_gaps: List of {skill, gap_value, tips, ...}
        profile: User profile with learning preferences
    
    Returns:
        Structured learning path with resource recommendations
    """
    
    if profile is None:
        profile = {}
    
    # Extract criteria from profile
    criteria = {
        "max_hours": profile.get("hours_per_week", 10) * 12,  # 12 weeks of learning
        "budget": profile.get("budget_preference", "any"),
        "learning_style": profile.get("learning_style", "any"),
        "difficulty": profile.get("difficulty_preference", "any")
    }
    
    # Sort skill gaps by severity (highest gap = most important)
    sorted_gaps = sorted(skill_gaps, key=lambda x: x.get("gap_value", 0), reverse=True)
    
    learning_path = []
    
    for i, gap in enumerate(sorted_gaps, 1):
        skill = gap.get("skill", "unknown")
        
        # Get all resources for this skill
        all_resources = get_resources_for_skill(skill)
        
        if not all_resources:
            continue  # Skip if no resources available
        
        # Rank resources based on criteria
        ranked = rank_resources(all_resources, criteria)
        
        if ranked:
            learning_path.append({
                "step": i,
                "skill": skill,
                "gap_value": gap.get("gap_value", 0),
                "gap_severity": assess_gap_severity(gap.get("gap_value", 0)),
                "recommended_resources": ranked[:5],  # Top 5 resources
                "estimated_hours": sum(r.get("hours_to_complete", 20) for r in ranked[:3]) / 3,
                "learning_tip": gap.get("learning_tip", "")
            })
    
    return learning_path


# ---------- ASSESS GAP SEVERITY ----------
def assess_gap_severity(gap_value):
    """
    Categorizes skill gap severity.
    """
    if gap_value >= 0.4:
        return "critical"
    elif gap_value >= 0.25:
        return "significant"
    elif gap_value >= 0.15:
        return "moderate"
    else:
        return "minor"


# ---------- RESOURCE SUMMARY ----------
def create_resource_summary(resources, max_items=5):
    """
    Creates summary of top resources.
    Includes checklist format for easy reading.
    """
    
    summary = []
    
    for i, resource in enumerate(resources[:max_items], 1):
        summary.append({
            "rank": i,
            "title": resource.get("title", "Unknown"),
            "type": resource.get("type", "unknown"),
            "provider": resource.get("provider", "Unknown"),
            "duration": format_duration(resource.get("hours_to_complete", 0)),
            "level": resource.get("difficulty", "Mixed"),
            "cost": format_cost(resource.get("price", 0)),
            "rating": f"{resource.get('rating', 0)}/5 ({resource.get('reviews', 0)} reviews)",
            "url": resource.get("url", ""),
            "key_learnings": resource.get("key_learnings", []),
            "score": f"{resource.get('score', 0)}/100",
            "why_recommended": generate_recommendation_reason(resource)
        })
    
    return summary


# ---------- FORMAT HELPERS ----------
def format_duration(hours):
    """Converts hours to readable format."""
    if hours < 1:
        return f"{int(hours * 60)} minutes"
    elif hours < 40:
        return f"{int(hours)} hours"
    else:
        weeks = hours / 10  # Assuming 10 hrs/week
        return f"{weeks:.1f} weeks ({int(hours)} hours)"


def format_cost(price):
    """Formats price with currency."""
    if price == 0:
        return "Free"
    elif price < 50:
        return f"${price}"
    else:
        return f"${price} (Premium)"


def generate_recommendation_reason(resource):
    """Generates why this resource is recommended."""
    reasons = []
    
    rating = resource.get("rating", 0)
    reviews = resource.get("reviews", 0)
    
    if rating >= 4.8:
        reasons.append("Highly rated")
    
    if reviews >= 5000:
        reasons.append("Very popular")
    
    if resource.get("price", 0) == 0:
        reasons.append("Free")
    
    if resource.get("type") == "video":
        reasons.append("Video-based (visual)")
    elif resource.get("type") == "project":
        reasons.append("Hands-on project")
    
    if resource.get("difficulty") == "beginner":
        reasons.append("Beginner-friendly")
    
    year = resource.get("updated_year", 2024)
    if year == 2024 or year == 2025:
        reasons.append("Recently updated")
    
    return " • ".join(reasons) if reasons else "Good match"


# ---------- RESOURCE BY TYPE ----------
def recommend_by_type(skill, resource_type="course"):
    """
    Gets resources of specific type for a skill.
    
    Args:
        skill: Skill to find resources for
        resource_type: "course", "book", "video", "cert", "project"
    
    Returns:
        Ranked list of resources of that type
    """
    
    resources = get_resources_for_skill(skill, resource_type)
    
    if not resources:
        return {"error": f"No {resource_type}s found for {skill}"}
    
    ranked = rank_resources(resources)
    
    return {
        "skill": skill,
        "type": resource_type,
        "count": len(ranked),
        "resources": ranked[:5]
    }


# ---------- BUDGET-AWARE RECOMMENDATIONS ----------
def recommend_by_budget(skill_gaps, budget="free"):
    """
    Recommends resources filtered by budget.
    
    Args:
        skill_gaps: List of skills needing resources
        budget: "free", "affordable" (<$100), "premium" (any price)
    
    Returns:
        Resources grouped by skill, filtered by budget
    """
    
    recommendations = []
    
    for gap in skill_gaps:
        skill = gap.get("skill", "")
        
        # Determine price filter
        if budget == "free":
            max_price = 0
        elif budget == "affordable":
            max_price = 100
        else:
            max_price = float('inf')
        
        resources = get_resources_for_skill(skill)
        
        # Filter by price
        filtered = [r for r in resources if r.get("price", 0) <= max_price]
        
        if filtered:
            ranked = rank_resources(filtered)
            recommendations.append({
                "skill": skill,
                "gap_severity": assess_gap_severity(gap.get("gap_value", 0)),
                "budget": budget,
                "resources": create_resource_summary(ranked, 3)
            })
    
    return recommendations


# ---------- MAIN FUNCTION: RECOMMEND RESOURCES ----------
def recommend_resources(skill_gaps, profile=None):
    """
    Main function to recommend learning resources.
    
    Args:
        skill_gaps: Output from skill_gap_agent
                   [{skill: str, gap_value: float, tips: str, ...}]
        profile: User profile with preferences
                {
                    "hours_per_week": int,
                    "budget_preference": "free", "affordable", "any",
                    "learning_style": "visual", "hands-on", "reading", "mixed",
                    "difficulty_preference": "beginner", "intermediate", "advanced", "any"
                }
    
    Returns:
        Complete resource recommendation set
    """
    
    if not skill_gaps:
        # No skill gaps - recommend professional development and specialization resources
        return {
            "status": "no_gaps",
            "message": "Excellent! No critical skill gaps detected.",
            "recommendation_type": "Professional Development & Specialization",
            "insights": [
                "You have a strong foundation for your target domain",
                "Consider deepening expertise in specialized areas",
                "Explore complementary skills for career advancement",
                "Focus on building portfolio projects and real-world experience"
            ],
            "suggested_focus_areas": [
                "Advanced certifications in your domain",
                "Leadership and management skills",
                "Emerging technologies and innovations",
                "Research publications and knowledge sharing",
                "Mentoring and teaching others"
            ],
            "resources": []
        }
    
    if profile is None:
        profile = {
            "hours_per_week": 10,
            "budget_preference": "any",
            "learning_style": "any",
            "difficulty_preference": "intermediate"
        }
    
    # Generate learning path
    learning_path = generate_learning_path(skill_gaps, profile)
    
    if not learning_path:
        return {
            "error": "No resources found for given skill gaps",
            "skill_gaps": skill_gaps
        }
    
    # Compile total stats
    total_skills = len(learning_path)
    total_hours = sum(step.get("estimated_hours", 0) for step in learning_path)
    critical_gaps = len([s for s in learning_path if s["gap_severity"] == "critical"])
    
    return {
        "summary": {
            "total_skills_to_learn": total_skills,
            "critical_gaps": critical_gaps,
            "estimated_total_hours": round(total_hours, 1),
            "estimated_weeks": round(total_hours / profile.get("hours_per_week", 10), 1),
            "budget_preference": profile.get("budget_preference", "any"),
            "learning_style": profile.get("learning_style", "any")
        },
        "learning_path": learning_path,
        "statistics": {
            "critical_skills": critical_gaps,
            "significant_skills": len([s for s in learning_path if s["gap_severity"] == "significant"]),
            "moderate_skills": len([s for s in learning_path if s["gap_severity"] == "moderate"])
        },
        "next_steps": [
            f"Start with: {learning_path[0]['skill']}" if learning_path else "No skills identified",
            "Follow the order above for optimal learning",
            "Adjust pace based on your weekly availability",
            f"Dedicate ~{round(total_hours / profile.get('hours_per_week', 10))} weeks to this learning path"
        ]
    }


# ---------- ALTERNATIVE RESOURCE SET ----------
def get_alternative_resources(skill, current_resource_score=70):
    """
    Gets alternative resources if current one isn't working out.
    
    Args:
        skill: Skill for which to find alternatives
        current_resource_score: Score of current resource
    
    Returns:
        Alternative resources ranked by different criteria
    """
    
    all_resources = get_resources_for_skill(skill)
    
    if not all_resources:
        return {"error": f"No resources found for {skill}"}
    
    # Rank resources
    ranked = rank_resources(all_resources)
    
    # Find alternatives with score not too close to current
    alternatives = []
    for r in ranked:
        if abs(r.get("score", 0) - current_resource_score) > 10:
            alternatives.append(r)
    
    # If not enough alternatives, return next best options
    if len(alternatives) < 2:
        alternatives = ranked[1:4]
    
    return {
        "skill": skill,
        "alternatives": create_resource_summary(alternatives[:3])
    }


# ---------- QUICK START RECOMMENDATIONS ----------
def get_quick_start_resources(skill, hours_available=5):
    """
    Gets quick-start resources for a skill.
    Perfect for: "I have 5 hours this week, what should I learn?"
    
    Args:
        skill: Skill to learn quickly
        hours_available: Hours available for learning
    
    Returns:
        Resource recommendations that fit in time frame
    """
    
    resources = get_resources_for_skill(skill)
    
    # Filter by duration
    quick_resources = [
        r for r in resources 
        if r.get("hours_to_complete", 100) <= hours_available * 2
    ]
    
    if not quick_resources:
        # Get shortest resources available
        quick_resources = sorted(
            resources,
            key=lambda x: x.get("hours_to_complete", 100)
        )[:5]
    
    ranked = rank_resources(quick_resources)
    
    return {
        "skill": skill,
        "time_available": hours_available,
        "resources": create_resource_summary(ranked[:3]),
        "note": "These resources can be completed within your available time"
    }
