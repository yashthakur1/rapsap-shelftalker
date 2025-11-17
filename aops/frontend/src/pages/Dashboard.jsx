import React, { useState } from 'react';
import UploadCSV from '../components/UploadCSV';
import OfferPreview from '../components/OfferPreview';
import TemplateManager from '../components/TemplateManager';
import PDFGenerator from '../components/PDFGenerator';

/**
 * Dashboard Page
 * Main workflow page combining all components
 */
export default function Dashboard() {
  const [selectedOffers, setSelectedOffers] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = () => {
    // Trigger refresh of offers list
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="space-y-8">
          {/* Step 1: Upload CSV */}
          <section>
            <div className="text-lg font-bold text-gray-800 mb-4 flex items-center space-x-2">
              <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">1</span>
              <span>Upload Offers</span>
            </div>
            <UploadCSV onUploadSuccess={handleUploadSuccess} />
          </section>

          {/* Step 2: Select Offers & Template */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Offers Preview */}
            <div className="lg:col-span-2">
              <section>
                <div className="text-lg font-bold text-gray-800 mb-4 flex items-center space-x-2">
                  <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">2</span>
                  <span>Select Offers</span>
                </div>
                <OfferPreview
                  key={refreshTrigger}
                  onSelectionChange={setSelectedOffers}
                  selectedTemplate={selectedTemplate}
                />
              </section>
            </div>

            {/* Template Manager */}
            <div>
              <section className="lg:sticky lg:top-24">
                <div className="text-lg font-bold text-gray-800 mb-4 flex items-center space-x-2">
                  <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">3</span>
                  <span>Template</span>
                </div>
                <TemplateManager onTemplateSelect={setSelectedTemplate} selectedOffers={selectedOffers} />
              </section>
            </div>
          </div>

          {/* Step 3: Generate PDF */}
          <section>
            <div className="text-lg font-bold text-gray-800 mb-4 flex items-center space-x-2">
              <span className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm">4</span>
              <span>Generate & Download</span>
            </div>
            <PDFGenerator
              selectedOffers={selectedOffers}
              selectedTemplate={selectedTemplate}
            />
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-6 text-center text-sm text-gray-600">
          <p>AOPS © 2025 • Automated Offer Print System</p>
        </div>
      </footer>
    </div>
  );
}
