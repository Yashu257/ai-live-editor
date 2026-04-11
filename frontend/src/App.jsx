import React, { useState, useEffect } from 'react';
import DynamicRenderer from './components/DynamicRenderer';
import PromptInput from './components/PromptInput';
import CodeViewer from './components/CodeViewer';
import { generateComponent } from './api';

// Default component code templates
const defaultComponents = {
  Hero: `import React from 'react';

export default function Hero() {
  return (
    <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Component Generator</h1>
        <p className="text-xl text-blue-100">Generate React components with AI-powered prompts</p>
      </div>
    </section>
  );
}`,
  Navbar: `import React from 'react';

export default function Navbar() {
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
}`,
  Footer: `import React from 'react';

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 py-6">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p className="text-sm">Built with React + FastAPI</p>
      </div>
    </footer>
  );
}`
};

/**
 * Main App component with component-based state management.
 * Each component (Hero, Navbar, Footer) maintains its own code state.
 * Only the targeted component is updated when backend responds.
 */
function App() {
  // State for each component's code
  const [components, setComponents] = useState(defaultComponents);
  const [activeComponent, setActiveComponent] = useState(null);
  const [highlightedComponent, setHighlightedComponent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Clear highlight after 2 seconds
  useEffect(() => {
    if (highlightedComponent) {
      const timer = setTimeout(() => {
        setHighlightedComponent(null);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [highlightedComponent]);

  const handleGenerate = async (prompt) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await generateComponent(prompt);
      if (result.success) {
        // Extract component name without .jsx extension
        const componentName = result.component.replace('.jsx', '');

        // Update only the targeted component
        setComponents(prev => ({
          ...prev,
          [componentName]: result.code
        }));

        setActiveComponent(componentName);
        setHighlightedComponent(componentName);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setError('Failed to connect to the server. Is the backend running?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      {/* Navbar Section */}
      <div className={`h-16 transition-all duration-300 ${highlightedComponent === 'Navbar' ? 'ring-4 ring-green-400 ring-offset-2' : ''}`}>
        <DynamicRenderer code={components.Navbar} title="Navbar" />
      </div>

      {/* Hero Section */}
      <div className={`h-64 transition-all duration-300 ${highlightedComponent === 'Hero' ? 'ring-4 ring-blue-400 ring-offset-2' : ''}`}>
        <DynamicRenderer code={components.Hero} title="Hero" />
      </div>

      <main className="flex-grow max-w-6xl mx-auto w-full p-8 space-y-6">
        <PromptInput onSubmit={handleGenerate} isLoading={isLoading} />

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {activeComponent && (
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-sm font-medium text-gray-500 mb-2">
              Last updated: {activeComponent}
            </h3>
            <CodeViewer code={components[activeComponent]} />
          </div>
        )}
      </main>

      {/* Footer Section */}
      <div className={`h-20 transition-all duration-300 ${highlightedComponent === 'Footer' ? 'ring-4 ring-purple-400 ring-offset-2' : ''}`}>
        <DynamicRenderer code={components.Footer} title="Footer" />
      </div>
    </div>
  );
}

export default App;
