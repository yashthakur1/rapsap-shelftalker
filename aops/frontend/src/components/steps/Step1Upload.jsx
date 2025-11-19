import React, { useState } from 'react';
import { Upload, FileSpreadsheet, CheckCircle2 } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/Card';
import { uploadCSV } from '../../services/api';
import toast from 'react-hot-toast';

export default function Step1Upload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedCount, setUploadedCount] = useState(0);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
    } else {
      toast.error('Please select a valid CSV file');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file first');
      return;
    }

    setUploading(true);
    try {
      const response = await uploadCSV(file);
      setUploadedCount(response.inserted_count);
      toast.success(`Successfully uploaded ${response.inserted_count} items`);
      onUploadSuccess(response);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to upload CSV');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Upload Product CSV</CardTitle>
          <CardDescription>
            Upload a CSV file with columns: Categories, Brand, Item Name, MRP, Rapsap Price, Savings
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* File Input Area */}
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary transition-colors">
            <input
              type="file"
              id="csv-upload"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
            />
            <label
              htmlFor="csv-upload"
              className="cursor-pointer flex flex-col items-center justify-center gap-4"
            >
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <FileSpreadsheet className="w-8 h-8 text-primary" />
              </div>
              {file ? (
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  <span className="font-medium">{file.name}</span>
                </div>
              ) : (
                <>
                  <div>
                    <p className="text-base font-medium mb-1">Click to upload CSV</p>
                    <p className="text-sm text-muted-foreground">or drag and drop</p>
                  </div>
                </>
              )}
            </label>
          </div>

          {/* Expected Format */}
          <div className="bg-muted rounded-lg p-4">
            <p className="text-sm font-medium mb-2">Expected CSV Format:</p>
            <div className="text-xs font-mono bg-white p-3 rounded border overflow-x-auto">
              <div>Categories,Brand,Item Name,MRP,Rapsap Price,Savings</div>
              <div className="text-muted-foreground">Groceries,Brand A,Product 1,100,80,20</div>
            </div>
          </div>

          {/* Upload Button */}
          <Button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full"
            size="lg"
          >
            {uploading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                Uploading...
              </>
            ) : (
              <>
                <Upload className="w-4 h-4 mr-2" />
                Upload CSV
              </>
            )}
          </Button>

          {uploadedCount > 0 && (
            <div className="text-center text-sm text-green-600 font-medium">
              ✓ {uploadedCount} items uploaded successfully
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
