import json
import os


# ---------- LOAD PACE ACCELERATION FACTORS ----------
def load_pace_config():
    """
    Loads configuration for pace customization factors.
    Returns default if file doesn't exist.
    """
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "pace_config.json"
    )
    
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    
    # Default configuration
    return {
        "hours_per_week_categories": {
            "low": {"min": 0, "max": 5, "multiplier": 1.5},
            "medium": {"min": 5, "max": 15, "multiplier": 1.0},
            "high": {"min": 15, "max": 30, "multiplier": 0.7},
            "very_high": {"min": 30, "max": 100, "multiplier": 0.5}
        },
        "complexity_tolerance": {
            "low": {"multiplier": 1.3, "description": "Prefers step-by-step learning"},
            "medium": {"multiplier": 1.0, "description": "Balanced approach"},
            "high": {"multiplier": 0.8, "description": "Comfortable with complex topics"}
        },
        "learning_capacity": {
            "slow": {"multiplier": 1.4, "retention_risk": "high"},
            "average": {"multiplier": 1.0, "retention_risk": "medium"},
            "fast": {"multiplier": 0.75, "retention_risk": "low"}
        }
    }


# ---------- ANALYZE LEARNING PACE PROFILE ----------
def analyze_learning_pace(profile):
    """
    Analyzes user's learning pace based on:
    - Available hours per week
    - Complexity tolerance (1-10 scale)
    - Learning capacity (1-10 scale)
    
    Returns categorization and relevant multiplier.
    """
    
    hours_per_week = profile.get("hours_per_week", 10)
    complexity_tolerance = profile.get("complexity_tolerance", 5)
    learning_capacity = profile.get("learning_capacity", 5)
    
    config = load_pace_config()
    
    # Categorize hours per week
    hours_category = "medium"
    hours_multiplier = 1.0
    
    for category, range_data in config["hours_per_week_categories"].items():
        if range_data["min"] <= hours_per_week < range_data["max"]:
            hours_category = category
            hours_multiplier = range_data["multiplier"]
            break
    
    # Categorize complexity tolerance
    if complexity_tolerance < 4:
        complexity_cat = "low"
    elif complexity_tolerance < 7:
        complexity_cat = "medium"
    else:
        complexity_cat = "high"
    
    complexity_multiplier = config["complexity_tolerance"][complexity_cat]["multiplier"]
    
    # Categorize learning capacity
    if learning_capacity < 4:
        capacity_cat = "slow"
    elif learning_capacity < 7:
        capacity_cat = "average"
    else:
        capacity_cat = "fast"
    
    capacity_data = config["learning_capacity"][capacity_cat]
    capacity_multiplier = capacity_data["multiplier"]
    
    return {
        "hours_per_week": {
            "value": hours_per_week,
            "category": hours_category,
            "multiplier": hours_multiplier
        },
        "complexity_tolerance": {
            "value": complexity_tolerance,
            "category": complexity_cat,
            "multiplier": complexity_multiplier,
            "description": config["complexity_tolerance"][complexity_cat]["description"]
        },
        "learning_capacity": {
            "value": learning_capacity,
            "category": capacity_cat,
            "multiplier": capacity_multiplier,
            "retention_risk": capacity_data["retention_risk"]
        }
    }


# ---------- CALCULATE PACE MULTIPLIER ----------
def calculate_pace_multiplier(pace_analysis):
    """
    Combines all factors into single pace multiplier.
    Multiplier > 1 means slower pace (longer timelines)
    Multiplier < 1 means faster pace (shorter timelines)
    """
    
    hours_mult = pace_analysis["hours_per_week"]["multiplier"]
    complexity_mult = pace_analysis["complexity_tolerance"]["multiplier"]
    capacity_mult = pace_analysis["learning_capacity"]["multiplier"]
    
    # Weighted average: hours (40%), complexity (35%), capacity (25%)
    combined = (hours_mult * 0.4) + (complexity_mult * 0.35) + (capacity_mult * 0.25)
    
    return round(combined, 2)


# ---------- ADJUST ROADMAP BY PACE ----------
def customize_roadmap_pace(roadmap, pace_analysis, profile):
    """
    Adjusts roadmap timelines based on learning pace profile.
    Returns customized roadmap with adjusted durations.
    """
    
    if not roadmap:
        return {"error": "No roadmap provided", "customization": None}
    
    multiplier = calculate_pace_multiplier(pace_analysis)
    
    # Parse and adjust each step's duration
    customized_steps = []
    
    for step in roadmap:
        adjusted_step = step.copy()
        
        # Parse estimated time (e.g., "3 months")
        if "estimated_time" in step:
            time_str = step["estimated_time"]
            try:
                # Extract number from string
                import re
                match = re.search(r'(\d+)', time_str)
                if match:
                    months = int(match.group(1))
                    adjusted_months = max(1, round(months * multiplier))
                    adjusted_step["estimated_time"] = f"{adjusted_months} months"
                    adjusted_step["original_time"] = time_str
                    adjusted_step["pace_multiplier"] = multiplier
            except:
                pass
        
        customized_steps.append(adjusted_step)
    
    return {
        "original_roadmap_length": len(roadmap),
        "customized_roadmap_length": len(customized_steps),
        "pace_multiplier": multiplier,
        "total_months_original": sum_months(roadmap),
        "total_months_customized": sum_months(customized_steps),
        "learning_hours_per_week": profile.get("hours_per_week", 10),
        "complexity_tolerance": profile.get("complexity_tolerance", 5),
        "learning_capacity": profile.get("learning_capacity", 5),
        "roadmap": customized_steps
    }


# ---------- HELPER: SUM MONTHS ----------
def sum_months(roadmap):
    """Calculates total months from roadmap steps."""
    total = 0
    import re
    
    for step in roadmap:
        if "estimated_time" in step:
            match = re.search(r'(\d+)', step["estimated_time"])
            if match:
                total += int(match.group(1))
    
    return total


# ---------- GENERATE PACE OPTIMIZATION TIPS ----------
def generate_pace_tips(pace_analysis, profile):
    """
    Generates personalized tips based on pace profile.
    """
    
    tips = []
    hours = pace_analysis["hours_per_week"]["value"]
    complexity = pace_analysis["complexity_tolerance"]["value"]
    capacity = pace_analysis["learning_capacity"]["value"]
    
    # Hours-based tips
    if hours < 5:
        tips.append("⏰ You have limited hours - focus on bite-sized lessons (15-30 min)")
        tips.append("💡 Use mobile learning apps for commute time")
        tips.append("📝 Consolidate learning into 2-3 focused sessions per week")
    elif hours > 30:
        tips.append("⚡ Your high availability allows deep diving into complex topics")
        tips.append("🎯 Consider intensive bootcamps or project-based learning")
        tips.append("🔄 Balance breadth and depth to avoid overwhelm")
    
    # Complexity-based tips
    if complexity < 4:
        tips.append("🧩 Break complex topics into smaller, digestible chunks")
        tips.append("📚 Use visual learning materials and diagrams")
        tips.append("🔄 Spend extra time on fundamentals before advanced topics")
    elif complexity >= 7:
        tips.append("💪 You can handle advanced concepts - challenge yourself with projects")
        tips.append("🚀 Consider advanced specializations early")
    
    # Capacity-based tips
    if capacity < 4:
        tips.append("🧠 Space out learning sessions to enhance retention")
        tips.append("✍️ Take detailed notes and review regularly")
        tips.append("🔁 Use spaced repetition techniques")
    elif capacity >= 7:
        tips.append("🎓 Your learning speed is strong - build projects to consolidate")
        tips.append("📖 Explore related topics to deepen understanding")
    
    return tips


# ---------- MAIN CUSTOMIZE PACE ----------
def customize_pace(profile, roadmap=None):
    """
    Main function to customize learning pace.
    
    Args:
        profile: User profile with hours_per_week, complexity_tolerance, learning_capacity
        roadmap: Optional roadmap to customize
    
    Returns:
        Complete pace customization report
    """
    
    # Validate profile
    if not profile:
        return {"error": "No profile provided"}
    
    # Analyze pace
    pace_analysis = analyze_learning_pace(profile)
    multiplier = calculate_pace_multiplier(pace_analysis)
    
    # Generate tips
    tips = generate_pace_tips(pace_analysis, profile)
    
    # Customize roadmap if provided
    customized_roadmap = None
    if roadmap:
        customized_roadmap = customize_roadmap_pace(roadmap, pace_analysis, profile)
    
    return {
        "profile_analysis": pace_analysis,
        "overall_pace_multiplier": multiplier,
        "pace_recommendation": get_pace_recommendation(multiplier),
        "tips": tips,
        "customized_roadmap": customized_roadmap
    }


# ---------- PACE RECOMMENDATION ----------
def get_pace_recommendation(multiplier):
    """Returns recommendation based on pace multiplier."""
    
    if multiplier > 1.3:
        return {
            "pace": "slow",
            "message": "Extended timeline recommended for thorough learning",
            "duration_vs_baseline": "30%+ longer"
        }
    elif multiplier > 1.1:
        return {
            "pace": "moderate",
            "message": "Take time to consolidate learning with practice",
            "duration_vs_baseline": "10-30% longer"
        }
    elif multiplier >= 0.9:
        return {
            "pace": "standard",
            "message": "Follow standard learning timeline",
            "duration_vs_baseline": "as planned"
        }
    elif multiplier >= 0.75:
        return {
            "pace": "accelerated",
            "message": "You can move faster - challenge yourself",
            "duration_vs_baseline": "15-25% shorter"
        }
    else:
        return {
            "pace": "fast-track",
            "message": "High capacity - consider intensive bootcamps or accelerated programs",
            "duration_vs_baseline": "25%+ shorter"
        }
