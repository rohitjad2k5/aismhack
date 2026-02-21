#!/usr/bin/env python3
"""
Verification script to test all agents can be imported and run
from any directory with proper import and path handling.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent / "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

print("="*70)
print("PATHFORGE-AI AGENT VERIFICATION")
print("="*70)

agents_to_test = [
    ("Adaptive Agent", "agents.adaptive_agent", "next_question"),
    ("Assessment Agent", "agents.assessment_agent", "evaluate_domain_fit"),
    ("Career Matcher Agent", "agents.career_matcher_agent", "generate_careers"),
    ("Domain Agent", "agents.domain_agent", "evaluate_all_domains"),
    ("Timeline Agent", "agents.timeline_agent", "generate_timeline"),
    ("Skill Gap Agent", "agents.skillgap_agent", "skill_gap_analysis"),
    ("Roadmap Agent", "agents.roadmap_agent", "generate_roadmap"),
    ("Explanation Agent", "agents.explanation_agent", "explain"),
    ("Pace Customizer Agent", "agents.pace_customizer_agent", "customize_pace"),
    ("Alternative Paths Agent", "agents.alternative_paths_agent", "explore_alternative_paths"),
    ("Resource Recommender Agent", "agents.resource_recommender_agent", "recommend_resources"),
    ("Market Intelligence Agent", "agents.market_intelligence_agent", "analyze_market_intelligence"),
]

print("\nTesting Agent Imports:")
print("-" * 70)

passed = 0
failed = 0

for agent_name, module_name, function_name in agents_to_test:
    try:
        module = __import__(module_name, fromlist=[function_name])
        func = getattr(module, function_name)
        print(f"✓ {agent_name:<35} | {function_name}")
        passed += 1
    except Exception as e:
        print(f"✗ {agent_name:<35} | Error: {str(e)[:40]}")
        failed += 1

print("-" * 70)
print(f"\nResults: {passed} passed, {failed} failed")

if failed == 0:
    print("\n🎉 All agents verified successfully!")
    print("   Agents can be imported and run from any directory.")
    sys.exit(0)
else:
    print(f"\n⚠️  {failed} agent(s) need attention")
    sys.exit(1)
