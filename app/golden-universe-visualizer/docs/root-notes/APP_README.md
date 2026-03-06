# Golden Universe Visualizer

Interactive visualization and exploration of the Golden Ratio and its mathematical properties.

## Features

- **Theory**: Explore the mathematical foundations of the Golden Ratio
- **Derivations**: Step-by-step mathematical derivations
- **Calculations**: Interactive calculators for Golden Ratio computations
- **Visualizations**: Beautiful interactive visualizations

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Zustand** - State management
- **Axios** - HTTP client
- **SCSS** - Styling with variables and nesting
- **ESLint & Prettier** - Code quality and formatting

## Getting Started

### Prerequisites

- Node.js 18+ (recommended: 20+)
- npm 8+

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env
```

### Development

```bash
# Start development server (http://localhost:3000)
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint
npm run lint:fix

# Formatting
npm run format
npm run format:check
```

### Build

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/          # React components
│   ├── Sidebar/        # Navigation sidebar
│   ├── Layout/         # Layout components
│   ├── Theory/         # Theory section components
│   ├── Derivations/    # Derivations section components
│   ├── Calculations/   # Calculations section components
│   └── Visualizations/ # Visualization components
├── pages/              # Page components (routes)
├── services/           # API services
├── utils/              # Utility functions and constants
│   ├── store.ts        # Zustand state management
│   ├── constants.ts    # App constants
│   └── helpers.ts      # Helper functions
├── styles/             # Global styles
│   ├── globals.scss    # Global styles
│   ├── variables.scss  # SCSS variables
│   └── reset.scss      # CSS reset
├── types/              # TypeScript type definitions
└── App.tsx             # Main app component with routing
```

## Architecture

The application follows a ContextLoom-inspired design with:

- **Left Sidebar Navigation**: Collapsible sidebar with hierarchical navigation
- **Component-based Architecture**: Modular, reusable components
- **Type-safe Development**: Strict TypeScript configuration
- **State Management**: Zustand for global state with persistence
- **Path Aliases**: Clean imports using @ prefix
- **Dark Theme**: Default dark theme with golden accent colors

## Configuration

### TypeScript

Strict TypeScript configuration with:
- Strict null checks
- No implicit any
- No unused locals/parameters
- Path aliases for clean imports

### ESLint

- TypeScript ESLint plugin
- React and React Hooks plugins
- Prettier integration for code formatting

### Environment Variables

See `.env.example` for available configuration options:
- `VITE_API_BASE_URL` - API endpoint
- `VITE_APP_NAME` - Application name
- `VITE_APP_VERSION` - Application version

## Design System

Based on the Golden Ratio (φ ≈ 1.618):

- **Spacing**: Scale based on φ (0.382rem, 0.618rem, 1rem, 1.618rem, 2.618rem)
- **Colors**: Golden accent colors (#c9a84e, #ffd700)
- **Theme**: Dark mode with high contrast

## Scripts Reference

- `npm run dev` - Start development server
- `npm run build` - Create production build
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - Run TypeScript type checking
- `npm test` - Run tests (placeholder)

## License

See LICENSE file in the project root.

## Contributing

See CONTRIBUTING.md in the project root.
