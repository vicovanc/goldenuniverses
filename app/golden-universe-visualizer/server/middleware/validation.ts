import { Request, Response, NextFunction } from 'express';
import { AppError } from './errorHandler';

export interface ValidationRule {
  field: string;
  type: 'string' | 'number' | 'boolean' | 'array' | 'object';
  required?: boolean;
  min?: number;
  max?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean;
}

export const validate = (rules: ValidationRule[], source: 'body' | 'query' | 'params' = 'body') => {
  return (req: Request, res: Response, next: NextFunction) => {
    const data = req[source];
    const errors: string[] = [];

    for (const rule of rules) {
      const value = data[rule.field];

      // Check required
      if (rule.required && (value === undefined || value === null || value === '')) {
        errors.push(`${rule.field} is required`);
        continue;
      }

      // Skip further validation if not required and not provided
      if (!rule.required && (value === undefined || value === null)) {
        continue;
      }

      // Type validation
      const actualType = Array.isArray(value) ? 'array' : typeof value;
      if (actualType !== rule.type) {
        errors.push(`${rule.field} must be of type ${rule.type}`);
        continue;
      }

      // String/Array length validation
      if ((rule.type === 'string' || rule.type === 'array') && value) {
        if (rule.min !== undefined && value.length < rule.min) {
          errors.push(`${rule.field} must be at least ${rule.min} characters/items`);
        }
        if (rule.max !== undefined && value.length > rule.max) {
          errors.push(`${rule.field} must be at most ${rule.max} characters/items`);
        }
      }

      // Number range validation
      if (rule.type === 'number' && typeof value === 'number') {
        if (rule.min !== undefined && value < rule.min) {
          errors.push(`${rule.field} must be at least ${rule.min}`);
        }
        if (rule.max !== undefined && value > rule.max) {
          errors.push(`${rule.field} must be at most ${rule.max}`);
        }
      }

      // Pattern validation
      if (rule.pattern && rule.type === 'string' && !rule.pattern.test(value)) {
        errors.push(`${rule.field} format is invalid`);
      }

      // Custom validation
      if (rule.custom && !rule.custom(value)) {
        errors.push(`${rule.field} validation failed`);
      }
    }

    if (errors.length > 0) {
      throw new AppError(`Validation failed: ${errors.join(', ')}`, 400);
    }

    next();
  };
};

// Common validators
export const validators = {
  derivationNumber: validate([
    { field: 'number', type: 'number', required: true, min: 1, max: 42 }
  ], 'params'),

  searchQuery: validate([
    { field: 'q', type: 'string', required: true, min: 2, max: 200 }
  ], 'query'),

  calculateRequest: validate([
    { field: 'scriptName', type: 'string', required: true },
    { field: 'parameters', type: 'object', required: false }
  ], 'body'),
};
