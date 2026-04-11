import React from 'react';

/**
 * CodeViewer component - Displays the generated React component code.
 * 
 * @param {Object} props
 * @param {string} props.code - The generated component code to display
 */
function CodeViewer({ code }) {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 bg-gray-800">
        <h3 className="text-white font-medium">Generated Code</h3>
        <button
          onClick={copyToClipboard}
          className="text-sm text-gray-300 hover:text-white transition-colors"
        >
          Copy
        </button>
      </div>
      <div className="p-4 bg-gray-900 overflow-auto max-h-[500px]">
        <pre className="text-sm text-gray-100 font-mono whitespace-pre-wrap">
          {code}
        </pre>
      </div>
    </div>
  );
}

export default CodeViewer;
