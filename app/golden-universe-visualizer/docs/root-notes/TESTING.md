# Testing Documentation

## Overview

This document provides comprehensive information about the testing infrastructure for the Golden Universe Visualization Application. Our testing strategy covers unit tests, integration tests, end-to-end tests, and accessibility testing to ensure high-quality, reliable code.

## Table of Contents

1. [Testing Stack](#testing-stack)
2. [Running Tests](#running-tests)
3. [Test Structure](#test-structure)
4. [Writing Tests](#writing-tests)
5. [Coverage Requirements](#coverage-requirements)
6. [Best Practices](#best-practices)
7. [CI/CD Integration](#cicd-integration)

## Testing Stack

### Unit & Integration Testing
- **Vitest**: Fast, modern test runner with native ESM support
- **React Testing Library**: Testing React components from user perspective
- **jsdom**: DOM implementation for Node.js testing
- **MSW (Mock Service Worker)**: API mocking for integration tests

### E2E Testing
- **Playwright**: Cross-browser end-to-end testing
- Supports Chromium, WebKit, and Firefox
- Mobile and tablet viewport testing

### Accessibility Testing
- **jest-axe**: Automated WCAG 2.1 compliance testing
- **axe-core**: Accessibility testing engine

## Running Tests

### Quick Start

```bash
# Run all unit tests
npm test

# Run tests in watch mode
npm run test:watch

# Run with UI dashboard
npm run test:ui

# Run with coverage report
npm run test:coverage
```

### Test Categories

```bash
# Unit tests only
npm run test:unit

# Integration tests
npm run test:integration

# Accessibility tests
npm run test:accessibility

# E2E tests
npm run test:e2e

# E2E tests with browser UI
npm run test:e2e:headed

# Debug E2E tests
npm run test:e2e:debug

# E2E test report
npm run test:e2e:report

# Run all tests (unit + integration + a11y + e2e)
npm run test:all

# CI/CD test suite
npm run test:ci
```

## Test Structure

```
src/
├── test/
│   ├── setup.ts                    # Global test setup
│   ├── utils/
│   │   └── test-utils.tsx          # Custom render functions, helpers
│   ├── fixtures/
│   │   └── mockData.ts             # Mock data for tests
│   ├── mocks/
│   │   ├── handlers.ts             # MSW request handlers
│   │   └── server.ts               # MSW server setup
│   ├── integration/
│   │   └── api.test.ts             # API integration tests
│   ├── accessibility/
│   │   └── accessibility.test.tsx  # WCAG compliance tests
│   └── e2e/
│       ├── navigation.spec.ts      # E2E navigation tests
│       ├── calculations.spec.ts    # E2E calculation tests
│       └── visualizations.spec.ts  # E2E visualization tests
├── components/
│   └── [Component]/
│       └── __tests__/
│           └── [Component].test.tsx # Component unit tests
├── hooks/
│   └── __tests__/
│       └── [hook].test.ts          # Hook unit tests
└── utils/
    └── __tests__/
        └── [utility].test.ts       # Utility unit tests
```

## Writing Tests

### Unit Tests

#### Component Testing

```typescript
import { describe, it, expect } from 'vitest';
import { renderWithProviders, screen, userEvent } from '@/test/utils/test-utils';
import MyComponent from '../MyComponent';

describe('MyComponent', () => {
  it('should render correctly', () => {
    renderWithProviders(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('should handle user interactions', async () => {
    const user = userEvent.setup();
    renderWithProviders(<MyComponent />);

    const button = screen.getByRole('button', { name: /click me/i });
    await user.click(button);

    expect(screen.getByText('Clicked!')).toBeInTheDocument();
  });
});
```

#### Hook Testing

```typescript
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useMyHook } from '../useMyHook';

describe('useMyHook', () => {
  it('should return initial state', () => {
    const { result } = renderHook(() => useMyHook());
    expect(result.current.value).toBe(0);
  });

  it('should update state', () => {
    const { result } = renderHook(() => useMyHook());

    act(() => {
      result.current.increment();
    });

    expect(result.current.value).toBe(1);
  });
});
```

#### Utility Testing

```typescript
import { describe, it, expect } from 'vitest';
import { formatNumber } from '../helpers';

describe('formatNumber', () => {
  it('should format to 2 decimals by default', () => {
    expect(formatNumber(3.14159)).toBe('3.14');
  });

  it('should format to specified decimals', () => {
    expect(formatNumber(3.14159, 4)).toBe('3.1416');
  });
});
```

### Integration Tests

```typescript
import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { server } from '../mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API Integration', () => {
  it('should fetch data successfully', async () => {
    const response = await fetch('/api/data');
    const data = await response.json();

    expect(response.ok).toBe(true);
    expect(data).toHaveProperty('results');
  });
});
```

### E2E Tests

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should complete user journey', async ({ page }) => {
    await page.click('text=Start');
    await expect(page).toHaveURL(/\/started/);

    await page.fill('input[name="name"]', 'Test User');
    await page.click('button[type="submit"]');

    await expect(page.locator('.success')).toBeVisible();
  });
});
```

### Accessibility Tests

```typescript
import { describe, it, expect } from 'vitest';
import { axe, toHaveNoViolations } from 'jest-axe';
import { renderWithProviders } from '../utils/test-utils';
import MyComponent from '@/components/MyComponent';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('should not have accessibility violations', async () => {
    const { container } = renderWithProviders(<MyComponent />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Test Utilities

### Custom Render Function

Use `renderWithProviders` for components that need context providers:

```typescript
import { renderWithProviders } from '@/test/utils/test-utils';

const { getByText, container } = renderWithProviders(<MyComponent />);
```

### Mock Data

Use standardized mock data from fixtures:

```typescript
import { mockTheoryLaw, mockCalculationResult } from '@/test/fixtures/mockData';
```

### API Mocking

MSW handles API mocking automatically. Override handlers as needed:

```typescript
server.use(
  http.get('/api/custom', () => {
    return HttpResponse.json({ custom: 'data' });
  })
);
```

## Coverage Requirements

### Minimum Coverage Targets

- **Lines**: 80%
- **Functions**: 80%
- **Branches**: 80%
- **Statements**: 80%

### Critical Path Coverage

The following must have 100% test coverage:
- Calculation engines
- API endpoints
- Authentication/authorization logic
- Data validation functions

### View Coverage Report

```bash
npm run test:coverage
```

Then open `coverage/index.html` in your browser.

## Best Practices

### 1. Test Behavior, Not Implementation

❌ **Bad**: Testing internal state
```typescript
expect(component.state.count).toBe(1);
```

✅ **Good**: Testing user-visible behavior
```typescript
expect(screen.getByText('Count: 1')).toBeInTheDocument();
```

### 2. Use Descriptive Test Names

❌ **Bad**:
```typescript
it('works', () => { ... });
```

✅ **Good**:
```typescript
it('should display error message when calculation fails', () => { ... });
```

### 3. Follow AAA Pattern

```typescript
it('should increment counter', async () => {
  // Arrange
  const user = userEvent.setup();
  renderWithProviders(<Counter />);

  // Act
  await user.click(screen.getByRole('button', { name: /increment/i }));

  // Assert
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

### 4. Mock External Dependencies

```typescript
vi.mock('@/services/api', () => ({
  fetchData: vi.fn(() => Promise.resolve(mockData)),
}));
```

### 5. Clean Up After Tests

```typescript
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});
```

### 6. Test Edge Cases

- Empty states
- Error states
- Loading states
- Boundary conditions
- Invalid inputs

### 7. Keep Tests Fast

- Mock expensive operations
- Avoid unnecessary API calls
- Use test utilities
- Run tests in parallel

### 8. Isolate Tests

Each test should be independent and not rely on other tests.

## Accessibility Testing Guidelines

### WCAG 2.1 AA Compliance

All components must pass WCAG 2.1 AA standards:

- **Perceivable**: Content must be presentable to all users
- **Operable**: Interface must be navigable by all users
- **Understandable**: Information must be clear
- **Robust**: Content must work with assistive technologies

### Keyboard Navigation

All interactive elements must be keyboard accessible:

```typescript
it('should be keyboard navigable', async () => {
  const user = userEvent.setup();
  renderWithProviders(<MyComponent />);

  await user.tab();
  expect(screen.getByRole('button')).toHaveFocus();

  await user.keyboard('{Enter}');
  // Assert action occurred
});
```

### Screen Reader Support

- Use semantic HTML
- Provide ARIA labels
- Maintain heading hierarchy
- Use landmark regions

### Color Contrast

Ensure sufficient color contrast ratios:
- Normal text: 4.5:1
- Large text: 3:1
- UI components: 3:1

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm run test:ci

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
```

### Pre-commit Hooks

Add to `.husky/pre-commit`:

```bash
#!/bin/sh
npm run test:unit
npm run lint
```

## Debugging Tests

### Vitest Debugging

```bash
# Run specific test file
npm test -- src/components/MyComponent/__tests__/MyComponent.test.tsx

# Run tests matching pattern
npm test -- --grep "should handle clicks"

# Show test output
npm test -- --reporter=verbose

# Debug single test
npm run test:ui
```

### Playwright Debugging

```bash
# Debug mode with browser
npm run test:e2e:debug

# Visual regression testing
npm run test:e2e:ui

# Run specific test
npx playwright test navigation.spec.ts

# Generate test code
npx playwright codegen http://localhost:3000
```

### Common Issues

#### Test Timeouts

Increase timeout for slow operations:

```typescript
test('slow operation', async () => {
  // ... test code
}, 30000); // 30 second timeout
```

#### Flaky Tests

- Add proper waits
- Mock time-dependent code
- Ensure test isolation
- Check for race conditions

#### Memory Leaks

- Clean up event listeners
- Clear timers
- Reset mocks
- Close connections

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [jest-axe Documentation](https://github.com/nickcolley/jest-axe)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## Support

For questions or issues:
1. Check existing test examples
2. Review documentation
3. Ask in team chat
4. Create an issue in the repository

---

**Last Updated**: 2026-02-25
**Version**: 1.0.0
