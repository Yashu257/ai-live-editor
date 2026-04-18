import React, { useState } from 'react';

/*
 * ErrorFix page - Interface for fixing code errors.
 * Allows users to paste error messages and get AI-powered fixes.
 */
function ErrorFix() {
  const [errorMessage, setErrorMessage] = useState('');
  const [result, setResult] = useState(null);
  const [scanResult, setScanResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [isApplying, setIsApplying] = useState(false);
  const [applyStatus, setApplyStatus] = useState(null);
  const [error, setError] = useState(null);

  const handleFix = async () => {
    if (!errorMessage.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);
    setScanResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/fix-error/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ error: errorMessage }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze error');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleScan = async () => {
    // Show confirmation popup
    const confirmed = window.confirm(
      'Do you want to scan entire project for related issues?'
    );
    
    if (!confirmed) return;

    setIsScanning(true);
    setError(null);
    setScanResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/scan-project/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ error_context: errorMessage }),
      });

      if (!response.ok) {
        throw new Error('Failed to scan project');
      }

      const data = await response.json();
      setScanResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsScanning(false);
    }
  };

  const handleApplyFix = async () => {
    if (!result || !result.changes) return;

    setIsApplying(true);
    setApplyStatus(null);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/apply-fix/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          changes: result.changes,
          error_summary: result.summary
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to apply fix');
      }

      const data = await response.json();
      
      if (data.status === 'success') {
        setApplyStatus({
          type: 'success',
          message: data.message,
          commitHash: data.commit_hash,
          commitMessage: data.commit_message
        });
      } else {
        setApplyStatus({
          type: 'error',
          message: data.message
        });
      }
    } catch (err) {
      setApplyStatus({
        type: 'error',
        message: err.message
      });
      setError(err.message);
    } finally {
      setIsApplying(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Fix Error</h1>

      {/* Error Input */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Paste your error message:
        </label>
        <textarea
          value={errorMessage}
          onChange={(e) => setErrorMessage(e.target.value)}
          placeholder="e.g., Cannot find module '../utils/helpers'..."
          className="w-full h-32 p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-4">
        <button
          onClick={handleFix}
          disabled={isLoading || !errorMessage.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {isLoading ? 'Analyzing...' : 'Fix Error'}
        </button>
        
        <button
          onClick={handleScan}
          disabled={isScanning || !errorMessage.trim()}
          className="px-6 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:bg-gray-400"
        >
          {isScanning ? 'Scanning...' : 'Scan Entire Project'}
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded">
          Error: {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="mt-6 space-y-4">
          {/* Summary */}
          <div className="p-4 bg-blue-50 rounded">
            <h3 className="font-medium text-blue-900">Summary</h3>
            <p className="text-blue-800">{result.summary}</p>
            <span className="inline-block mt-2 px-2 py-1 text-xs bg-blue-200 rounded">
              Confidence: {result.confidence}
            </span>
          </div>

          {/* Affected Files */}
          <div className="p-4 bg-gray-50 rounded">
            <h3 className="font-medium">Affected Files</h3>
            <ul className="mt-2 space-y-1">
              {result.affected_files.map((file, idx) => (
                <li key={idx} className="text-sm text-gray-700">{file}</li>
              ))}
            </ul>
          </div>

          {/* Changes */}
          <div className="mt-6">
            <h3 className="font-medium text-lg mb-4">Code Changes</h3>
            {result.changes.map((change, idx) => (
              <div key={idx} className="mb-6 border rounded-lg overflow-hidden">
                {/* File Name */}
                <div className="bg-gray-100 px-4 py-2 border-b">
                  <p className="font-medium text-gray-800">{change.file}</p>
                </div>
                
                {/* Before Fix */}
                <div className="bg-red-50">
                  <div className="px-4 py-1 bg-red-100 border-b border-red-200">
                    <span className="text-xs font-medium text-red-700">Before Fix</span>
                  </div>
                  <pre className="p-4 text-sm text-red-800 overflow-x-auto">{change.before}</pre>
                </div>
                
                {/* After Fix */}
                <div className="bg-green-50">
                  <div className="px-4 py-1 bg-green-100 border-b border-green-200">
                    <span className="text-xs font-medium text-green-700">After Fix</span>
                  </div>
                  <pre className="p-4 text-sm text-green-800 overflow-x-auto">{change.after}</pre>
                </div>
              </div>
            ))}
          </div>

          {/* Scan Results */}
          {scanResult && scanResult.issues.length > 0 && (
            <div className="p-4 bg-orange-50 border border-orange-200 rounded">
              <h3 className="font-medium text-orange-900 mb-2">
                Project Scan Found {scanResult.issues.length} Related Issues
              </h3>
              <ul className="space-y-2">
                {scanResult.issues.map((issue, idx) => (
                  <li key={idx} className="text-sm">
                    <span className="font-medium">{issue.file}:</span>{' '}
                    <span className="text-orange-800">{issue.problem}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Confirmation Message */}
          <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded">
            <p className="font-medium text-yellow-800">Do you want to apply these changes?</p>
          </div>

          {/* Apply Status */}
          {applyStatus && (
            <div className={`mt-4 p-4 rounded ${
              applyStatus.type === 'success' 
                ? 'bg-green-50 border border-green-200' 
                : 'bg-red-50 border border-red-200'
            }`}>
              <p className={`font-medium ${
                applyStatus.type === 'success' ? 'text-green-800' : 'text-red-800'
              }`}>
                {applyStatus.message}
              </p>
              {applyStatus.commitHash && (
                <p className="text-sm text-green-600 mt-1">
                  Commit: {applyStatus.commitHash.substring(0, 7)}
                </p>
              )}
              {applyStatus.commitMessage && (
                <p className="text-sm text-gray-600 mt-1">
                  Message: {applyStatus.commitMessage}
                </p>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="mt-4 flex space-x-4">
            <button
              onClick={handleApplyFix}
              disabled={isApplying || (applyStatus && applyStatus.type === 'success')}
              className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isApplying ? 'Applying...' : (applyStatus?.type === 'success' ? 'Applied' : 'Apply Fix')}
            </button>
            <button
              onClick={() => setResult(null)}
              disabled={isApplying}
              className="px-6 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:bg-gray-400"
            >
              Reject Fix
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ErrorFix;
