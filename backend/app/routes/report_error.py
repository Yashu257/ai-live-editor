"""
Error Reporting API module.
Provides endpoint for external systems to report errors for AI analysis.
"""

from fastapi import APIRouter, Request
from app.services.ai_service import generate_fix

router = APIRouter(prefix="/api")


@router.post("/report-error")
async def report_error(request: Request):
    """
    Report an error for AI analysis.
    Endpoint: POST /api/report-error
    """
    data = await request.json()
    error = data.get("error", "Unknown error")

    print("Received error:", error)

    # Call AI logic
    result = generate_fix(error)

    return result
