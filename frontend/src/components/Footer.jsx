import React from 'react';

/**
 * Simple footer component
 */
function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 py-6 mt-12">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p className="text-sm">
          Built with React + FastAPI
        </p>
      </div>
    </footer>
  );
}

export default Footer;
