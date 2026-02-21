import json
import os


# ---------- LOAD DOMAIN RELATIONSHIPS ----------
def load_domain_relationships():
    """
    Loads mapping of domains and their alternatives.
    Shows skill overlap, transfer paths, and career relationships.
    """
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "alternative_paths.json"
    )
    
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    
    # Default fallback
    return {
        "domain_relationships": {},
        "skill_transfers": {},
        "pivot_paths": {}
    }


# ---------- LOAD CAREERS ----------
def load_careers():
    """Loads career data with domain and trait requirements."""
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "careers.json"
    )
    
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    
    return []


# ---------- ANALYZE CURRENT SKILLS ----------
def analyze_user_skills(profile):
    """
    Analyzes user's strongest traits from their profile.
    Returns ranked list of traits they excel at.
    """
    
    TRAITS = [
        "analytical", "creative", "social", "leadership",
        "practical", "empathy", "risk", "focus", "curiosity"
    ]
    
    skills = []
    for trait in TRAITS:
        value = profile.get(trait, 0)
        if value > 0:
            skills.append({
                "trait": trait,
                "strength": value,
                "level": "weak" if value < 4 else "moderate" if value < 7 else "strong"
            })
    
    # Sort by strength (descending)
    skills.sort(key=lambda x: x["strength"], reverse=True)
    
    return skills[:5]  # Return top 5 skills


# ---------- FIND SKILL OVERLAP ----------
def calculate_skill_overlap(user_skills, target_domain, profile):
    """
    Calculates how well user's skills match different domains.
    Returns similarity score for each domain.
    """
    
    relationships = load_domain_relationships()
    careers = load_careers()
    
    # Get traits needed for each domain
    domain_traits = {}
    for career in careers:
        domain = career["domain"]
        if domain not in domain_traits:
            domain_traits[domain] = []
        domain_traits[domain].extend(career["traits"])
    
    # Calculate overlap for each domain
    user_trait_names = [s["trait"] for s in user_skills]
    user_strengths = {s["trait"]: s["strength"] for s in user_skills}
    
    overlaps = []
    for domain, required_traits in domain_traits.items():
        if domain == target_domain:
            continue  # Skip the target domain itself
        
        # Count matching traits
        matches = 0
        match_strength = 0
        
        for trait in set(required_traits):
            if trait in user_trait_names:
                matches += 1
                match_strength += user_strengths.get(trait, 0)
        
        if matches > 0:
            overlap_percentage = (matches / len(set(required_traits))) * 100
            overlap_score = match_strength / matches if matches > 0 else 0
            
            overlaps.append({
                "domain": domain,
                "matching_traits": matches,
                "required_traits": len(set(required_traits)),
                "overlap_percentage": round(overlap_percentage, 1),
                "average_strength": round(overlap_score, 2)
            })
    
    # Sort by overlap percentage
    overlaps.sort(key=lambda x: x["overlap_percentage"], reverse=True)
    
    return overlaps


# ---------- FIND ALTERNATIVE PATHS ----------
def find_alternative_paths(target_domain, profile):
    """
    Finds alternative career paths user could pursue.
    Analyzes skill overlap and career progression options.
    """
    
    # Analyze user's skills
    user_skills = analyze_user_skills(profile)
    
    if not user_skills:
        return {
            "error": "Unable to analyze user skills",
            "alternatives": []
        }
    
    # Calculate skill overlap with other domains
    overlaps = calculate_skill_overlap(user_skills, target_domain, profile)
    
    # Get top alternatives (>50% skill overlap or top 3)
    strong_alternatives = [o for o in overlaps if o["overlap_percentage"] >= 50]
    if len(strong_alternatives) < 3:
        strong_alternatives.extend(overlaps[:3 - len(strong_alternatives)])
    
    # Build detailed alternative paths
    alternatives = []
    relationships = load_domain_relationships()
    
    for alt in strong_alternatives:
        domain = alt["domain"]
        
        # Get pivot info if available
        pivot_info = relationships.get("pivot_paths", {}).get(
            f"{target_domain}_to_{domain}", 
            {}
        )
        
        # Get skill transfer info
        skill_transfers = relationships.get("skill_transfers", {}).get(
            f"{target_domain}_to_{domain}",
            []
        )
        
        alternatives.append({
            "domain": domain,
            "skill_overlap": alt,
            "difficulty": assess_difficulty(alt["overlap_percentage"]),
            "time_to_transition": estimate_transition_time(alt["overlap_percentage"]),
            "transferable_skills": user_skills[:int(alt["matching_traits"])],
            "pivot_info": pivot_info,
            "skill_transfers": skill_transfers,
            "risk_level": assess_risk(alt["overlap_percentage"])
        })
    
    return {
        "current_domain": target_domain,
        "user_top_skills": user_skills,
        "total_alternatives_found": len(overlaps),
        "strong_alternatives": len(strong_alternatives),
        "alternatives": alternatives
    }


# ---------- ASSESS DIFFICULTY ----------
def assess_difficulty(overlap_percentage):
    """
    Assesses pivot difficulty based on skill overlap.
    Higher overlap = easier transition.
    """
    
    if overlap_percentage >= 75:
        return {
            "level": "easy",
            "description": "Similar skill requirements - smooth transition",
            "learning_effort": "minimal"
        }
    elif overlap_percentage >= 60:
        return {
            "level": "moderate",
            "description": "Good skill overlap - manageable transition",
            "learning_effort": "moderate"
        }
    elif overlap_percentage >= 50:
        return {
            "level": "challenging",
            "description": "Decent overlap but requires new skills",
            "learning_effort": "significant"
        }
    else:
        return {
            "level": "difficult",
            "description": "Limited overlap - major retraining needed",
            "learning_effort": "extensive"
        }


# ---------- ESTIMATE TRANSITION TIME ----------
def estimate_transition_time(overlap_percentage):
    """
    Estimates time needed to transition between domains.
    Based on skill gap (inverse of overlap).
    """
    
    skill_gap = 100 - overlap_percentage
    
    if skill_gap <= 25:
        return {
            "months": "3-6",
            "description": "Can transition within months"
        }
    elif skill_gap <= 40:
        return {
            "months": "6-12",
            "description": "1 year of focused learning"
        }
    elif skill_gap <= 60:
        return {
            "months": "12-18",
            "description": "1-1.5 years of intensive training"
        }
    else:
        return {
            "months": "18-24+",
            "description": "2+ years - consider bootcamp or degree"
        }


# ---------- ASSESS RISK LEVEL ----------
def assess_risk(overlap_percentage):
    """
    Assesses career transition risk.
    Lower overlap = higher risk of regret/failure.
    """
    
    if overlap_percentage >= 70:
        return {
            "level": "low",
            "confidence": "high",
            "recommendation": "Safe choice - strong skill foundation"
        }
    elif overlap_percentage >= 55:
        return {
            "level": "medium",
            "confidence": "moderate",
            "recommendation": "Viable but requires commitment to learning"
        }
    elif overlap_percentage >= 40:
        return {
            "level": "high",
            "confidence": "low",
            "recommendation": "Consider gaining relevant experience first"
        }
    else:
        return {
            "level": "very_high",
            "confidence": "very_low",
            "recommendation": "Major career change - extensive preparation needed"
        }


# ---------- LATERAL MOVES ----------
def find_lateral_moves(current_domain, target_domain, profile):
    """
    Suggests lateral moves within the same domain.
    Alternative job titles or specializations.
    """
    
    relationships = load_domain_relationships()
    lateral = relationships.get("lateral_moves", {}).get(
        f"{target_domain}_variants",
        []
    )
    
    careers = load_careers()
    domain_careers = [c for c in careers if c["domain"] == target_domain]
    
    moves = []
    for career in domain_careers:
        moves.append({
            "career": career["career"],
            "required_traits": career["traits"],
            "is_specialization": career.get("is_specialization", False),
            "skill_requirement": "similar" if career.get("is_specialization") else "foundational"
        })
    
    return {
        "domain": target_domain,
        "career_variants": moves,
        "total_options": len(moves)
    }


# ---------- GENERATE PIVOT RECOMMENDATIONS ----------
def generate_pivot_recommendations(alternatives):
    """
    Generates specific action steps for each alternative path.
    """
    
    recommendations = []
    
    for alt in alternatives.get("alternatives", []):
        domain = alt["domain"]
        difficulty = alt["difficulty"]["level"]
        time_estimate = alt["time_to_transition"]["months"]
        
        # Generate steps based on difficulty
        if difficulty == "easy":
            steps = [
                "1. Fine-tune specialized skills in your new domain",
                "2. Update portfolio with domain-specific projects",
                "3. Network in the new domain community",
                "4. Apply for positions (3-6 months)"
            ]
        elif difficulty == "moderate":
            steps = [
                "1. Fill skill gaps (2-3 months learning)",
                "2. Work on cross-domain projects",
                "3. Gain exposure through internship/freelance",
                "4. Build portfolio in new domain",
                "5. Apply for positions (6-12 months)"
            ]
        elif difficulty == "challenging":
            steps = [
                "1. Take foundational courses in new domain (3-4 months)",
                "2. Build proof projects demonstrating new skills",
                "3. Consider contract/project-based work first",
                "4. Gradually increase exposure to new domain",
                "5. Plan for 12-18 months transition"
            ]
        else:
            steps = [
                "1. Consider if this is truly the right path (reflect)",
                "2. Enroll in structured program/bootcamp (3-6 months)",
                "3. Build strong foundational knowledge",
                "4. Complete significant projects in new domain",
                "5. Gain practical experience",
                "6. Plan for 18-24+ months transition"
            ]
        
        recommendations.append({
            "domain": domain,
            "transition_period": time_estimate,
            "action_steps": steps,
            "priority": "immediate" if alt["risk_level"]["level"] == "low" else "medium" if alt["risk_level"]["level"] == "medium" else "low"
        })
    
    return recommendations


# ---------- MAIN FUNCTION: EXPLORE ALTERNATIVES ----------
def explore_alternative_paths(current_domain, target_domain, profile):
    """
    Main function to explore alternative career paths.
    
    Args:
        current_domain: User's current domain (optional)
        target_domain: Primary target domain
        profile: User profile with traits and preferences
    
    Returns:
        Comprehensive alternative paths analysis
    """
    
    # Validate inputs
    if not target_domain or not profile:
        return {"error": "Target domain and profile required"}
    
    # Find alternative paths
    alternatives = find_alternative_paths(target_domain, profile)
    
    if alternatives.get("error"):
        return alternatives
    
    # Generate pivot recommendations
    recommendations = generate_pivot_recommendations(alternatives)
    
    # Find lateral moves in target domain
    lateral_moves = find_lateral_moves(current_domain, target_domain, profile)
    
    return {
        "analysis": alternatives,
        "pivot_recommendations": recommendations,
        "lateral_moves": lateral_moves,
        "summary": {
            "primary_target": target_domain,
            "alternatives_count": alternatives["strong_alternatives"],
            "best_alternative": alternatives["alternatives"][0] if alternatives["alternatives"] else None,
            "consideration": "Review alternatives based on your interests and life circumstances"
        }
    }


# ---------- COMPARE PATHS ----------
def compare_career_paths(paths_to_compare, profile):
    """
    Compares multiple career paths side-by-side.
    Helps user evaluate different options.
    """
    
    user_skills = analyze_user_skills(profile)
    
    comparison = []
    
    for path in paths_to_compare:
        overlaps = calculate_skill_overlap(user_skills, path, profile)
        best_overlap = overlaps[0] if overlaps else None
        
        if best_overlap:
            comparison.append({
                "domain": path,
                "skill_overlap": f"{best_overlap['overlap_percentage']}%",
                "difficulty": assess_difficulty(best_overlap["overlap_percentage"])["level"],
                "time_to_transition": assess_difficulty(best_overlap["overlap_percentage"])["learning_effort"],
                "risk_level": assess_risk(best_overlap["overlap_percentage"])["level"],
                "fit_score": round(best_overlap["overlap_percentage"] / 100 * 10, 1)
            })
    
    # Sort by fit score
    comparison.sort(key=lambda x: x["fit_score"], reverse=True)
    
    return {
        "comparison": comparison,
        "recommendation": comparison[0]["domain"] if comparison else "Unable to determine",
        "all_viable": all(c["fit_score"] >= 5 for c in comparison)
    }


# ---------- SAFE VS AMBITIOUS PATHS ----------
def categorize_by_risk(alternatives):
    """
    Categorizes alternative paths by risk level.
    Helps user choose between safe and ambitious options.
    """
    
    safe = []
    moderate = []
    ambitious = []
    
    for alt in alternatives.get("alternatives", []):
        risk = alt["risk_level"]["level"]
        if risk == "low":
            safe.append(alt)
        elif risk in ["medium"]:
            moderate.append(alt)
        else:
            ambitious.append(alt)
    
    return {
        "safe_choices": safe,
        "moderate_choices": moderate,
        "ambitious_choices": ambitious,
        "recommendation_by_personality": {
            "risk_averse": "Choose from safe_choices",
            "balanced": "Choose from moderate_choices",
            "ambitious": "Consider ambitious_choices"
        }
    }
