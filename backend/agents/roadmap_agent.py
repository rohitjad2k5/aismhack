import json
import os
import random

def load_templates():

    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "roadmap_templates.json"
    )

    with open(path) as f:
        return json.load(f)


def generate_roadmap(career):

    templates = load_templates()

    if career in templates:
        steps = templates[career]
    else:
        # fallback dynamic roadmap
        steps = [
            "Learn Fundamentals",
            "Develop Skills",
            "Build Projects",
            "Gain Experience",
            "Apply Professionally"
        ]

    roadmap = []

    for i, step in enumerate(steps):
        roadmap.append({
            "step": i+1,
            "title": step,
            "estimated_time": f"{random.randint(2,12)} months"
        })

    return roadmap