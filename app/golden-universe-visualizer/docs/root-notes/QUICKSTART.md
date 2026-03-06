# Quick Start Guide

Welcome to the Golden Universe Visualizer! This guide will help you get the application running in minutes.

## Prerequisites

- Node.js 18+ (recommended: Node.js 20+ for optimal Vite performance)
- npm 8+

## Installation & Setup

1. **Navigate to the project directory**
   ```bash
   cd "/Users/Cristiana_1/Documents/Golden Universe/app/golden-universe-visualizer"
   ```

2. **Install dependencies** (if not already done)
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**

   The application should automatically open at `http://localhost:3000`

   If it doesn't open automatically, navigate to: http://localhost:3000

## What You'll See

When you first launch the application, you'll see:

- **Home Page**: An overview of the Golden Universe Visualizer with feature cards
- **Sidebar Navigation**: A collapsible left sidebar with sections for:
  - Theory
  - Derivations
  - Calculations
  - Visualizations
- **Dark Theme**: The application uses a golden-themed dark mode by default

## Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Check TypeScript types
npm run type-check
```

## Project Structure Overview

```
src/
├── components/       # React components
│   ├── Sidebar/     # Navigation sidebar
│   └── Layout/      # Layout components
├── pages/           # Page components (Home, Theory, etc.)
├── services/        # API service layer
├── utils/           # Utilities (store, constants, helpers)
├── styles/          # Global SCSS styles
└── types/           # TypeScript type definitions
```

## Key Features

- **React Router**: Navigate between sections using the sidebar
- **Zustand Store**: Global state management for theme, sidebar, etc.
- **TypeScript**: Fully typed for better development experience
- **SCSS**: Styled with SCSS using Golden Ratio-based spacing
- **Path Aliases**: Clean imports using `@/` prefix

## Customization

### Change Theme

The theme is managed in Zustand store (`src/utils/store.ts`). The default is dark mode.

### Modify Navigation

Edit the navigation structure in `src/utils/constants.ts` (`NAVIGATION_ITEMS` array).

### API Configuration

Configure API endpoints in `.env`:
```
VITE_API_BASE_URL=http://localhost:3000/api
```

## Next Steps

1. Explore the codebase structure
2. Add content to the placeholder pages (Theory, Derivations, etc.)
3. Implement visualizations using Canvas or WebGL
4. Connect to a backend API for dynamic data

## Troubleshooting

**Port already in use?**
- Edit `vite.config.ts` and change the port number

**Node version warning?**
- Upgrade to Node.js 20+ for best results
- The app will still work with Node.js 18, but you'll see warnings

**Build errors?**
- Run `npm run type-check` to see TypeScript errors
- Run `npm run lint` to check for linting issues

## Need Help?

Check the main README.md for detailed documentation, or review the code comments for inline guidance.

Happy coding!
