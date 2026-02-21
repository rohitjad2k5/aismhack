# Alternative Paths Agent Documentation

## Overview
The **Alternative Paths Agent** helps users explore different career directions based on their skills. Instead of committing to a single domain, users can see:
- **Alternative domains** they could pursue with minimal retraining
- **Skill transfers** that leverage existing expertise
- **Risk assessment** for each path (easy pivots vs ambitious moves)
- **Lateral moves** within their domain (specializations)
- **Detailed action steps** for each alternative

## How It Works

### 1. Skill Analysis
The agent analyzes your top 5 strengths from 9 traits:
```python
TRAITS = [
    "analytical", "creative", "social", "leadership",
    "practical", "empathy", "risk", "focus", "curiosity"
]
```

**Example Profile:**
```python
profile = {
    "analytical": 9,    # Strong
    "focus": 8,         # Strong
    "curiosity": 8,     # Strong
    "creative": 5,      # Moderate
    "social": 4,        # Weak
    "practical": 7,
    "leadership": 6,
    "empathy": 3,
    "risk": 5
}
```

### 2. Alternative Discovery
For each alternative domain, the agent calculates:
- **Skill Overlap %**: How many required traits you already have
- **Matching Traits**: Specific skills that transfer
- **Difficulty Level**: How hard the pivot is
- **Time to Transition**: Estimated months needed
- **Risk Level**: Probability of success

### 3. Recommendation Tiers

| Overlap | Difficulty | Time | Risk | Action |
|---------|-----------|------|------|--------|
| **75%+** | Easy | 3-6 months | Low | Direct pivot |
| **60-75%** | Moderate | 6-12 months | Medium | Manageable transition |
| **50-60%** | Challenging | 12-18 months | High | Significant effort |
| **<50%** | Difficult | 18-24+ months | Very High | Major retraining |

## Core Functions

### 1. Explore Alternative Paths
```python
from agents.alternative_paths_agent import explore_alternative_paths

result = explore_alternative_paths(
    current_domain="technology",
    target_domain="technology",
    profile={...}
)
```

**Returns:**
```python
{
    "analysis": {
        "current_domain": "technology",
        "user_top_skills": [...],
        "total_alternatives_found": 8,
        "strong_alternatives": 3,
        "alternatives": [
            {
                "domain": "data_science",
                "skill_overlap": {
                    "overlap_percentage": 75.0,
                    "matching_traits": 3,
                    ...
                },
                "difficulty": {...},
                "time_to_transition": {...},
                "risk_level": {...},
                "transferable_skills": [...]
            },
            ...
        ]
    },
    "pivot_recommendations": [
        {
            "domain": "data_science",
            "transition_period": "6-12 months",
            "action_steps": [
                "1. Fine-tune specialized skills...",
                "2. Update portfolio...",
                ...
            ],
            "priority": "immediate"
        }
    ],
    "lateral_moves": {...},
    "summary": {...}
}
```

### 2. Analyze User Skills
```python
from agents.alternative_paths_agent import analyze_user_skills

skills = analyze_user_skills(profile)
# Returns top 5 traits with strength levels
```

**Output:**
```python
[
    {"trait": "analytical", "strength": 9, "level": "strong"},
    {"trait": "focus", "strength": 8, "level": "strong"},
    {"trait": "curiosity", "strength": 8, "level": "strong"},
    {"trait": "practical", "strength": 7, "level": "moderate"},
    {"trait": "leadership", "strength": 6, "level": "moderate"}
]
```

### 3. Compare Multiple Paths
```python
from agents.alternative_paths_agent import compare_career_paths

comparison = compare_career_paths(
    paths_to_compare=["technology", "business", "finance", "design"],
    profile={...}
)
```

**Output:**
```python
{
    "comparison": [
        {
            "domain": "finance",
            "skill_overlap": "75%",
            "difficulty": "moderate",
            "time_to_transition": "significant",
            "risk_level": "medium",
            "fit_score": 7.5
        },
        ...
    ],
    "recommendation": "finance",
    "all_viable": True
}
```

### 4. Risk-Based Categorization
```python
from agents.alternative_paths_agent import categorize_by_risk

categories = categorize_by_risk(alternatives)
```

**Returns:**
- `safe_choices` - Low risk, similar skills (70%+ overlap)
- `moderate_choices` - Medium risk, decent skills (55-70% overlap)
- `ambitious_choices` - High risk, significant change needed (<55% overlap)

### 5. Lateral Moves
```python
from agents.alternative_paths_agent import find_lateral_moves

moves = find_lateral_moves(
    current_domain="technology",
    target_domain="technology",
    profile={...}
)
```

**Finds specializations within same domain:**
- Technology: Frontend, Backend, Full-stack, Mobile, DevOps, Architect
- Data Science: ML Engineer, Analytics Engineer, Data Engineer, MLOps
- Business: Product Manager, Analyst, Consultant, Entrepreneur
- Healthcare: Clinical, Research, Management, Medical Tech

## Real-World Examples

### Example 1: Software Engineer → Data Science
```
Profile: High analytical, high focus, high curiosity (weak social)

Analysis:
  Skill Overlap: 75% ✓
  Difficulty: Easy
  Time: 6-12 months
  Risk: Low ✓
  
Action Steps:
  1. Learn statistics and ML algorithms (3-4 months)
  2. Build 2-3 ML projects (portfolio)
  3. Do Kaggle competitions
  4. Network in DS community
  5. Apply for positions

Recommendation: Safe pivot, go for it!
```

### Example 2: Healthcare Professional → Education
```
Profile: High empathy, high social, good focus (weak analytical)

Analysis:
  Skill Overlap: 75% ✓
  Difficulty: Easy
  Time: 6-12 months
  Risk: Low ✓
  
Transferable Skills:
  • Patient/student empathy
  • Clear communication
  • Domain expertise
  • Mentoring ability

Action Steps:
  1. Get teaching certification (2-3 months)
  2. Design online course
  3. Start instructing
  4. Build student testimonials
```

### Example 3: Finance → Technology
```
Profile: High analytical, high risk tolerance, low social

Analysis:
  Skill Overlap: 50%
  Difficulty: Challenging
  Time: 18-24 months
  Risk: High ⚠️
  
Skill Gap:
  • Need: System design, programming, software architecture
  • Have: analytical thinking, problem-solving

Recommendation:
  "Major pivot. Consider coding bootcamp or 
   transition to FinTech for hybrid role first.
   18-24 month commitment needed."

Action Steps:
  1. Enroll in coding bootcamp (4-6 months)
  2. Build portfolio projects (3-4 months)
  3. Contribute to open source (ongoing)
  4. Target FinTech roles first
  5. Gradually transition to mainstream tech
```

## Return Value Breakdown

```python
result = explore_alternative_paths(current, target, profile)

# Main sections:
result["analysis"]               # Detailed skill overlap analysis
result["pivot_recommendations"]  # Step-by-step action plans  
result["lateral_moves"]          # Specializations in target domain
result["summary"]                # Quick overview & recommendations
```

### Analysis Section
```python
{
    "current_domain": "technology",
    "user_top_skills": [
        {"trait": "analytical", "strength": 9, "level": "strong"},
        ...
    ],
    "total_alternatives_found": 8,
    "strong_alternatives": 3,    # Hit >50% overlap threshold
    "alternatives": [...]
}
```

### Alternative Details
```python
{
    "domain": "data_science",
    "skill_overlap": {
        "overlap_percentage": 75.0,
        "matching_traits": 3,
        "required_traits": 4,
        "average_strength": 7.5
    },
    "difficulty": {
        "level": "moderate",
        "description": "Good skill overlap - manageable transition",
        "learning_effort": "moderate"
    },
    "time_to_transition": {
        "months": "6-12",
        "description": "1 year of focused learning"
    },
    "risk_level": {
        "level": "medium",
        "confidence": "moderate",
        "recommendation": "Viable but requires commitment to learning"
    },
    "transferable_skills": [...]
}
```

## Configuration

Edit `backend/data/alternative_paths.json` to customize:
- Domain relationships (which domains are related)
- Skill transfers (what carries over)
- Pivot paths (specific step-by-step transitions)
- Lateral moves (specializations)
- Career progression (levels and titles)
- Risk mitigation (strategies for each risk level)

## Integration with Master Orchestrator

The agent is automatically included in the full career report:

```python
def build_full_report(best, results, profile):
    return {
        "best_domain": best,
        "skill_gap": skill_gap_analysis(...),
        "roadmap": generate_roadmap(...),
        "pace_customization": customize_pace(...),
        "alternative_paths": explore_alternative_paths(...)  # ← Added
    }
```

## Testing

Run the comprehensive test suite:
```bash
python backend/test_alternative_paths.py
```

Tests include:
- **Tech to alternatives** - Software engineer exploring options
- **Data science pivots** - Data scientist considering moves
- **Healthcare to education** - Specific domain transition
- **Path comparison** - Side-by-side evaluation
- **Risk categorization** - Safe vs ambitious options
- **Detailed pivot analysis** - Deep dive on one transition

## Key Features

✅ **Skill-Based Matching** - Compare traits to find compatible domains  
✅ **Risk Assessment** - Know if pivot is safe or ambitious  
✅ **Lateral Moves** - Find specializations within domain  
✅ **Time Estimates** - Know how long transition takes  
✅ **Action Plans** - Step-by-step next actions  
✅ **Skill Transfers** - See what carries over  
✅ **Confidence Scoring** - Understand probability of success  

## Advanced Usage

### Explore Safe Pivots Only
```python
alternatives = explore_alternative_paths(None, "technology", profile)
safe = categorize_by_risk(alternatives['analysis'])['safe_choices']
for opt in safe:
    print(f"Safe: {opt['domain']}")
```

### Compare Specific Domains
```python
comparison = compare_career_paths(
    ["data_science", "finance", "business"],
    profile
)
best = comparison['comparison'][0]['domain']
```

### Get Action Plan for Specific Path
```python
result = explore_alternative_paths(None, "technology", profile)
for pivot in result['pivot_recommendations']:
    if pivot['domain'] == 'data_science':
        for step in pivot['action_steps']:
            print(f"• {step}")
```

## Examples of Skill Transfers

### Technology → Data Science
- Problem-solving mindset
- Programming foundation
- System thinking
- Debugging skills
- Performance optimization

### Technology → Business
- Project management
- Communication skills
- Requirements understanding
- Stakeholder management
- Technical advantage

### Data Science → Finance
- Statistical analysis
- Data handling
- Quantitative reasoning
- Pattern recognition
- Risk assessment

### Healthcare → Education
- Empathy and patience
- Clear communication
- Domain expertise
- Mentoring ability
- Understanding learner needs

## Future Enhancements

🔮 **Machine Learning Integration** - Predict success probability  
🔮 **Market Demand Analysis** - Show job market fit for alternatives  
🔮 **Salary Impact** - Calculate income change for each pivot  
🔮 **Interview Prep** - Prepare for pivot interviews  
🔮 **Mentor Matching** - Connect with people who made the transition  
🔮 **Community Insights** - Learn from others' pivot experiences  
🔮 **Real-time Updates** - Track job market trends  
