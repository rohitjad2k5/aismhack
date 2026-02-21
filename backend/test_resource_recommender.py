"""
Test examples for Resource Recommender Agent
Shows how to recommend learning resources based on skill gaps
"""

from agents.resource_recommender_agent import (
    recommend_resources,
    get_resources_for_skill,
    rank_resources,
    generate_learning_path,
    recommend_by_budget,
    get_quick_start_resources
)


def test_basic_recommendation():
    """Test basic resource recommendation"""
    print("\n" + "="*70)
    print("TEST 1: Basic Resource Recommendation")
    print("="*70)
    
    skill_gaps = [
        {
            "skill": "Python",
            "gap_value": 0.4,
            "learning_tip": "Focus on fundamentals and practical coding"
        },
        {
            "skill": "statistics",
            "gap_value": 0.25,
            "learning_tip": "Understand distributions and hypothesis testing"
        }
    ]
    
    profile = {
        "hours_per_week": 10,
        "budget_preference": "affordable",
        "learning_style": "any",
        "difficulty_preference": "beginner"
    }
    
    result = recommend_resources(skill_gaps, profile)
    
    print(f"\n✓ Resource Recommendation Generated")
    print(f"  Total Skills: {result['summary']['total_skills_to_learn']}")
    print(f"  Critical Gaps: {result['summary']['critical_gaps']}")
    print(f"  Total Hours: {result['summary']['estimated_total_hours']}")
    print(f"  Weeks to Complete: {result['summary']['estimated_weeks']}")
    
    print(f"\nLearning Path ({len(result['learning_path'])} steps):")
    for step in result['learning_path'][:2]:
        print(f"  Step {step['step']}: {step['skill']}")
        print(f"    Severity: {step['gap_severity']}")
        print(f"    Est. Hours: {step['estimated_hours']:.0f}")
        if step['recommended_resources']:
            top = step['recommended_resources'][0]
            print(f"    Top Resource: {top['title']}")
            print(f"      Type: {top['type']} | Rating: {top['rating']}/5 | Cost: ${top.get('price', 0)}")


def test_budget_filtering():
    """Test budget-aware recommendations"""
    print("\n" + "="*70)
    print("TEST 2: Budget-Aware Recommendations")
    print("="*70)
    
    skill_gaps = [
        {"skill": "Python", "gap_value": 0.4},
        {"skill": "web development", "gap_value": 0.35},
        {"skill": "data science", "gap_value": 0.25}
    ]
    
    profile = {
        "hours_per_week": 8,
        "budget_preference": "free",
        "learning_style": "any",
        "difficulty_preference": "beginner"
    }
    
    print("\nRecommendations for FREE budget:")
    result = recommend_resources(skill_gaps, profile)
    
    if result.get('learning_path'):
        for step in result['learning_path'][:1]:
            if step['recommended_resources']:
                for i, res in enumerate(step['recommended_resources'][:2], 1):
                    cost_str = "Free" if res.get('price', 0) == 0 else f"${res.get('price', 0)}"
                    print(f"  {i}. {res['title']} ({cost_str})")
                    print(f"     Provider: {res['provider']} | Rating: {res['rating']}/5")


def test_learning_style_matching():
    """Test learning style based recommendations"""
    print("\n" + "="*70)
    print("TEST 3: Learning Style Matching")
    print("="*70)
    
    skill_gaps = [
        {"skill": "statistics", "gap_value": 0.3},
        {"skill": "Python", "gap_value": 0.25}
    ]
    
    # Visual learner
    profile_visual = {
        "hours_per_week": 10,
        "budget_preference": "any",
        "learning_style": "visual",
        "difficulty_preference": "beginner"
    }
    
    # Hands-on learner
    profile_hands_on = {
        "hours_per_week": 10,
        "budget_preference": "any",
        "learning_style": "hands-on",
        "difficulty_preference": "beginner"
    }
    
    print("\nVisual Learner Recommendations:")
    visual_result = recommend_resources(skill_gaps, profile_visual)
    if visual_result.get('learning_path'):
        path = visual_result['learning_path'][0]
        if path['recommended_resources']:
            res = path['recommended_resources'][0]
            print(f"  Top: {res['title']} (Type: {res['type']})")
            print(f"  Learning Style: {res.get('learning_style', [])}")
    
    print("\nHands-On Learner Recommendations:")
    hands_result = recommend_resources(skill_gaps, profile_hands_on)
    if hands_result.get('learning_path'):
        path = hands_result['learning_path'][0]
        if path['recommended_resources']:
            res = path['recommended_resources'][0]
            print(f"  Top: {res['title']} (Type: {res['type']})")
            print(f"  Learning Style: {res.get('learning_style', [])}")


def test_time_constrained():
    """Test recommendations for time-constrained learners"""
    print("\n" + "="*70)
    print("TEST 4: Time-Constrained Learning")
    print("="*70)
    
    skill_gaps = [
        {"skill": "Python", "gap_value": 0.3},
        {"skill": "machine learning", "gap_value": 0.4}
    ]
    
    # Very limited time
    profile = {
        "hours_per_week": 3,
        "budget_preference": "any",
        "learning_style": "any",
        "difficulty_preference": "beginner"
    }
    
    result = recommend_resources(skill_gaps, profile)
    
    print(f"\nProfile: Only {profile['hours_per_week']} hours per week available")
    print(f"Recommendation: {result['summary']['estimated_weeks']} weeks to complete")
    
    print("\nSuggested learning order:")
    for step in result['learning_path'][:2]:
        res = step['recommended_resources'][0] if step['recommended_resources'] else None
        if res:
            hours = res.get('hours_to_complete', 0)
            print(f"  • {step['skill']}: {hours} hours ({res['title']})")
    
    print(f"\nNext Steps:")
    for step in result['next_steps'][:2]:
        print(f"  • {step}")


def test_quick_start():
    """Test quick-start resources (learn in 5 hours)"""
    print("\n" + "="*70)
    print("TEST 5: Quick Start Resources")
    print("="*70)
    
    print("\nIf you have 5 hours this week, learn Python:")
    quick = get_quick_start_resources("Python", hours_available=5)
    
    if quick.get('resources'):
        for res in quick['resources'][:2]:
            print(f"\n  {res['title']}")
            print(f"    Provider: {res['provider']}")
            print(f"    Duration: {res['duration']}")
            print(f"    Cost: {res['cost']}")
            print(f"    Rating: {res['rating']}")
    
    print(f"\n  Note: {quick.get('note', '')}")


def test_alternative_resources():
    """Test finding alternative resources if current one isn't working"""
    print("\n" + "="*70)
    print("TEST 6: Resource Alternatives")
    print("="*70)
    
    skill_gaps = [
        {"skill": "Python", "gap_value": 0.35}
    ]
    
    profile = {
        "hours_per_week": 10,
        "budget_preference": "free",
        "learning_style": "video",
        "difficulty_preference": "beginner"
    }
    
    print("\nInitial Recommendation:")
    result = recommend_resources(skill_gaps, profile)
    
    if result.get('learning_path'):
        path = result['learning_path'][0]
        if path['recommended_resources']:
            primary = path['recommended_resources'][0]
            print(f"  Primary: {primary['title']} (Score: {primary.get('score', 0)})")
            
            print(f"\n  Alternatives:")
            for alt in path['recommended_resources'][1:3]:
                print(f"    • {alt['title']}")
                print(f"      Provider: {alt['provider']} | Duration: {alt.get('hours_to_complete', 0)} hours")


def test_comprehensive_profile():
    """Test comprehensive recommendation for complete profile"""
    print("\n" + "="*70)
    print("TEST 7: Comprehensive Learning Recommendation")
    print("="*70)
    
    skill_gaps = [
        {
            "skill": "Python",
            "gap_value": 0.4,
            "learning_tip": "Focus on syntax and data structures"
        },
        {
            "skill": "data science",
            "gap_value": 0.35,
            "learning_tip": "Learn statistics and machine learning"
        },
        {
            "skill": "machine learning",
            "gap_value": 0.3,
            "learning_tip": "Understand algorithms and implementation"
        },
        {
            "skill": "statistics",
            "gap_value": 0.25,
            "learning_tip": "Probability and hypothesis testing"
        }
    ]
    
    profile = {
        "hours_per_week": 15,
        "budget_preference": "affordable",
        "learning_style": "hands-on",
        "difficulty_preference": "intermediate"
    }
    
    result = recommend_resources(skill_gaps, profile)
    
    print(f"\n📊 Summary:")
    print(f"  Skills to Learn: {result['summary']['total_skills_to_learn']}")
    print(f"  Critical Gaps: {result['summary']['critical_gaps']}")
    print(f"  Total Time: {result['summary']['estimated_hours']} hours ({result['summary']['estimated_weeks']} weeks)")
    print(f"  Budget: {result['summary']['budget_preference']}")
    print(f"  Learning Style: {result['summary']['learning_style']}")
    
    print(f"\n📚 Learning Path:")
    for step in result['learning_path'][:3]:
        print(f"\n  Step {step['step']}: {step['skill'].upper()}")
        print(f"    Gap Severity: {step['gap_severity']}")
        print(f"    Est. Time: {step['estimated_hours']:.0f} hours")
        
        if step['recommended_resources']:
            res = step['recommended_resources'][0]
            print(f"\n    Top Resource:")
            print(f"      📌 {res['title']}")
            print(f"      👤 {res['provider']}")
            print(f"      ⏱️  {res.get('hours_to_complete', 0)} hours")
            print(f"      💰 {format_cost(res.get('price', 0))}")
            print(f"      ⭐ {res['rating']}/5 ({res.get('reviews', 0)} reviews)")
            print(f"      📖 {res.get('difficulty', 'Mixed')}")


def format_cost(price):
    if price == 0:
        return "Free"
    else:
        return f"${price}"


if __name__ == "__main__":
    test_basic_recommendation()
    test_budget_filtering()
    test_learning_style_matching()
    test_time_constrained()
    test_quick_start()
    test_alternative_resources()
    test_comprehensive_profile()
    
    print("\n" + "="*70)
    print("✓ All Resource Recommender Tests Completed!")
    print("="*70 + "\n")
