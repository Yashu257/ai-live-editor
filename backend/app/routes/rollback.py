"""
Rollback route module.
Provides POST /rollback endpoint for reverting last AI fix.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.git_service import rollback_last_commit

# Create router for rollback endpoint
router = APIRouter()


class RollbackRequest(BaseModel):
    """
    Request model for rollback.
    
    Fields:
        confirmed: Must be True to proceed (safety check)
    """
    confirmed: bool = False


class RollbackResponse(BaseModel):
    """
    Response model for rollback endpoint.
    
    Fields:
        status: "success" or "error"
        message: Human-readable result message
        reverted_commit: Optional hash of reverted commit
        new_commit: Optional hash of revert commit
    """
    status: str
    message: str
    reverted_commit: str = None
    new_commit: str = None


@router.post("/", response_model=RollbackResponse)
async def rollback(request: RollbackRequest):
    """
    Rollback the last commit (AI fix recovery).
    
    Endpoint: POST /rollback
    
    Args:
        request: RollbackRequest with confirmation flag
        
    Returns:
        RollbackResponse with status and details
        
    Raises:
        HTTPException: If rollback fails
        
    Example:
        {
          "confirmed": true
        }
    
    Safety:
        - Requires explicit confirmation (confirmed=True)
        - Logs all rollback actions to .rollback-log
        - Creates revert commit (safer than reset)
    """
    try:
        # Call git service to rollback
        result = rollback_last_commit(confirmed=request.confirmed)
        
        if result["success"]:
            return RollbackResponse(
                status="success",
                message=result["message"],
                reverted_commit=result.get("reverted_commit"),
                new_commit=result.get("new_commit")
            )
        else:
            # Return error without raising HTTPException for known issues
            return RollbackResponse(
                status="error",
                message=result["message"]
            )
            
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Rollback failed: {str(e)}"
        )
