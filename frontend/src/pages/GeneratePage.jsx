import React, { useState } from 'react';
import PromptInput from '../components/PromptInput';
import { generateComponent } from '../services/api';

/**
 * Generate Page - Component generation interface.
 * Users enter prompts to generate React components.
 */
function GeneratePage() {
  const [generatedCode, setGeneratedCode] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async (prompt) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await generateComponent(prompt);
      setGeneratedCode(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Generate Component</h1>
      
      <PromptInput onSubmit={handleGenerate} isLoading={isLoading} />
      
      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded">
          Error: {error}
        </div>
      )}
      
      {generatedCode && (
        <div className="mt-6 bg-gray-900 text-gray-100 p-4 rounded overflow-auto">
          <h3 className="text-lg font-medium mb-2">{generatedCode.component}</h3>
          <pre className="text-sm">{generatedCode.code}</pre>
        </div>
      )}
    </div>
  );
}

export default GeneratePage;
