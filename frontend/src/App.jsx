import React, { useState } from 'react';
import GeneratePage from './pages/GeneratePage';
import ErrorFix from './pages/ErrorFix';

/**
 * Main App component with navigation between pages.
 * Routes: Generate (default) | Error Fix
 */
function App() {
  // Simple page navigation state
  const [currentPage, setCurrentPage] = useState('generate');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <span className="text-xl font-bold text-blue-600">AI DevOps Assistant</span>
          <div className="space-x-4">
            <button
              onClick={() => setCurrentPage('generate')}
              className={`px-4 py-2 rounded ${currentPage === 'generate' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:text-blue-600'}`}
            >
              Generate
            </button>
            <button
              onClick={() => setCurrentPage('error-fix')}
              className={`px-4 py-2 rounded ${currentPage === 'error-fix' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:text-blue-600'}`}
            >
              Fix Error
            </button>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <main className="py-8">
        {currentPage === 'generate' && <GeneratePage />}
        {currentPage === 'error-fix' && <ErrorFix />}
      </main>
    </div>
  );
}

export default App;
