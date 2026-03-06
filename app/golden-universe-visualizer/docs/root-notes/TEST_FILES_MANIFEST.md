# Test Files Manifest

## Overview

This document lists all test files created for the Golden Universe Visualization Application as part of EPIC-012: Testing & Quality.

## Configuration Files

### Test Configuration

| File | Purpose | Location |
|------|---------|----------|
| `vitest.config.ts` | Vitest configuration with coverage settings | Root |
| `playwright.config.ts` | Playwright E2E test configuration | Root |
| `src/test/setup.ts` | Global test setup and mocks | `src/test/` |

## Test Infrastructure

### Test Utilities

| File | Purpose | Location |
|------|---------|----------|
| `src/test/utils/test-utils.tsx` | Custom render functions, helpers, and utilities | `src/test/utils/` |
| `src/test/fixtures/mockData.ts` | Mock data fixtures for all test types | `src/test/fixtures/` |
| `src/test/mocks/handlers.ts` | MSW request handlers for API mocking | `src/test/mocks/` |
| `src/test/mocks/server.ts` | MSW server setup for Node.js environment | `src/test/mocks/` |

## Unit Tests

### Component Tests

| File | Component | Location |
|------|-----------|----------|
| `src/components/Sidebar/__tests__/Sidebar.test.tsx` | Sidebar navigation component | `src/components/Sidebar/` |

**Test Coverage:**
- Sidebar rendering with title and navigation items
- Collapse/expand functionality
- Navigation highlighting and routing
- Expandable nested items
- Keyboard navigation
- ARIA labels and accessibility

### Hook Tests

| File | Hook | Location |
|------|------|----------|
| `src/hooks/__tests__/useMediaQuery.test.ts` | Media query hooks | `src/hooks/` |
| `src/hooks/__tests__/useKeyboardShortcuts.test.ts` | Keyboard shortcuts hook | `src/hooks/` |

**Test Coverage:**
- `useMediaQuery`: Media query matching, breakpoint detection, responsive values
- `useKeyboardShortcuts`: Keyboard event handling, modifier keys, input field handling

### Utility Tests

| File | Utility | Location |
|------|---------|----------|
| `src/utils/__tests__/helpers.test.ts` | Helper functions | `src/utils/` |

**Test Coverage:**
- Golden ratio constant (PHI)
- Fibonacci calculations
- Number formatting
- Golden rectangle calculations
- Debounce and throttle functions
- Validation and math utilities

## Integration Tests

| File | Purpose | Location |
|------|---------|----------|
| `src/test/integration/api.test.ts` | API endpoint integration tests | `src/test/integration/` |

**Test Coverage:**
- Calculation API endpoints
- Search API endpoints
- Theory API endpoints
- Content API endpoints
- Health check endpoint
- Error handling
- Rate limiting

## Accessibility Tests

| File | Purpose | Location |
|------|---------|----------|
| `src/test/accessibility/accessibility.test.tsx` | WCAG 2.1 AA compliance tests | `src/test/accessibility/` |

**Test Coverage:**
- Sidebar component accessibility
- App component accessibility
- WCAG 2.1 AA compliance
- Heading hierarchy
- Link and button labels
- Keyboard navigation
- Screen reader support
- Form accessibility
- Focus management
- Alternative text for images

## E2E Tests

### Navigation Tests

| File | Purpose | Location |
|------|---------|----------|
| `src/test/e2e/navigation.spec.ts` | Navigation and routing E2E tests | `src/test/e2e/` |

**Test Coverage:**
- Homepage loading
- Navigation between pages
- Active navigation highlighting
- Sidebar collapse/expand
- Nested navigation items
- Responsive navigation (mobile, tablet)
- Keyboard navigation
- Deep linking
- 404 handling

### Calculation Tests

| File | Purpose | Location |
|------|---------|----------|
| `src/test/e2e/calculations.spec.ts` | Calculation feature E2E tests | `src/test/e2e/` |

**Test Coverage:**
- Calculations page loading
- Calculation form display
- Particle mass calculations
- Input validation
- Calculation history
- Result export
- Preset calculations
- Real-time calculations
- Error handling

### Visualization Tests

| File | Purpose | Location |
|------|---------|----------|
| `src/test/e2e/visualizations.spec.ts` | Visualization feature E2E tests | `src/test/e2e/` |

**Test Coverage:**
- Visualizations page loading
- Visualization gallery display
- Canvas rendering
- Visualization selection
- Interactive controls
- Zoom and pan functionality
- Fullscreen mode
- Export functionality
- Performance testing
- 3D scene rendering
- Camera rotation
- Responsive visualizations

## Documentation

| File | Purpose | Location |
|------|---------|----------|
| `TESTING.md` | Comprehensive testing documentation | Root |
| `TESTING_QUICK_REFERENCE.md` | Quick reference guide for common testing patterns | Root |
| `TEST_FILES_MANIFEST.md` | This file - complete list of test files | Root |

## Package.json Test Scripts

```json
{
  "test": "vitest run",
  "test:watch": "vitest",
  "test:ui": "vitest --ui",
  "test:coverage": "vitest run --coverage",
  "test:unit": "vitest run --dir src --exclude \"**/e2e/**\" --exclude \"**/integration/**\"",
  "test:integration": "vitest run src/test/integration",
  "test:accessibility": "vitest run src/test/accessibility",
  "test:e2e": "playwright test",
  "test:e2e:headed": "playwright test --headed",
  "test:e2e:debug": "playwright test --debug",
  "test:e2e:ui": "playwright test --ui",
  "test:e2e:report": "playwright show-report",
  "test:all": "npm run test:unit && npm run test:integration && npm run test:accessibility && npm run test:e2e",
  "test:ci": "npm run lint && npm run type-check && npm run test:coverage && npm run test:e2e"
}
```

## Test Statistics

### Files Created

- **Configuration**: 3 files
- **Test Infrastructure**: 4 files
- **Unit Tests**: 4 files
- **Integration Tests**: 1 file
- **Accessibility Tests**: 1 file
- **E2E Tests**: 3 files
- **Documentation**: 3 files

**Total**: 19 files

### Test Categories

| Category | Files | Test Cases (Approx) |
|----------|-------|---------------------|
| Unit Tests | 4 | 80+ |
| Integration Tests | 1 | 25+ |
| Accessibility Tests | 1 | 20+ |
| E2E Tests | 3 | 30+ |
| **Total** | **9** | **155+** |

### Coverage Goals

- **Lines**: ≥80%
- **Functions**: ≥80%
- **Branches**: ≥80%
- **Statements**: ≥80%

### Accessibility Standards

- **WCAG 2.1**: Level AA compliance
- **Screen Readers**: Full support
- **Keyboard Navigation**: 100% coverage
- **Color Contrast**: Minimum 4.5:1 for normal text

## Technology Stack

### Testing Frameworks
- **Vitest** 4.0.18 - Unit & integration testing
- **React Testing Library** 16.3.2 - Component testing
- **Playwright** 1.58.2 - E2E testing
- **jest-axe** 10.0.0 - Accessibility testing

### Supporting Libraries
- **@testing-library/user-event** 14.6.1 - User interaction simulation
- **@testing-library/jest-dom** 6.9.1 - DOM matchers
- **msw** 2.12.10 - API mocking
- **jsdom** 26.1.0 - DOM implementation
- **vitest-canvas-mock** 1.1.3 - Canvas mocking
- **axe-core** 4.11.1 - Accessibility engine

## Test Execution Matrix

### Local Development

| Command | Environment | Purpose |
|---------|-------------|---------|
| `npm run test:watch` | Development | Active development with auto-rerun |
| `npm run test:ui` | Development | Visual test debugging |
| `npm run test:coverage` | Development | Check coverage locally |
| `npm run test:e2e:headed` | Development | Debug E2E tests visually |

### Pre-commit

| Command | Environment | Purpose |
|---------|-------------|---------|
| `npm run test:unit` | Pre-commit | Fast unit test verification |
| `npm run lint` | Pre-commit | Code quality check |

### CI/CD Pipeline

| Command | Environment | Purpose |
|---------|-------------|---------|
| `npm run test:ci` | CI | Full test suite with coverage |
| `npm run test:all` | CI | Complete test verification |

## Test Patterns Used

### Unit Testing Patterns
- **AAA (Arrange-Act-Assert)**: Standard test structure
- **Mock Service Worker**: API mocking without touching components
- **Custom Render**: Provider-wrapped rendering for context
- **Test Utilities**: Reusable test helpers and fixtures

### Integration Testing Patterns
- **MSW Handlers**: Centralized API mock definitions
- **End-to-end Data Flow**: Testing complete user workflows
- **Error Scenarios**: Comprehensive error handling verification

### E2E Testing Patterns
- **Page Object Model**: (Can be implemented as needed)
- **User-centric Tests**: Testing from user perspective
- **Visual Regression**: Screenshot comparison (configured)
- **Cross-browser Testing**: Chromium, mobile variants

### Accessibility Testing Patterns
- **Automated WCAG Checks**: Using axe-core rules
- **Keyboard Navigation**: Tab order and shortcuts
- **Screen Reader Simulation**: ARIA labels and roles
- **Focus Management**: Focus trap and restoration

## Future Enhancements

### Potential Additions
- [ ] Visual regression testing with Percy or Chromatic
- [ ] Performance testing with Lighthouse CI
- [ ] Load testing for calculation engine
- [ ] Snapshot testing for stable components
- [ ] Component interaction testing library
- [ ] API contract testing with Pact
- [ ] Mutation testing with Stryker
- [ ] Test data generation with Faker.js

### Coverage Expansion
- [ ] Results Dashboard component tests
- [ ] Theory Explorer component tests
- [ ] Calculation Runner component tests
- [ ] Search functionality tests
- [ ] PWA functionality tests
- [ ] WebSocket connection tests
- [ ] Python calculation engine tests
- [ ] Database query tests

## Maintenance Notes

### Regular Tasks
- Review and update test coverage monthly
- Update mock data to match API changes
- Refresh E2E selectors after UI changes
- Run accessibility audits quarterly
- Update dependencies regularly
- Review and remove flaky tests
- Optimize slow-running tests

### Breaking Changes Checklist
- [ ] Update test utilities if providers change
- [ ] Update mock handlers if API changes
- [ ] Update E2E selectors if markup changes
- [ ] Update accessibility tests if ARIA changes
- [ ] Regenerate snapshots if needed
- [ ] Update documentation

## Contributors

Testing infrastructure implemented as part of:
- **EPIC**: EPIC-012: Testing & Quality
- **Tickets**: GU-056 through GU-060
- **Date**: 2026-02-25

---

**Version**: 1.0.0
**Last Updated**: 2026-02-25
