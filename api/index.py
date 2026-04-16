"""
FastAPI backend for Vercel Serverless.
This file serves as the entry point for all /api/* requests.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from any origin
# Required for frontend running on different domain to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domain in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Request model for the generate endpoint
class GenerateRequest(BaseModel):
    """Model for the generate request body."""
    prompt: str


@app.get("/")
async def root():
    """
    Health check endpoint.
    Returns a simple message to confirm backend is running.
    """
    return {"message": "Backend is running"}


@app.post("/api/generate")
async def generate(request: GenerateRequest):
    """
    Generate a React component based on the provided prompt.
    
    Args:
        request: GenerateRequest object containing the prompt
        
    Returns:
        JSON with component name and generated code
    """
    prompt = request.prompt
    
    # Return generated component response
    return {
        "component": "Hero.jsx",
        "code": f"<h1>Generated for {prompt}</h1>"
    }
