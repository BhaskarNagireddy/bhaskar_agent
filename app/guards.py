import os, json, re
from pathlib import Path

PROFILE = os.getenv("PROFILE", "bhaskar")
DATA_ROOT = Path(os.getenv("DATA_ROOT", "./data/bhaskar")).resolve()
ALLOW_EXTERNAL = os.getenv("ALLOW_EXTERNAL_IO","false").lower()=="true"

CANONICAL_NAME = "Bhaskar Satyendra Kumar Nagireddy"

def assert_project_scope() -> None:
    if DATA_ROOT.name != "bhaskar":
        raise RuntimeError("Data root must be /data/bhaskar (Bhaskar scope only).")
    if not ALLOW_EXTERNAL:
        os.environ["NO_NETWORK"] = "1"

def load_json_strict(path: Path):
    path = path.resolve()
    if DATA_ROOT not in path.parents and path != DATA_ROOT:
        raise PermissionError("Forbidden: outside Bhaskar data scope.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_owner(resume: dict) -> None:
    if resume.get("owner_id") != "bhaskar":
        raise ValueError("Resume owner must be 'bhaskar'.")
    name = resume.get("basics", {}).get("name", "")
    if name != CANONICAL_NAME:
        raise ValueError("Resume name must match Bhaskar’s canonical name.")

BANNED_PATTERNS = [r"\bNarayana\b", r"\bCleveland State University\b.*TA"]

def forbid_other_identities(text: str) -> None:
    for pat in BANNED_PATTERNS:
        if re.search(pat, text, re.I):
            raise ValueError("Detected non-Bhaskar identity data in output. Blocked.")
