/*
 * API service module.
 * Handles all communication with the backend.
 * Single Responsibility: HTTP requests only.
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

/*
 * Generate a React component from a prompt.
 * @param {string} prompt - User description
 * @returns {Promise<{component: string, code: string}>}
 */
export async function generateComponent(prompt) {
  const response = await fetch(`${API_BASE_URL}/generate/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to generate component');
  }

  return response.json();
}

/*
 * Analyze and fix a code error.
 * @param {string} errorMessage - The error message
 * @param {string} codeSnippet - Optional code that caused error
 * @param {string} filePath - Optional file path
 * @returns {Promise<{analysis: string, affected_files: Array, suggested_fix: string, explanation: string}>}
 */
export async function fixError(errorMessage, codeSnippet = '', filePath = '') {
  const response = await fetch(`${API_BASE_URL}/fix-error/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      error_message: errorMessage,
      code_snippet: codeSnippet,
      file_path: filePath,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to analyze error');
  }

  return response.json();
}
