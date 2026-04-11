import React from 'react';

/**
 * Simple navigation bar component
 */
function Navbar() {
  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <span className="text-xl font-bold text-blue-600">GenUI</span>
          <div className="space-x-4">
            <a href="#" className="text-gray-600 hover:text-blue-600">Home</a>
            <a href="#" className="text-gray-600 hover:text-blue-600">About</a>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
