from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from .models import JobJSON, AnalyzeResponse
from .guards import assert_project_scope, DATA_ROOT
from .stores import load_bhaskar_resume
from .llm import extract_job_signals, score_match

load_dotenv()
assert_project_scope()

app = FastAPI(title="Agent Bhaskar")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bhaskar AI Agent"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(job: JobJSON):
    if job.source != "bhaskar_chat":
        raise HTTPException(status_code=400, detail="Job must come from Bhaskar Chat scope.")
    resume = load_bhaskar_resume()
    your_skills = resume.get("skills", [])
    signals = extract_job_signals(job.description_text)
    score, gaps = score_match(signals["must_have"], your_skills)
    return AnalyzeResponse(
        must_have=signals["must_have"],
        nice_to_have=signals["nice_to_have"],
        keywords=signals["keywords"],
        red_flags=signals["red_flags"],
        score=score,
        gaps=gaps
    )

