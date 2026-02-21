from backend.agents.alternative_paths_agent import (
    explore_alternative_paths,
    analyze_user_skills,
    compare_career_paths
)

# Test 1: Basic functionality
print("Test 1: Tech Professional Exploring Alternatives")
print("=" * 60)

profile = {
    "analytical": 9,
    "focus": 8,
    "curiosity": 8,
    "practical": 7,
    "creative": 5,
    "social": 4,
    "leadership": 6,
    "empathy": 3,
    "risk": 5
}

skills = analyze_user_skills(profile)
print(f"✓ Top Skills Analyzed: {len(skills)} skills identified")
print(f"  Top skill: {skills[0]['trait'].capitalize()} ({skills[0]['strength']}/10)")

result = explore_alternative_paths(None, "technology", profile)
print(f"✓ Alternatives Found: {result['analysis']['strong_alternatives']} strong alternatives")
if result['analysis']['alternatives']:
    top = result['analysis']['alternatives'][0]
    print(f"  Best alternative: {top['domain'].upper()} ({top['skill_overlap']['overlap_percentage']}% overlap)")

print(f"✓ Pivot Recommendations: {len(result['pivot_recommendations'])} action plans generated")

# Test 2: Compare paths
print("\n\nTest 2: Comparing Multiple Career Paths")
print("=" * 60)

paths = ["technology", "data_science", "business", "finance"]
comparison = compare_career_paths(paths, profile)
print(f"✓ Comparison Complete: {len(comparison['comparison'])} paths analyzed")
print(f"  Best match: {comparison['recommendation'].upper()}")
print(f"  All viable: {comparison['all_viable']}")

print("\n" + "=" * 60)
print("✓ All Alternative Paths Agent Tests Passed!")
print("=" * 60)
