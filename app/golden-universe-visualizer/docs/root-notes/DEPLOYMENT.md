# Deployment Guide

Complete guide for deploying the Golden Universe Visualizer to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Deployment Options](#deployment-options)
  - [Vercel (Recommended)](#vercel-deployment)
  - [Netlify](#netlify-deployment)
  - [Docker](#docker-deployment)
  - [Manual Deployment](#manual-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Analytics](#monitoring--analytics)
- [Post-Deployment](#post-deployment)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying, ensure you have:

- Node.js 20.x or higher
- npm or yarn package manager
- Git repository with your code
- Account on your chosen hosting platform (Vercel/Netlify)
- (Optional) Docker installed for containerized deployment
- (Optional) Google Analytics account
- (Optional) Sentry account for error tracking

## Environment Configuration

### 1. Copy Environment Files

```bash
# For production
cp .env.example .env.production.local

# For staging
cp .env.example .env.staging.local
```

### 2. Configure Environment Variables

Edit `.env.production.local` with your production values:

```env
# API Configuration
VITE_API_BASE_URL=https://api.golden-universe.app/api

# Application
VITE_APP_NAME=Golden Universe Visualizer
VITE_APP_VERSION=1.0.0
VITE_APP_ENV=production

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG_MODE=false
VITE_ENABLE_SENTRY=true

# Analytics
VITE_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
VITE_SENTRY_DSN=https://your-key@sentry.io/project-id
VITE_SENTRY_ENVIRONMENT=production
VITE_SENTRY_TRACES_SAMPLE_RATE=0.1
```

### 3. Required Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_BASE_URL` | Backend API URL | Yes | `https://api.example.com/api` |
| `VITE_GOOGLE_ANALYTICS_ID` | GA4 Measurement ID | No | `G-XXXXXXXXXX` |
| `VITE_SENTRY_DSN` | Sentry DSN for error tracking | No | `https://key@sentry.io/id` |

## Deployment Options

### Vercel Deployment

#### Option 1: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/golden-universe-visualizer)

#### Option 2: CLI Deployment

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy to Production**
   ```bash
   npm run deploy:vercel
   # or
   vercel --prod
   ```

4. **Configure Environment Variables**
   ```bash
   vercel env add VITE_API_BASE_URL production
   vercel env add VITE_GOOGLE_ANALYTICS_ID production
   vercel env add VITE_SENTRY_DSN production
   ```

#### Option 3: GitHub Integration

1. Import your repository in Vercel dashboard
2. Configure build settings:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add environment variables in Vercel dashboard
4. Deploy automatically on push to main branch

### Netlify Deployment

#### Option 1: One-Click Deploy

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/golden-universe-visualizer)

#### Option 2: CLI Deployment

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Initialize Site**
   ```bash
   netlify init
   ```

4. **Deploy to Production**
   ```bash
   npm run deploy:netlify
   # or
   netlify deploy --prod
   ```

#### Option 3: GitHub Integration

1. Connect repository in Netlify dashboard
2. Configure build settings (already set in `netlify.toml`)
3. Add environment variables in Netlify dashboard
4. Deploy automatically on push

### Docker Deployment

#### Build and Run Locally

```bash
# Build the image
docker build -t golden-universe-visualizer .

# Run the container
docker run -p 3000:3000 -p 3001:3001 \
  -e VITE_API_BASE_URL=https://api.example.com/api \
  golden-universe-visualizer
```

#### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Deploy to Cloud Platform

**AWS ECS:**
```bash
# Tag and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker tag golden-universe-visualizer:latest your-account.dkr.ecr.us-east-1.amazonaws.com/golden-universe:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/golden-universe:latest
```

**Google Cloud Run:**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/golden-universe
gcloud run deploy golden-universe --image gcr.io/your-project/golden-universe --platform managed
```

### Manual Deployment

For deploying to a traditional web server:

1. **Build the Application**
   ```bash
   npm run build:production
   ```

2. **Transfer Files**
   ```bash
   # The dist folder contains all static files
   rsync -avz dist/ user@server:/var/www/html/
   ```

3. **Configure Web Server**

   **Nginx:**
   ```nginx
   server {
     listen 80;
     server_name golden-universe.app;
     root /var/www/html;
     index index.html;

     # Compression
     gzip on;
     gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

     # Cache static assets
     location /assets/ {
       expires 1y;
       add_header Cache-Control "public, immutable";
     }

     # SPA fallback
     location / {
       try_files $uri $uri/ /index.html;
     }

     # Security headers
     add_header X-Frame-Options "DENY";
     add_header X-Content-Type-Options "nosniff";
     add_header X-XSS-Protection "1; mode=block";
   }
   ```

   **Apache:**
   ```apache
   <VirtualHost *:80>
     ServerName golden-universe.app
     DocumentRoot /var/www/html

     <Directory /var/www/html>
       Options -Indexes +FollowSymLinks
       AllowOverride All
       Require all granted

       # SPA fallback
       RewriteEngine On
       RewriteBase /
       RewriteRule ^index\.html$ - [L]
       RewriteCond %{REQUEST_FILENAME} !-f
       RewriteCond %{REQUEST_FILENAME} !-d
       RewriteRule . /index.html [L]
     </Directory>

     # Enable compression
     AddOutputFilterByType DEFLATE text/html text/css application/javascript
   </VirtualHost>
   ```

## CI/CD Pipeline

### GitHub Actions Workflows

The project includes three GitHub Actions workflows:

#### 1. CI/CD Pipeline (`.github/workflows/ci.yml`)

Runs on every push and PR:
- Linting and type checking
- Running tests
- Building the application
- Building Docker image (on main/develop)

#### 2. Vercel Deployment (`.github/workflows/deploy-vercel.yml`)

Automatic deployment to Vercel on push to main branch.

**Required Secrets:**
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `VITE_API_BASE_URL`
- `VITE_GOOGLE_ANALYTICS_ID`
- `VITE_SENTRY_DSN`

#### 3. Netlify Deployment (`.github/workflows/deploy-netlify.yml`)

Automatic deployment to Netlify on push to main branch.

**Required Secrets:**
- `NETLIFY_AUTH_TOKEN`
- `NETLIFY_SITE_ID`
- `VITE_API_BASE_URL`
- `VITE_GOOGLE_ANALYTICS_ID`
- `VITE_SENTRY_DSN`

### Setting Up GitHub Secrets

1. Go to repository Settings → Secrets and variables → Actions
2. Add required secrets for your deployment platform
3. Commit and push to trigger workflows

## Monitoring & Analytics

### Google Analytics Setup

1. Create a GA4 property at [analytics.google.com](https://analytics.google.com)
2. Copy your Measurement ID (format: `G-XXXXXXXXXX`)
3. Add to environment variables: `VITE_GOOGLE_ANALYTICS_ID`
4. Analytics will automatically initialize on app start

**Tracked Events:**
- Page views
- Visualization interactions
- Calculations
- Search queries
- Errors

### Sentry Error Tracking

1. Create a project at [sentry.io](https://sentry.io)
2. Copy your DSN
3. Add to environment variables: `VITE_SENTRY_DSN`
4. Configure sample rates as needed

**Features:**
- Error tracking
- Performance monitoring
- Session replay
- Release tracking

### Health Monitoring

The application includes a health check endpoint:

```bash
# Check application health
curl https://your-domain.com/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "version": "1.0.0",
  "uptime": 3600000,
  "checks": {
    "api": true,
    "database": true,
    "memory": true
  }
}
```

## Post-Deployment

### 1. Verify Deployment

- [ ] Application loads correctly
- [ ] All routes work (test SPA routing)
- [ ] API connectivity working
- [ ] Static assets loading (images, fonts)
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Performance is acceptable (Lighthouse score > 90)

### 2. Configure Custom Domain

**Vercel:**
```bash
vercel domains add golden-universe.app
```

**Netlify:**
```bash
netlify domains:add golden-universe.app
```

### 3. Set Up SSL/TLS

Both Vercel and Netlify provide automatic SSL certificates.

For manual deployment:
```bash
# Using Let's Encrypt with Certbot
sudo certbot --nginx -d golden-universe.app
```

### 4. Configure DNS

Point your domain to the deployment platform:

**Vercel:**
- Add A record: `76.76.21.21`
- Add CNAME: `cname.vercel-dns.com`

**Netlify:**
- Add A record: Check Netlify dashboard for IP
- Add CNAME: `your-site.netlify.app`

### 5. Set Up Monitoring Alerts

Configure alerts in Sentry, Google Analytics, or your hosting platform for:
- Error rate spikes
- Performance degradation
- Downtime
- High traffic

## Troubleshooting

### Build Fails

**Issue:** Build fails with "Out of memory"
```bash
# Solution: Increase Node memory
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

**Issue:** TypeScript errors
```bash
# Solution: Run type check first
npm run type-check
```

### Deployment Issues

**Issue:** Environment variables not working
- Ensure variables are prefixed with `VITE_`
- Check they're added in hosting platform
- Rebuild after adding variables

**Issue:** Routing not working (404 on refresh)
- Verify SPA fallback is configured
- Check `vercel.json` or `netlify.toml`
- Ensure web server redirects are set up

### Performance Issues

**Issue:** Slow initial load
- Check bundle size: `npm run build:analyze`
- Verify compression is enabled
- Check CDN configuration
- Optimize images

**Issue:** API requests failing
- Verify CORS headers
- Check API URL in environment
- Verify API is accessible from deployment

### Common Errors

**"Module not found"**
```bash
# Clear cache and rebuild
npm run clean
npm ci
npm run build
```

**"Failed to fetch"**
- Check API URL is correct
- Verify CORS configuration
- Check network tab in DevTools

## Performance Optimization

### Bundle Size Optimization

1. **Analyze bundle:**
   ```bash
   npm run build:analyze
   ```

2. **Code splitting:** Already configured in `vite.config.ts`

3. **Tree shaking:** Automatically handled by Vite

### Compression

Both Gzip and Brotli compression are enabled by default.

### CDN Configuration

For static assets, configure CDN in environment:
```env
VITE_CDN_URL=https://cdn.golden-universe.app
```

## Rollback Procedures

### Vercel
```bash
# List deployments
vercel ls

# Rollback to previous deployment
vercel rollback <deployment-url>
```

### Netlify
```bash
# List deployments
netlify deploy:list

# Restore deployment
netlify deploy:restore <deploy-id>
```

### Docker
```bash
# Rollback to previous image
docker pull golden-universe:previous-tag
docker-compose up -d
```

## Security Checklist

- [ ] Environment variables secured
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] CSP policy set
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Dependencies updated
- [ ] Secrets not committed to repo
- [ ] API endpoints authenticated
- [ ] Error messages don't expose sensitive info

## Support

For deployment issues:
1. Check this documentation
2. Review GitHub Issues
3. Contact the development team
4. Check hosting platform status page

---

**Last Updated:** 2024-01-01
**Version:** 1.0.0
