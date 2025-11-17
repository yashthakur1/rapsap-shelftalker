import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { generatePDF, fetchTemplateById } from '../services/api';

/**
 * PDFGenerator Component
 * Handles PDF generation and download
 */
export default function PDFGenerator({ selectedOffers, selectedTemplate }) {
  const [loading, setLoading] = useState(false);
  const [generatedPDF, setGeneratedPDF] = useState(null);
  

  const handleGeneratePDF = async () => {
    if (!selectedOffers || selectedOffers.length === 0) {
      toast.error('Please select at least one offer');
      return;
    }

    if (!selectedTemplate) {
      toast.error('Please select a template');
      return;
    }

    setLoading(true);
    try {
      // Read app-level PDF defaults from localStorage (if set)
      let storedLayoutOptions = null;
      try {
        const ps = localStorage.getItem('aops.pdf.pageSize');
        const pp = localStorage.getItem('aops.pdf.perPage');
        if (ps || pp) {
          storedLayoutOptions = {};
          if (ps) storedLayoutOptions.pageSize = ps;
          if (pp) storedLayoutOptions.perPage = parseInt(pp, 10) || undefined;
        }
      } catch (e) {
        // ignore localStorage errors
      }

      // Fetch latest template metadata so custom layout options are honored
      let layoutOptionsToUse = null;
      const templateResponse = await fetchTemplateById(selectedTemplate);
      const templateMeta = templateResponse?.template;
      const templateLayout = templateMeta?.layout_options;
      if (templateLayout && typeof templateLayout === 'object') {
        layoutOptionsToUse = { ...templateLayout };
      }
      if (storedLayoutOptions) {
        layoutOptionsToUse = layoutOptionsToUse
          ? { ...layoutOptionsToUse, ...storedLayoutOptions }
          : { ...storedLayoutOptions };
      }

      const response = await generatePDF(
        selectedOffers,
        selectedTemplate,
        layoutOptionsToUse
      );

      setGeneratedPDF(response);
      toast.success(`✓ PDF generated with ${response.offer_count} offers!`);
    } catch (error) {
      toast.error(`PDF generation failed: ${error.message}`);
      console.error('PDF error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (generatedPDF?.file_path) {
      const filename = generatedPDF.file_path.split('/').pop();
      const link = document.createElement('a');
      link.href = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${generatedPDF.pdf_url}`;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      toast.success('✓ Download started!');
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-md p-6 md:p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Generate PDF</h2>

      {/* Status Info */}
      <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">
        <p className="text-sm text-gray-700">
          <strong>Selected Offers:</strong> {selectedOffers?.length || 0}
        </p>
        <p className="text-sm text-gray-700">
          <strong>Template:</strong> {selectedTemplate ? 'Selected ✓' : 'Not selected'}
        </p>
      </div>

      {/* Generate Button */}
      {/* Custom Size Controls */}

      <button
        onClick={handleGeneratePDF}
        disabled={
          loading ||
          !selectedOffers ||
          selectedOffers.length === 0 ||
          !selectedTemplate
        }
        className={`w-full py-3 px-6 rounded-lg font-bold text-white text-lg transition-all mb-4 ${
          loading ||
          !selectedOffers ||
          selectedOffers.length === 0 ||
          !selectedTemplate
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
        }`}
      >
        {loading ? '⏳ Generating PDF...' : '🖨️ Generate PDF'}
      </button>

      {/* Success Message & Download */}
      {generatedPDF && (
        <div className="bg-green-50 border-2 border-green-300 rounded-lg p-4">
          <h3 className="font-semibold text-green-800 mb-2">✓ PDF Generated Successfully!</h3>
          <p className="text-sm text-gray-700 mb-2">
            {generatedPDF.offer_count} offers rendered • File size: {(generatedPDF.file_size / 1024).toFixed(2)} KB
          </p>
          <button
            onClick={handleDownload}
            className="w-full py-2 px-4 bg-green-600 hover:bg-green-700 text-white rounded-lg font-bold transition-colors"
          >
            📥 Download PDF
          </button>
        </div>
      )}

      {/* Info */}
      <div className="bg-gray-50 border-l-4 border-gray-400 p-4 mt-4">
        <p className="text-xs text-gray-600">
          <strong>💡 Note:</strong> PDF generation may take a few seconds depending on the number of offers.
        </p>
      </div>
    </div>
  );
}
