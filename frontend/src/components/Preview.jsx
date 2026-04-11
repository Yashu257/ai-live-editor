import React from 'react';

/**
 * Preview component - Renders the generated component in an iframe for safety.
 * 
 * @param {Object} props
 * @param {string} props.code - The generated component code to preview
 */
function Preview({ code }) {
  // Create a simple HTML page that renders the component
  // Note: This is a basic preview - in production, you'd want to use
  // a proper bundler or sandbox for security
  const previewHtml = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
          // Expose React hooks globally for Babel-transformed code
          const useState = React.useState;
          const useEffect = React.useEffect;
          const useRef = React.useRef;
          const useCallback = React.useCallback;
          const useMemo = React.useMemo;
          const useContext = React.useContext;
          const useReducer = React.useReducer;
        </script>
        <style>
          body { margin: 0; padding: 20px; font-family: system-ui, sans-serif; }
        </style>
      </head>
      <body>
        <div id="root"></div>
        <script type="text/babel">
          ${code.replace('export default ', 'const GeneratedComponent = ').replace(/import.*from.*;/g, '')}
          
          const root = ReactDOM.createRoot(document.getElementById('root'));
          root.render(<GeneratedComponent />);
        </script>
      </body>
    </html>
  `;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-4 py-3 bg-gray-800">
        <h3 className="text-white font-medium">Live Preview</h3>
      </div>
      <div className="h-[500px]">
        <iframe
          srcDoc={previewHtml}
          title="Component Preview"
          className="w-full h-full border-0"
          sandbox="allow-scripts allow-forms"
        />
      </div>
    </div>
  );
}

export default Preview;
