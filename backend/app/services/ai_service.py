"""
AI Service module.
Handles AI-powered code generation and fix suggestions.
Single Responsibility: AI operations only.
"""

import re
from typing import Dict, List, Any


def generate_component(prompt: str) -> Dict[str, str]:
    """
    Generate a React component from a user prompt.
    
    Args:
        prompt: User description of desired component
        
    Returns:
        Dictionary with component name and generated code
    """
    # Determine component type from prompt
    component_type = _determine_component_type(prompt)
    
    # Generate component name
    component_name = _generate_component_name(prompt, component_type)
    
    # Generate code based on type
    code = _generate_code_by_type(prompt, component_type)
    
    return {
        "component": f"{component_name}.jsx",
        "code": code
    }


def suggest_fix(error_message: str, code_snippet: str = None, analysis: Dict = None) -> Dict[str, str]:
    """
    Suggest a fix for a code error.
    
    Args:
        error_message: The error message or exception
        code_snippet: Optional code that caused the error
        analysis: Analysis result from analyzer service
        
    Returns:
        Dictionary with fixed code and explanation
    """
    # Parse error type
    error_type = _parse_error_type(error_message)
    
    # Generate fix based on error type
    fix_result = _generate_fix(error_type, code_snippet, analysis)
    
    return fix_result


def generate_fix(error: str) -> dict:
    """
    Generate a structured fix for the given error.
    
    This function prepares an AI prompt and returns a structured response.
    Currently uses mock logic; ready for real AI integration.
    
    Prompt rules:
    - Fix ONLY the given error
    - Do NOT rewrite entire project
    - Maintain existing structure
    - Follow SOLID principles
    - Identify dependent functions if needed
    - Return clean structured JSON
    
    Args:
        error: The error message or stack trace
        
    Returns:
        Dictionary with summary, affected_files, changes, and confidence
        
    Example output:
        {
            "summary": "Import error: Missing module 'axios'",
            "affected_files": ["src/api/client.js"],
            "changes": [
                {
                    "file": "src/api/client.js",
                    "before": "import axios from 'axios';",
                    "after": "// npm install axios\\nimport axios from 'axios';"
                }
            ],
            "confidence": "high"
        }
    """
    # Prepare structured prompt for AI
    # In production, this would be sent to an AI service (OpenAI, Claude, etc.)
    ai_prompt = _build_error_fix_prompt(error)
    
    # Simulate AI response with structured mock data
    # Replace this with actual AI call when integrating
    mock_response = _simulate_ai_error_fix(error, ai_prompt)
    
    return mock_response


def _build_error_fix_prompt(error: str) -> str:
    """
    Build a structured prompt for the AI error fix service.
    
    Args:
        error: The error message to fix
        
    Returns:
        Formatted prompt string for AI
    """
    return f"""Fix the following error with minimal changes:

ERROR:
{error}

RULES:
1. Fix ONLY this specific error
2. Do NOT rewrite the entire project
3. Maintain existing code structure and style
4. Follow SOLID principles
5. Identify and update dependent functions if necessary
6. Return the response in the following JSON format:

{{
  "summary": "Brief description of the error and fix",
  "affected_files": ["path/to/file1.js", "path/to/file2.js"],
  "changes": [
    {{
      "file": "path/to/file.js",
      "before": "original code snippet",
      "after": "fixed code snippet"
    }}
  ],
  "confidence": "high" // or "medium" or "low"
}}

Provide the minimal fix that resolves the error while maintaining code quality."""


def _simulate_ai_error_fix(error: str, prompt: str) -> dict:
    """
    Intelligent error analysis with realistic fixes.
    Uses keyword-based rules to generate specific, production-quality responses.
    
    Args:
        error: The error message
        prompt: The AI prompt (for context)
        
    Returns:
        Structured fix response with summary, files, changes, confidence, explanation
    """
    error_lower = error.lower()
    
    # Database connection error - HIGH CONFIDENCE (clear pattern)
    if any(kw in error_lower for kw in ["database", "connection", "db", "sql", "postgres", "mysql"]):
        if "connection" in error_lower or "failed" in error_lower:
            return {
                "summary": "Database connection failure due to uninitialized connection or missing connection string.",
                "affected_files": ["database.py", "config.py"],
                "changes": [
                    {
                        "file": "database.py",
                        "before": "connection = None\n\ndef query(sql):\n    return connection.execute(sql)",
                        "after": "import os\nimport logging\nimport psycopg2\n\nlogger = logging.getLogger(__name__)\nDB_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/mydb')\n\ndef query(sql, params=None):\n    conn = None\n    cur = None\n    try:\n        conn = psycopg2.connect(DB_URI)\n        cur = conn.cursor()\n        cur.execute(sql, params or ())\n        conn.commit()\n        return cur.fetchall()\n    except psycopg2.Error as e:\n        logger.error(f'Database error: {e}')\n        raise\n    finally:\n        if cur:\n            cur.close()\n        if conn:\n            conn.close()"
                    }
                ],
                "confidence": "high",
                "explanation": "Creates a new connection per query with proper error handling and resource cleanup. Environment variable allows flexible deployment without code changes."
            }
        elif "timeout" in error_lower:
            return {
                "summary": "Database query timeout due to slow queries and missing connection management.",
                "affected_files": ["database.py"],
                "changes": [
                    {
                        "file": "database.py",
                        "before": "def query(sql):\n    return connection.execute(sql)",
                        "after": "import os\nimport logging\nimport psycopg2\n\nlogger = logging.getLogger(__name__)\nDB_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/mydb')\n\ndef query(sql, params=None, timeout=30):\n    conn = None\n    cur = None\n    try:\n        conn = psycopg2.connect(DB_URI, connect_timeout=timeout)\n        cur = conn.cursor()\n        cur.execute(sql, params or ())\n        conn.commit()\n        return cur.fetchall()\n    except psycopg2.Error as e:\n        logger.error(f'Database error: {e}')\n        raise\n    finally:\n        if cur:\n            cur.close()\n        if conn:\n            conn.close()"
                    }
                ],
                "confidence": "high",
                "explanation": "Adds connection timeout parameter to prevent hanging on slow queries. Proper resource cleanup prevents connection leaks."
            }
    
    # Authentication/Auth error - HIGH CONFIDENCE
    if any(kw in error_lower for kw in ["auth", "unauthorized", "401", "jwt", "token", "login"]):
        if "token" in error_lower or "jwt" in error_lower or "expired" in error_lower:
            return {
                "summary": "JWT token validation failure due to missing or expired token in request headers.",
                "affected_files": ["auth.py", "middleware/auth.py"],
                "changes": [
                    {
                        "file": "middleware/auth.py",
                        "before": "def authenticate(request):\n    return request.user",
                        "after": "import jwt\nfrom flask import request\n\nSECRET_KEY = os.getenv('JWT_SECRET')\n\ndef authenticate(request):\n    token = request.headers.get('Authorization', '').replace('Bearer ', '')\n    if not token:\n        raise Unauthorized('Missing token')\n    try:\n        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])\n        return payload\n    except jwt.ExpiredSignatureError:\n        raise Unauthorized('Token expired')"
                    }
                ],
                "confidence": "high",
                "explanation": "Proper JWT validation extracts the token from Authorization header and verifies signature and expiration."
            }
        else:
            return {
                "summary": "Authentication failure likely due to missing or invalid credentials validation.",
                "affected_files": ["auth.py", "services/user.py"],
                "changes": [
                    {
                        "file": "auth.py",
                        "before": "def login(username, password):\n    user = find_user(username)\n    return user",
                        "after": "import bcrypt\n\ndef login(username, password):\n    user = find_user(username)\n    if not user or not bcrypt.checkpw(password.encode(), user.password_hash):\n        raise Unauthorized('Invalid credentials')\n    return generate_token(user)"
                    }
                ],
                "confidence": "high",
                "explanation": "Adds secure password hashing comparison using bcrypt to prevent unauthorized access."
            }
    
    # API/Network/CORS error - MEDIUM-HIGH CONFIDENCE
    if any(kw in error_lower for kw in ["cors", "network", "fetch", "api", "axios", "request"]):
        if "cors" in error_lower:
            return {
                "summary": "CORS policy blocking cross-origin requests due to missing or restrictive origin configuration.",
                "affected_files": ["main.py", "middleware/cors.py"],
                "changes": [
                    {
                        "file": "main.py",
                        "before": "app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:3000'])",
                        "after": "from fastapi.middleware.cors import CORSMiddleware\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','),\n    allow_credentials=True,\n    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],\n    allow_headers=['Authorization', 'Content-Type']\n)"
                    }
                ],
                "confidence": "high",
                "explanation": "Configurable CORS origins via environment variable allows flexible deployment to different environments."
            }
        else:
            return {
                "summary": "API request failure due to missing error handling and retry logic.",
                "affected_files": ["services/api.js"],
                "changes": [
                    {
                        "file": "services/api.js",
                        "before": "const response = await fetch('/api/data');\nconst data = await response.json();",
                        "after": "async function fetchWithRetry(url, options = {}, retries = 3) {\n  for (let i = 0; i < retries; i++) {\n    try {\n      const response = await fetch(url, {\n        ...options,\n        headers: { 'Content-Type': 'application/json', ...options.headers }\n      });\n      if (!response.ok) throw new Error(`HTTP ${response.status}`);\n      return await response.json();\n    } catch (err) {\n      if (i === retries - 1) throw err;\n      await new Promise(r => setTimeout(r, 1000 * (i + 1)));\n    }\n  }\n}"
                    }
                ],
                "confidence": "medium",
                "explanation": "Retry logic with exponential backoff handles transient network failures gracefully."
            }
    
    # Import/Module error - HIGH CONFIDENCE
    if any(kw in error_lower for kw in ["import", "module", "cannot find", "no module named", "require"]):
        if "python" in error_lower or ".py" in error_lower:
            return {
                "summary": "Python module import failure due to missing dependency in requirements or incorrect module path.",
                "affected_files": ["requirements.txt"],
                "changes": [
                    {
                        "file": "requirements.txt",
                        "before": "# Dependencies",
                        "after": "# Dependencies\npsycopg2-binary==2.9.9\npython-dotenv==1.0.0"
                    }
                ],
                "confidence": "high",
                "explanation": "Missing dependencies must be declared in requirements.txt for proper environment setup."
            }
        else:
            return {
                "summary": "JavaScript module resolution failure due to missing npm package or incorrect import path.",
                "affected_files": ["package.json"],
                "changes": [
                    {
                        "file": "package.json",
                        "before": '{\n  "dependencies": {\n    "react": "^18.0.0"\n  }\n}',
                        "after": '{\n  "dependencies": {\n    "react": "^18.0.0",\n    "axios": "^1.6.0"\n  }\n}'
                    }
                ],
                "confidence": "high",
                "explanation": "Missing npm packages must be added to package.json and installed before import."
            }
    
    # Syntax error - HIGH CONFIDENCE
    if any(kw in error_lower for kw in ["syntax", "unexpected", "parse", "invalid syntax"]):
        return {
            "summary": "Syntax error due to malformed code structure - likely missing brackets, quotes, or punctuation.",
            "affected_files": ["app.py"],
            "changes": [
                {
                    "file": "app.py",
                    "before": "def process_data(data\n    return data.filter(lambda x: x.active)",
                    "after": "def process_data(data):\n    return data.filter(lambda x: x.active)"
                }
            ],
            "confidence": "high",
            "explanation": "Python function definitions require parentheses and colon: def name(params):"
        }
    
    # Undefined/Null/Type error - MEDIUM CONFIDENCE
    if any(kw in error_lower for kw in ["undefined", "cannot read", "typeerror", "null", "none"]):
        if "cannot read" in error_lower and "undefined" in error_lower:
            return {
                "summary": "Property access on undefined/null value without proper null checking.",
                "affected_files": ["components/UserCard.jsx"],
                "changes": [
                    {
                        "file": "components/UserCard.jsx",
                        "before": "const email = user.profile.contact.email;",
                        "after": "const email = user?.profile?.contact?.email ?? 'no-email@example.com';"
                    }
                ],
                "confidence": "high",
                "explanation": "Optional chaining (?.) prevents runtime errors when accessing nested properties on potentially null objects."
            }
        else:
            return {
                "summary": "Variable is undefined or null at point of use, indicating missing initialization or check.",
                "affected_files": ["utils/helpers.js"],
                "changes": [
                    {
                        "file": "utils/helpers.js",
                        "before": "function calculateTotal(items) {\n  return items.reduce((sum, item) => sum + item.price, 0);\n}",
                        "after": "function calculateTotal(items) {\n  if (!items || !Array.isArray(items)) return 0;\n  return items.reduce((sum, item) => sum + (item?.price || 0), 0);\n}"
                    }
                ],
                "confidence": "medium",
                "explanation": "Defensive programming checks for null/undefined before array operations and property access."
            }
    
    # Reference error - HIGH CONFIDENCE
    if any(kw in error_lower for kw in ["reference", "is not defined", "not defined", "nameerror"]):
        return {
            "summary": "Variable or function used before declaration or in wrong scope.",
            "affected_files": ["app.py"],
            "changes": [
                {
                    "file": "app.py",
                    "before": "result = process_data(data)\n\ndef process_data(items):\n    return [i * 2 for i in items]",
                    "after": "def process_data(items):\n    return [i * 2 for i in items]\n\nresult = process_data(data)"
                }
            ],
            "confidence": "high",
            "explanation": "Python requires functions to be defined before they are called. Functions must appear earlier in the file or be imported."
        }
    
    # File/Path error - MEDIUM CONFIDENCE
    if any(kw in error_lower for kw in ["file not found", "no such file", "enoent", "path", "permission"]):
        return {
            "summary": "File system operation failed due to missing file, incorrect path, or insufficient permissions.",
            "affected_files": ["utils/file_handler.py"],
            "changes": [
                {
                    "file": "utils/file_handler.py",
                    "before": "def read_config():\n    with open('config.json') as f:\n        return json.load(f)",
                    "after": "import os\n\ndef read_config():\n    config_path = os.getenv('CONFIG_PATH', 'config.json')\n    if not os.path.exists(config_path):\n        raise FileNotFoundError(f'Config not found: {config_path}')\n    with open(config_path) as f:\n        return json.load(f)"
                }
            ],
            "confidence": "medium",
            "explanation": "Path validation and environment-based configuration prevents hardcoded path failures."
        }
    
    # Memory/Performance error - MEDIUM CONFIDENCE
    if any(kw in error_lower for kw in ["memory", "out of memory", "oom", "performance", "slow"]):
        return {
            "summary": "Memory or performance issue due to inefficient data handling or resource leaks.",
            "affected_files": ["services/data_processor.py"],
            "changes": [
                {
                    "file": "services/data_processor.py",
                    "before": "def process_large_file(path):\n    data = open(path).read()\n    return data.split('\\n')",
                    "after": "def process_large_file(path, chunk_size=10000):\n    with open(path) as f:\n        while chunk := f.read(chunk_size):\n            yield chunk.split('\\n')"
                }
            ],
            "confidence": "medium",
            "explanation": "Streaming/chunked processing avoids loading entire files into memory, preventing OOM errors."
        }
    
    # Fallback - LOW CONFIDENCE (when no clear pattern matches)
    return {
        "summary": "Unable to determine specific root cause from error message. Review stack trace and application context.",
        "affected_files": ["app.py", "main.py"],
        "changes": [
            {
                "file": "app.py",
                "before": "def handle_request():\n    return process()",
                "after": "import logging\n\nlogger = logging.getLogger(__name__)\n\ndef handle_request():\n    try:\n        return process()\n    except Exception as e:\n        logger.exception('Request failed')\n        raise"
            }
        ],
        "confidence": "low",
        "explanation": "Adding comprehensive error logging will help identify the root cause of future failures."
    }


def _determine_component_type(prompt: str) -> str:
    """Determine component type from prompt keywords."""
    prompt_lower = prompt.lower()
    
    type_keywords = {
        "hero": ["hero", "banner", "landing", "header section"],
        "navbar": ["nav", "navbar", "navigation", "menu", "header"],
        "footer": ["footer", "bottom", "copyright"],
        "form": ["form", "input", "login", "signup", "contact"],
        "card": ["card", "product", "item", "preview"],
        "button": ["button", "cta", "action", "click"],
    }
    
    for comp_type, keywords in type_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            return comp_type
    
    return "component"


def _generate_component_name(prompt: str, component_type: str) -> str:
    """Generate a PascalCase component name."""
    # Extract key words from prompt
    words = re.findall(r'\b[A-Za-z]+\b', prompt)
    
    if words:
        # Use first meaningful word + type
        name = words[0].capitalize() + component_type.capitalize()
    else:
        name = component_type.capitalize()
    
    return name


def _generate_code_by_type(prompt: str, component_type: str) -> str:
    """Generate component code based on type."""
    
    templates = {
        "hero": '''import React from 'react';

export default function Hero() {
  return (
    <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">{title}</h1>
        <p className="text-xl text-blue-100">{description}</p>
      </div>
    </section>
  );
}''',
        "navbar": '''import React from 'react';

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <span className="text-xl font-bold text-blue-600">Brand</span>
          <div className="space-x-4">
            <a href="#" className="text-gray-600 hover:text-blue-600">Home</a>
            <a href="#" className="text-gray-600 hover:text-blue-600">About</a>
          </div>
        </div>
      </div>
    </nav>
  );
}''',
        "footer": '''import React from 'react';

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 py-6">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p className="text-sm">Built with React</p>
      </div>
    </footer>
  );
}''',
        "form": '''import React, { useState } from 'react';

export default function Form() {
  const [input, setInput] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', input);
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="border p-2 rounded"
        placeholder="Enter text..."
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        Submit
      </button>
    </form>
  );
}''',
    }
    
    # Get template or default
    code = templates.get(component_type, templates["hero"])
    
    # Customize with prompt content
    code = code.replace("{title}", prompt[:30] if len(prompt) > 30 else prompt)
    code = code.replace("{description}", f"Generated for: {prompt}")
    
    return code


def _parse_error_type(error_message: str) -> str:
    """Parse the error type from error message."""
    error_patterns = {
        "syntax": ["syntax", "parse", "unexpected token"],
        "import": ["import", "module", "cannot find"],
        "type": ["type", "undefined", "null", "cannot read"],
        "reference": ["reference", "is not defined", "not defined"],
        "network": ["network", "fetch", "cors", "connection"],
    }
    
    error_lower = error_message.lower()
    
    for error_type, patterns in error_patterns.items():
        if any(pattern in error_lower for pattern in patterns):
            return error_type
    
    return "general"


def _generate_fix(error_type: str, code_snippet: str, analysis: Dict) -> Dict[str, str]:
    """Generate a fix based on error type."""
    
    fixes = {
        "syntax": {
            "code": "// Fix: Check for missing brackets, semicolons, or quotes\\n{original}",
            "explanation": "Syntax error detected. Check for missing punctuation or brackets."
        },
        "import": {
            "code": "// Fix: Ensure module is installed and path is correct\\nimport Module from 'correct-path';",
            "explanation": "Import error. Verify the module is installed and import path is correct."
        },
        "type": {
            "code": "// Fix: Add null check before accessing property\\nif (value) {\\n  // access property here\\n}",
            "explanation": "Type error. Add null/undefined checks before accessing properties."
        },
        "reference": {
            "code": "// Fix: Define variable before use\\nconst variableName = value;",
            "explanation": "Reference error. Variable used before declaration. Define it first."
        },
        "network": {
            "code": "// Fix: Add error handling for fetch\\ntry {\\n  const res = await fetch(url);\\n} catch (e) {\\n  console.error(e);\\n}",
            "explanation": "Network error. Add try-catch and check CORS settings."
        },
        "general": {
            "code": "// Review error message and stack trace for details",
            "explanation": "Review the error message and stack trace to identify the issue."
        }
    }
    
    result = fixes.get(error_type, fixes["general"])
    
    if code_snippet:
        result["code"] = result["code"].replace("{original}", code_snippet)
    
    return result
