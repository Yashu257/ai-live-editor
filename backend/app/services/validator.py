"""
Validator Service module.
Validates code changes before applying to prevent system-breaking modifications.
Single Responsibility: Safety validation only.
"""

from typing import List, Dict, Any


# Critical files that should never be auto-modified
CRITICAL_FILES = [
    # Config files
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "config.json",
    "config.yaml",
    "config.yml",
    "settings.json",
    "package.json",
    "requirements.txt",
    "Pipfile",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    # Git files
    ".gitignore",
    ".gitattributes",
    # CI/CD
    ".github/workflows",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    # Database
    "migrations/",
    "schema.sql",
    # Security
    "secrets.json",
    "key.pem",
    "cert.pem",
]

# Validation limits
MAX_FILES_CHANGED = 10
MAX_LINES_REMOVED = 50
MAX_LINES_ADDED = 100


def validate_changes(changes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate code changes for safety before applying.
    
    Args:
        changes: List of change dictionaries with:
            - file: Path to file
            - before: Original code
            - after: New code
            
    Returns:
        Validation result:
            - status: "approved" or "rejected"
            - reason: Explanation if rejected
            - details: Validation details
            
    Safety Checks:
        1. Critical file protection
        2. Large deletion prevention
        3. File count limits
        4. Suspicious pattern detection
    """
    results = {
        "status": "approved",
        "reason": None,
        "details": {
            "files_checked": len(changes),
            "files_blocked": [],
            "warnings": []
        }
    }
    
    # Check 1: Limit number of files
    if len(changes) > MAX_FILES_CHANGED:
        results["status"] = "rejected"
        results["reason"] = f"Too many files changed ({len(changes)} > {MAX_FILES_CHANGED}). Review manually."
        results["details"]["warnings"].append(f"File count exceeds limit of {MAX_FILES_CHANGED}")
        return results
    
    # Check each change
    for change in changes:
        file_path = change.get("file", "")
        before_code = change.get("before", "")
        after_code = change.get("after", "")
        
        # Check 2: Critical file protection
        if _is_critical_file(file_path):
            results["status"] = "rejected"
            results["reason"] = f"Cannot auto-modify critical file: {file_path}"
            results["details"]["files_blocked"].append(file_path)
            results["details"]["warnings"].append(f"Critical file blocked: {file_path}")
            return results
        
        # Check 3: Large deletion detection
        before_lines = before_code.split('\n') if before_code else []
        after_lines = after_code.split('\n') if after_code else []
        
        lines_removed = len(before_lines) - len(after_lines)
        
        if lines_removed > MAX_LINES_REMOVED:
            results["status"] = "rejected"
            results["reason"] = f"Large code deletion detected in {file_path} ({lines_removed} lines). Review manually."
            results["details"]["warnings"].append(
                f"Large deletion in {file_path}: {lines_removed} lines"
            )
            return results
        
        # Check 4: Large addition warning (not blocking, just warning)
        lines_added = len(after_lines) - len(before_lines)
        if lines_added > MAX_LINES_ADDED:
            results["details"]["warnings"].append(
                f"Large addition in {file_path}: {lines_added} lines"
            )
        
        # Check 5: Suspicious patterns
        suspicious = _check_suspicious_patterns(before_code, after_code)
        if suspicious:
            results["status"] = "rejected"
            results["reason"] = f"Suspicious modification detected in {file_path}: {suspicious}"
            results["details"]["warnings"].append(f"Suspicious pattern in {file_path}")
            return results
    
    return results


def _is_critical_file(file_path: str) -> bool:
    """
    Check if file is in the critical files list.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is critical, False otherwise
    """
    # Normalize path for comparison
    normalized_path = file_path.lower().replace('\\', '/')
    
    for critical in CRITICAL_FILES:
        # Check for exact match or directory prefix
        critical_normalized = critical.lower().replace('\\', '/')
        
        if normalized_path.endswith(critical_normalized):
            return True
        
        # Check if file is in critical directory
        if critical_normalized.endswith('/') and normalized_path.startswith(critical_normalized):
            return True
    
    return False


def _check_suspicious_patterns(before: str, after: str) -> str:
    """
    Check for suspicious modification patterns.
    
    Args:
        before: Original code
        after: New code
        
    Returns:
        Description of suspicious pattern, or empty string if OK
    """
    after_lower = after.lower()
    
    # Dangerous patterns to check for
    dangerous_patterns = {
        "rm -rf": "Dangerous deletion command detected",
        "drop table": "Database table deletion detected",
        "delete from": "Database deletion detected",
        "os.system(": "System command execution detected",
        "subprocess.call(": "Subprocess execution detected",
        "eval(": "Code evaluation detected",
        "exec(": "Code execution detected",
        "__import__(": "Dynamic import detected",
        "password": "Password in code detected",
        "secret_key": "Secret key in code detected",
        "api_key": "API key in code detected",
    }
    
    for pattern, description in dangerous_patterns.items():
        if pattern in after_lower and pattern not in before.lower():
            return description
    
    return ""


def validate_with_override(changes: List[Dict[str, Any]], 
                            override: bool = False,
                            override_reason: str = "") -> Dict[str, Any]:
    """
    Validate changes with optional admin override.
    
    Args:
        changes: List of changes to validate
        override: If True, bypass validation (requires reason)
        override_reason: Required when override is True
        
    Returns:
        Validation result
    """
    # If override is requested, require reason
    if override:
        if not override_reason:
            return {
                "status": "rejected",
                "reason": "Override requested but no reason provided",
                "details": {"override_requested": True}
            }
        
        # Log the override for audit
        return {
            "status": "approved",
            "reason": f"Override approved: {override_reason}",
            "details": {
                "override": True,
                "override_reason": override_reason,
                "files_affected": len(changes)
            }
        }
    
    # Normal validation
    return validate_changes(changes)
