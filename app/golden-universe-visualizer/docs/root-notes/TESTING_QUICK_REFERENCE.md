# Testing Quick Reference

## Common Commands

```bash
# Run all tests
npm test

# Watch mode (auto-rerun on changes)
npm run test:watch

# Coverage report
npm run test:coverage

# Unit tests only
npm run test:unit

# E2E tests
npm run test:e2e

# E2E with browser UI
npm run test:e2e:headed

# All tests (CI pipeline)
npm run test:ci
```

## Quick Test Templates

### Component Test

```typescript
import { describe, it, expect } from 'vitest';
import { renderWithProviders, screen, userEvent } from '@/test/utils/test-utils';
import MyComponent from '../MyComponent';

describe('MyComponent', () => {
  it('should render', () => {
    renderWithProviders(<MyComponent />);
    expect(screen.getByText('Text')).toBeInTheDocument();
  });

  it('should handle clicks', async () => {
    const user = userEvent.setup();
    renderWithProviders(<MyComponent />);
    await user.click(screen.getByRole('button'));
    expect(screen.getByText('Clicked')).toBeInTheDocument();
  });
});
```

### Hook Test

```typescript
import { renderHook, act } from '@testing-library/react';
import { useMyHook } from '../useMyHook';

describe('useMyHook', () => {
  it('should work', () => {
    const { result } = renderHook(() => useMyHook());
    act(() => result.current.action());
    expect(result.current.state).toBe('expected');
  });
});
```

### E2E Test

```typescript
import { test, expect } from '@playwright/test';

test('user flow', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Button');
  await expect(page).toHaveURL('/result');
});
```

### Accessibility Test

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';
import { renderWithProviders } from '@/test/utils/test-utils';

expect.extend(toHaveNoViolations);

it('should be accessible', async () => {
  const { container } = renderWithProviders(<Component />);
  expect(await axe(container)).toHaveNoViolations();
});
```

## Common Assertions

```typescript
// Existence
expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toBeNull();

// Text content
expect(element).toHaveTextContent('text');
expect(element).toContainHTML('<span>text</span>');

// Attributes
expect(element).toHaveAttribute('href', '/path');
expect(element).toHaveClass('active');
expect(element).toHaveStyle({ color: 'red' });

// Form elements
expect(input).toHaveValue('value');
expect(checkbox).toBeChecked();
expect(button).toBeDisabled();

// Focus
expect(element).toHaveFocus();

// Numbers
expect(value).toBe(42);
expect(value).toBeGreaterThan(10);
expect(value).toBeCloseTo(1.618, 5);

// Arrays
expect(array).toHaveLength(3);
expect(array).toContain(item);
expect(array).toEqual(expect.arrayContaining([1, 2]));

// Objects
expect(obj).toHaveProperty('key', 'value');
expect(obj).toEqual({ key: 'value' });
expect(obj).toMatchObject({ key: 'value' });

// Functions
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledTimes(2);
expect(fn).toHaveBeenCalledWith('arg1', 'arg2');

// Promises
await expect(promise).resolves.toBe('value');
await expect(promise).rejects.toThrow();

// Async
await waitFor(() => {
  expect(element).toBeInTheDocument();
});
```

## Common Queries

```typescript
// By role (preferred)
screen.getByRole('button', { name: /submit/i });
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('heading', { level: 1 });

// By label text
screen.getByLabelText('Email address');

// By placeholder
screen.getByPlaceholderText('Enter email');

// By text content
screen.getByText('Hello World');
screen.getByText(/hello/i); // regex

// By display value (forms)
screen.getByDisplayValue('Current value');

// By alt text (images)
screen.getByAltText('Profile picture');

// By title
screen.getByTitle('Close');

// By test ID (last resort)
screen.getByTestId('custom-element');

// Query variants
getBy...    // throws error if not found
queryBy...  // returns null if not found
findBy...   // async, waits for element
getAllBy... // returns array
queryAllBy... // returns empty array
findAllBy... // async, returns array
```

## User Interactions

```typescript
const user = userEvent.setup();

// Click
await user.click(button);
await user.dblClick(button);
await user.tripleClick(button);

// Type
await user.type(input, 'hello');
await user.clear(input);

// Keyboard
await user.keyboard('{Enter}');
await user.keyboard('{Shift>}A{/Shift}'); // Shift+A
await user.tab();

// Select
await user.selectOptions(select, 'option1');

// Upload
await user.upload(fileInput, file);

// Hover
await user.hover(element);
await user.unhover(element);

// Pointer
await user.pointer({ keys: '[MouseLeft]', target: element });
```

## Mocking

```typescript
import { vi } from 'vitest';

// Mock function
const mockFn = vi.fn();
mockFn.mockReturnValue('value');
mockFn.mockResolvedValue('async value');
mockFn.mockRejectedValue(new Error('error'));

// Mock module
vi.mock('@/services/api', () => ({
  fetchData: vi.fn(() => Promise.resolve(data)),
}));

// Mock timers
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.runAllTimers();
vi.restoreAllMocks();

// Spy on functions
const spy = vi.spyOn(obj, 'method');
spy.mockImplementation(() => 'mocked');

// Clear mocks
vi.clearAllMocks();
vi.resetAllMocks();
vi.restoreAllMocks();
```

## Debugging

```typescript
// Print DOM
screen.debug();
screen.debug(element);

// Get element info
screen.logTestingPlaygroundURL();

// Wait for element
await screen.findByText('Text');
await waitFor(() => expect(element).toBeInTheDocument());

// Pause test
await page.pause(); // Playwright
```

## Accessibility Checkers

```typescript
// Check specific rules
const results = await axe(container, {
  rules: {
    'color-contrast': { enabled: true },
  },
});

// Check specific elements
const results = await axe(container, {
  include: ['.my-component'],
  exclude: ['.third-party'],
});
```

## Coverage Thresholds

Add to `vitest.config.ts`:

```typescript
coverage: {
  lines: 80,
  functions: 80,
  branches: 80,
  statements: 80,
}
```

## Test File Patterns

```
*.test.ts       // Unit tests
*.test.tsx      // Component tests
*.spec.ts       // E2E tests
*.integration.test.ts // Integration tests
*.a11y.test.tsx // Accessibility tests
```

## Useful Flags

```bash
# Vitest
--watch          # Watch mode
--ui             # UI dashboard
--coverage       # Coverage report
--run            # Run once
--reporter       # Change reporter
--grep "pattern" # Filter tests

# Playwright
--headed         # Show browser
--debug          # Debug mode
--ui             # UI mode
--project        # Specific project
--grep           # Filter tests
--update-snapshots # Update screenshots
```

## Resources

- [Testing Library Cheatsheet](https://testing-library.com/docs/react-testing-library/cheatsheet)
- [Playwright Cheatsheet](https://playwright.dev/docs/intro)
- [Vitest API](https://vitest.dev/api/)
- [jest-axe Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
