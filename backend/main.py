from fastapi import FastAPI
from backend.routes import resume_routes, jd_routes, match_routes, ats_routes, report_routes

app = FastAPI(
    title="AI Resume Analyzer",
    description="Backend APIs for Resume Analysis",
    version="1.0"
)

# Register routes
app.include_router(resume_routes.router)
app.include_router(jd_routes.router)
app.include_router(match_routes.router)
app.include_router(ats_routes.router)
app.include_router(report_routes.router)

@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Backend Running"}