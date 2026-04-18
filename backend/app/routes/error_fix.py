"""
Error fixing route module.
Provides POST /fix-error endpoint for analyzing and fixing code errors.
Uses AI service for generating structured fixes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.services.ai_service import generate_fix

# Create router for error fixing endpoints
router = APIRouter()


class ErrorFixRequest(BaseModel):
    """
    Request model for error fixing.
    
    Fields:
        error: The error message or stack trace to analyze
    """
    error: str


class Change(BaseModel):
    """
    Represents a single code change.
    
    Fields:
        file: Path to the file being modified
        before: Original code snippet
        after: Fixed code snippet
    """
    file: str
    before: str
    after: str


class ErrorFixResponse(BaseModel):
    """
    Response model for error fixing.
    
    Fields:
        summary: Brief description of the error and fix
        affected_files: List of file paths that need changes
        changes: Array of specific code changes
        confidence: Confidence level of the fix (high/medium/low)
    """
    summary: str
    affected_files: List[str]
    changes: List[Change]
    confidence: str


@router.post("/", response_model=ErrorFixResponse)
async def fix_error(request: ErrorFixRequest):
    """
    Analyze an error and return structured fix suggestions.
    
    Endpoint: POST /fix-error
    
    Args:
        request: ErrorFixRequest containing the error message
        
    Returns:
        ErrorFixResponse with summary, affected files, and suggested changes
        
    Raises:
        HTTPException: If processing fails
        
    Example:
        {
          "error": "Cannot find module '../utils/helpers'"
        }
    """
    try:
        # Use AI service to generate structured fix
        result = generate_fix(request.error)
        
        # Convert changes to Change models
        changes = [
            Change(**change) for change in result["changes"]
        ]
        
        return ErrorFixResponse(
            summary=result["summary"],
            affected_files=result["affected_files"],
            changes=changes,
            confidence=result["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )
