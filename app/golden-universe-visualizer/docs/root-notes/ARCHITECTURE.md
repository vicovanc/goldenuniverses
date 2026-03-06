# Golden Universe Visualizer - Architecture

Technical architecture and system design documentation for the Golden Universe Visualization Application.

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Application Structure](#application-structure)
4. [Component Architecture](#component-architecture)
5. [Data Flow](#data-flow)
6. [State Management](#state-management)
7. [Routing](#routing)
8. [API Design](#api-design)
9. [Performance Optimization](#performance-optimization)
10. [Security](#security)
11. [Deployment](#deployment)

## System Overview

The Golden Universe Visualizer is a modern single-page application (SPA) built with React and TypeScript, designed to provide an interactive exploration platform for the Golden Universe Theory and its mathematical foundations.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Client Browser                     │
│  ┌──────────────────────────────────────────────┐  │
│  │        React Application (SPA)                │  │
│  │  ┌────────────┐  ┌────────────┐              │  │
│  │  │   Pages    │  │ Components │              │  │
│  │  └────────────┘  └────────────┘              │  │
│  │  ┌────────────┐  ┌────────────┐              │  │
│  │  │   State    │  │   Hooks    │              │  │
│  │  └────────────┘  └────────────┘              │  │
│  │  ┌────────────┐  ┌────────────┐              │  │
│  │  │  Services  │  │   Utils    │              │  │
│  │  └────────────┘  └────────────┘              │  │
│  └──────────────────────────────────────────────┘  │
│         │                    │                      │
│         │ HTTP/WebSocket     │ IndexedDB/Cache      │
│         ↓                    ↓                      │
└─────────────────────────────────────────────────────┘
         │
         │ API Requests
         ↓
┌─────────────────────────────────────────────────────┐
│              Backend Server (Node.js)                │
│  ┌──────────────────────────────────────────────┐  │
│  │           Express API Server                  │  │
│  │  ┌────────────┐  ┌────────────┐              │  │
│  │  │ REST API   │  │ WebSocket  │              │  │
│  │  └────────────┘  └────────────┘              │  │
│  │  ┌────────────┐  ┌────────────┐              │  │
│  │  │  Database  │  │   Cache    │              │  │
│  │  │ (SQLite)   │  │  (Redis)   │              │  │
│  │  └────────────┘  └────────────┘              │  │
│  └──────────────────────────────────────────────┘  │
│         │                                           │
│         │ File System Access                        │
│         ↓                                           │
│  ┌──────────────────────────────────────────────┐  │
│  │    Golden Universe Data (41 folders)          │  │
│  │         237 Python Calculation Files           │  │
│  │         Theory Markdown Documents              │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend

- **Framework**: React 19.2.0
  - Component-based architecture
  - Hooks for state and effects
  - Concurrent rendering
  - Suspense for code splitting

- **Language**: TypeScript 5.9.3
  - Static type checking
  - Enhanced IDE support
  - Better refactoring
  - Type-safe APIs

- **Routing**: React Router 6.30.3
  - Declarative routing
  - Nested routes
  - Lazy loading
  - Dynamic parameters

- **State Management**: Zustand 5.0.11
  - Lightweight state container
  - React hooks integration
  - TypeScript support
  - Minimal boilerplate

- **Styling**: SCSS/Sass 1.97.3
  - Modular CSS
  - Variables and mixins
  - Nested selectors
  - Component-scoped styles

- **3D Graphics**: Three.js 0.183.1 + React Three Fiber 9.5.0
  - WebGL rendering
  - 3D scene management
  - React component integration
  - Performance optimized

- **Data Visualization**: D3.js 7.9.0
  - Charts and graphs
  - Data transformations
  - SVG rendering
  - Interactive visualizations

- **Math Rendering**: KaTeX 0.16.33
  - LaTeX equation display
  - Fast rendering
  - Server-side compatible
  - Extensive symbol support

- **Markdown**: Marked 15.0.12
  - Markdown parsing
  - Custom renderers
  - Syntax highlighting
  - Sanitization

- **Code Highlighting**: Highlight.js 11.11.1
  - Python syntax support
  - Multiple themes
  - Automatic language detection

- **Search**: FlexSearch 0.8.212
  - Full-text search
  - Fuzzy matching
  - Fast indexing
  - Minimal memory footprint

### Backend

- **Runtime**: Node.js 20+
  - JavaScript runtime
  - Event-driven architecture
  - Non-blocking I/O

- **Framework**: Express 5.2.1
  - RESTful API server
  - Middleware support
  - Routing
  - Static file serving

- **Database**: Better-SQLite3 11.10.0
  - Fast synchronous SQLite
  - ACID transactions
  - In-memory option
  - Zero configuration

- **Security**:
  - Helmet 8.1.0 (HTTP headers)
  - CORS 2.8.6 (Cross-origin)
  - Rate limiting (8.2.1)
  - Input validation

- **Performance**:
  - Compression 1.8.1 (gzip/brotli)
  - Morgan 1.10.1 (logging)
  - Caching strategies

### Build & Development

- **Build Tool**: Vite 7.3.1
  - Fast HMR (Hot Module Replacement)
  - ES modules based
  - Optimized builds
  - Plugin ecosystem

- **Package Manager**: npm
  - Dependency management
  - Script execution
  - Workspaces support

- **Linting**: ESLint 9.39.3
  - Code quality checks
  - TypeScript rules
  - React rules
  - Custom configurations

- **Formatting**: Prettier 3.8.1
  - Consistent code style
  - Auto-formatting
  - IDE integration

- **Type Checking**: TypeScript Compiler
  - Static analysis
  - Type validation
  - Build-time checks

## Application Structure

### Directory Organization

```
golden-universe-visualizer/
├── public/                  # Static assets
│   ├── favicon.ico
│   ├── manifest.json
│   ├── robots.txt
│   ├── sitemap.xml
│   └── icons/
├── server/                  # Backend server
│   ├── server.ts           # Main server file
│   ├── database/           # Database schemas & queries
│   ├── routes/             # API route handlers
│   ├── middleware/         # Express middleware
│   └── utils/              # Server utilities
├── src/                     # Frontend source code
│   ├── assets/             # Images, fonts, etc.
│   ├── components/         # React components
│   │   ├── Common/         # Shared components
│   │   ├── Layout/         # Layout components
│   │   ├── Theory/         # Theory-specific
│   │   ├── Calculations/   # Calculator components
│   │   ├── Visualizations/ # 3D visualizations
│   │   ├── Search/         # Search components
│   │   └── ...
│   ├── pages/              # Page components
│   │   ├── Home.tsx
│   │   ├── Theory.tsx
│   │   ├── Derivations.tsx
│   │   ├── Calculations.tsx
│   │   ├── Visualizations.tsx
│   │   └── NotFound.tsx
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API services
│   ├── contexts/           # React contexts
│   ├── utils/              # Utility functions
│   ├── types/              # TypeScript types
│   ├── styles/             # Global styles
│   │   ├── globals.scss
│   │   ├── variables.scss
│   │   ├── accessibility.scss
│   │   └── print.scss
│   ├── App.tsx             # Root component
│   ├── main.tsx            # Entry point
│   └── vite-env.d.ts       # Vite types
├── scripts/                # Build/utility scripts
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
├── vite.config.ts          # Vite config
├── USER_GUIDE.md           # User documentation
├── FEATURES.md             # Feature list
└── ARCHITECTURE.md         # This file
```

## Component Architecture

### Component Hierarchy

```
App (ErrorBoundary wrapper)
├── UXProvider (context)
├── BrowserRouter
    ├── AppHeader
    │   ├── Logo
    │   ├── Navigation
    │   ├── SearchButton
    │   └── ThemeToggle
    ├── MainLayout
    │   ├── Sidebar (collapsible)
    │   │   └── NavigationTree
    │   └── Outlet (React Router)
    │       ├── Home
    │       │   ├── HeroSection
    │       │   ├── AchievementsSection
    │       │   ├── StatisticsSection
    │       │   ├── FeaturesGrid
    │       │   └── QuickLinks
    │       ├── Theory
    │       │   ├── TheoryNav
    │       │   ├── ContentViewer
    │       │   │   ├── MarkdownRenderer
    │       │   │   ├── MathRenderer
    │       │   │   └── CodeBlock
    │       │   └── TableOfContents
    │       ├── Derivations
    │       │   ├── FileTree
    │       │   ├── CodeViewer
    │       │   └── ResultsDisplay
    │       ├── Calculations
    │       │   ├── CalculatorSelector
    │       │   ├── InputForm
    │       │   └── ResultsPanel
    │       ├── Visualizations
    │       │   ├── Canvas3D
    │       │   ├── Controls
    │       │   └── Settings
    │       └── NotFound
    └── ToastContainer
```

### Component Categories

#### 1. Layout Components
- **MainLayout**: Primary layout wrapper
- **AppHeader**: Top navigation bar
- **Sidebar**: Collapsible side navigation
- **Footer**: Bottom information

#### 2. Common Components
- **LoadingFallback**: Loading spinner/skeleton
- **ErrorBoundary**: Error catching wrapper
- **Toast**: Notification system
- **Skeleton**: Loading placeholders
- **Button**: Reusable button component
- **Modal**: Dialog/overlay system
- **AnimatedCounter**: Animated number display

#### 3. Content Components
- **MarkdownRenderer**: Markdown to HTML
- **MathRenderer**: LaTeX equations
- **CodeBlock**: Syntax-highlighted code
- **TableOfContents**: Auto-generated TOC
- **Breadcrumbs**: Navigation trail

#### 4. Feature Components
- **SearchBar**: Global search interface
- **TheoryViewer**: Theory document display
- **Calculator**: Interactive calculators
- **Visualization3D**: 3D graphics canvas
- **FileTree**: Hierarchical file browser

## Data Flow

### Client-Side Data Flow

```
User Interaction
     ↓
Event Handler
     ↓
State Update (Zustand/React State)
     ↓
Component Re-render
     ↓
UI Update
```

### Server Data Flow

```
HTTP Request
     ↓
Express Middleware
     ↓
Route Handler
     ↓
Business Logic
     ↓
Database Query (SQLite)
     ↓
Response Transformation
     ↓
HTTP Response
```

### Data Fetching Pattern

```typescript
// Service layer
export const fetchTheoryContent = async (id: string) => {
  const response = await fetch(`/api/theory/${id}`);
  if (!response.ok) throw new Error('Failed to fetch');
  return response.json();
};

// Component usage
const TheoryPage = ({ id }: Props) => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTheoryContent(id)
      .then(setContent)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Skeleton />;
  if (error) return <ErrorDisplay error={error} />;
  return <ContentViewer content={content} />;
};
```

## State Management

### Zustand Stores

#### App Store
```typescript
interface AppState {
  theme: 'dark' | 'light';
  sidebarOpen: boolean;
  searchQuery: string;
  setTheme: (theme: 'dark' | 'light') => void;
  toggleSidebar: () => void;
  setSearchQuery: (query: string) => void;
}
```

#### Content Store
```typescript
interface ContentState {
  theories: Theory[];
  derivations: Derivation[];
  calculations: Calculation[];
  loading: boolean;
  fetchTheories: () => Promise<void>;
  fetchDerivations: () => Promise<void>;
}
```

### React Context

- **UXContext**: User experience preferences
- **ThemeContext**: Theme configuration
- **SearchContext**: Search state and results

## Routing

### Route Structure

```typescript
<Routes>
  <Route path="/" element={<MainLayout />}>
    <Route index element={<Home />} />
    <Route path="theory/*" element={<Theory />} />
    <Route path="derivations/*" element={<Derivations />} />
    <Route path="calculations/*" element={<Calculations />} />
    <Route path="visualizations/*" element={<Visualizations />} />
    <Route path="*" element={<NotFound />} />
  </Route>
</Routes>
```

### Nested Routes (Theory Example)

```
/theory
/theory/:category
/theory/:category/:topic
/theory/:category/:topic/:section
```

### Route Parameters

- **Dynamic segments**: `:id`, `:category`
- **Query parameters**: `?search=newton&filter=constants`
- **Hash fragments**: `#section-1`

## API Design

### REST Endpoints

#### Theory

```
GET    /api/theory           # List all theory documents
GET    /api/theory/:id       # Get specific theory
GET    /api/theory/search    # Search theories
```

#### Derivations

```
GET    /api/derivations      # List derivation folders
GET    /api/derivations/:id  # Get specific derivation
POST   /api/derivations/run  # Execute calculation
```

#### Calculations

```
POST   /api/calculate        # Run calculation
GET    /api/calculate/:type  # Get calculator info
```

#### Search

```
POST   /api/search           # Perform search
GET    /api/search/index     # Get search index
```

### Response Format

```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
  metadata?: {
    timestamp: number;
    version: string;
  };
}
```

## Performance Optimization

### Frontend Optimizations

1. **Code Splitting**
   - Route-based splitting
   - Component lazy loading
   - Dynamic imports

2. **Memoization**
   - React.memo for components
   - useMemo for expensive calculations
   - useCallback for function references

3. **Virtual Scrolling**
   - react-window for long lists
   - Infinite scroll implementation
   - Viewport optimization

4. **Asset Optimization**
   - Image lazy loading
   - WebP format support
   - Responsive images
   - SVG optimization

5. **Caching**
   - Service worker caching
   - Memory cache for API responses
   - IndexedDB for persistent data

### Backend Optimizations

1. **Database**
   - Indexed columns
   - Prepared statements
   - Connection pooling
   - Query optimization

2. **Caching**
   - Response caching
   - Static asset caching
   - Computed result caching

3. **Compression**
   - Gzip/Brotli compression
   - Minified responses
   - Asset bundling

## Security

### Frontend Security

- XSS prevention (React auto-escaping)
- CSRF protection
- Content Security Policy
- Secure dependencies
- Input validation

### Backend Security

- Helmet.js for HTTP headers
- CORS configuration
- Rate limiting
- SQL injection prevention
- Input sanitization
- Error message sanitization

## Deployment

### Build Process

```bash
# Install dependencies
npm install

# Run type checking
npm run type-check

# Run linting
npm run lint

# Build frontend
npm run build

# Build backend
npm run server:build
```

### Production Configuration

- Environment variables
- Database setup
- SSL/TLS certificates
- Reverse proxy (nginx)
- CDN integration
- Monitoring & logging

### Hosting Options

- **Static hosting**: Netlify, Vercel, GitHub Pages
- **Full-stack**: AWS, Google Cloud, Azure, DigitalOcean
- **Serverless**: AWS Lambda, Google Cloud Functions

---

## Design Principles

1. **Component Reusability**: DRY principle
2. **Type Safety**: TypeScript everywhere
3. **Performance First**: Optimize early
4. **Accessibility**: WCAG 2.1 AA compliance
5. **Progressive Enhancement**: Works without JavaScript
6. **Mobile First**: Responsive by default
7. **Documentation**: Code and architecture docs
8. **Testing**: Unit and E2E tests (future)

---

**Architecture Version**: 1.0.0
**Last Updated**: February 25, 2026
**Maintained By**: Golden Universe Theory Team
