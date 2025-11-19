import React, { useState } from 'react';
import { Button } from '../ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/Card';
import { generatePDF } from '../../services/api';
import toast from 'react-hot-toast';
import { Download, FileDown, CheckCircle, Printer } from 'lucide-react';

export default function Step4Download({ template, offers }) {
  const [generating, setGenerating] = useState(false);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [pdfInfo, setPdfInfo] = useState(null);

  const handleGeneratePDF = async () => {
    setGenerating(true);
    try {
      const offerIds = offers.map(o => o.id).filter(Boolean);
      const result = await generatePDF(offerIds, template.id, {
        pageSize: 'A4',
        perPage: 6,
        orientation: 'portrait',
      });

      setPdfUrl(result.pdf_url);
      setPdfInfo(result);
      toast.success('PDF generated successfully!');
    } catch (error) {
      toast.error('Failed to generate PDF');
      console.error(error);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = () => {
    if (pdfUrl) {
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = `shelf-talkers-${Date.now()}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      toast.success('Download started!');
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Download Shelf Talkers</CardTitle>
          <CardDescription>
            Generate and download your print-ready shelf talkers
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Summary */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-muted rounded-lg p-4">
              <p className="text-sm text-muted-foreground">Total Items</p>
              <p className="text-2xl font-semibold mt-1">{offers.length}</p>
            </div>
            <div className="bg-muted rounded-lg p-4">
              <p className="text-sm text-muted-foreground">Template</p>
              <p className="text-lg font-medium mt-1">{template.name}</p>
            </div>
          </div>

          {/* Generate/Download Area */}
          {!pdfUrl ? (
            <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <FileDown className="w-8 h-8 text-primary" />
              </div>
              <h3 className="font-medium mb-2">Ready to Generate PDF</h3>
              <p className="text-sm text-muted-foreground mb-6">
                Click the button below to generate your print-ready PDF
              </p>
              <Button
                onClick={handleGeneratePDF}
                disabled={generating}
                size="lg"
                className="min-w-[200px]"
              >
                {generating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Generating PDF...
                  </>
                ) : (
                  <>
                    <FileDown className="w-4 h-4 mr-2" />
                    Generate PDF
                  </>
                )}
              </Button>
            </div>
          ) : (
            <div className="border-2 border-green-200 bg-green-50 rounded-lg p-8 text-center">
              <div className="w-16 h-16 rounded-full bg-green-500 flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-medium mb-2 text-green-900">PDF Ready!</h3>
              <p className="text-sm text-green-700 mb-6">
                Your shelf talkers PDF has been generated successfully
                {pdfInfo?.file_size && (
                  <span className="block mt-1">
                    File size: {(pdfInfo.file_size / 1024).toFixed(2)} KB
                  </span>
                )}
              </p>
              <div className="flex gap-3 justify-center">
                <Button
                  onClick={handleDownload}
                  size="lg"
                  className="min-w-[180px]"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Download PDF
                </Button>
                <Button
                  onClick={handleGeneratePDF}
                  variant="outline"
                  size="lg"
                >
                  Regenerate
                </Button>
              </div>
            </div>
          )}

          {/* Instructions */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-3">
            <div className="flex items-start gap-3">
              <Printer className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-900 mb-2">Printing Instructions</h4>
                <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
                  <li>Download the PDF file</li>
                  <li>Print on A4 size paper</li>
                  <li>Use landscape orientation</li>
                  <li>Cut along the grid lines with scissors</li>
                  <li>Attach shelf talkers to your shelves</li>
                </ol>
              </div>
            </div>
          </div>

          {/* Start Over Button */}
          <div className="pt-4 border-t">
            <Button
              variant="ghost"
              onClick={() => window.location.reload()}
              className="w-full"
            >
              Start New Upload
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
