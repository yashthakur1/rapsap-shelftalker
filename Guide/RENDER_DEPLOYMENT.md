# Deploy Frontend on Render

## Step-by-Step Instructions

### 1. Connect Your GitHub Repository
- Go to [render.com](https://render.com)
- Click **"New +"** → **"Web Service"**
- Connect your GitHub account and select the `rapsap-shelftalker` repository
- Choose your branch (main)

### 2. Configure the Service
- **Name**: `aops-frontend` (or your preferred name)
- **Environment**: Static Site
- **Build Command**: `cd aops/frontend && npm install && npm run build`
- **Publish Directory**: `aops/frontend/dist`

### 3. Set Environment Variables
Add this in the Render dashboard under "Environment":
```
VITE_API_URL=https://your-backend-url.com
```
Replace `your-backend-url.com` with your actual backend URL (if deployed on Render or elsewhere).

### 4. Deploy
- Click **"Create Web Service"**
- Render will automatically build and deploy your frontend
- Your site will be available at: `https://aops-frontend.onrender.com` (or custom domain)

## Auto-Deploy on Push
Render automatically redeploys whenever you push to the selected branch.

## Custom Domain
1. Go to Service Settings → Custom Domain
2. Add your domain (e.g., `aops.yourdomain.com`)
3. Follow DNS configuration instructions

## Environment Variables in Production
Make sure to set `VITE_API_URL` to your production backend URL in Render dashboard under Environment variables.

## Troubleshooting

**Build fails?**
- Check that `aops/frontend/package.json` exists
- Verify `npm run build` works locally: `npm run build`
- Check build logs in Render dashboard

**Frontend can't reach backend?**
- Verify `VITE_API_URL` is set correctly in Render environment
- Ensure backend has CORS enabled for your Render domain
- Check browser console for API errors

**Static files not loading?**
- Verify "Publish Directory" is set to `aops/frontend/dist`
- Ensure `render.yaml` is in repository root (optional but recommended)

## Alternative: Use render.yaml (Recommended)
The `render.yaml` file in your repository root provides Infrastructure as Code:

```yaml
services:
  - type: web
    name: aops-frontend
    env: static
    buildCommand: cd aops/frontend && npm install && npm run build
    staticPublishPath: ./aops/frontend/dist
    routes:
      - path: /
        destination: /index.html
```

This allows one-click deployment via `render.yaml` instead of manual configuration.

## Quick Deployment Checklist
- ✅ GitHub repository connected to Render
- ✅ Build command: `cd aops/frontend && npm install && npm run build`
- ✅ Publish directory: `aops/frontend/dist`
- ✅ `VITE_API_URL` environment variable set
- ✅ Backend CORS configured for your Render domain
- ✅ Custom domain configured (optional)
