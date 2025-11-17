import axios from 'axios';

// API base URL - adjust for your environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handling interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred';
    console.error('API Error:', message);
    return Promise.reject(new Error(message));
  }
);

/**
 * Upload CSV file containing offers
 * @param {File} file - CSV file to upload
 * @returns {Promise} Response with inserted_count and preview
 */
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/offers/upload-csv`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

/**
 * Fetch paginated list of offers
 * @param {number} skip - Number of offers to skip
 * @param {number} limit - Number of offers to return
 * @returns {Promise} Response with offers and total count
 */
export const fetchOffers = async (skip = 0, limit = 50) => {
  return api.get('/offers', { params: { skip, limit } });
};

/**
 * Fetch a single offer by ID
 * @param {string} offerId - MongoDB ObjectId
 * @returns {Promise} Offer document
 */
export const fetchOfferById = async (offerId) => {
  return api.get(`/offers/${offerId}`);
};

/**
 * Clear all offers from database
 * WARNING: This action cannot be undone
 * @returns {Promise} Response with deleted_count
 */
export const clearAllOffers = async () => {
  return api.post('/offers/clear-all');
};

/**
 * Upload custom template as ZIP
 * @param {File} file - ZIP file containing template
 * @param {string} name - Template name
 * @returns {Promise} Response with template_id and file_path
 */
export const uploadTemplate = async (file, name = 'Custom Template') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);
  
  const response = await axios.post(`${API_BASE_URL}/templates/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

/**
 * Fetch all available templates
 * @returns {Promise} Response with list of templates
 */
export const fetchTemplates = async () => {
  return api.get('/templates');
};

/**
 * Fetch only preset templates
 * @returns {Promise} Response with preset templates
 */
export const fetchPresetTemplates = async () => {
  return api.get('/templates/preset');
};

/**
 * Fetch a single template by ID
 * @param {string} templateId - MongoDB ObjectId
 * @returns {Promise} Template document with content
 */
export const fetchTemplateById = async (templateId) => {
  return api.get(`/templates/${templateId}`);
};

/**
 * Update layout options for a template
 * @param {string} templateId
 * @param {Object} layoutOptions
 */
export const updateTemplateLayout = async (templateId, layoutOptions) => {
  return api.put(`/templates/${templateId}/layout`, layoutOptions);
};

/**
 * Generate PDF with selected offers
 * @param {Array<string>} offerIds - List of offer IDs
 * @param {string} templateId - Template to use
 * @param {Object} layoutOptions - Layout configuration
 * @returns {Promise} Response with pdf_url and file_path
 */
export const generatePDF = async (offerIds, templateId, layoutOptions = null) => {
  return api.post('/pdf/generate', {
    offer_ids: offerIds,
    template_id: templateId,
    layout_options: layoutOptions,
  });
};

/**
 * Preview PDF (generate without saving)
 * @param {Array<string>} offerIds - List of offer IDs (first one used for preview)
 * @param {string} templateId - Template to use
 * @returns {Promise} Response with html_preview
 */
export const previewPDF = async (offerIds, templateId, layoutOptions = null) => {
  return api.post('/pdf/preview', {
    offer_ids: offerIds,
    template_id: templateId,
    layout_options: layoutOptions,
  });
};

export default api;
