import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { uploadCSV, clearAllOffers } from '../services/api';

/**
 * UploadCSV Component
 * Handles CSV file selection and upload
 */
export default function UploadCSV({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState('');
  const [clearing, setClearing] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      toast.error('Please select a CSV file');
      return;
    }

    setLoading(true);
    try {
      const response = await uploadCSV(file);
      toast.success(`✓ ${response.inserted_count} offers uploaded successfully!`);
      
      // Reset form
      setFile(null);
      setFileName('');
      
      // Notify parent component or navigate to product selection when used as first screen
      if (onUploadSuccess) {
        onUploadSuccess(response);
      } else {
        // default behaviour for standalone upload page: go to product selection
        navigate('/product-selection', { replace: true });
      }
    } catch (error) {
      toast.error(`✗ Upload failed: ${error.message}`);
      console.error('Upload error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearOffers = async () => {
    // Confirmation dialog
    const confirmed = window.confirm(
      '⚠️ Are you sure you want to delete ALL offers from the database? This action cannot be undone.'
    );
    
    if (!confirmed) {
      return;
    }

    setClearing(true);
    try {
      const response = await clearAllOffers();
      toast.success(`✓ ${response.deleted_count} offers deleted successfully!`);
      
      // Reset form
      setFile(null);
      setFileName('');
      
      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess({ inserted_count: 0 });
      }
    } catch (error) {
      toast.error(`✗ Clear failed: ${error.message}`);
      console.error('Clear error:', error);
    } finally {
      setClearing(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-md p-6 md:p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Offers CSV</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* File Input */}
        <div className="relative">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={loading}
            className="hidden"
            id="csv-input"
          />
          <label
            htmlFor="csv-input"
            className="block border-2 border-dashed border-blue-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 transition-colors bg-blue-50"
          >
            <div className="text-blue-600 font-semibold text-lg mb-2">
              📁 Choose CSV File
            </div>
            <div className="text-sm text-gray-600">
              or drag and drop
            </div>
            {fileName && (
              <div className="text-sm text-green-600 font-semibold mt-2">
                ✓ {fileName}
              </div>
            )}
          </label>
        </div>

        {/* CSV Format Info */}
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
            <p className="text-sm font-semibold text-gray-700 mb-2">CSV Format (flexible):</p>
            <p className="text-xs text-gray-600 mb-2">Supported headers (case-insensitive):</p>
            <code className="text-xs text-gray-600 block whitespace-pre-wrap">
              Examples: Categories, Brand, Item Name, MRP, Rapsap Price, Savings
            </code>
            <p className="text-xs text-gray-600 mt-2">We also accept columns named: product_id, product_name, brand, price, mrp, offer_type, offer_details, valid_till. Unrecognized columns will be preserved as custom fields.</p>
          </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!file || loading}
          className={`w-full py-3 rounded-lg font-bold text-white transition-all ${
            loading || !file
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
          }`}
        >
          {loading ? '⏳ Uploading...' : '📤 Upload CSV'}
        </button>

        {/* Clear All Offers Button */}
        <button
          type="button"
          onClick={handleClearOffers}
          disabled={clearing}
          className={`w-full py-3 rounded-lg font-bold text-white transition-all ${
            clearing
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-red-500 hover:bg-red-600 hover:shadow-lg'
          }`}
        >
          {clearing ? '⏳ Clearing...' : '🗑️ Clear All Offers'}
        </button>
      </form>
    </div>
  );
}
