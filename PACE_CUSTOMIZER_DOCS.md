# Pace Customizer Agent Documentation

## Overview
The **Pace Customizer Agent** adjusts learning roadmaps based on individual learner characteristics:
- **Available hours per week** - How much time they can dedicate to learning
- **Complexity tolerance** - Comfort level with difficult/abstract concepts
- **Learning capacity** - Speed at which they learn and retain information

## How It Works

### 1. Profile Analysis
The agent analyzes three dimensions of the user's learning profile:

```python
profile = {
    "hours_per_week": 10,          # Scale: 0-100
    "complexity_tolerance": 5,      # Scale: 1-10 (1=low, 10=high)
    "learning_capacity": 5          # Scale: 1-10 (1=slow, 10=fast)
}
```

### 2. Pace Calculation
Each dimension is converted to a multiplier:
- **Hours per week**: 
  - 0-5 hrs: 1.5x (slower pace needed)
  - 5-15 hrs: 1.0x (standard pace)
  - 15-30 hrs: 0.7x (can accelerate)
  - 30+ hrs: 0.5x (fast track possible)

- **Complexity tolerance**:
  - Low (1-3): 1.3x (more time for foundational learning)
  - Medium (4-6): 1.0x (balanced)
  - High (7-10): 0.8x (can handle complex topics faster)

- **Learning capacity**:
  - Slow (1-3): 1.4x (needs more review/retention time)
  - Average (4-6): 1.0x (standard)
  - Fast (7-10): 0.75x (quick learner, can accelerate)

### 3. Timeline Adjustment
The final multiplier is calculated as a weighted average:
```
multiplier = (hours_mult × 0.4) + (complexity_mult × 0.35) + (capacity_mult × 0.25)
```

This multiplier is applied to each step's duration in the roadmap.

## Usage Examples

### Basic Usage - Just Profile Analysis
```python
from agents.pace_customizer_agent import customize_pace

profile = {
    "hours_per_week": 10,
    "complexity_tolerance": 5,
    "learning_capacity": 5
}

result = customize_pace(profile)

print(result['pace_recommendation'])  # {"pace": "standard", ...}
print(result['tips'])  # Personalized learning tips
```

### With Roadmap Customization
```python
from agents.pace_customizer_agent import customize_pace
from agents.roadmap_agent import generate_roadmap

profile = {
    "hours_per_week": 5,
    "complexity_tolerance": 3,
    "learning_capacity": 4
}

roadmap = generate_roadmap("Data Science")
result = customize_pace(profile, roadmap)

# Get customized roadmap with adjusted timelines
customized_roadmap = result['customized_roadmap']['roadmap']
```

### Detailed Analysis
```python
from agents.pace_customizer_agent import analyze_learning_pace, calculate_pace_multiplier

pace_analysis = analyze_learning_pace(profile)
print(pace_analysis['hours_per_week'])      # Hours category & multiplier
print(pace_analysis['complexity_tolerance']) # Complexity category & multiplier
print(pace_analysis['learning_capacity'])    # Capacity category & multiplier

multiplier = calculate_pace_multiplier(pace_analysis)
print(f"Combined pace multiplier: {multiplier}")
```

## Return Value Structure

```python
{
    "profile_analysis": {
        "hours_per_week": {
            "value": 10,
            "category": "medium",
            "multiplier": 1.0
        },
        "complexity_tolerance": {
            "value": 5,
            "category": "medium",
            "multiplier": 1.0,
            "description": "Balanced approach"
        },
        "learning_capacity": {
            "value": 5,
            "category": "average",
            "multiplier": 1.0,
            "retention_risk": "medium"
        }
    },
    "overall_pace_multiplier": 1.0,
    "pace_recommendation": {
        "pace": "standard",
        "message": "Follow standard learning timeline",
        "duration_vs_baseline": "as planned"
    },
    "tips": [
        "⏰ You have limited hours - focus on bite-sized lessons...",
        "💡 Use mobile learning apps for commute time...",
        ...
    ],
    "customized_roadmap": {
        "original_roadmap_length": 5,
        "customized_roadmap_length": 5,
        "pace_multiplier": 1.0,
        "total_months_original": 12,
        "total_months_customized": 12,
        "learning_hours_per_week": 10,
        "roadmap": [
            {
                "step": 1,
                "title": "Learn Fundamentals",
                "estimated_time": "3 months",
                "original_time": "3 months",
                "pace_multiplier": 1.0
            },
            ...
        ]
    }
}
```

## Pace Tiers

| Tier | Multiplier | Expected Duration | Suitable For |
|------|-----------|------------------|--------------|
| **Slow** | > 1.3 | 30%+ longer | New learners, limited time, learning challenges |
| **Moderate** | 1.1-1.3 | 10-30% longer | Busy professionals, prefer deliberate pace |
| **Standard** | 0.9-1.1 | As planned | Balanced learners, standard commitment |
| **Accelerated** | 0.75-0.9 | 15-25% shorter | Experienced learners, good availability |
| **Fast-track** | < 0.75 | 25%+ shorter | Full-time, bootcamp-ready, high capacity |

## Integration with Master Orchestrator

The agent is already integrated in `master_orchestrator.py`:

```python
def build_full_report(best, results, profile):
    roadmap = generate_roadmap(best["domain"])
    
    return {
        "best_domain": best,
        "top_5": results[:5],
        "explanation": explain(best, profile),
        "skill_gap": skill_gap_analysis(profile, best),
        "roadmap": roadmap,
        "timeline": generate_timeline(best),
        "pace_customization": customize_pace(profile, roadmap)  # ← Added
    }
```

## Testing

Run the test file to see examples:
```bash
python backend/test_pace_customizer.py
```

This includes tests for:
- Slow learners (limited time, low complexity tolerance)
- Fast learners (ample time, high complexity tolerance)
- Balanced learners (moderate profile)
- Comparison across different profiles

## Configuration

Customize pace parameters in `backend/data/pace_config.json`:
- Adjust multipliers for each hour category
- Modify complexity/capacity thresholds
- Update personalized tips and recommendations

## Key Features

✅ **Personalized Timeline Adjustment** - Roadmap duration adapts to learner pace  
✅ **Retention Risk Assessment** - Identifies if pace might impact learning  
✅ **Actionable Tips** - Specific recommendations based on profile  
✅ **Multiple Factors** - Considers time, complexity, and capacity  
✅ **Flexible Configuration** - Easy to customize via JSON config  
✅ **Detailed Analytics** - Breaks down each dimension separately  

## Tips Generation

The agent generates context-specific tips based on profile:

### For Limited Time:
- Focus on bite-sized lessons
- Use mobile/commute time effectively
- Consolidate into focused sessions

### For High Complexity Tolerance:
- Dive into advanced topics early
- Take on challenging projects
- Explore cutting-edge technologies

### For Slow Learners:
- Use spaced repetition
- Space out sessions
- Keep detailed notes and review regularly

## Future Enhancements

- Integration with calendar/time-tracking apps
- Real-time pace adjustment based on actual progress
- ML-based learning capacity estimation
- Comparison with similar learner profiles
- Historical pace data analysis
- Stress/burnout prevention alerts
