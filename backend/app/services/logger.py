"""
Logger Service module.
Centralized logging for all system operations.
Tracks errors, AI responses, fixes, and rollbacks for debugging and audit.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Default log file path
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "operations.json")


def log_event(event_type: str, data: Dict[str, Any], log_file: Optional[str] = None) -> bool:
    """
    Log an event to the operations log file.
    
    Args:
        event_type: Type of event (e.g., "error_input", "ai_response", "apply_fix", "rollback")
        data: Event data to log
        log_file: Optional custom log file path
        
    Returns:
        True if logged successfully, False otherwise
        
    Example:
        log_event("apply_fix", {
            "file": "src/api.js",
            "commit_hash": "abc123",
            "timestamp": "2024-01-15T10:30:00"
        })
    """
    try:
        # Use default or custom log file
        log_path = log_file or LOG_FILE_PATH
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        # Build log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        
        # Read existing logs or start new list
        logs = _read_logs(log_path)
        
        # Append new entry
        logs.append(log_entry)
        
        # Write back to file
        _write_logs(log_path, logs)
        
        return True
        
    except Exception as e:
        # Log to stderr if file logging fails
        import sys
        print(f"Logging failed: {str(e)}", file=sys.stderr)
        return False


def _read_logs(log_path: str) -> list:
    """
    Read existing logs from file.
    
    Args:
        log_path: Path to log file
        
    Returns:
        List of log entries (empty if file doesn't exist or is invalid)
    """
    if not os.path.exists(log_path):
        return []
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        # Return empty if file is corrupted
        return []
    except Exception:
        return []


def _write_logs(log_path: str, logs: list) -> None:
    """
    Write logs to file.
    
    Args:
        log_path: Path to log file
        logs: List of log entries to write
    """
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def get_logs(event_type: Optional[str] = None, limit: int = 100) -> list:
    """
    Retrieve logs from the log file.
    
    Args:
        event_type: Optional filter by event type
        limit: Maximum number of entries to return (default: 100)
        
    Returns:
        List of log entries, most recent first
    """
    try:
        logs = _read_logs(LOG_FILE_PATH)
        
        # Filter by type if specified
        if event_type:
            logs = [log for log in logs if log.get("type") == event_type]
        
        # Sort by timestamp (most recent first) and limit
        logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return logs[:limit]
        
    except Exception:
        return []


def get_logs_by_date(start_date: str, end_date: str) -> list:
    """
    Get logs within a date range.
    
    Args:
        start_date: Start date (ISO format: YYYY-MM-DD)
        end_date: End date (ISO format: YYYY-MM-DD)
        
    Returns:
        List of log entries within the date range
    """
    try:
        logs = _read_logs(LOG_FILE_PATH)
        
        filtered_logs = []
        for log in logs:
            timestamp = log.get("timestamp", "")
            if timestamp:
                # Extract date part (YYYY-MM-DD)
                log_date = timestamp[:10]
                if start_date <= log_date <= end_date:
                    filtered_logs.append(log)
        
        # Sort by timestamp (most recent first)
        filtered_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return filtered_logs
        
    except Exception:
        return []


# Convenience functions for specific event types

def log_error_input(error_message: str, source: str = "user") -> bool:
    """
    Log an error input from the user.
    
    Args:
        error_message: The error message submitted
        source: Source of the error (default: "user")
    """
    return log_event("error_input", {
        "error_message": error_message,
        "source": source
    })


def log_ai_response(prompt: str, response: Dict[str, Any], duration_ms: int = 0) -> bool:
    """
    Log an AI response.
    
    Args:
        prompt: The prompt sent to AI
        response: The AI response data
        duration_ms: Response time in milliseconds
    """
    return log_event("ai_response", {
        "prompt": prompt,
        "response": response,
        "duration_ms": duration_ms
    })


def log_apply_fix(changes: list, commit_hash: str = None, success: bool = True,
                  error_summary: str = None, error_message: str = None) -> bool:
    """
    Log an applied fix.
    
    Args:
        changes: List of changes applied
        commit_hash: Git commit hash
        success: Whether the operation succeeded
        error_summary: Summary of the error being fixed
        error_message: Error message if the operation failed
    """
    data = {
        "changes_count": len(changes),
        "changes": changes,
        "commit_hash": commit_hash,
        "success": success
    }
    if error_summary:
        data["error_summary"] = error_summary
    if error_message:
        data["error_message"] = error_message
    return log_event("apply_fix", data)


def log_rollback(reverted_commit: str, new_commit: str, reason: str = "") -> bool:
    """
    Log a rollback operation.
    
    Args:
        reverted_commit: Hash of the reverted commit
        new_commit: Hash of the revert commit
        reason: Optional reason for rollback
    """
    return log_event("rollback", {
        "reverted_commit": reverted_commit,
        "new_commit": new_commit,
        "reason": reason
    })
