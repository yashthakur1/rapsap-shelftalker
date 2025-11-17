import React, { useEffect, useState } from 'react';
import toast from 'react-hot-toast';

/**
 * Settings Page
 * Configuration and system settings
 */
export default function Settings() {
  const [pageSize, setPageSize] = useState('A4');
  const [perPage, setPerPage] = useState(24);

  useEffect(() => {
    try {
      const ps = localStorage.getItem('aops.pdf.pageSize');
      const pp = localStorage.getItem('aops.pdf.perPage');
      if (ps) setPageSize(ps);
      if (pp) setPerPage(parseInt(pp, 10));
    } catch (e) {
      // ignore
    }
  }, []);
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-4">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-800">⚙️ Settings</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 md:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-md p-8">
          {/* API Configuration */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">API Configuration</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  API Base URL
                </label>
                <input
                  type="text"
                  defaultValue={import.meta.env.VITE_API_URL || 'http://localhost:8000'}
                  readOnly
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg bg-gray-50 text-gray-600"
                />
                <p className="text-xs text-gray-600 mt-1">
                  Configure via .env file: VITE_API_URL
                </p>
              </div>
            </div>
          </section>

          {/* PDF Settings */}
          <section className="mb-8 border-t pt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">PDF Settings</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Default Page Size
                </label>
                <select value={pageSize} onChange={(e) => setPageSize(e.target.value)} className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none">
                  <option>A4</option>
                  <option>Letter</option>
                  <option>A3</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Offers Per Page
                </label>
                <input
                  type="number"
                  value={perPage}
                  onChange={(e) => setPerPage(Number(e.target.value || 1))}
                  min="1"
                  max="100"
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>
          </section>

          {/* System Info */}
          <section className="border-t pt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">System Information</h2>
            <div className="space-y-2 text-sm text-gray-600">
              <p><strong>AOPS Version:</strong> 1.0.0</p>
              <p><strong>Frontend Framework:</strong> React 18 + Vite</p>
              <p><strong>Styling:</strong> Tailwind CSS 3</p>
              <p><strong>Backend:</strong> FastAPI (Python)</p>
              <p><strong>Database:</strong> MongoDB</p>
            </div>
          </section>

          {/* Action Buttons */}
          <div className="mt-8 pt-8 border-t space-y-2">
            <button onClick={() => {
                try {
                  localStorage.setItem('aops.pdf.pageSize', pageSize);
                  localStorage.setItem('aops.pdf.perPage', String(perPage));
                  toast.success('✓ Settings saved');
                } catch (e) { toast.error('Failed to save settings'); }
              }}
              className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors">
              Save Settings
            </button>
            <button onClick={() => {
                try {
                  localStorage.removeItem('aops.pdf.pageSize');
                  localStorage.removeItem('aops.pdf.perPage');
                  setPageSize('A4'); setPerPage(24);
                  toast.success('✓ Reset to defaults');
                } catch (e) { toast.error('Failed to reset'); }
              }}
              className="w-full py-2 px-4 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg font-semibold transition-colors">
              Reset to Defaults
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
