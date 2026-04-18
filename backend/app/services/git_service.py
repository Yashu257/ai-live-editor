"""
Git Service module.
Handles applying approved fixes to the codebase and managing git operations.
Single Responsibility: File modifications and version control.
"""

import subprocess
import os
from typing import List, Dict, Optional

from app.services.validator import validate_changes
from app.services.logger import log_event, log_apply_fix


def push_changes(commit_message: str, repo_path: str = ".") -> Dict:
    """
    Push changes to remote repository with safety checks.
    
    Executes:
        git add .
        git commit -m "<commit_message>"
        git push origin <current_branch>
    
    Args:
        commit_message: Message for the git commit
        repo_path: Path to the git repository (default: current directory)
        
    Returns:
        Dictionary with operation results:
            - success: bool
            - message: str
            - commit_hash: str (if successful)
            - status: str
            
    Safety:
        - Checks for uncommitted changes before committing
        - Prevents empty commits
        - Logs all operations
        - Handles errors gracefully
    """
    result = {
        "success": False,
        "message": "",
        "commit_hash": None,
        "status": "pending"
    }
    
    try:
        # Safety check: Ensure there are changes to commit
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        if not status_result.stdout.strip():
            # No changes to commit
            result["status"] = "no_changes"
            result["message"] = "No changes to commit"
            log_event("git_push", {
                "status": "no_changes",
                "commit_message": commit_message,
                "reason": "Working directory clean"
            })
            return result
        
        # Stage all changes
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Create commit
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Get commit hash
        hash_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        commit_hash = hash_result.stdout.strip()
        result["commit_hash"] = commit_hash
        
        # Push to remote
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        branch = branch_result.stdout.strip()
        
        subprocess.run(
            ["git", "push", "origin", branch],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Success
        result["success"] = True
        result["status"] = "success"
        result["message"] = f"Successfully pushed to {branch}: {commit_hash[:7]}"
        
        # Log the push
        log_event("git_push", {
            "status": "success",
            "commit_message": commit_message,
            "commit_hash": commit_hash,
            "branch": branch
        })
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Git operation failed: {e.stderr}"
        result["status"] = "error"
        result["message"] = error_msg
        
        # Log the failure
        log_event("git_push", {
            "status": "error",
            "commit_message": commit_message,
            "error": error_msg
        })
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        result["status"] = "error"
        result["message"] = error_msg
        
        # Log the failure
        log_event("git_push", {
            "status": "error",
            "commit_message": commit_message,
            "error": error_msg
        })
    
    return result


def _has_changes_to_commit(repo_path: str = ".") -> bool:
    """
    Check if there are uncommitted changes in the repository.
    
    Args:
        repo_path: Repository root path
        
    Returns:
        True if there are changes to commit, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def apply_fix(changes: List[Dict[str, str]], 
              error_summary: Optional[str] = None,
              repo_path: str = ".") -> Dict:
    """
    Apply approved fixes to files and commit to git.
    
    Args:
        changes: List of change dictionaries with keys:
            - file: Path to the file
            - before: Original code to find
            - after: Replacement code
        repo_path: Path to the git repository (default: current directory)
        
    Returns:
        Dictionary with operation results:
            - success: bool
            - modified_files: List of modified file paths
            - commit_hash: str (if successful)
            - message: str
            
    Safety:
        - Only modifies files listed in changes
        - Validates file exists before modification
        - Creates commit only if changes are applied
        - Validates changes for safety before applying
    """
    results = {
        "success": False,
        "modified_files": [],
        "commit_hash": None,
        "message": ""
    }
    
    try:
        # Step 1: Validate changes for safety
        validation = validate_changes(changes)
        
        if validation["status"] == "rejected":
            results["message"] = f"Validation failed: {validation['reason']}"
            results["validation_details"] = validation.get("details", {})
            return results
        
        # Step 2: Apply file modifications
        modified = _apply_file_changes(changes, repo_path)
        
        if not modified:
            results["message"] = "No files were modified"
            return results
            
        results["modified_files"] = modified
        
        # Step 3: Stage modified files
        _stage_files(modified, repo_path)
        
        # Step 4: Create commit with contextual message
        if error_summary:
            commit_message = f"AI fix: {error_summary[:50]}"
        else:
            commit_message = "AI fix applied"
        
        commit_hash = _create_commit(repo_path, commit_message)
        results["commit_hash"] = commit_hash
        
        # Step 5: Push to remote
        _push_changes(repo_path)
        
        results["success"] = True
        results["message"] = f"Successfully applied fix and pushed commit {commit_hash[:7]}"
        results["commit_message"] = commit_message
        
        # Log the successful fix application
        log_apply_fix(
            changes=changes,
            commit_hash=commit_hash,
            success=True,
            error_summary=error_summary
        )
        
    except FileNotFoundError as e:
        results["message"] = f"File not found: {str(e)}"
        log_apply_fix(changes=changes, success=False, error_message=results["message"])
    except PermissionError as e:
        results["message"] = f"Permission denied: {str(e)}"
        log_apply_fix(changes=changes, success=False, error_message=results["message"])
    except subprocess.CalledProcessError as e:
        results["message"] = f"Git command failed: {e.stderr}"
        log_apply_fix(changes=changes, success=False, error_message=results["message"])
    except Exception as e:
        results["message"] = f"Error applying fix: {str(e)}"
        log_apply_fix(changes=changes, success=False, error_message=results["message"])
    
    return results


def _apply_file_changes(changes: List[Dict[str, str]], repo_path: str) -> List[str]:
    """
    Apply code replacements to specified files.
    
    Args:
        changes: List of change dictionaries
        repo_path: Repository root path
        
    Returns:
        List of successfully modified file paths
        
    Safety:
        - Only modifies files explicitly listed
        - Verifies "before" content exists before replacement
        - Creates backup if needed (future enhancement)
    """
    modified_files = []
    
    for change in changes:
        file_path = os.path.join(repo_path, change["file"])
        before_code = change["before"]
        after_code = change["after"]
        
        # Safety check: File must exist
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Safety check: Verify "before" content exists
        if before_code not in content:
            raise ValueError(
                f"Could not find 'before' code in {file_path}. "
                "File may have changed since fix was generated."
            )
        
        # Replace before with after
        new_content = content.replace(before_code, after_code, 1)
        
        # Write modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        modified_files.append(change["file"])
    
    return modified_files


def _stage_files(files: List[str], repo_path: str) -> None:
    """
    Stage modified files for commit.
    
    Args:
        files: List of file paths to stage
        repo_path: Repository root path
    """
    # Stage only the modified files (safety: explicit file list)
    cmd = ["git", "add"] + files
    subprocess.run(
        cmd,
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True
    )


def _create_commit(repo_path: str, message: str = "AI fix applied") -> str:
    """
    Create a git commit with staged changes.
    
    Args:
        repo_path: Repository root path
        message: Commit message
        
    Returns:
        Commit hash
    """
    # Configure git user if not set (required for commit)
    try:
        subprocess.run(
            ["git", "config", "user.email"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        # Set default user for CI/automated environments
        subprocess.run(
            ["git", "config", "user.email", "ai-devops@assistant.local"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "AI DevOps Assistant"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
    
    # Create commit
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True
    )
    
    # Get commit hash
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True
    )
    
    return result.stdout.strip()


def _push_changes(repo_path: str) -> None:
    """
    Push committed changes to remote repository.
    
    Args:
        repo_path: Repository root path
        
    Note:
        Pushes to current branch. Requires authentication
        to be configured in the environment.
    """
    # Get current branch name
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True
    )
    branch = result.stdout.strip()
    
    # Push to remote
    subprocess.run(
        ["git", "push", "origin", branch],
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True
    )


def get_repo_status(repo_path: str = ".") -> Dict:
    """
    Get current git repository status.
    
    Args:
        repo_path: Repository root path
        
    Returns:
        Dictionary with status information
    """
    try:
        # Check if in git repo
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
        
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip()
        
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        has_changes = bool(result.stdout.strip())
        
        return {
            "is_git_repo": True,
            "branch": branch,
            "has_uncommitted_changes": has_changes
        }
        
    except subprocess.CalledProcessError:
        return {
            "is_git_repo": False,
            "branch": None,
            "has_uncommitted_changes": False
        }


def rollback_last_commit(repo_path: str = ".", confirmed: bool = False) -> Dict:
    """
    Rollback the last commit using git revert or reset.
    
    Args:
        repo_path: Path to the git repository
        confirmed: Must be True to proceed (safety check)
        
    Returns:
        Dictionary with rollback results:
            - success: bool
            - reverted_commit: str (hash of reverted commit)
            - new_commit: str (hash of revert commit, if using revert)
            - message: str
            
    Safety:
        - Requires explicit confirmation
        - Logs rollback action
        - Uses revert (safer) by default, can use reset with flag
    """
    results = {
        "success": False,
        "reverted_commit": None,
        "new_commit": None,
        "message": ""
    }
    
    # Safety: Require explicit confirmation
    if not confirmed:
        results["message"] = "Rollback not confirmed. Set confirmed=True to proceed."
        return results
    
    try:
        # Step 1: Get last commit hash
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        last_commit = result.stdout.strip()
        results["reverted_commit"] = last_commit
        
        # Step 2: Check if last commit is an AI fix (for logging)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        last_message = result.stdout.strip()
        
        # Step 3: Perform rollback using revert (safer than reset)
        # Revert creates a new commit that undoes the last commit
        subprocess.run(
            ["git", "revert", "--no-edit", "HEAD"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Get new commit hash
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        new_commit = result.stdout.strip()
        results["new_commit"] = new_commit
        
        # Step 4: Push to remote
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip()
        
        subprocess.run(
            ["git", "push", "origin", branch],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Log rollback action
        _log_rollback(last_commit, last_message, new_commit, repo_path)
        
        results["success"] = True
        results["message"] = f"Successfully rolled back commit {last_commit[:7]}. New revert commit: {new_commit[:7]}."
        
    except subprocess.CalledProcessError as e:
        results["message"] = f"Git command failed: {e.stderr}"
    except Exception as e:
        results["message"] = f"Rollback failed: {str(e)}"
    
    return results


def _log_rollback(reverted_commit: str, original_message: str, 
                  new_commit: str, repo_path: str) -> None:
    """
    Log rollback action for audit purposes.
    
    Args:
        reverted_commit: Hash of the reverted commit
        original_message: Message of the reverted commit
        new_commit: Hash of the revert commit
        repo_path: Repository path
    """
    import datetime
    
    log_entry = f"""
[{datetime.datetime.now().isoformat()}] ROLLBACK EXECUTED
  Reverted: {reverted_commit}
  Original Message: {original_message}
  Revert Commit: {new_commit}
  Repository: {repo_path}
"""
    
    # Write to rollback log file
    log_path = os.path.join(repo_path, ".rollback-log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_entry)
