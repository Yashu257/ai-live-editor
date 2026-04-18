"""
Analyzer Service module.
Analyzes errors to identify affected files and dependencies.
Single Responsibility: Error analysis only.
"""

import re
from typing import Dict, List, Any, Optional


def analyze_error(
    error_message: str,
    code_snippet: Optional[str] = None,
    file_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze an error and identify affected files/functions.
    
    Args:
        error_message: The error message or stack trace
        code_snippet: Optional code that caused the error
        file_path: Optional path to the file with error
        
    Returns:
        Analysis result with description and affected files list
    """
    # Extract file paths from error message
    extracted_files = _extract_file_paths(error_message)
    
    # Identify affected functions
    affected_functions = _identify_functions(error_message, code_snippet)
    
    # Build affected files list
    affected_files = _build_affected_files(
        extracted_files=extracted_files,
        affected_functions=affected_functions,
        provided_file=file_path
    )
    
    # Generate analysis description
    description = _generate_description(error_message, affected_files)
    
    return {
        "description": description,
        "affected_files": affected_files,
        "error_type": _classify_error(error_message),
        "severity": _determine_severity(error_message)
    }


def _extract_file_paths(error_message: str) -> List[str]:
    """Extract file paths from error message or stack trace."""
    # Pattern to match common file path formats
    # Matches: /path/to/file.js, C:\path\file.js, ./relative/path.jsx
    file_pattern = r'(?:[\w]:)?[\\/][\w\-_.\/\\]+\.(js|jsx|ts|tsx|py)'
    
    matches = re.findall(file_pattern, error_message, re.IGNORECASE)
    
    # Also look for full paths
    full_path_pattern = r'File "([^"]+)"'
    full_paths = re.findall(full_path_pattern, error_message)
    
    return list(set(matches + full_paths))


def _identify_functions(error_message: str, code_snippet: Optional[str]) -> List[Dict[str, Any]]:
    """Identify affected functions from error and code."""
    functions = []
    
    # Extract function names from error message
    func_pattern = r'in\s+(\w+)\s*\(|at\s+(\w+)\s*\(|function\s+(\w+)'
    func_matches = re.findall(func_pattern, error_message)
    
    # Flatten tuple results
    func_names = [f for match in func_matches for f in match if f]
    
    for func_name in func_names:
        functions.append({
            "name": func_name,
            "line": None  # Will be populated if available
        })
    
    # If code snippet provided, try to find line numbers
    if code_snippet:
        line_info = _find_function_in_code(code_snippet, func_names)
        functions = line_info
    
    return functions


def _find_function_in_code(code: str, function_names: List[str]) -> List[Dict[str, Any]]:
    """Find function definitions in code and their line numbers."""
    functions = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        for func_name in function_names:
            # Match function definitions
            pattern = rf'(?:function|def|const|let|var)\s+{re.escape(func_name)}\s*[\(=]'
            if re.search(pattern, line):
                functions.append({
                    "name": func_name,
                    "line": i
                })
    
    return functions


def _build_affected_files(
    extracted_files: List[str],
    affected_functions: List[Dict],
    provided_file: Optional[str]
) -> List[Dict[str, Any]]:
    """Build the list of affected files with metadata."""
    files = []
    
    # Use provided file if available
    if provided_file:
        files.append({
            "file": provided_file,
            "function": affected_functions[0]["name"] if affected_functions else None,
            "line_number": affected_functions[0].get("line") if affected_functions else None
        })
    
    # Add extracted files
    for file_path in extracted_files:
        if file_path not in [f["file"] for f in files]:
            files.append({
                "file": file_path,
                "function": None,
                "line_number": None
            })
    
    # If no files found, add placeholder
    if not files:
        files.append({
            "file": "unknown",
            "function": affected_functions[0]["name"] if affected_functions else None,
            "line_number": None
        })
    
    return files


def _generate_description(error_message: str, affected_files: List[Dict]) -> str:
    """Generate a human-readable analysis description."""
    error_type = _classify_error(error_message)
    
    file_count = len(affected_files)
    file_list = ", ".join([f["file"] for f in affected_files[:3]])
    
    descriptions = {
        "syntax": f"Syntax error detected in {file_count} file(s): {file_list}. Check for missing punctuation.",
        "import": f"Import/module error in {file_count} file(s): {file_list}. Verify dependencies.",
        "type": f"Type error in {file_count} file(s): {file_list}. Check variable types.",
        "reference": f"Reference error in {file_count} file(s): {file_list}. Variable not defined.",
        "network": f"Network error detected. Check API endpoints and CORS settings.",
        "general": f"Error detected in {file_count} file(s): {file_list}. Review error message."
    }
    
    return descriptions.get(error_type, descriptions["general"])


def _classify_error(error_message: str) -> str:
    """Classify the error type from the message."""
    error_patterns = {
        "syntax": ["syntax", "parse", "unexpected token", "invalid syntax"],
        "import": ["import", "module", "cannot find", "no module named"],
        "type": ["type", "undefined", "null", "cannot read", "attribute"],
        "reference": ["reference", "is not defined", "not defined", "nameerror"],
        "network": ["network", "fetch", "cors", "connection", "timeout"],
    }
    
    error_lower = error_message.lower()
    
    for error_type, patterns in error_patterns.items():
        if any(pattern in error_lower for pattern in patterns):
            return error_type
    
    return "general"


def _determine_severity(error_message: str) -> str:
    """Determine error severity level."""
    critical_keywords = ["fatal", "crash", "out of memory", "stack overflow"]
    warning_keywords = ["warning", "deprecation", "deprecated"]
    
    error_lower = error_message.lower()
    
    if any(keyword in error_lower for keyword in critical_keywords):
        return "critical"
    elif any(keyword in error_lower for keyword in warning_keywords):
        return "warning"
    
    return "error"


def analyze_dependencies(error: str) -> list:
    """
    Analyze error and identify affected files using rule-based detection.
    
    Maps error keywords to relevant files based on domain logic.
    Returns only files relevant to the error context.
    
    Args:
        error: The error message to analyze
        
    Returns:
        List of file paths that might be affected
        
    Example:
        Input: "database connection failed"
        Output: ["database.py", "config.py", "connection.py"]
    """
    error_lower = error.lower()
    
    # Define keyword-to-files mapping with logical domain grouping
    # Files are ordered by relevance (primary first, dependents second)
    domain_rules = {
        # Database errors - prioritize DB and config files
        ("database", "db", "sql", "postgres", "mysql", "query", "connection", "pool"): [
            "database.py", "db.py", "config.py", "connection.py"
        ],
        
        # Authentication errors - auth system files
        ("auth", "authentication", "login", "logout", "password", "credential", 
         "jwt", "token", "session", "unauthorized", "401", "forbidden", "403"): [
            "auth.py", "authentication.py", "middleware/auth.py", 
            "services/user.py", "models/user.py"
        ],
        
        # API/Network errors - API layer and HTTP handling
        ("api", "endpoint", "route", "request", "response", "fetch", 
         "axios", "http", "cors", "network", "timeout", "503", "502"): [
            "api.py", "routes/api.py", "services/api.py", 
            "utils/http.py", "middleware/cors.py", "main.py"
        ],
        
        # Frontend/Component errors
        ("react", "component", "render", "dom", "jsx", "tsx", 
         "frontend", "ui", "view", "template"): [
            "App.jsx", "components/", "pages/", "hooks/", "utils/frontend.js"
        ],
        
        # Import/Module errors - dependency management
        ("import", "module", "require", "cannot find module", 
         "no module named", "package", "dependency"): [
            "requirements.txt", "package.json", "setup.py", "pyproject.toml"
        ],
        
        # File system errors
        ("file not found", "enoent", "path", "directory", 
         "file system", "permission", "access"): [
            "utils/file.py", "services/storage.py", "config.py"
        ],
        
        # Memory/Performance errors
        ("memory", "oom", "out of memory", "performance", 
         "slow", "timeout", "leak"): [
            "services/data_processor.py", "utils/performance.py", "cache.py"
        ],
        
        # Syntax/Compilation errors - likely in the main code
        ("syntax", "parse", "invalid syntax", "compilation", "compile"): [
            "app.py", "main.py", "index.js"  # Entry points most likely
        ],
    }
    
    # Collect files from matching rules
    affected_files = []
    matched_keywords = []
    
    for keywords, files in domain_rules.items():
        # Check if any keyword in this group matches
        if any(kw in error_lower for kw in keywords):
            affected_files.extend(files)
            matched_keywords.extend([kw for kw in keywords if kw in error_lower])
    
    # Remove duplicates while preserving order (most relevant first)
    seen = set()
    unique_files = []
    for f in affected_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)
    
    # If no matches found, extract any file paths mentioned in error
    if not unique_files:
        extracted = _extract_file_paths(error)
        if extracted:
            return extracted
        # Last resort: return common entry points but log this
        return ["main.py", "app.py"]
    
    return unique_files
