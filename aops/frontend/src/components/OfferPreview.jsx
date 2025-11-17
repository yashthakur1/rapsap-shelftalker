import React, { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { fetchOffers } from '../services/api';

/**
 * OfferPreview Component
 * Displays offers in a responsive grid with selection checkboxes
 */
export default function OfferPreview({ onSelectionChange }) {
  const [offers, setOffers] = useState([]);
  const [selected, setSelected] = useState(new Set());
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ skip: 0, limit: 50, total: 0 });

  // Load offers on mount and when pagination changes
  useEffect(() => {
    loadOffers();
  }, [pagination.skip]);

  

  const loadOffers = async () => {
    setLoading(true);
    try {
      const response = await fetchOffers(pagination.skip, pagination.limit);
      setOffers(response.offers || []);
      setPagination(p => ({ ...p, total: response.total }));
    } catch (error) {
      toast.error(`Failed to load offers: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOffer = (offerId) => {
    const newSelected = new Set(selected);
    if (newSelected.has(offerId)) {
      newSelected.delete(offerId);
    } else {
      newSelected.add(offerId);
    }
    setSelected(newSelected);
    
    // Notify parent of selection change
    if (onSelectionChange) {
      onSelectionChange(Array.from(newSelected));
    }
  };

  const handleSelectAll = () => {
    const newSelected = selected.size === offers.length ? new Set() : new Set(offers.map(o => o.id || o._id));
    setSelected(newSelected);
    if (onSelectionChange) {
      onSelectionChange(Array.from(newSelected));
    }
  };

  if (offers.length === 0 && !loading) {
    return (
      <div className="bg-white rounded-2xl shadow-md p-8 text-center">
        <div className="text-4xl mb-2">📭</div>
        <p className="text-gray-600 text-lg">No offers uploaded yet</p>
        <p className="text-gray-500 text-sm">Upload a CSV file to get started</p>
      </div>
    );
  }

  const totalPages = Math.ceil(pagination.total / pagination.limit);
  const currentPage = Math.floor(pagination.skip / pagination.limit) + 1;

  return (
    <div className="relative z-0 bg-white rounded-2xl shadow-md p-6 md:p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Offers Preview</h2>
        <div className="text-sm text-gray-600">
          {selected.size} / {pagination.total} selected
        </div>
      </div>

      

      {/* Select All Checkbox */}
      {offers.length > 0 && (
        <div className="mb-4 pb-4 border-b flex items-center">
          <input
            type="checkbox"
            id="select-all"
            checked={selected.size === offers.length && offers.length > 0}
            onChange={handleSelectAll}
            className="w-5 h-5 rounded cursor-pointer"
          />
          <label htmlFor="select-all" className="ml-2 text-sm font-semibold text-gray-700 cursor-pointer">
            Select All on This Page
          </label>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-8">
          <div className="text-gray-600">⏳ Loading offers...</div>
        </div>
      )}

      {/* Offers Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-6">
        {offers.map((offer) => {
          const offerId = offer.id || offer._id;
          const isSelected = selected.has(offerId);
          
          return (
            <div
              key={offerId}
              className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                isSelected
                  ? 'border-blue-500 bg-blue-50 shadow-md'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
              onClick={() => handleSelectOffer(offerId)}
            >
              {/* Checkbox */}
              <div className="flex items-start mb-2">
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => handleSelectOffer(offerId)}
                  className="w-4 h-4 rounded mt-1 cursor-pointer"
                  onClick={(e) => e.stopPropagation()}
                />
              </div>

              {/* Product Info */}
              <h3 className="font-bold text-sm text-gray-800 mb-1">
                {offer.product_name}
              </h3>
              <p className="text-xs text-gray-600 mb-2">{offer.brand}</p>

              {/* Offer Badge */}
              <div className="inline-block bg-yellow-300 text-gray-800 px-2 py-1 rounded text-xs font-bold mb-2">
                {offer.offer_type}
              </div>

              {/* Price Info */}
              <div className="mt-3 pt-3 border-t">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs text-gray-600">Price:</span>
                  <span className="font-bold text-blue-600">₹{offer.price}</span>
                </div>
                {offer.mrp && (
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs text-gray-600">MRP:</span>
                    <span className="text-xs text-gray-400 line-through">₹{offer.mrp}</span>
                  </div>
                )}
                <div className="text-xs text-gray-600 mt-2">
                  Valid: {offer.valid_till}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <button
            onClick={() => setPagination(p => ({ ...p, skip: Math.max(0, p.skip - p.limit) }))}
            disabled={pagination.skip === 0}
            className="px-4 py-2 rounded-lg bg-gray-200 text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300"
          >
            ← Previous
          </button>
          <span className="text-sm text-gray-600">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setPagination(p => ({ ...p, skip: p.skip + p.limit }))}
            disabled={currentPage >= totalPages}
            className="px-4 py-2 rounded-lg bg-gray-200 text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}
