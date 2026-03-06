# Multi-stage production Dockerfile for Golden Universe Visualizer

# Stage 1: Build the application
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies for native modules
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production=false

# Copy application source
COPY . .

# Build the application
ARG VITE_API_BASE_URL
ARG VITE_GOOGLE_ANALYTICS_ID
ARG VITE_SENTRY_DSN
ARG COMMIT_SHA
ENV NODE_ENV=production

RUN npm run build

# Stage 2: Build the backend server
FROM node:20-alpine AS server-builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.server.json ./

# Install dependencies
RUN npm ci --only=production=false

# Copy server source
COPY server ./server

# Build server
RUN npm run server:build

# Stage 3: Production runtime
FROM node:20-alpine AS runtime

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create app user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy built files from builder stages
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=server-builder --chown=nodejs:nodejs /app/server/dist ./server/dist

# Copy necessary files
COPY --chown=nodejs:nodejs package*.json ./
COPY --chown=nodejs:nodejs server/database ./server/database

# Install production dependencies only
RUN npm ci --only=production && npm cache clean --force

# Switch to nodejs user
USER nodejs

# Expose ports
EXPOSE 3000 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1); });"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start the application
CMD ["node", "server/dist/server.js"]
