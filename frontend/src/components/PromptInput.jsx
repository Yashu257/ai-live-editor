import React, { useState } from 'react';

/**
 * PromptInput component - Allows users to enter a description of the component they want.
 * 
 * @param {Object} props
 * @param {Function} props.onSubmit - Callback when user submits the prompt
 * @param {boolean} props.isLoading - Whether a request is in progress
 */
function PromptInput({ onSubmit, isLoading }) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim() && !isLoading) {
      onSubmit(prompt.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
      <label 
        htmlFor="prompt" 
        className="block text-sm font-medium text-gray-700 mb-2"
      >
        What component would you like to create?
      </label>
      <textarea
        id="prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="e.g., A card component with a title, description, and a blue button..."
        className="w-full h-24 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        disabled={isLoading}
      />
      <div className="mt-4 flex justify-end">
        <button
          type="submit"
          disabled={!prompt.trim() || isLoading}
          className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg
                     hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500
                     disabled:bg-gray-400 disabled:cursor-not-allowed
                     transition-colors"
        >
          {isLoading ? 'Generating...' : 'Generate Component'}
        </button>
      </div>
    </form>
  );
}

export default PromptInput;
