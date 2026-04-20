"""
Main FastAPI application entry point.
Configures the app with CORS and includes all route modules.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.routes import generate, error_fix, scan, apply_fix, rollback, report_error

# Initialize FastAPI application
app = FastAPI(
    title="AI DevOps Assistant",
    description="AI-powered code generation and error fixing API",
    version="1.0.0"
)

# Configure CORS middleware
# Allows frontend to communicate with backend from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Include route modules
# Each module handles a specific domain (generation, error fixing, scanning, applying, rollback, error-reporting)
app.include_router(generate.router, prefix="/generate", tags=["code-generation"])
app.include_router(error_fix.router, prefix="/fix-error", tags=["error-fixing"])
app.include_router(scan.router, prefix="/scan-project", tags=["project-scan"])
app.include_router(apply_fix.router, prefix="/apply-fix", tags=["apply-fix"])
app.include_router(rollback.router, prefix="/rollback", tags=["rollback"])
app.include_router(report_error.router, tags=["error-reporting"])


@app.get("/")
async def health_check():
    """Root endpoint - health check."""
    return {"status": "running", "service": "AI DevOps Assistant"}
