import React from 'react';

/**
 * Renders JSX code from a string using a sandboxed iframe.
 * Used to display dynamically generated components.
 *
 * @param {Object} props
 * @param {string} props.code - The component code to render
 * @param {string} props.title - Title for the iframe
 */
function DynamicRenderer({ code, title = 'Dynamic Component' }) {
  if (!code) return null;

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
          const useState = React.useState;
          const useEffect = React.useEffect;
          const useRef = React.useRef;
          const useCallback = React.useCallback;
          const useMemo = React.useMemo;
          const useContext = React.useContext;
          const useReducer = React.useReducer;
        </script>
        <style>
          body { margin: 0; font-family: system-ui, sans-serif; }
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
    <iframe
      srcDoc={previewHtml}
      title={title}
      className="w-full border-0"
      style={{ height: '100%', minHeight: '100%' }}
      sandbox="allow-scripts allow-forms"
    />
  );
}

export default DynamicRenderer;
