import datetime

def fetch_events():

    # later replace with APIs
    # (Google events, govt exam API, hackathon APIs)

    return [
        {
            "title":"GATE Exam",
            "date":"2026-09-25",
            "tags":["engineering","exam"]
        },
        {
            "title":"Smart India Hackathon",
            "date":"2026-03-12",
            "tags":["engineering","hackathon","coding"]
        },
        {
            "title":"Medical Research Fellowship",
            "date":"2026-04-10",
            "tags":["medical","research"]
        }
    ]


def upcoming(events):

    today = datetime.date.today()

    valid = []

    for e in events:
        d = datetime.date.fromisoformat(e["date"])
        if d >= today:
            valid.append(e)

    return valid