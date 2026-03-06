import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';
import { mockCalculationResult, mockSearchResults, mockTheoryLaw } from '../fixtures/mockData';

// Start MSW server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));

// Reset handlers after each test
afterEach(() => server.resetHandlers());

// Stop server after all tests
afterAll(() => server.close());

describe('API Integration Tests', () => {
  describe('Calculation API', () => {
    it('should successfully create a calculation', async () => {
      const response = await fetch('/api/calculations/particle-mass', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          n: 1,
          phi: 1.618033988749895,
        }),
      });

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(data.data).toBeDefined();
      expect(data.data.type).toBe('particle_mass');
    });

    it('should handle calculation errors', async () => {
      server.use(
        http.post('/api/calculations/particle-mass', async () => {
          return HttpResponse.json(
            {
              success: false,
              error: 'Invalid parameters',
            },
            { status: 400 }
          );
        })
      );

      const response = await fetch('/api/calculations/particle-mass', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          n: -1, // Invalid
        }),
      });

      expect(response.ok).toBe(false);
      expect(response.status).toBe(400);
      const data = await response.json();
      expect(data.success).toBe(false);
      expect(data.error).toBeDefined();
    });

    it('should retrieve calculation by ID', async () => {
      const calcId = 'test-calc-123';
      const response = await fetch(`/api/calculations/${calcId}`);

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(data.data.id).toBe(calcId);
    });

    it('should list all calculations', async () => {
      const response = await fetch('/api/calculations');

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(Array.isArray(data.data)).toBe(true);
      expect(data.data.length).toBeGreaterThan(0);
    });
  });

  describe('Search API', () => {
    it('should return search results', async () => {
      const response = await fetch('/api/search?q=lagrangian');

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(Array.isArray(data.results)).toBe(true);
      expect(data.total).toBeGreaterThanOrEqual(0);
    });

    it('should return empty results for empty query', async () => {
      const response = await fetch('/api/search?q=');

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(data.results).toEqual([]);
      expect(data.total).toBe(0);
    });

    it('should handle POST search requests', async () => {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: 'golden ratio',
          filters: {
            type: 'theory',
          },
        }),
      });

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(Array.isArray(data.results)).toBe(true);
    });

    it('should handle search errors', async () => {
      server.use(
        http.get('/api/search', async () => {
          return new HttpResponse(null, { status: 500 });
        })
      );

      const response = await fetch('/api/search?q=test');
      expect(response.ok).toBe(false);
      expect(response.status).toBe(500);
    });
  });

  describe('Theory API', () => {
    it('should retrieve all theory laws', async () => {
      const response = await fetch('/api/theory/laws');

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(Array.isArray(data.data)).toBe(true);
    });

    it('should retrieve specific theory law', async () => {
      const lawId = 'lagrangian';
      const response = await fetch(`/api/theory/laws/${lawId}`);

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(data.data.id).toBe(lawId);
    });

    it('should handle not found theory law', async () => {
      server.use(
        http.get('/api/theory/laws/:id', async () => {
          return HttpResponse.json(
            {
              success: false,
              error: 'Not found',
            },
            { status: 404 }
          );
        })
      );

      const response = await fetch('/api/theory/laws/nonexistent');
      expect(response.ok).toBe(false);
      expect(response.status).toBe(404);
    });
  });

  describe('Content API', () => {
    it('should retrieve content by path', async () => {
      const response = await fetch('/api/content/theory/fundamentals');

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(data.data.content).toBeDefined();
      expect(data.data.metadata).toBeDefined();
    });
  });

  describe('Health Check', () => {
    it('should return healthy status', async () => {
      const response = await fetch('/api/health');

      expect(response.ok).toBe(true);
      const data = await response.json();
      expect(data.success).toBe(true);
      expect(data.status).toBe('healthy');
      expect(data.timestamp).toBeDefined();
    });
  });

  describe('Error Handling', () => {
    it('should handle 500 errors', async () => {
      const response = await fetch('/api/error');

      expect(response.ok).toBe(false);
      expect(response.status).toBe(500);
    });

    it('should handle network errors', async () => {
      server.use(
        http.get('/api/test-network-error', async () => {
          return HttpResponse.error();
        })
      );

      try {
        await fetch('/api/test-network-error');
        expect.fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeDefined();
      }
    });
  });

  describe('Rate Limiting', () => {
    it('should handle rate limit responses', async () => {
      server.use(
        http.get('/api/rate-limited', async () => {
          return new HttpResponse(null, {
            status: 429,
            statusText: 'Too Many Requests',
            headers: {
              'Retry-After': '60',
            },
          });
        })
      );

      const response = await fetch('/api/rate-limited');
      expect(response.status).toBe(429);
      expect(response.headers.get('Retry-After')).toBe('60');
    });
  });
});
