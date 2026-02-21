"""
Test examples for Market Intelligence Agent
Shows how market analysis validates domain choices
"""

from agents.market_intelligence_agent import (
    analyze_market_intelligence,
    calculate_demand_score,
    calculate_competition_score,
    calculate_opportunity_score,
    calculate_success_probability,
    extract_in_demand_skills,
    get_salary_insights,
    generate_job_alerts,
    fetch_market_data
)


def test_basic_market_analysis():
    """Test basic market intelligence analysis"""
    print("\n" + "="*70)
    print("TEST 1: Basic Market Analysis for Data Science")
    print("="*70)
    
    profile = {
        "hours_per_week": 15,
        "learning_capacity": 7,
        "current_skills": ["Python", "Statistics"]
    }
    
    skill_gaps = [
        {"skill": "Machine Learning", "gap_value": 0.35},
        {"skill": "Deep Learning", "gap_value": 0.4},
        {"skill": "SQL", "gap_value": 0.2}
    ]
    
    result = analyze_market_intelligence("data_science", profile, skill_gaps)
    
    print(f"\n✓ Market Analysis Complete")
    print(f"  Domain: {result['domain']}")
    print(f"  Total Jobs Available: {result['market_overview']['total_job_openings']}")
    print(f"  Market Size: {result['market_overview']['market_size_assessment']}")
    print(f"  Hiring Trend: {result['market_overview']['hiring_trend']}")
    
    print(f"\n📊 Scores:")
    print(f"  Demand Score: {result['scores']['demand_score']['score']}/100")
    print(f"  Competition Score: {result['scores']['competition_score']['score']}/100")
    print(f"  Opportunity Score: {result['scores']['opportunity_score']['score']}/100 ({result['scores']['opportunity_score']['tier']})")
    print(f"  Success Probability: {result['scores']['success_probability']['probability']}% ({result['scores']['success_probability']['confidence']})")


def test_demand_analysis():
    """Test demand score calculation"""
    print("\n" + "="*70)
    print("TEST 2: Demand Score Analysis")
    print("="*70)
    
    market_data = fetch_market_data("technology")
    demand = calculate_demand_score(market_data)
    
    print(f"\nTechnology Domain Demand Analysis:")
    print(f"  Overall Score: {demand['score']}/100")
    print(f"\n  Breakdowns:")
    print(f"    • Job Openings: {demand['factors']['job_openings']['value']} ({demand['factors']['job_openings']['rating']} demand)")
    print(f"    • Hiring Trend: {demand['factors']['hiring_trend']['value']} (bonus: {demand['factors']['hiring_trend']['contribution']})")
    print(f"    • Average Salary: {demand['factors']['salary_premium']['value']} ({demand['factors']['salary_premium']['rating']})")


def test_competition_analysis():
    """Test competition score"""
    print("\n" + "="*70)
    print("TEST 3: Competition Analysis")
    print("="*70)
    
    market_data = fetch_market_data("data_science")
    user_skills = ["Python", "Statistics", "SQL"]
    
    competition = calculate_competition_score(market_data, user_skills)
    
    print(f"\nData Science Competition Analysis:")
    print(f"  Overall Score: {competition['score']}/100 ({competition['difficulty_level']})")
    print(f"\n  Factors:")
    print(f"    • Required Skills: {competition['factors']['required_skills']['unique_count']} unique skills")
    print(f"    • Average Experience: {competition['factors']['experience_gap']['average_required']}")
    print(f"    • Entry-Level Jobs: {competition['factors']['entry_level_availability']['count']} available")
    print(f"    • Your Skill Match: {competition['factors']['skill_match_with_user']['match_ratio']}")


def test_opportunity_score():
    """Test opportunity combining demand and competition"""
    print("\n" + "="*70)
    print("TEST 4: Opportunity Score")
    print("="*70)
    
    market_data = fetch_market_data("finance")
    demand = calculate_demand_score(market_data)
    competition = calculate_competition_score(market_data)
    opportunity = calculate_opportunity_score(demand, competition)
    
    print(f"\nFinance Domain Opportunity Analysis:")
    print(f"  Demand: {opportunity['analysis']['demand_score']}/100")
    print(f"  Competition: {opportunity['analysis']['competition_score']}/100")
    print(f"  Opportunity Score: {opportunity['score']}/100")
    print(f"  Tier: {opportunity['tier'].upper()}")
    print(f"  Interpretation: {opportunity['analysis']['interpretation']}")


def test_success_probability():
    """Test success probability calculation"""
    print("\n" + "="*70)
    print("TEST 5: Success Probability")
    print("="*70)
    
    # Strong candidate
    profile = {
        "hours_per_week": 20,
        "learning_capacity": 8,
        "current_skills": ["Python", "SQL", "Statistics"]
    }
    
    skill_gaps = [
        {"skill": "Machine Learning", "gap_value": 0.2},
        {"skill": "TensorFlow", "gap_value": 0.3}
    ]
    
    market_data = fetch_market_data("data_science")
    demand = calculate_demand_score(market_data)
    competition = calculate_competition_score(market_data, profile["current_skills"])
    success_prob = calculate_success_probability(profile, skill_gaps, competition, demand)
    
    print(f"\nStrong Candidate Profile:")
    print(f"  Learning Capacity: {profile['learning_capacity']}/10")
    print(f"  Hours/Week: {profile['hours_per_week']}")
    print(f"  Current Skills: {', '.join(profile['current_skills'])}")
    print(f"\n  Success Probability: {success_prob['probability']}% ({success_prob['confidence']})")
    print(f"\n  Factor Breakdown:")
    for factor, data in success_prob['factors'].items():
        print(f"    • {factor}: {data['value']} (contributes {data['contribution']} points)")


def test_in_demand_skills():
    """Test skill extraction from market"""
    print("\n" + "="*70)
    print("TEST 6: In-Demand Skills")
    print("="*70)
    
    market_data = fetch_market_data("technology")
    skills = extract_in_demand_skills(market_data, top_n=8)
    
    print(f"\nTop Skills in Technology:")
    total_jobs = market_data['total_jobs']
    for i, skill in enumerate(skills, 1):
        print(f"  {i}. {skill['skill']} - Required in {skill['percentage_of_jobs']}% of jobs ({skill['frequency']}/{total_jobs})")


def test_salary_insights():
    """Test salary data extraction"""
    print("\n" + "="*70)
    print("TEST 7: Salary Insights")
    print("="*70)
    
    domains = ["data_science", "technology", "finance", "design"]
    
    print(f"\nAverage Salary Comparison by Domain:")
    print(f"{'Domain':<20} {'Min':<15} {'Max':<15} {'Average':<15}")
    print("-" * 65)
    
    for domain in domains:
        market_data = fetch_market_data(domain)
        salary = get_salary_insights(market_data)
        print(f"{domain:<20} ${salary['minimum']:<14,} ${salary['maximum']:<14,} ${salary['average']:<14,.0f}")


def test_job_alerts():
    """Test job matching to user skills"""
    print("\n" + "="*70)
    print("TEST 8: Job Alerts - Jobs Matching Your Skills")
    print("="*70)
    
    user_skills = ["Python", "SQL", "Statistics"]
    market_data = fetch_market_data("data_science")
    
    jobs = generate_job_alerts(market_data, user_skills, top_n=3)
    
    print(f"\nData Science jobs matching your skills: {user_skills}")
    for i, job in enumerate(jobs, 1):
        print(f"\n  {i}. {job['title']} at {job['company']}")
        print(f"     Location: {job['location']}")
        print(f"     Salary: {job['salary']}")
        print(f"     Match Score: {job['match_score']}%")
        print(f"     ✓ You have: {', '.join(job['matching_skills']) if job['matching_skills'] else 'none'}")
        print(f"     ✗ You need: {', '.join(job['missing_skills'][:3]) if job['missing_skills'] else 'nothing'}")


def test_comprehensive_market_analysis():
    """Test complete market intelligence for a domain"""
    print("\n" + "="*70)
    print("TEST 9: Comprehensive Market Intelligence")
    print("="*70)
    
    profile = {
        "hours_per_week": 12,
        "learning_capacity": 6,
        "current_skills": ["Java", "System Design", "Algorithms", "SQL"]
    }
    
    skill_gaps = [
        {"skill": "Cloud Computing", "gap_value": 0.4},
        {"skill": "Microservices", "gap_value": 0.35},
        {"skill": "DevOps", "gap_value": 0.5}
    ]
    
    print("\n🔍 Analyzing Technology Market for Cloud Engineer Role...")
    
    result = analyze_market_intelligence("technology", profile, skill_gaps)
    
    print(f"\n📊 MARKET OVERVIEW")
    print(f"  Total Jobs Available: {result['market_overview']['total_job_openings']}")
    print(f"  Market Size: {result['market_overview']['market_size_assessment']}")
    print(f"  Hiring Trend: {result['market_overview']['hiring_trend']}")
    
    print(f"\n🎯 OPPORTUNITY ASSESSMENT")
    opp = result['scores']['opportunity_score']
    print(f"  Opportunity Score: {opp['score']}/100 ({opp['tier'].upper()})")
    print(f"  Demand: {result['scores']['demand_score']['score']}/100")
    print(f"  Competition: {result['scores']['competition_score']['score']}/100")
    
    print(f"\n✅ SUCCESS PROBABILITY")
    succ = result['scores']['success_probability']
    print(f"  {succ['probability']}% success likelihood ({succ['confidence']})")
    
    print(f"\n💰 SALARY EXPECTATIONS")
    salary = result['market_insights']['salary_range']
    print(f"  Range: ${salary['minimum']:,} - ${salary['maximum']:,}")
    print(f"  Average: ${salary['average']:,.0f}")
    
    print(f"\n🔥 TOP IN-DEMAND SKILLS")
    for i, skill in enumerate(result['market_insights']['in_demand_skills'][:5], 1):
        print(f"  {i}. {skill['skill']} (in {skill['percentage_of_jobs']}% of jobs)")
    
    print(f"\n🎪 MATCHING JOBS")
    for i, job in enumerate(result['market_insights']['top_job_matches'][:2], 1):
        print(f"  {i}. {job['title']} at {job['company']}")
        print(f"     Match: {job['match_score']}% | {job['location']} | {job['salary']}")
    
    print(f"\n💡 RECOMMENDATION")
    print(f"  {result['recommendation']}")
    
    print(f"\n📋 NEXT STEPS")
    for step in result['next_steps']:
        print(f"  → {step}")


def test_market_comparison():
    """Compare market opportunity across domains"""
    print("\n" + "="*70)
    print("TEST 10: Domain Comparison - Which Has Best Opportunity?")
    print("="*70)
    
    profile = {
        "hours_per_week": 15,
        "learning_capacity": 7,
        "current_skills": ["Python", "Statistics", "SQL"]
    }
    
    domains = ["data_science", "technology", "finance"]
    
    print(f"\nComparing Market Opportunities:")
    print(f"{'Domain':<20} {'Demand':<10} {'Competition':<12} {'Opportunity':<12} {'Success %':<10}")
    print("-" * 64)
    
    for domain in domains:
        market_data = fetch_market_data(domain)
        demand = calculate_demand_score(market_data)
        competition = calculate_competition_score(market_data, profile["current_skills"])
        opportunity = calculate_opportunity_score(demand, competition)
        success = calculate_success_probability(profile, [], competition, demand)
        
        print(f"{domain:<20} {demand['score']:<10.0f} {competition['score']:<12.0f} {opportunity['score']:<12.0f} {success['probability']:<10.1f}%")


if __name__ == "__main__":
    test_basic_market_analysis()
    test_demand_analysis()
    test_competition_analysis()
    test_opportunity_score()
    test_success_probability()
    test_in_demand_skills()
    test_salary_insights()
    test_job_alerts()
    test_comprehensive_market_analysis()
    test_market_comparison()
    
    print("\n" + "="*70)
    print("✓ All Market Intelligence Tests Completed!")
    print("="*70 + "\n")
