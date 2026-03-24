from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import resume_routes, auth_routes
from .database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend API for AI-powered resume analysis and job matching",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database connection on startup
    """
    await connect_to_mongo()
    print("✓ Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Close database connection on shutdown
    """
    await close_mongo_connection()
    print("✓ Application shutdown complete")


app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(resume_routes.router, prefix="/api", tags=["Resume"])


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Resume Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
