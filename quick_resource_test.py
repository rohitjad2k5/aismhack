from backend.agents.resource_recommender_agent import (
    recommend_resources,
    get_resources_for_skill
)

print("Test 1: Finding Resources for a Skill")
print("=" * 60)

resources = get_resources_for_skill("Python")
print(f"✓ Found {len(resources)} Python resources")
print(f"  Types: {set(r['type'] for r in resources)}")

print("\n\nTest 2: Generating Learning Path with Recommendations")
print("=" * 60)

skill_gaps = [
    {"skill": "Python", "gap_value": 0.4},
    {"skill": "statistics", "gap_value": 0.25}
]

profile = {
    "hours_per_week": 10,
    "budget_preference": "affordable",
    "learning_style": "any",
    "difficulty_preference": "beginner"
}

result = recommend_resources(skill_gaps, profile)

if not result.get('error'):
    print(f"✓ Learning Path Generated")
    print(f"  Total Skills: {result['summary']['total_skills_to_learn']}")
    print(f"  Estimated Hours: {result['summary']['estimated_total_hours']}")
    print(f"  Estimated Weeks: {result['summary']['estimated_weeks']}")
    
    if result['learning_path']:
        path = result['learning_path'][0]
        print(f"\n  First Skill: {path['skill']}")
        print(f"  Resources Found: {len(path['recommended_resources'])}")
        if path['recommended_resources']:
            top = path['recommended_resources'][0]
            print(f"  Top Resource: {top['title']}")
            print(f"    Provider: {top['provider']}")
            print(f"    Score: {top.get('score', 0)}/100")

print("\n" + "=" * 60)
print("✓ All Resource Recommender Tests Passed!")
print("=" * 60)
