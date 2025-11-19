import React, { useState, useEffect } from 'react';
import { Button } from '../ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/Card';
import { fetchTemplates, fetchPresetTemplates, previewPDF } from '../../services/api';
import toast from 'react-hot-toast';
import { Eye, Palette } from 'lucide-react';

export default function Step2Template({ onTemplateSelect, uploadedData }) {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [previewHtml, setPreviewHtml] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const data = await fetchPresetTemplates();
      setTemplates(data.templates || []);
      if (data.templates?.length > 0) {
        handleSelectTemplate(data.templates[0]);
      }
    } catch (error) {
      toast.error('Failed to load templates');
    }
  };

  const handleSelectTemplate = async (template) => {
    setSelectedTemplate(template);
    setLoading(true);

    try {
      // Generate preview with first few items
      const sampleOffers = uploadedData?.preview?.slice(0, 3) || [];
      if (sampleOffers.length > 0) {
        const offerIds = sampleOffers.map(o => o.id).filter(Boolean);
        const html = await previewPDF(offerIds, template.id, {
          pageSize: 'A4',
          perPage: 6,
        });
        setPreviewHtml(html);
      }
    } catch (error) {
      console.error('Preview error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = () => {
    if (selectedTemplate) {
      onTemplateSelect(selectedTemplate);
    } else {
      toast.error('Please select a template');
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Select Template</CardTitle>
          <CardDescription>
            Choose a template for your shelf talkers
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            {/* Template Selection */}
            <div className="space-y-4">
              <h3 className="font-medium text-sm text-muted-foreground">Available Templates</h3>
              <div className="space-y-2">
                {templates.map((template) => (
                  <button
                    key={template.id}
                    onClick={() => handleSelectTemplate(template)}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      selectedTemplate?.id === template.id
                        ? 'border-primary bg-primary/5'
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium">{template.name}</h4>
                        {template.description && (
                          <p className="text-sm text-muted-foreground mt-1">
                            {template.description}
                          </p>
                        )}
                      </div>
                      {selectedTemplate?.id === template.id && (
                        <Palette className="w-5 h-5 text-primary" />
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Preview */}
            <div className="space-y-4">
              <h3 className="font-medium text-sm text-muted-foreground flex items-center gap-2">
                <Eye className="w-4 h-4" />
                Preview
              </h3>
              <div className="border rounded-lg overflow-hidden bg-gray-50 min-h-[400px]">
                {loading ? (
                  <div className="flex items-center justify-center h-[400px]">
                    <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                  </div>
                ) : previewHtml ? (
                  <iframe
                    srcDoc={previewHtml}
                    className="w-full h-[400px] bg-white"
                    title="Template Preview"
                  />
                ) : (
                  <div className="flex items-center justify-center h-[400px] text-muted-foreground">
                    Select a template to see preview
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="mt-6 flex justify-end">
            <Button
              onClick={handleContinue}
              disabled={!selectedTemplate}
              size="lg"
            >
              Continue to Preview
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
