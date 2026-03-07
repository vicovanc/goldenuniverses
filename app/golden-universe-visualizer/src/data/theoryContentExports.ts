/**
 * Re-export file for theoryContent to fix Vercel build issues
 * This file ensures proper module resolution in production builds
 */

export {
  THEORY_LAWS,
  EXPERIMENTAL_VALIDATIONS,
  DERIVATION_FILES,
  type TheoryLaw
} from './theoryContent';