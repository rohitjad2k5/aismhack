import requests
import httpx
from datetime import datetime


# ==============================
# 🔐 ADZUNA API CONFIG
# ==============================

ADZUNA_APP_ID = "960f8b21"
ADZUNA_APP_KEY = "8fb4058a6c35aa1cb7ba18ee322e9f39"


# ==============================
# 🧠 DOMAIN → JOB ROLE MAPPING
# ==============================

def map_domain_to_roles(domain):
    mapping = {
        "research": ["Research Scientist", "AI Researcher", "Data Scientist"],
        "engineering": ["Software Engineer", "Mechanical Engineer"],
        "technology": ["Software Developer", "Backend Developer", "Full Stack Developer"],
        "business": ["Business Analyst", "Product Manager"],
        "law": ["Legal Associate", "Corporate Lawyer"]
    }
    return mapping.get(domain.lower(), [domain])


# ==============================
# 🛑 FALLBACK HANDLER
# ==============================

def fallback_market_data(domain):
    return {
        "domain": domain,
        "job_count": 0,
        "average_salary": None,
        "hiring_trend": "unknown",
        "note": "Fallback used - API unavailable"
    }


# ==============================
# 🔵 SYNC VERSION
# ==============================

def get_market_data(domain, location="us"):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
        job_roles = map_domain_to_roles(domain)

        all_jobs = []
        seen_titles = set()
        salaries = []

        for role in job_roles:

            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "what": role,
                "results_per_page": 20
            }

            response = requests.get(
                url,
                params=params,
                timeout=10,
                headers={"User-Agent": "career-ai-agent"}
            )

            if response.status_code != 200:
                continue

            data = response.json()

            if "results" not in data:
                continue

            for job in data["results"]:

                title = job.get("title")

                # Remove duplicates
                if title in seen_titles:
                    continue
                seen_titles.add(title)

                salary_min = job.get("salary_min")
                salary_max = job.get("salary_max")

                if salary_min and salary_max:
                    salaries.append((salary_min + salary_max) / 2)

                all_jobs.append({
                    "title": title,
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name"),
                    "salary": salary_max,
                })

        if not all_jobs:
            return fallback_market_data(domain)

        avg_salary = round(sum(salaries) / len(salaries), 2) if salaries else None

        return {
            "domain": domain,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "job_count": len(all_jobs),
            "average_salary": avg_salary,
            "salary_samples": len(salaries),
            "hiring_trend": "growing" if len(all_jobs) > 25 else "stable",
            "jobs": all_jobs
        }

    except Exception as e:
        print("Market API Error:", e)
        return fallback_market_data(domain)


# ==============================
# 🟢 ASYNC VERSION (FastAPI)
# ==============================

async def async_get_market_data(domain, location="us"):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
        job_roles = map_domain_to_roles(domain)

        all_jobs = []
        seen_titles = set()
        salaries = []

        async with httpx.AsyncClient() as client:

            for role in job_roles:

                params = {
                    "app_id": ADZUNA_APP_ID,
                    "app_key": ADZUNA_APP_KEY,
                    "what": role,
                    "results_per_page": 20
                }

                response = await client.get(url, params=params, timeout=10)

                if response.status_code != 200:
                    continue

                data = response.json()

                if "results" not in data:
                    continue

                for job in data["results"]:

                    title = job.get("title")

                    if title in seen_titles:
                        continue
                    seen_titles.add(title)

                    salary_min = job.get("salary_min")
                    salary_max = job.get("salary_max")

                    if salary_min and salary_max:
                        salaries.append((salary_min + salary_max) / 2)

                    all_jobs.append({
                        "title": title,
                        "company": job.get("company", {}).get("display_name"),
                        "location": job.get("location", {}).get("display_name"),
                        "salary": salary_max,
                    })

        if not all_jobs:
            return fallback_market_data(domain)

        avg_salary = round(sum(salaries) / len(salaries), 2) if salaries else None

        return {
            "domain": domain,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "job_count": len(all_jobs),
            "average_salary": avg_salary,
            "salary_samples": len(salaries),
            "hiring_trend": "growing" if len(all_jobs) > 25 else "stable",
            "jobs": all_jobs
        }

    except Exception as e:
        print("Async Market API Error:", e)
        return fallback_market_data(domain)


# ==============================
# 📊 DEMAND SCORE
# ==============================

def calculate_demand_score(job_count):
    return min(round((job_count / 2000) * 100, 1), 100)


# ==============================
# ⚔️ COMPETITION SCORE
# ==============================

def calculate_competition_score(job_count):
    return max(100 - calculate_demand_score(job_count), 0)


# ==============================
# 🎯 OPPORTUNITY SCORE
# ==============================

def calculate_opportunity_score(demand, competition):
    return round(min(max((demand - competition) / 2 + 50, 0), 100), 1)