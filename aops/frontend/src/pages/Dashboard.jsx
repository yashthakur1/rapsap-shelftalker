import React, { useState } from 'react';
import StepIndicator from '../components/ui/StepIndicator';
import Step1Upload from '../components/steps/Step1Upload';
import Step2Template from '../components/steps/Step2Template';
import Step3Preview from '../components/steps/Step3Preview';
import Step4Download from '../components/steps/Step4Download';

/**
 * Dashboard Page
 * Clean and minimal 4-step workflow for creating shelf talkers
 */
export default function Dashboard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadedData, setUploadedData] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [previewData, setPreviewData] = useState(null);

  const handleUploadSuccess = (data) => {
    setUploadedData(data);
    setCurrentStep(2);
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setCurrentStep(3);
  };

  const handlePreviewContinue = (data) => {
    setPreviewData(data);
    setCurrentStep(4);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-border">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-6">
          <h1 className="text-3xl font-bold text-foreground">Shelf Talker Generator</h1>
          <p className="text-muted-foreground mt-1">
            Create professional shelf talkers in 4 simple steps
          </p>
        </div>
      </header>

      {/* Step Indicator */}
      <StepIndicator currentStep={currentStep} />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-8 pb-16">
        {currentStep === 1 && (
          <Step1Upload onUploadSuccess={handleUploadSuccess} />
        )}

        {currentStep === 2 && (
          <Step2Template
            onTemplateSelect={handleTemplateSelect}
            uploadedData={uploadedData}
          />
        )}

        {currentStep === 3 && (
          <Step3Preview
            template={selectedTemplate}
            onContinue={handlePreviewContinue}
          />
        )}

        {currentStep === 4 && (
          <Step4Download
            template={selectedTemplate}
            offers={previewData?.offers || []}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-border mt-auto">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-6 text-center text-sm text-muted-foreground">
          <p>Shelf Talker Generator © 2025 • Powered by Rapsap</p>
        </div>
      </footer>
    </div>
  );
}
