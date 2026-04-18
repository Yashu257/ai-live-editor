"""
Project scan route module.
Provides POST /scan-project endpoint for detecting project-wide issues.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Create router for scan endpoints
router = APIRouter()


class ScanRequest(BaseModel):
    """
    Request model for project scan.
    
    Fields:
        error_context: Optional error message to focus scan
    """
    error_context: str = ""


class Issue(BaseModel):
    """
    Represents a detected issue in the project.
    
    Fields:
        file: Path to the affected file
        problem: Description of the issue
    """
    file: str
    problem: str


class ScanResponse(BaseModel):
    """
    Response model for project scan.
    
    Fields:
        issues: List of detected issues
    """
    issues: List[Issue]


def _mock_project_scan(error_context: str) -> List[Issue]:
    """
    Mock project scan logic.
    In production, replace with actual AST parsing and dependency analysis.
    
    Args:
        error_context: Error message to focus scan on
        
    Returns:
        List of detected issues
    """
    error_lower = error_context.lower()
    
    # Database-related error context
    if "database" in error_lower or "db" in error_lower or "connection" in error_lower:
        return [
            Issue(
                file="src/services/auth.js",
                problem="Depends on outdated DB connection function"
            ),
            Issue(
                file="src/models/user.js",
                problem="Uses deprecated query method"
            ),
            Issue(
                file="src/middleware/session.js",
                problem="References database pool that may be closed"
            )
        ]
    
    # Import/module-related error context
    if "import" in error_lower or "module" in error_lower:
        return [
            Issue(
                file="src/components/Header.jsx",
                problem="Imports missing utility function"
            ),
            Issue(
                file="src/pages/Dashboard.jsx",
                problem="Circular dependency with auth module"
            )
        ]
    
    # Auth-related error context
    if "auth" in error_lower or "login" in error_lower or "token" in error_lower:
        return [
            Issue(
                file="src/routes/private.js",
                problem="Uses deprecated auth middleware"
            ),
            Issue(
                file="src/services/api.js",
                problem="Token refresh logic may fail silently"
            ),
            Issue(
                file="src/components/ProtectedRoute.jsx",
                problem="Depends on auth state that resets on refresh"
            )
        ]
    
    # Default scan results
    return [
        Issue(
            file="src/utils/helpers.js",
            problem="Contains deprecated utility functions"
        ),
        Issue(
            file="src/config/settings.js",
            problem="Missing environment variable validation"
        )
    ]


@router.post("/", response_model=ScanResponse)
async def scan_project(request: ScanRequest):
    """
    Scan entire project for related issues and risks.
    
    Endpoint: POST /scan-project
    
    Args:
        request: ScanRequest with optional error context
        
    Returns:
        ScanResponse with list of detected issues
        
    Raises:
        HTTPException: If scan fails
        
    Example:
        {
          "error_context": "database connection failed"
        }
    """
    try:
        # Perform project scan (mock for now)
        issues = _mock_project_scan(request.error_context)
        
        return ScanResponse(issues=issues)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Project scan failed: {str(e)}"
        )
