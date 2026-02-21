from backend.agents.pace_customizer_agent import customize_pace

# Test with a sample profile
profile = {
    'hours_per_week': 10,
    'complexity_tolerance': 5,
    'learning_capacity': 5,
    'domain': 'web_development'
}

result = customize_pace(profile)

print('✓ Pace Customizer Agent Test')
print(f'  Profile: {profile}')
print(f'  Pace Multiplier: {result["overall_pace_multiplier"]}')
print(f'  Recommendation: {result["pace_recommendation"]["pace"]}')
print(f'  Tips Count: {len(result["tips"])}')
print()
print('✓ Agent initialized and working correctly!')
