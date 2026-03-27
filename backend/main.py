from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from database import connect_to_mongo, close_mongo_connection
from routers import resume_routes, auth_routes, ats_routes, match_routes, jd_processor_api
from config import settings
from logger import get_logger

logger = get_logger(__name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["200/day", "50/hour"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    logger.info("Application startup complete")
    yield
    await close_mongo_connection()
    logger.info("Application shutdown complete")


app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend API for AI-powered resume analysis and job matching",
    version="1.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(resume_routes.router, prefix="/api", tags=["Resume"])
app.include_router(ats_routes.router, prefix="/api", tags=["ATS Scoring"])
app.include_router(match_routes.router, prefix="/api", tags=["Matching"])
app.include_router(jd_processor_api.router, prefix="/api", tags=["Job Description"])


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)