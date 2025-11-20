import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import OfferPreview from '../components/OfferPreview';

export default function ProductSelection() {
  const [selectedOffers, setSelectedOffers] = useState([]);
  const navigate = useNavigate();

  const handleNext = () => {
    if (!selectedOffers || selectedOffers.length === 0) {
      alert('Please select at least one product to continue');
      return;
    }
    navigate('/templates', { state: { selectedOffers } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-600 to-blue-100">
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="space-y-8">
          <section>
            <div className="text-lg font-bold text-gray-800 mb-4 flex items-center space-x-2">
              <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">1</span>
              <span>Select Products</span>
            </div>
            <OfferPreview onSelectionChange={setSelectedOffers} />
          </section>

          <div className="flex justify-end">
            <button
              onClick={handleNext}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700"
            >
              Next → Select Template
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
