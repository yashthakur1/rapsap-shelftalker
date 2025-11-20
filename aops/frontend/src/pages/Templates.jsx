import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import TemplateManager from '../components/TemplateManager';
import PDFGenerator from '../components/PDFGenerator';

export default function Templates() {
  const location = useLocation();
  const navigate = useNavigate();
  const selectedOffersFromState = (location.state && location.state.selectedOffers) || [];

  const [selectedOffers, setSelectedOffers] = useState(selectedOffersFromState);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [selectedBrand, setSelectedBrand] = useState(null);

  const handleBack = () => {
    navigate('/product-selection', { state: { selectedOffers } });
  };

  // If user navigated here without selected offers, send them back to upload
  if (!selectedOffers || selectedOffers.length === 0) {
    // keep a small UX: show a message and nav button
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="bg-white rounded-lg p-8 shadow-md text-center">
          <h3 className="text-lg font-semibold mb-4">No products selected</h3>
          <p className="text-sm text-gray-600 mb-6">Please upload a CSV and select products first.</p>
          <div className="flex gap-2 justify-center">
            <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={() => navigate('/upload')}>Upload CSV</button>
            <button className="px-4 py-2 bg-gray-200 rounded" onClick={() => navigate('/product-selection')}>Select Products</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-600 to-blue-100">
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <TemplateManager
              onTemplateSelect={setSelectedTemplate}
              selectedOffers={selectedOffers}
              selectedBrand={selectedBrand}
              onBrandSelect={setSelectedBrand}
            />
          </div>

          <div>
            <PDFGenerator
              selectedOffers={selectedOffers}
              selectedTemplate={selectedTemplate}
              selectedBrand={selectedBrand}
            />
          </div>
        </div>

        {/* Back Button */}
        <div className="mt-8 flex justify-start">
          <button
            onClick={handleBack}
            className="px-6 py-3 bg-gray-400 text-white rounded-lg font-semibold hover:bg-gray-500 transition-all"
          >
            ← Back to Products
          </button>
        </div>
      </main>
    </div>
  );
}
