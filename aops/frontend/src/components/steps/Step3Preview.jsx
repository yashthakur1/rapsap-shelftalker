import React, { useState, useEffect } from 'react';
import { Button } from '../ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/Card';
import { fetchOffers, previewPDF } from '../../services/api';
import toast from 'react-hot-toast';
import { Grid3x3, Loader2 } from 'lucide-react';

export default function Step3Preview({ template, onContinue }) {
  const [offers, setOffers] = useState([]);
  const [previewHtml, setPreviewHtml] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadOffersAndPreview();
  }, [template]);

  const loadOffersAndPreview = async () => {
    setLoading(true);
    try {
      // Fetch all offers
      const data = await fetchOffers(0, 100);
      setOffers(data.offers || []);

      // Generate A4 grid preview
      if (data.offers?.length > 0 && template) {
        const offerIds = data.offers.map(o => o.id).filter(Boolean);
        const html = await previewPDF(offerIds, template.id, {
          pageSize: 'A4',
          perPage: 6,
          orientation: 'portrait',
        });
        setPreviewHtml(html);
      }
    } catch (error) {
      toast.error('Failed to load preview');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Grid3x3 className="w-5 h-5" />
            A4 Grid Preview
          </CardTitle>
          <CardDescription>
            Preview how your shelf talkers will look when printed on A4 paper
            <br />
            <span className="text-xs">
              {offers.length} items • 6 per page • Ready to cut with scissors
            </span>
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Preview Area */}
          <div className="border-2 rounded-lg overflow-hidden bg-gray-100">
            {loading ? (
              <div className="flex flex-col items-center justify-center h-[600px]">
                <Loader2 className="w-12 h-12 text-primary animate-spin" />
                <p className="mt-4 text-sm text-muted-foreground">Generating preview...</p>
              </div>
            ) : previewHtml ? (
              <div className="bg-white">
                <iframe
                  srcDoc={previewHtml}
                  className="w-full h-[600px]"
                  title="A4 Grid Preview"
                />
              </div>
            ) : (
              <div className="flex items-center justify-center h-[600px] text-muted-foreground">
                No preview available
              </div>
            )}
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-900">
              <strong>Print Instructions:</strong> The shelf talkers are arranged in a 2×3 grid
              per A4 page. After downloading, print on A4 paper and cut along the grid lines
              with scissors.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-between">
            <Button
              variant="outline"
              onClick={() => window.history.back()}
            >
              Back
            </Button>
            <Button
              onClick={() => onContinue({ offers, previewHtml })}
              disabled={loading || !previewHtml}
              size="lg"
            >
              Continue to Download
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
