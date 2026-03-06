# Deployment Guide for Golden Universe Visualizer

## Dual Environment Setup

This application supports two content delivery modes:
- **Local Development**: Reads content from local file system
- **Production (Vercel)**: Fetches content from GitHub repository

## Environment Configuration

### Local Development (.env.local)

```env
# Use local file system for content
NEXT_PUBLIC_CONTENT_SOURCE=local
CONTENT_BASE_PATH=../../

# Optional: GitHub token for higher API rate limits (if testing GitHub mode locally)
# GITHUB_TOKEN=your_github_token_here
```

### Production (Vercel)

Set these environment variables in your Vercel project:

```env
# Use GitHub for content
NEXT_PUBLIC_CONTENT_SOURCE=github
GITHUB_OWNER=vicovanc
GITHUB_REPO=goldenuniverse
GITHUB_BRANCH=main

# Optional: GitHub token for higher API rate limits
GITHUB_TOKEN=your_github_token_here
```

## GitHub Repository Structure

Your GitHub repository (https://github.com/vicovanc/goldenuniverse) should have this structure:

```
goldenuniverse/
├── derivations/           # Mathematical derivations
│   ├── 01_FORCE_UNIFICATION/
│   ├── 02_FUNDAMENTAL_CONSTANTS/
│   └── ...
├── theory/               # Theory documentation
│   ├── laws/
│   ├── explanations/
│   └── ...
├── visualizations/       # Visualization data
│   └── ...
└── app/                 # Application folder
    └── golden-universe-visualizer/
        ├── src/
        ├── server/
        ├── package.json
        └── ...
```

## Deployment to Vercel

### 1. Prepare Your Repository

1. Push your entire Golden Universe folder to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/vicovanc/goldenuniverse.git
   git push -u origin main
   ```

2. Ensure the repository is public (as specified)

### 2. Deploy to Vercel

1. Go to [Vercel](https://vercel.com) and sign in with GitHub

2. Click "New Project" and import your GitHub repository

3. Configure the project:
   - **Framework Preset**: Vite
   - **Root Directory**: `app/golden-universe-visualizer`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. Set Environment Variables:
   - `NEXT_PUBLIC_CONTENT_SOURCE`: `github`
   - `GITHUB_OWNER`: `vicovanc`
   - `GITHUB_REPO`: `goldenuniverse`
   - `GITHUB_BRANCH`: `main`
   - `GITHUB_TOKEN`: (optional, for higher rate limits)

5. Deploy!

### 3. API Routes on Vercel

The Express server will be automatically converted to Vercel Functions. Create a `vercel.json` file if needed:

```json
{
  "functions": {
    "api/index.js": {
      "maxDuration": 10
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api" }
  ]
}
```

## How It Works

### Content Service

The `server/contentService.ts` file handles dual-mode content fetching:

- **Local Mode**: Reads files directly from the file system using Node.js `fs` module
- **GitHub Mode**: Fetches files using GitHub API (public repository access)

### API Endpoints

All API endpoints automatically use the content service and work in both modes:
- `/api/derivations` - Lists all derivations
- `/api/derivations/:id` - Get specific derivation
- `/api/derivations/folder/:name/files` - List files in derivation folder
- `/api/derivations/folder/:name/file/:filename` - Get file content

The response includes a `source` field indicating whether content came from "local" or "github".

## Testing

### Test Local Mode
```bash
# Set environment for local mode
cp .env.local.example .env.local
npm run dev
npm run server:dev

# Test API
curl http://localhost:3001/api/derivations
```

### Test GitHub Mode Locally
```bash
# Edit .env.local
NEXT_PUBLIC_CONTENT_SOURCE=github
GITHUB_OWNER=vicovanc
GITHUB_REPO=goldenuniverse
GITHUB_BRANCH=main

# Restart servers
npm run dev
npm run server:dev

# Test API
curl http://localhost:3001/api/derivations
```

## Troubleshooting

### GitHub API Rate Limits
- Public repositories: 60 requests/hour without token
- With token: 5000 requests/hour
- Add `GITHUB_TOKEN` environment variable for higher limits

### Vercel Build Fails
- Check Node.js version compatibility
- Ensure all dependencies are in `package.json`
- Check build logs for specific errors

### Content Not Loading
- Verify environment variables are set correctly
- Check GitHub repository is public
- Confirm folder structure matches expected paths
- Check browser console for API errors

## Security Notes

- Never commit `.env.local` file
- Use Vercel's environment variables UI for production secrets
- GitHub tokens should have minimal required permissions
- Consider using GitHub App instead of personal access token for production