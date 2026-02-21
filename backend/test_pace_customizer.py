"""
Test examples for Pace Customizer Agent
Shows how to use the agent with different user profiles
"""

from agents.pace_customizer_agent import customize_pace, analyze_learning_pace
from agents.roadmap_agent import generate_roadmap


def test_pace_slow_learner():
    """Test for someone with limited time, low complexity tolerance, slower learning"""
    print("\n" + "="*60)
    print("TEST 1: Slow Learner Profile")
    print("="*60)
    
    profile = {
        "hours_per_week": 3,
        "complexity_tolerance": 2,
        "learning_capacity": 3,
        "domain": "data_science"
    }
    
    # Get pace analysis
    pace_analysis = analyze_learning_pace(profile)
    print(f"\nPace Analysis:\n{pace_analysis}")
    
    # Generate roadmap and customize
    roadmap = generate_roadmap("Data Science")
    result = customize_pace(profile, roadmap)
    
    print(f"\nPace Recommendation: {result['pace_recommendation']}")
    print(f"Overall Multiplier: {result['overall_pace_multiplier']}")
    print("\nTips:")
    for tip in result['tips']:
        print(f"  • {tip}")
    
    print("\nCustomized Roadmap:")
    if result['customized_roadmap']:
        for step in result['customized_roadmap']['roadmap']:
            print(f"  Step {step['step']}: {step['title']}")
            print(f"    Time: {step.get('estimated_time', 'N/A')} (Original: {step.get('original_time', 'N/A')})")


def test_pace_fast_learner():
    """Test for someone with lots of time, high complexity tolerance, fast learning"""
    print("\n" + "="*60)
    print("TEST 2: Fast Learner Profile")
    print("="*60)
    
    profile = {
        "hours_per_week": 40,
        "complexity_tolerance": 9,
        "learning_capacity": 9,
        "domain": "machine_learning"
    }
    
    pace_analysis = analyze_learning_pace(profile)
    print(f"\nPace Analysis:\n{pace_analysis}")
    
    roadmap = generate_roadmap("Machine Learning")
    result = customize_pace(profile, roadmap)
    
    print(f"\nPace Recommendation: {result['pace_recommendation']}")
    print(f"Overall Multiplier: {result['overall_pace_multiplier']}")
    print("\nTips:")
    for tip in result['tips']:
        print(f"  • {tip}")


def test_pace_balanced():
    """Test for someone with balanced profile"""
    print("\n" + "="*60)
    print("TEST 3: Balanced Learner Profile")
    print("="*60)
    
    profile = {
        "hours_per_week": 10,
        "complexity_tolerance": 5,
        "learning_capacity": 5,
        "domain": "web_development"
    }
    
    pace_analysis = analyze_learning_pace(profile)
    print(f"\nPace Analysis:\n{pace_analysis}")
    
    roadmap = generate_roadmap("Web Development")
    result = customize_pace(profile, roadmap)
    
    print(f"\nPace Recommendation: {result['pace_recommendation']}")
    print(f"Overall Multiplier: {result['overall_pace_multiplier']}")
    print("\nCustomized Timeline:")
    if result['customized_roadmap']:
        orig_months = result['customized_roadmap']['total_months_original']
        custom_months = result['customized_roadmap']['total_months_customized']
        print(f"  Original: ~{orig_months} months")
        print(f"  Customized: ~{custom_months} months")


def test_comparison():
    """Compare different profiles"""
    print("\n" + "="*60)
    print("TEST 4: Profile Comparison")
    print("="*60)
    
    profiles = [
        {
            "name": "Part-timer",
            "hours_per_week": 5,
            "complexity_tolerance": 4,
            "learning_capacity": 5
        },
        {
            "name": "Full-timer",
            "hours_per_week": 20,
            "complexity_tolerance": 6,
            "learning_capacity": 7
        },
        {
            "name": "Career Switcher",
            "hours_per_week": 30,
            "complexity_tolerance": 5,
            "learning_capacity": 6
        }
    ]
    
    for profile_data in profiles:
        name = profile_data.pop('name')
        result = customize_pace(profile_data)
        print(f"\n{name}:")
        print(f"  Hours/week: {profile_data['hours_per_week']}")
        print(f"  Pace Multiplier: {result['overall_pace_multiplier']}")
        print(f"  Recommendation: {result['pace_recommendation']['pace']}")
        print(f"  Duration: {result['pace_recommendation']['duration_vs_baseline']}")


if __name__ == "__main__":
    test_pace_slow_learner()
    test_pace_fast_learner()
    test_pace_balanced()
    test_comparison()
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
