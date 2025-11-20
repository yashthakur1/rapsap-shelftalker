import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Settings from './pages/Settings';
import UploadCSV from './components/UploadCSV';
import ProductSelection from './pages/ProductSelection';
import Templates from './pages/Templates';

/**
 * Main App Component
 * Routing and layout structure
 */
function App() {
  return (
    <Router>
      <Navbar />
      <div className="bg-gray-50">
        <Routes>
          <Route path="/" element={<Navigate to="/upload" replace />} />
          <Route path="/upload" element={<UploadCSV />} />
          <Route path="/product-selection" element={<ProductSelection />} />
          <Route path="/templates" element={<Templates />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
      
      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#fff',
            color: '#333',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            borderRadius: '8px',
            padding: '16px',
          },
        }}
      />
    </Router>
  );
}

export default App;
