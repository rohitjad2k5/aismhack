"""
Test examples for Alternative Paths Agent
Shows how to explore career alternatives and pivots
"""

from agents.alternative_paths_agent import (
    explore_alternative_paths,
    find_alternative_paths,
    compare_career_paths,
    categorize_by_risk,
    analyze_user_skills
)


def test_tech_to_alternatives():
    """Test exploring alternatives from Technology domain"""
    print("\n" + "="*70)
    print("TEST 1: Technology Professional Exploring Alternatives")
    print("="*70)
    
    profile = {
        "analytical": 9,
        "focus": 8,
        "curiosity": 8,
        "creative": 5,
        "social": 4,
        "practical": 7,
        "leadership": 6,
        "empathy": 3,
        "risk": 5
    }
    
    # Analyze their current skills
    skills = analyze_user_skills(profile)
    print(f"\nTop Skills:")
    for skill in skills:
        print(f"  • {skill['trait'].capitalize()}: {skill['strength']}/10 ({skill['level']})")
    
    # Explore alternatives
    result = explore_alternative_paths("technology", "technology", profile)
    
    print(f"\nAlternatives Found: {result['analysis']['strong_alternatives']}")
    print("\nTop 3 Alternative Paths:")
    for i, alt in enumerate(result['analysis']['alternatives'][:3], 1):
        print(f"\n  {i}. {alt['domain'].upper()}")
        print(f"     Skill Overlap: {alt['skill_overlap']['overlap_percentage']}%")
        print(f"     Difficulty: {alt['difficulty']['level']}")
        print(f"     Time to Transition: {alt['time_to_transition']['months']}")
        print(f"     Risk Level: {alt['risk_level']['level']}")
        print(f"     Confidence: {alt['risk_level']['confidence']}")


def test_data_science_alternatives():
    """Test exploring alternatives from Data Science domain"""
    print("\n" + "="*70)
    print("TEST 2: Data Scientist Considering Pivots")
    print("="*70)
    
    profile = {
        "analytical": 9,
        "curiosity": 9,
        "focus": 7,
        "practical": 6,
        "social": 4,
        "creative": 5,
        "leadership": 3,
        "empathy": 4,
        "risk": 6
    }
    
    result = explore_alternative_paths(None, "data_science", profile)
    
    print(f"\nAlternative Paths Analysis for Data Science")
    print(f"Strong Alternatives: {result['analysis']['strong_alternatives']}")
    
    print("\nRecommendations by Risk Tolerance:")
    recommendations = result['pivot_recommendations']
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"\n  {i}. Pivot to {rec['domain'].upper()}")
        print(f"     Transition Period: {rec['transition_period']}")
        print(f"     Priority: {rec['priority']}")
        print(f"     Action Steps:")
        for step in rec['action_steps'][:3]:
            print(f"       • {step}")


def test_healthcare_to_education():
    """Test specific pivot: Healthcare to Education"""
    print("\n" + "="*70)
    print("TEST 3: Healthcare Professional to Education Pivot")
    print("="*70)
    
    profile = {
        "empathy": 9,
        "social": 8,
        "focus": 7,
        "analytical": 6,
        "curious": 7,
        "leadership": 6,
        "creative": 5,
        "practical": 6,
        "risk": 2
    }
    
    result = explore_alternative_paths("healthcare", "healthcare", profile)
    
    print(f"\nProfile Summary:")
    print(f"  Empathy: {profile['empathy']}/10")
    print(f"  Social: {profile['social']}/10")
    print(f"  Focus: {profile['focus']}/10")
    
    if result['analysis']['alternatives']:
        top_alt = result['analysis']['alternatives'][0]
        print(f"\nBest Alternative: {top_alt['domain'].upper()}")
        print(f"  Skill Overlap: {top_alt['skill_overlap']['overlap_percentage']}%")
        print(f"  Difficulty: {top_alt['difficulty']['description']}")
        print(f"  Risk Assessment: {top_alt['risk_level']['recommendation']}")


def test_compare_multiple_paths():
    """Test comparing multiple career paths"""
    print("\n" + "="*70)
    print("TEST 4: Comparing Multiple Career Paths")
    print("="*70)
    
    profile = {
        "analytical": 8,
        "creative": 7,
        "social": 6,
        "leadership": 7,
        "practical": 5,
        "empathy": 6,
        "risk": 7,
        "focus": 6,
        "curiosity": 8
    }
    
    paths_to_compare = ["technology", "business", "design", "finance"]
    
    print(f"\nComparing Paths: {', '.join(paths_to_compare)}")
    
    from agents.alternative_paths_agent import compare_career_paths
    comparison = compare_career_paths(paths_to_compare, profile)
    
    print(f"\nPath Comparison Results:")
    print(f"{'Domain':<20} {'Overlap':<10} {'Difficulty':<15} {'Risk':<12} {'Fit Score':<10}")
    print("-" * 67)
    
    for item in comparison['comparison']:
        print(f"{item['domain']:<20} {item['skill_overlap']:<10} {item['difficulty']:<15} {item['risk_level']:<12} {item['fit_score']:<10}")
    
    print(f"\nBest Choice: {comparison['recommendation'].upper()}")
    print(f"All Viable: {comparison['all_viable']}")


def test_risk_categorization():
    """Test risk categorization of alternatives"""
    print("\n" + "="*70)
    print("TEST 5: Risk-Based Path Categorization")
    print("="*70)
    
    profile = {
        "analytical": 7,
        "creative": 6,
        "social": 5,
        "leadership": 4,
        "practical": 7,
        "empathy": 5,
        "risk": 3,  # Low risk tolerance
        "focus": 7,
        "curiosity": 6
    }
    
    alternatives = explore_alternative_paths(None, "technology", profile)
    risk_categorized = categorize_by_risk(alternatives['analysis'])
    
    print(f"\nRisk Categorization:")
    print(f"Safe Choices ({len(risk_categorized['safe_choices'])}):")
    for alt in risk_categorized['safe_choices'][:2]:
        print(f"  • {alt['domain']}")
    
    print(f"\nModerate Choices ({len(risk_categorized['moderate_choices'])}):")
    for alt in risk_categorized['moderate_choices'][:2]:
        print(f"  • {alt['domain']}")
    
    print(f"\nAmbitious Choices ({len(risk_categorized['ambitious_choices'])}):")
    for alt in risk_categorized['ambitious_choices'][:2]:
        print(f"  • {alt['domain']}")
    
    print(f"\nRecommendation for Risk-Averse: {risk_categorized['recommendation_by_personality']['risk_averse']}")
    print(f"Recommendation for Balanced: {risk_categorized['recommendation_by_personality']['balanced']}")
    print(f"Recommendation for Ambitious: {risk_categorized['recommendation_by_personality']['ambitious']}")


def test_detailed_pivot_analysis():
    """Test detailed analysis of a specific pivot"""
    print("\n" + "="*70)
    print("TEST 6: Detailed Pivot Analysis - Tech to Finance")
    print("="*70)
    
    profile = {
        "analytical": 8,
        "focus": 7,
        "curiosity": 7,
        "risk": 6,
        "creative": 4,
        "social": 5,
        "leadership": 4,
        "practical": 6,
        "empathy": 3
    }
    
    result = explore_alternative_paths("technology", "technology", profile)
    
    print(f"\nUser Profile:")
    print(f"  Analytical: {profile['analytical']}/10")
    print(f"  Risk Tolerance: {profile['risk']}/10")
    print(f"  Curiosity: {profile['curiosity']}/10")
    
    # Find finance option
    finance_alt = None
    for alt in result['analysis']['alternatives']:
        if alt['domain'] == 'finance':
            finance_alt = alt
            break
    
    if finance_alt:
        print(f"\nPivot to Finance Analysis:")
        print(f"  Skill Overlap: {finance_alt['skill_overlap']['overlap_percentage']}%")
        print(f"  Required Traits: {finance_alt['skill_overlap']['required_traits']}")
        print(f"  Matching Traits: {finance_alt['skill_overlap']['matching_traits']}")
        print(f"  Average Strength: {finance_alt['skill_overlap']['average_strength']}/10")
        
        print(f"\n  Difficulty: {finance_alt['difficulty']['level']}")
        print(f"  Description: {finance_alt['difficulty']['description']}")
        
        print(f"\n  Time to Transition: {finance_alt['time_to_transition']['months']}")
        print(f"  Time Description: {finance_alt['time_to_transition']['description']}")
        
        print(f"\n  Risk Level: {finance_alt['risk_level']['level']}")
        print(f"  Confidence: {finance_alt['risk_level']['confidence']}")
        print(f"  Recommendation: {finance_alt['risk_level']['recommendation']}")


if __name__ == "__main__":
    test_tech_to_alternatives()
    test_data_science_alternatives()
    test_healthcare_to_education()
    test_compare_multiple_paths()
    test_risk_categorization()
    test_detailed_pivot_analysis()
    
    print("\n" + "="*70)
    print("All Alternative Paths Tests Completed!")
    print("="*70 + "\n")
