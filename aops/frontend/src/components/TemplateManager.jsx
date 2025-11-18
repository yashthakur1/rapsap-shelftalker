import React, { useEffect, useState, useRef } from 'react';
import toast from 'react-hot-toast';
import { fetchTemplates, uploadTemplate, fetchOffers, previewPDF, updateTemplateLayout } from '../services/api';

/**
 * TemplateManager Component
 * Handles template selection and custom template uploads
 */
export default function TemplateManager({ onTemplateSelect, selectedOffers = [], selectedBrand, onBrandSelect }) {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [previewHtml, setPreviewHtml] = useState('');
  const [previewLoading, setPreviewLoading] = useState(false);
  const [brands, setBrands] = useState([]);
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const iframeRef = useRef(null);

  // Load templates on mount
  useEffect(() => {
    loadTemplates();
    loadBrands();
  }, []);

  const loadBrands = async () => {
    try {
      const response = await fetch('http://localhost:8000/branding');
      const data = await response.json();
      setBrands(data.brands || []);
      // Default to first brand if available and not already selected
      if (data.brands && data.brands.length > 0 && !selectedBrand) {
        if (onBrandSelect) onBrandSelect(data.brands[0]);
      }
    } catch (error) {
      console.error('Failed to load brands:', error);
    }
  };

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const response = await fetchTemplates();
      setTemplates(response.templates || []);
      
      // Preserve selection if possible, otherwise auto-select first
      const incoming = response.templates || [];
      const hasCurrent = selectedTemplate && incoming.find(t => (t.id || t._id) === selectedTemplate);
      if (hasCurrent) {
        // Keep existing selection
        if (onTemplateSelect) onTemplateSelect(selectedTemplate);
      } else if (incoming.length > 0) {
        const firstTemplate = incoming[0];
        const templateId = firstTemplate.id || firstTemplate._id;
        setSelectedTemplate(templateId);
        if (onTemplateSelect) onTemplateSelect(templateId);
      }
    } catch (error) {
      toast.error(`Failed to load templates: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTemplateChange = (templateId) => {
    setSelectedTemplate(templateId);
    if (onTemplateSelect) {
      onTemplateSelect(templateId);
    }
  };

  const handleTemplateUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.zip')) {
      toast.error('Please upload a ZIP file');
      return;
    }

    setUploading(true);
    try {
      const templateName = prompt('Enter template name:', 'My Custom Template');
      if (!templateName) return;

      await uploadTemplate(file, templateName);
      toast.success('✓ Template uploaded successfully!');
      
      // Reload templates
      await loadTemplates();
    } catch (error) {
      toast.error(`Upload failed: ${error.message}`);
    } finally {
      setUploading(false);
      e.target.value = ''; // Reset input
    }
  };

  // When selected template or selectedOffers change, render a preview for the selected product
  useEffect(() => {
    const doPreview = async () => {
      // Only render preview when a template is selected AND the user has selected a product
      if (!selectedTemplate || !selectedOffers || selectedOffers.length === 0) {
        setPreviewHtml('');
        return;
      }

      const firstOfferId = selectedOffers[0];
      if (!firstOfferId) {
        setPreviewHtml('');
        return;
      }

      try {
        setPreviewLoading(true);
        const template = templates.find((t) => (t.id || t._id) === selectedTemplate);
        const layoutOptions = template?.layout_options || {};
        
        // Inject branding into layout options
        if (selectedBrand) {
          layoutOptions.branding = selectedBrand;
        }
        
        const resp = await previewPDF([firstOfferId], selectedTemplate, layoutOptions);
        setPreviewHtml(resp.html_preview || '');
      } catch (err) {
        console.error('Template preview failed', err.message || err);
        toast.error(`Template preview failed: ${err.message || err}`);
        setPreviewHtml('');
      } finally {
        setPreviewLoading(false);
      }
    };

    doPreview();
  }, [selectedTemplate, selectedOffers, templates, selectedBrand]);

  // Listen for size messages from iframe preview and apply height
  useEffect(() => {
    const handler = (e) => {
      try {
        const data = e.data || {};
        if (data && data.type === 'template-preview-size' && iframeRef.current) {
          const h = parseInt(data.height, 10) || 480;
          iframeRef.current.style.height = (h + 16) + 'px';
        }
      } catch (err) {
        // ignore
      }
    };

    window.addEventListener('message', handler);
    return () => window.removeEventListener('message', handler);
  }, []);

  return (
    <div className="relative z-20 bg-white rounded-2xl shadow-md p-6 md:p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Template Manager</h2>

      {/* Loading State */}
      {loading ? (
        <div className="text-center py-8 text-gray-600">
          ⏳ Loading templates...
        </div>
      ) : (
        <>
          {/* Template Selection */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Select Template:
            </label>
            <select
              value={selectedTemplate || ''}
              onChange={(e) => handleTemplateChange(e.target.value)}
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
            >
              <option value="">-- Choose a template --</option>
              {templates.map((template) => {
                const templateId = template.id || template._id;
                return (
                  <option key={templateId} value={templateId}>
                    {template.is_preset ? '⭐' : '📦'} {template.name}
                  </option>
                );
              })}
            </select>
          </div>

          {/* Template Info */}
          {selectedTemplate && templates.length > 0 && (
            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">
              {(() => {
                const template = templates.find(t => (t.id || t._id) === selectedTemplate);
                return template ? (
                  <>
                    <h3 className="font-semibold text-gray-800 mb-1">{template.name}</h3>
                    <p className="text-sm text-gray-600">{template.description}</p>
                    {template.layout_options && (
                      <div className="text-xs text-gray-600 mt-2">
                        {(() => {
                          const lo = template.layout_options || {};
                          const ps = lo.pageSize;
                          let sizeLabel = '';
                          if (typeof ps === 'string') {
                            sizeLabel = ps;
                          } else if (ps && typeof ps === 'object') {
                            const w = ps.width != null ? String(ps.width) : '';
                            const h = ps.height != null ? String(ps.height) : '';
                            sizeLabel = [w, h].filter(Boolean).join(' × ');
                          } else {
                            sizeLabel = 'Custom';
                          }
                          const perPage = lo.perPage != null ? lo.perPage : '-';
                          return (
                            <>
                              Layout: {sizeLabel} ({perPage} per page)
                            </>
                          );
                        })()}
                      </div>
                    )}
                    
                    {/* Branding Selection */}
                    {brands.length > 0 && (
                      <div className="mt-4">
                        <label className="block text-xs font-semibold text-gray-700 mb-2">
                          Brand Selection:
                        </label>
                        <select
                          value={selectedBrand?.id || ''}
                          onChange={(e) => {
                            const brand = brands.find(b => b.id === e.target.value);
                            if (onBrandSelect) onBrandSelect(brand);
                          }}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:border-blue-500 focus:outline-none text-sm"
                        >
                          {brands.map((brand) => (
                            <option key={brand.id} value={brand.id}>
                              {brand.name}
                            </option>
                          ))}
                        </select>
                        {selectedBrand && (
                          <div className="mt-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                            {/* Logo Preview */}
                            {selectedBrand.logo_url && (
                              <div className="mb-3 pb-3 border-b border-gray-300">
                                <span className="text-xs font-semibold text-gray-700 block mb-2">Logo Preview:</span>
                                <div className="bg-gradient-to-r from-blue-500 to-blue-700 p-3 rounded flex items-center justify-center" style={{
                                  background: `linear-gradient(180deg, ${selectedBrand.colors?.primary || '#5074F3'} 0%, ${selectedBrand.colors?.accent || '#2F448D'} 100%)`
                                }}>
                                    <img
                                      src={selectedBrand.logo_url ? encodeURI(`${API_BASE}${selectedBrand.logo_url}`) : ''}
                                      alt={selectedBrand.name}
                                      className="max-h-12 max-w-full object-contain"
                                      style={{ filter: (selectedBrand.logo_url || '').toLowerCase().endsWith('.svg') ? 'brightness(0) invert(1)' : 'none' }}
                                      onError={(e) => {
                                        // If image fails to load, remove filter and show broken image so user can detect issue
                                        e.target.style.filter = 'none';
                                      }}
                                    />
                                </div>
                              </div>
                            )}
                            {/* Color Info */}
                            <div className="mb-2">
                              <div className="flex items-center gap-2 text-xs">
                                <span className="font-semibold text-gray-700">Primary:</span>
                                <div 
                                  className="w-5 h-5 rounded border border-gray-300 shadow-sm" 
                                  style={{ backgroundColor: selectedBrand.colors?.primary || '#5074F3' }}
                                ></div>
                                <span className="text-gray-600 font-mono">{selectedBrand.colors?.primary || '#5074F3'}</span>
                              </div>
                            </div>
                            <div className="mb-2">
                              <div className="flex items-center gap-2 text-xs">
                                <span className="font-semibold text-gray-700">Accent:</span>
                                <div 
                                  className="w-5 h-5 rounded border border-gray-300 shadow-sm" 
                                  style={{ backgroundColor: selectedBrand.colors?.accent || '#2F448D' }}
                                ></div>
                                <span className="text-gray-600 font-mono">{selectedBrand.colors?.accent || '#2F448D'}</span>
                              </div>
                            </div>
                            {/* Font Info */}
                            <div className="text-xs pt-2 border-t border-gray-300">
                              <div className="flex items-start gap-2">
                                <span className="font-semibold text-gray-700">Fonts:</span>
                                <div className="flex-1">
                                  <div className="text-gray-600">
                                    <span className="font-medium">Heading:</span> {selectedBrand.fonts?.heading?.replace(/['"]/g, '').split(',')[0] || 'Barlow Condensed'}
                                  </div>
                                  <div className="text-gray-600">
                                    <span className="font-medium">Body:</span> {selectedBrand.fonts?.body?.replace(/['"]/g, '').split(',')[0] || 'DM Sans'}
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                    
                    {/* Allow editing pageSize (width/height) on the selected template */}
                    <div className="mt-3">
                      {(() => {
                        const lo = template.layout_options || {};
                        const ps = lo.pageSize;
                        let defaultW = '';
                        let defaultH = '';
                        if (ps && typeof ps === 'object') {
                          defaultW = ps.width ? String(ps.width).replace(/mm$/i, '') : '';
                          defaultH = ps.height ? String(ps.height).replace(/mm$/i, '') : '';
                        }

                        return (
                          <div className="grid grid-cols-2 gap-2 items-end">
                            <div>
                              <label className="text-xs text-gray-600">Width (mm)</label>
                              <input type="text" defaultValue={defaultW} id={`tpl-w-${template.id || template._id}`} className="w-full mt-1 px-2 py-1 border rounded" />
                            </div>
                            <div>
                              <label className="text-xs text-gray-600">Height (mm)</label>
                              <input type="text" defaultValue={defaultH} id={`tpl-h-${template.id || template._id}`} className="w-full mt-1 px-2 py-1 border rounded" />
                            </div>
                            <div className="col-span-2 mt-2">
                              <button
                                onClick={async () => {
                                  try {
                                    const w = document.getElementById(`tpl-w-${template.id || template._id}`).value.trim();
                                    const h = document.getElementById(`tpl-h-${template.id || template._id}`).value.trim();
                                    if (!w && !h) {
                                      toast.error('Enter width or height to update');
                                      return;
                                    }
                                    const pageSize = {};
                                    if (w) pageSize.width = w.toString().endsWith('mm') ? w : `${w}mm`;
                                    if (h) pageSize.height = h.toString().endsWith('mm') ? h : `${h}mm`;

                                    const newLayout = Object.assign({}, template.layout_options || {});
                                    newLayout.pageSize = pageSize;

                                    await updateTemplateLayout(template.id || template._id, newLayout);
                                    toast.success('✓ Template layout updated');
                                    // Update local templates state so UI reflects change without reloading and losing selection
                                    try {
                                      const updatedTemplates = (templates || []).map(t => {
                                        const tid = t.id || t._id;
                                        if (tid === (template.id || template._id)) {
                                          return Object.assign({}, t, { layout_options: newLayout });
                                        }
                                        return t;
                                      });
                                      setTemplates(updatedTemplates);
                                    } catch (e) {
                                      // fallback to reload if local update fails
                                      await loadTemplates();
                                    }
                                  } catch (err) {
                                    console.error('Update failed', err);
                                    toast.error('Failed to update template');
                                  }
                                }}
                                className="px-3 py-2 bg-green-600 text-white rounded-md"
                              >
                                Save Layout
                              </button>
                            </div>
                          </div>
                        );
                      })()}
                    </div>
                  </>
                ) : null;
              })()}
            </div>
          )}

          {/* Template Preview - just below template info and above upload */}
          {selectedTemplate && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Template Preview</h3>
              <div className="border rounded-md overflow-hidden ">
                {previewLoading ? (
                  <div className="p-8 text-center text-gray-600">⏳ Rendering preview...</div>
                ) : previewHtml ? (
                  (() => {
                    // Wrap previewHtml to ensure consistent background, fonts and full-block display
                    // Include a small script that measures content size and posts it to the parent for auto-resize and scaling
                    const framed = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1" /><style>
                        html,body{height:100%;margin:0;font-family:Inter, Arial, Helvetica, sans-serif;background:#ffffff;color:#111}
                        img{max-width:100%;height:auto;display:block}
                        *{box-sizing:border-box}
                        /* Force top-level elements to expand to full width when possible */
                        body > * {max-width:100% !important; margin-left:auto !important; margin-right:auto !important}
                        </style></head><body>
                          <div id="__preview_root">${previewHtml}</div>
                          <script>
                            (function(){
                              function fit(){
                                try{
                                  var root = document.getElementById('__preview_root');
                                  if(!root) root = document.body;
                                  // Measure intrinsic size
                                  var contentWidth = root.scrollWidth || document.documentElement.scrollWidth || document.body.scrollWidth;
                                  var contentHeight = root.scrollHeight || document.documentElement.scrollHeight || document.body.scrollHeight;
                                  var viewportWidth = window.innerWidth || document.documentElement.clientWidth;
                                  var scale = 1;
                                  if(contentWidth > viewportWidth && contentWidth > 0){
                                    scale = viewportWidth / contentWidth;
                                    root.style.transform = 'scale(' + scale + ')';
                                    root.style.transformOrigin = 'top left';
                                  }
                                  // calculate scaled height
                                  var scaledHeight = Math.ceil((contentHeight || document.body.scrollHeight) * scale);
                                  document.body.style.height = scaledHeight + 'px';
                                  // post message to parent with computed height
                                  window.parent.postMessage({ type: 'template-preview-size', height: scaledHeight }, '*');
                                }catch(e){
                                  // ignore
                                }
                              }
                              window.addEventListener('load', function(){ setTimeout(fit, 50); });
                              window.addEventListener('resize', fit);
                              setTimeout(fit, 200);
                            })();
                          </script>
                      </body></html>`;
                      return (
                        <iframe
                          ref={iframeRef}
                          title="template-preview"
                          srcDoc={framed}
                          style={{ width: '100%', height: 480, border: 'none' }}
                        />
                      );
                  })()
                ) : (
                  <div className="p-6 text-center text-gray-500">No preview available</div>
                )}
              </div>
            </div>
          )}

          {/* Upload Custom Template */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3">Upload Custom Template</h3>
            <p className="text-sm text-gray-600 mb-4">
              Upload a ZIP file containing your HTML template and CSS files.
            </p>
            
            <label className="block">
              <input
                type="file"
                accept=".zip"
                onChange={handleTemplateUpload}
                disabled={uploading}
                className="hidden"
              />
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center cursor-pointer hover:border-gray-400 transition-colors">
                {uploading ? (
                  <div className="text-gray-600">⏳ Uploading...</div>
                ) : (
                  <>
                    <div className="text-gray-600 font-semibold mb-1">📦 Choose ZIP File</div>
                    <div className="text-xs text-gray-500">or drag and drop</div>
                  </>
                )}
              </div>
            </label>
          </div>

          {/* Template Info */}
          <div className="bg-gray-50 border-l-4 border-gray-400 p-4 mt-6">
            <p className="text-xs text-gray-600">
              <strong>💡 Tip:</strong> Your template should use Jinja2 syntax. Use {'{{ offer.field }}'} to reference offer data.
            </p>
          </div>
        </>
      )}
    </div>
  );
}
