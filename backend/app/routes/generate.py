"""
Code generation route module.
Handles endpoints for generating React components from prompts.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ai_service import generate_component

# Create router for generation endpoints
router = APIRouter()


class GenerateRequest(BaseModel):
    """Request model for code generation."""
    prompt: str


class GenerateResponse(BaseModel):
    """Response model for code generation."""
    component: str
    code: str


@router.post("/", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """
    Generate a React component based on user prompt.
    
    Args:
        request: GenerateRequest containing the prompt
        
    Returns:
        GenerateResponse with component name and generated code
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        result = generate_component(request.prompt)
        return GenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
