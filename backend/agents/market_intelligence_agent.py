import json
import os
from datetime import datetime
from collections import Counter


# ---------- LOAD MARKET DATA SOURCES ----------
def load_market_data_sources():
    """
    Loads market data configuration with free API sources and mock data.
    """
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "market_data.json"
    )
    
    if not os.path.exists(path):
        return {
            "status": "offline",
            "message": "Market data unavailable"
        }
    
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"status": "error"}


# ---------- FETCH MARKET DATA FOR A DOMAIN ----------
def fetch_market_data(domain, location="US"):
    """
    Retrieves market data for a specific domain and location.
    Uses local market data cache.
    """
    all_data = load_market_data_sources()
    
    if all_data.get("status") == "offline":
        return {"total_jobs": 0, "jobs": []}
    
    domain_lower = domain.lower().replace(" ", "_")
    
    # Look for domain in job_data
    for key in all_data.get("job_data", {}):
        if domain_lower in key.lower():
            domain_data = all_data["job_data"][key]
            # Handle both "listings" and "jobs" keys
            jobs = domain_data.get("jobs", domain_data.get("listings", []))
            
            return {
                "total_jobs": len(jobs),
                "jobs": jobs,
                "hiring_trend": domain_data.get("hiring_trend", "stable"),
                "average_salary": domain_data.get("average_salary", 0),
                "market_size": domain_data.get("market_size", "medium")
            }
    
    return {"total_jobs": 0, "jobs": [], "hiring_trend": "unknown"}


# ---------- CALCULATE DEMAND SCORE (0-100) ----------
def calculate_demand_score(market_data):
    """
    Calculates demand score based on:
    - Job openings (0-60 points)
    - Hiring trend bonus (-10 to +20 points)
    - Salary premium bonus (0-15 points)
    """
    total_jobs = market_data.get("total_jobs", 0)
    
    # Job openings scoring
    job_points = min(60, (total_jobs / 10) * 60)
    
    # Hiring trend bonus
    trend = market_data.get("hiring_trend", "stable")
    trend_bonus = {"booming": 20, "growing": 10, "stable": 0, "declining": -10}.get(trend, 0)
    
    # Salary premium bonus
    salary = market_data.get("average_salary", 0)
    salary_bonus = min(15, (salary / 200000) * 15)
    
    score = job_points + trend_bonus + salary_bonus
    
    return {
        "score": max(0, min(100, score)),
        "factors": {
            "job_openings": {
                "value": total_jobs,
                "contribution": job_points,
                "rating": "high demand" if total_jobs > 20 else "low demand"
            },
            "hiring_trend": {
                "value": trend,
                "contribution": trend_bonus
            },
            "salary_premium": {
                "value": f"${salary:,}",
                "contribution": salary_bonus,
                "rating": "high" if salary > 150000 else "moderate"
            }
        }
    }


# ---------- CALCULATE COMPETITION SCORE (0-100) ----------
def calculate_competition_score(market_data, user_skills=None):
    """
    Calculates competition based on:
    - Required skills diversity (0-40 points)
    - Experience requirements (0-30 points)
    - Entry-level job availability (±20 points)
    - Skill match with user (±10 points)
    """
    jobs = market_data.get("jobs", [])
    
    # Skills diversity
    all_skills = []
    for job in jobs:
        all_skills.extend(job.get("required_skills", []))
    unique_skills = len(set(all_skills))
    skills_points = min(40, unique_skills * 2)
    
    # Experience requirements
    exp_values = [j.get("experience_years", 0) for j in jobs]
    avg_exp = sum(exp_values) / len(exp_values) if exp_values else 0
    exp_points = 30 - (avg_exp * 5)
    
    # Entry-level availability
    entry_level = sum(1 for j in jobs if j.get("experience_years", 0) <= 2)
    entry_bonus = min(20, (entry_level / len(jobs)) * 40) if jobs else 0
    
    # Skill match
    skill_match = 0
    if user_skills and jobs:
        job_skills = set(s.lower() for j in jobs for s in j.get("required_skills", []))
        user_skills_lower = set(s.lower() for s in user_skills)
        if job_skills:
            skill_match = (len(user_skills_lower & job_skills) / len(job_skills)) * 100
    
    score = skills_points + exp_points + entry_bonus - (skill_match / 10)
    
    return {
        "score": max(0, min(100, score)),
        "difficulty_level": "hard" if score > 70 else "moderate" if score > 40 else "easy",
        "factors": {
            "required_skills": {
                "unique_count": unique_skills,
                "contribution": skills_points
            },
            "experience_gap": {
                "average_required": f"{avg_exp:.1f} years",
                "contribution": exp_points
            },
            "entry_level_availability": {
                "count": entry_level,
                "contribution": entry_bonus
            },
            "skill_match_with_user": {
                "match_ratio": f"{skill_match:.1f}%",
                "contribution": -skill_match / 10
            }
        }
    }


# ---------- CALCULATE OPPORTUNITY SCORE (0-100) ----------
def calculate_opportunity_score(demand_score, competition_score):
    """
    Combines demand and competition into opportunity rating.
    Opportunity = (Demand - Competition) / 2 + 50
    """
    demand = demand_score["score"] if isinstance(demand_score, dict) else demand_score
    competition = competition_score["score"] if isinstance(competition_score, dict) else competition_score
    
    score = ((demand - competition) / 2) + 50
    score = max(0, min(100, score))
    
    # Tier interpretation
    if score >= 75:
        tier = "excellent"
        interpretation = "High demand + Low competition = Best time to transition"
    elif score >= 60:
        tier = "good"
        interpretation = "Decent demand, moderate competition"
    elif score >= 40:
        tier = "moderate"
        interpretation = "Balanced market, may require some upskilling"
    else:
        tier = "challenging"
        interpretation = "Low demand + High competition"
    
    return {
        "score": score,
        "tier": tier,
        "analysis": {
            "demand_score": demand,
            "competition_score": competition,
            "interpretation": interpretation
        }
    }


# ---------- CALCULATE SUCCESS PROBABILITY (0-100%) ----------
def calculate_success_probability(profile, skill_gaps=None, competition_score=None, demand_score=None):
    """
    Estimates transition success probability (0-100%).
    Factors:
    - Skill match (30%): how many skills user already has
    - Learning capacity (20%): hours/week and complexity tolerance
    - Available time (20%): hours per week available
    - Market demand (15%): job availability
    - Competition (15%): how many competing candidates
    """
    skill_gaps = skill_gaps or []
    competition = competition_score["score"] if isinstance(competition_score, dict) else (competition_score or 50)
    demand = demand_score["score"] if isinstance(demand_score, dict) else (demand_score or 50)
    
    # Skill match (30%)
    if skill_gaps:
        # Handle both dict and string formats in skill_gaps
        gap_values = []
        for sg in skill_gaps:
            if isinstance(sg, dict):
                gap_values.append(sg.get("gap_value", 0.5))
            else:
                # If it's a string (skill name), assume 0.5 gap
                gap_values.append(0.5)
        
        avg_gap = sum(gap_values) / len(gap_values) if gap_values else 0.5
        skill_match = (1 - avg_gap) * 100
    else:
        skill_match = 50
    
    skill_factor = (skill_match / 100) * 30
    
    # Learning capacity (20%)
    capacity = profile.get("learning_capacity", 5)
    capacity_factor = (capacity / 10) * 20
    
    # Available time (20%)
    hours = profile.get("hours_per_week", 15)
    time_factor = min(20, (hours / 30) * 20)
    
    # Market factors (30% combined)
    demand_factor = (demand / 100) * 15
    competition_factor = max(0, (100 - competition) / 100) * 15
    
    probability = skill_factor + capacity_factor + time_factor + demand_factor + competition_factor
    
    confidence = "high" if probability > 70 else "moderate" if probability > 40 else "low"
    
    return {
        "probability": max(0, min(100, probability)),
        "confidence": confidence,
        "factors": {
            "skill_match": {
                "value": f"{skill_match:.0f}%",
                "contribution": skill_factor
            },
            "learning_capacity": {
                "value": f"{capacity}/10",
                "contribution": capacity_factor
            },
            "available_time": {
                "value": f"{hours} hrs/week",
                "contribution": time_factor
            },
            "market_demand": {
                "value": f"{demand:.0f}/100",
                "contribution": demand_factor
            },
            "competition": {
                "value": f"{competition:.0f}/100",
                "contribution": competition_factor
            }
        }
    }


# ---------- EXTRACT IN-DEMAND SKILLS ----------
def extract_in_demand_skills(market_data, top_n=10):
    """
    Returns top skills ranked by frequency in job listings (0-100 scale).
    Shows which skills appear most across all job postings.
    """
    jobs = market_data.get("jobs", [])
    skill_freq = Counter()
    
    for job in jobs:
        for skill in job.get("required_skills", []):
            skill_freq[skill.lower()] += 1
    
    total_jobs = len(jobs) if jobs else 1
    
    skills_list = []
    for skill, freq in skill_freq.most_common(top_n):
        percentage = (freq / total_jobs) * 100
        skills_list.append({
            "skill": skill.title(),
            "frequency": freq,
            "percentage_of_jobs": f"{percentage:.1f}%"
        })
    
    return skills_list


# ---------- GET SALARY INSIGHTS ----------
def get_salary_insights(market_data):
    """
    Analyzes salary data and returns min, max, average.
    """
    jobs = market_data.get("jobs", [])
    salaries = []
    
    for job in jobs:
        sal_range = job.get("salary_range", {})
        if sal_range.get("min"):
            salaries.append(sal_range["min"])
        if sal_range.get("max"):
            salaries.append(sal_range["max"])
    
    if not salaries:
        return {
            "minimum": 0,
            "maximum": 0,
            "average": 0,
            "currency": "USD"
        }
    
    return {
        "minimum": min(salaries),
        "maximum": max(salaries),
        "average": sum(salaries) / len(salaries),
        "currency": "USD"
    }


# ---------- GENERATE JOB ALERTS ----------
def generate_job_alerts(market_data, user_skills, top_n=5):
    """
    Matches user's current skills to job listings.
    Returns jobs ranked by skill match percentage.
    """
    jobs = market_data.get("jobs", [])
    user_skills_lower = set(s.lower() for s in user_skills)
    
    matched_jobs = []
    
    for job in jobs:
        job_skills = set(s.lower() for s in job.get("required_skills", []))
        matching = user_skills_lower & job_skills
        missing = job_skills - user_skills_lower
        
        if job_skills:
            match_score = (len(matching) / len(job_skills)) * 100
        else:
            match_score = 0
        
        matched_jobs.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "salary": f"${job.get('salary_range', {}).get('min', 0):,} - ${job.get('salary_range', {}).get('max', 0):,}",
            "match_score": match_score,
            "matching_skills": [s.title() for s in matching],
            "missing_skills": [s.title() for s in list(missing)[:3]]
        })
    
    # Sort by match score descending
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    
    return matched_jobs[:top_n]


# ---------- MAIN ANALYZE FUNCTION ----------
def analyze_market_intelligence(domain, profile, skill_gaps=None, location="US"):
    """
    Comprehensive market intelligence analysis for a domain.
    Returns demand, competition, opportunity, success probability, and recommendations.
    """
    market_data = fetch_market_data(domain, location)
    
    # Get user skills from profile
    user_skills = profile.get("current_skills", [])
    
    # Calculate scores
    demand_result = calculate_demand_score(market_data)
    competition_result = calculate_competition_score(market_data, user_skills)
    opportunity_result = calculate_opportunity_score(demand_result, competition_result)
    success_result = calculate_success_probability(profile, skill_gaps, competition_result, demand_result)
    
    # Get market insights
    in_demand = extract_in_demand_skills(market_data)
    salary = get_salary_insights(market_data)
    job_matches = generate_job_alerts(market_data, user_skills, top_n=3)
    
    # Generate recommendation
    if opportunity_result["score"] >= 75:
        recommendation = "🟢 EXCELLENT - Strong demand meets your skills"
    elif opportunity_result["score"] >= 60:
        recommendation = "🟡 GOOD - Solid opportunity with moderate effort"
    elif opportunity_result["score"] >= 40:
        recommendation = "🟠 MODERATE - Achievable with focused upskilling"
    else:
        recommendation = "🔴 CHALLENGING - High competition, lower success probability | → Consider alternative paths or extensive upskilling"
    
    return {
        "domain": domain,
        "location": location,
        "market_overview": {
            "total_job_openings": market_data.get("total_jobs", 0),
            "market_size_assessment": "large" if market_data.get("total_jobs", 0) > 100 else "medium" if market_data.get("total_jobs", 0) > 20 else "small",
            "hiring_trend": market_data.get("hiring_trend", "stable")
        },
        "scores": {
            "demand_score": {
                "score": demand_result["score"],
                "factors": demand_result["factors"]
            },
            "competition_score": {
                "score": competition_result["score"],
                "difficulty_level": competition_result["difficulty_level"],
                "factors": competition_result["factors"]
            },
            "opportunity_score": {
                "score": opportunity_result["score"],
                "tier": opportunity_result["tier"],
                "interpretation": opportunity_result["analysis"]["interpretation"]
            },
            "success_probability": {
                "probability": success_result["probability"],
                "confidence": success_result["confidence"],
                "factors": success_result["factors"]
            }
        },
        "market_insights": {
            "in_demand_skills": in_demand,
            "salary_range": {
                "minimum": salary["minimum"],
                "maximum": salary["maximum"],
                "average": salary["average"],
                "currency": salary["currency"]
            },
            "top_job_matches": job_matches
        },
        "recommendation": recommendation,
        "next_steps": [
            f"1. Master '{in_demand[0]['skill']}' - Most in-demand skill for {domain}" if in_demand else f"1. Learn key skills for {domain}",
            f"2. Build portfolio matching top jobs in {domain}",
            f"3. Target companies with openings: {job_matches[0]['company'] if job_matches else 'Various'}",
            f"4. Network with professionals in this domain",
            f"5. Monitor salary trends and job growth"
        ]
    }
