# Deployment Quick Start Guide

Get your Golden Universe Visualizer deployed in minutes!

## Prerequisites

- Node.js 20.x or higher installed
- Git repository set up
- Account on Vercel or Netlify (free tier works)

## Step 1: Prepare Your Environment (2 minutes)

```bash
# Copy environment template
cp .env.example .env.production.local

# Edit with your values (use any text editor)
nano .env.production.local
```

**Minimum required variables:**
```env
VITE_API_BASE_URL=https://your-api-url.com/api
VITE_APP_NAME=Golden Universe Visualizer
VITE_APP_VERSION=1.0.0
```

**Optional but recommended:**
```env
VITE_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
VITE_SENTRY_DSN=https://your-key@sentry.io/project-id
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_SENTRY=true
```

## Step 2: Choose Your Deployment Method

### Option A: Vercel (Fastest - 1 minute)

#### Method 1: One-Click Deploy
1. Click: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/golden-universe-visualizer)
2. Connect your GitHub account
3. Add environment variables in the UI
4. Click "Deploy"
5. Done! Your app is live

#### Method 2: CLI Deploy
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### Option B: Netlify (2 minutes)

#### Method 1: One-Click Deploy
1. Click: [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/golden-universe-visualizer)
2. Connect your GitHub account
3. Configure build settings (pre-configured in netlify.toml)
4. Add environment variables
5. Deploy

#### Method 2: CLI Deploy
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Initialize
netlify init

# Deploy
netlify deploy --prod
```

### Option C: Docker (5 minutes)

```bash
# Build the image
docker build -t golden-universe-visualizer .

# Run the container
docker run -d -p 3000:3000 -p 3001:3001 \
  -e VITE_API_BASE_URL=https://your-api.com/api \
  --name golden-universe \
  golden-universe-visualizer

# Check it's running
docker ps

# View logs
docker logs golden-universe
```

Visit http://localhost:3000

## Step 3: Configure GitHub Actions (Optional - 5 minutes)

Automatic deployments on every push to main:

1. **Go to GitHub Settings**
   - Settings → Secrets and variables → Actions

2. **Add Secrets for Vercel** (if using Vercel):
   ```
   VERCEL_TOKEN
   VERCEL_ORG_ID
   VERCEL_PROJECT_ID
   VITE_API_BASE_URL
   VITE_GOOGLE_ANALYTICS_ID
   VITE_SENTRY_DSN
   ```

3. **Or Add Secrets for Netlify** (if using Netlify):
   ```
   NETLIFY_AUTH_TOKEN
   NETLIFY_SITE_ID
   VITE_API_BASE_URL
   VITE_GOOGLE_ANALYTICS_ID
   VITE_SENTRY_DSN
   ```

4. **Push to main branch**
   ```bash
   git add .
   git commit -m "Configure deployment"
   git push origin main
   ```

5. **Watch it deploy**
   - Go to Actions tab in GitHub
   - See your deployment in progress

## Step 4: Verify Deployment (2 minutes)

### Check These:
- [ ] Application loads at your deployment URL
- [ ] No console errors (press F12 → Console)
- [ ] Navigation works (click around)
- [ ] Visualizations render correctly
- [ ] Mobile view looks good (press F12 → Toggle device toolbar)

### Quick Test:
```bash
# Check if site is up
curl -I https://your-deployment-url.com

# Should return: HTTP/2 200
```

## Step 5: Set Up Monitoring (Optional - 5 minutes)

### Google Analytics
1. Go to [analytics.google.com](https://analytics.google.com)
2. Create a GA4 property
3. Copy Measurement ID (G-XXXXXXXXXX)
4. Add to environment variables
5. Redeploy

### Sentry
1. Go to [sentry.io](https://sentry.io)
2. Create a project
3. Copy DSN
4. Add to environment variables
5. Redeploy

## Common Issues & Quick Fixes

### Issue: Build fails with "out of memory"
```bash
# Solution: Increase Node memory
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

### Issue: Environment variables not working
- Make sure they start with `VITE_`
- Check they're added in your platform's UI
- Redeploy after adding variables

### Issue: Page refreshes give 404
- Vercel: Already configured in vercel.json
- Netlify: Already configured in netlify.toml
- Other: Configure SPA fallback routing

### Issue: API requests failing
- Check CORS settings on your API
- Verify VITE_API_BASE_URL is correct
- Check API is accessible from deployment

## Performance Check

After deployment, test performance:

1. **Open Lighthouse** (in Chrome DevTools)
2. **Run audit** in "Production" mode
3. **Target scores:**
   - Performance: > 90
   - Accessibility: > 90
   - Best Practices: > 90
   - SEO: > 90

If scores are low, see PERFORMANCE_OPTIMIZATION.md

## Next Steps

1. **Set up custom domain** (in Vercel/Netlify dashboard)
2. **Enable SSL** (automatic on Vercel/Netlify)
3. **Configure monitoring alerts**
4. **Share your deployment!**

## Deployment Commands Cheat Sheet

```bash
# Local development
npm start                    # Start dev server
npm run build               # Build for production
npm run preview             # Preview production build

# Production builds
npm run build:production    # Build with production env
npm run build:staging       # Build with staging env
npm run build:analyze       # Build and open analyzer

# Deployment
npm run deploy:vercel       # Deploy to Vercel
npm run deploy:netlify      # Deploy to Netlify

# Pre-deployment checks
./scripts/deploy-check.sh   # Run all checks
npm run lint                # Check code quality
npm run type-check          # Check TypeScript
npm test                    # Run tests

# Docker
docker-compose up -d        # Start with docker-compose
docker-compose logs -f      # View logs
docker-compose down         # Stop services
```

## Getting Help

- **Documentation**: See DEPLOYMENT.md for detailed guides
- **Checklist**: Use PRODUCTION_CHECKLIST.md before deploying
- **Issues**: Check GitHub Issues
- **Questions**: Open a GitHub Discussion

## Success!

Your Golden Universe Visualizer should now be live! 🎉

**Share your deployment:**
- Tweet about it
- Show it to friends
- Add to your portfolio
- Submit to showcases

---

**Deployment Time:** ~10 minutes total
**Difficulty:** Easy
**Cost:** Free (with free tier plans)

Happy deploying! 🚀
