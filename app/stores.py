from pathlib import Path
from .guards import load_json_strict, validate_owner, DATA_ROOT

def load_bhaskar_resume() -> dict:
    resume = load_json_strict(DATA_ROOT / "resume.json")
    validate_owner(resume)
    return resume
