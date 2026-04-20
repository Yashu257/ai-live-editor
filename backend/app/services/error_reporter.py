"""
Error Reporter Service module.
Provides helper function for external systems to send errors to AI backend.
Single Responsibility: Client-side error reporting to AI service.
"""

import requests
from typing import Optional, Dict, Any


def send_error_to_ai(error_message: str, source: str = "server") -> Dict[str, Any]:
    """
    Send an error to the AI DevOps Assistant for analysis.
    
    This is a helper function designed for server-side code integration.
    It sends a POST request to the local AI backend and returns
    the AI-generated fix analysis.
    
    NO automatic git push or fix application - only returns analysis.
    
    Args:
        error_message: The error message or exception details
        source: Source identifier (default: "server")
                Examples: "server", "api", "stream", "worker"
    
    Returns:
        Dictionary with AI analysis:
            - status: "success" or "error"
            - summary: Brief error description
            - affected_files: List of likely affected files
            - changes: Suggested code changes
            - confidence: "high", "medium", or "low"
            - explanation: Why the fix works
    
    Example Usage:
        try:
            # Some server logic that might fail
            connect_database()
        except Exception as e:
            # Send error to AI for analysis
            result = send_error_to_ai(str(e), source="server")
            
            if result.get("status") == "success":
                print(f"AI Analysis: {result['summary']}")
                print(f"Confidence: {result['confidence']}")
                print(f"Suggested files: {result['affected_files']}")
            else:
                print(f"AI analysis failed: {result.get('message')}")
    
    Note:
        This function requires the AI backend to be running
        on http://127.0.0.1:8000
    """
    url = "http://127.0.0.1:8000/report-error/"
    
    payload = {
        "error": error_message,
        "source": source
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # 30 second timeout for AI processing
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "Cannot connect to AI backend. Is it running on port 8000?",
            "summary": None,
            "affected_files": [],
            "changes": [],
            "confidence": "low"
        }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "AI analysis timed out. Try again later.",
            "summary": None,
            "affected_files": [],
            "changes": [],
            "confidence": "low"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Request failed: {str(e)}",
            "summary": None,
            "affected_files": [],
            "changes": [],
            "confidence": "low"
        }


# Convenience function for common server error patterns
def report_exception(exception: Exception, source: str = "server") -> Dict[str, Any]:
    """
    Convenience wrapper to send an Exception object to AI.
    
    Args:
        exception: The exception instance to report
        source: Source identifier (default: "server")
    
    Returns:
        Same as send_error_to_ai()
    
    Example:
        try:
            process_data()
        except ValueError as e:
            result = report_exception(e, source="data-processor")
    """
    error_message = f"{type(exception).__name__}: {str(exception)}"
    return send_error_to_ai(error_message, source)
