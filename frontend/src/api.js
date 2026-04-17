/**
 * API module for communicating with the FastAPI backend.
 * Contains functions to generate components from user prompts.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Generate a React component based on the provided prompt.
 * 
 * @param {string} prompt - The user's description of the desired component
 * @returns {Promise<{success: boolean, code: string, message: string}>} - The generation result
 */
export async function generateComponent(prompt) {
  const response = await fetch(`${API_BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to generate component');
  }

  return response.json();
}
