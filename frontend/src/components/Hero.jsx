import React from 'react';

/**
 * Hero section component with gradient background
 */
function Hero() {
  return (
    <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Component Generator
        </h1>
        <p className="text-xl text-blue-100 max-w-2xl mx-auto">
          Generate React components with AI-powered prompts
        </p>
      </div>
    </section>
  );
}

export default Hero;
