import re
from typing import Dict, List, Tuple
from .guards import forbid_other_identities

def extract_job_signals(job_text: str) -> Dict[str, List[str]]:
    words = re.findall(r"[A-Za-z\+\#\.]+", job_text)
    lower = [w.lower() for w in words]
    must = sorted({w for w in lower if w in {
        "python","sql","docker","kubernetes","airflow","aws","azure","gcp",
        "playwright","selenium","pytest","ci","cd","etl","dbt"
    }})
    nice = sorted({w for w in lower if w in {"fastapi","pandas","numpy","git","linux","terraform"}} - set(must))
    keywords = sorted(set(lower))[:20]
    red = []
    if "citizenship" in lower or "clearance" in lower:
        red.append("Citizenship/Clearance requirement")
    return {"must_have": list(must), "nice_to_have": list(nice), "keywords": keywords, "red_flags": red}

def score_match(must_have: List[str], your_skills: List[str]) -> Tuple[float, List[str]]:
    ys = {s.lower() for s in your_skills}
    covered = [s for s in must_have if s.lower() in ys]
    gaps = [s for s in must_have if s.lower() not in ys]
    score = (len(covered) / max(1, len(must_have))) * 100.0
    return round(score, 1), gaps

def safe_text(text: str) -> str:
    forbid_other_identities(text)
    return text
