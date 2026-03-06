# Contributing to Golden Universe Visualizer

Thank you for your interest in contributing to the Golden Universe Visualizer! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We expect all participants to:

- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing others' private information
- Any conduct that could be considered inappropriate in a professional setting

## Getting Started

### Prerequisites

- Node.js 20.x or higher
- npm or yarn package manager
- Git
- Code editor (VS Code recommended)

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/golden-universe-visualizer.git
   cd golden-universe-visualizer
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/golden-universe-visualizer.git
   ```

4. **Install dependencies**
   ```bash
   npm install
   ```

5. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

6. **Start development server**
   ```bash
   npm start
   ```

## Development Workflow

### Branch Strategy

We use a simplified Git flow:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes

### Creating a Feature Branch

```bash
# Update your local repository
git checkout develop
git pull upstream develop

# Create a feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in your feature branch
2. Follow the coding standards (see below)
3. Test your changes thoroughly
4. Commit your changes with descriptive messages

### Keeping Your Branch Updated

```bash
# Fetch latest changes
git fetch upstream

# Rebase your branch
git rebase upstream/develop
```

## Coding Standards

### TypeScript Guidelines

- Use TypeScript for all new code
- Enable strict mode
- Define proper types (avoid `any`)
- Use interfaces for object shapes
- Document complex types with JSDoc comments

```typescript
// Good
interface VisualizationProps {
  data: number[];
  width: number;
  height: number;
  onUpdate?: (value: number) => void;
}

// Bad
function render(props: any) { ... }
```

### React Best Practices

- Use functional components with hooks
- Keep components small and focused
- Use meaningful component names
- Implement proper prop validation
- Handle loading and error states

```typescript
// Good
export const PhaseSpaceVisualization: React.FC<VisualizationProps> = ({
  data,
  width,
  height,
}) => {
  // Component implementation
};

// Bad
export const PSV = (p: any) => { ... };
```

### Code Style

- Use 2 spaces for indentation
- Use single quotes for strings
- Add semicolons at the end of statements
- Use trailing commas in objects and arrays
- Keep lines under 100 characters when possible

```typescript
// Good
const config = {
  name: 'Golden Ratio',
  value: 1.618033988749,
  precision: 12,
};

// Bad
const config = {name:"Golden Ratio",value:1.618033988749,precision:12}
```

### Naming Conventions

- **Components**: PascalCase (`PhaseSpaceVisualization`)
- **Files**: PascalCase for components, camelCase for utilities
- **Functions**: camelCase (`calculateGoldenRatio`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_ITERATIONS`)
- **Interfaces**: PascalCase with descriptive names
- **Types**: PascalCase ending with `Type` when needed

### File Organization

```
src/
├── components/
│   ├── Visualizations/     # Visualization components
│   ├── Theory/             # Theory-related components
│   └── UI/                 # Reusable UI components
├── services/               # API and external services
├── utils/                  # Utility functions
├── calculations/           # Mathematical calculations
├── types/                  # TypeScript type definitions
└── styles/                 # Global styles
```

### Formatting

We use Prettier for code formatting:

```bash
# Format your code
npm run format

# Check formatting
npm run format:check
```

### Linting

We use ESLint for code linting:

```bash
# Lint your code
npm run lint

# Fix auto-fixable issues
npm run lint:fix
```

## Commit Guidelines

### Commit Message Format

We follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```bash
# Feature
feat(visualization): add phase space visualization component

# Bug fix
fix(calculation): correct golden ratio precision calculation

# Documentation
docs(readme): update installation instructions

# Refactoring
refactor(components): extract common visualization logic

# Performance
perf(rendering): optimize Three.js render loop
```

### Commit Best Practices

- Keep commits atomic (one logical change per commit)
- Write clear, descriptive commit messages
- Reference issue numbers when applicable
- Separate subject from body with a blank line
- Use imperative mood ("add feature" not "added feature")

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

2. **Run all checks**
   ```bash
   npm run lint
   npm run type-check
   npm run test
   npm run build
   ```

3. **Update documentation** if needed

4. **Test thoroughly** in different browsers/devices

### Creating a Pull Request

1. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill in the PR template

3. **PR Title Format**
   ```
   [Type] Brief description
   ```
   Example: `[Feature] Add phase space visualization`

4. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Manual testing completed
   - [ ] Tested in multiple browsers

   ## Screenshots (if applicable)
   Add screenshots here

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex logic
   - [ ] Documentation updated
   - [ ] No new warnings
   - [ ] Tests passing
   ```

### Review Process

1. At least one maintainer review required
2. All CI checks must pass
3. No merge conflicts
4. Address review comments
5. Request re-review after changes

### After Approval

- Squash commits if requested
- Ensure CI is green
- Maintainer will merge the PR

## Testing Guidelines

### Unit Tests

Write unit tests for:
- Utility functions
- Calculation logic
- Store actions and selectors
- Custom hooks

```typescript
// Example test
describe('calculateGoldenRatio', () => {
  it('should return correct value with default precision', () => {
    const result = calculateGoldenRatio();
    expect(result).toBeCloseTo(1.618033988749, 10);
  });
});
```

### Component Tests

Write component tests for:
- User interactions
- Conditional rendering
- Props handling
- State management

```typescript
// Example component test
describe('PhaseSpaceVisualization', () => {
  it('should render without crashing', () => {
    render(<PhaseSpaceVisualization data={[]} />);
    expect(screen.getByRole('canvas')).toBeInTheDocument();
  });
});
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Documentation

### Code Documentation

- Add JSDoc comments for complex functions
- Document component props with TypeScript interfaces
- Explain non-obvious logic with inline comments
- Keep comments up-to-date with code changes

```typescript
/**
 * Calculates the golden ratio to specified precision
 * @param precision - Number of decimal places (default: 12)
 * @returns The golden ratio as a number
 */
export function calculateGoldenRatio(precision = 12): number {
  // Implementation
}
```

### README Updates

Update README.md when:
- Adding new features
- Changing setup instructions
- Modifying architecture
- Adding dependencies

### Documentation Files

Update relevant docs when changing:
- `DEPLOYMENT.md` - Deployment procedures
- `API.md` - API endpoints
- `ARCHITECTURE.md` - System architecture
- Component-specific docs

## Issue Reporting

### Before Creating an Issue

1. Search existing issues
2. Check if it's already fixed in latest version
3. Gather relevant information

### Bug Reports

Include:
- Clear, descriptive title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/videos if applicable
- Environment details (browser, OS, etc.)
- Error messages and stack traces

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What should happen

**Screenshots**
Add screenshots

**Environment**
- Browser: Chrome 120
- OS: macOS 14.0
- Version: 1.0.0
```

### Feature Requests

Include:
- Clear, descriptive title
- Problem the feature solves
- Proposed solution
- Alternative solutions considered
- Additional context

### Security Issues

**DO NOT** create public issues for security vulnerabilities.
Email security concerns to: security@golden-universe.app

## Questions?

- Check existing documentation
- Search closed issues
- Ask in discussions
- Contact maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project website (if applicable)

Thank you for contributing to Golden Universe Visualizer!

---

**Last Updated:** 2024-01-01
**Version:** 1.0.0
