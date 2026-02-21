import requests
import feedparser
if skill_gaps: topic = skill_gaps[0] # Example else: topic = f"advanced {domain} techniques" papers = get_research_papers(topic) return { "topic": topic, "papers": papers }

ARXIV_URL = "http://export.arxiv.org/api/query"

def get_research_papers(topic="research methodology", max_results=5):
    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": max_results
    }

    response = requests.get(ARXIV_URL, params=params)
    feed = feedparser.parse(response.text)

    papers = []

    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })

    return papers