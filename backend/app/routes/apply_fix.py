"""
Apply Fix route module.
Provides POST /apply-fix endpoint for applying approved fixes to the codebase.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.services.git_service import apply_fix

# Create router for apply fix endpoint
router = APIRouter()


class Change(BaseModel):
    """
    Represents a single code change to apply.
    
    Fields:
        file: Path to the file being modified
        before: Original code snippet to find
        after: Replacement code snippet
    """
    file: str
    before: str
    after: str


class ApplyFixRequest(BaseModel):
    """
    Request model for applying fixes.
    
    Fields:
        changes: List of changes to apply
        error_summary: Optional summary of the error for commit message
    """
    changes: List[Change]
    error_summary: str = None


class ApplyFixResponse(BaseModel):
    """
    Response model for apply fix endpoint.
    
    Fields:
        status: "success" or "error"
        message: Human-readable result message
        commit_hash: Optional commit hash if successful
        commit_message: The commit message used for the fix
        modified_files: Optional list of modified files
    """
    status: str
    message: str
    commit_hash: str = None
    commit_message: str = None
    modified_files: List[str] = []


@router.post("/", response_model=ApplyFixResponse)
async def apply_fix_endpoint(request: ApplyFixRequest):
    """
    Apply approved fixes to the codebase and push to repository.
    
    Endpoint: POST /apply-fix
    
    Args:
        request: ApplyFixRequest containing list of changes
        
    Returns:
        ApplyFixResponse with status and details
        
    Raises:
        HTTPException: If git operations fail
        
    Example:
        {
          "changes": [
            {
              "file": "src/api.js",
              "before": "import axios from 'axios';",
              "after": "// npm install axios\\nimport axios from 'axios';"
            }
          ]
        }
    """
    try:
        # Convert Pydantic models to dicts for git_service
        changes = [change.dict() for change in request.changes]
        
        # Call git service to apply fixes with error summary for commit message
        result = apply_fix(changes, error_summary=request.error_summary)
        
        if result["success"]:
            return ApplyFixResponse(
                status="success",
                message="Fix applied and pushed to GitHub",
                commit_hash=result.get("commit_hash"),
                commit_message=result.get("commit_message"),
                modified_files=result.get("modified_files", [])
            )
        else:
            # Return error without raising HTTPException
            # (still 200 OK, but status indicates failure)
            return ApplyFixResponse(
                status="error",
                message="Git push failed: " + result["message"],
                modified_files=result.get("modified_files", [])
            )
            
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to apply fix: {str(e)}"
        )
