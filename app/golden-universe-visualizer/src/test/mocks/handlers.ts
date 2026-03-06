import { http, HttpResponse } from 'msw';
import { mockApiResponses, mockCalculationResult, mockSearchResults, mockTheoryLaw } from '../fixtures/mockData';

/**
 * MSW handlers for mocking API requests
 */
export const handlers = [
  // Calculation endpoints
  http.post('/api/calculations/particle-mass', async () => {
    return HttpResponse.json(mockApiResponses.calculations.success);
  }),

  http.get('/api/calculations/:id', async ({ params }) => {
    return HttpResponse.json({
      success: true,
      data: { ...mockCalculationResult, id: params.id },
    });
  }),

  http.get('/api/calculations', async () => {
    return HttpResponse.json({
      success: true,
      data: [mockCalculationResult],
    });
  }),

  // Search endpoints
  http.get('/api/search', async ({ request }) => {
    const url = new URL(request.url);
    const query = url.searchParams.get('q');

    if (!query) {
      return HttpResponse.json(mockApiResponses.search.empty);
    }

    return HttpResponse.json(mockApiResponses.search.success);
  }),

  http.post('/api/search', async () => {
    return HttpResponse.json(mockApiResponses.search.success);
  }),

  // Theory endpoints
  http.get('/api/theory/laws', async () => {
    return HttpResponse.json({
      success: true,
      data: [mockTheoryLaw],
    });
  }),

  http.get('/api/theory/laws/:id', async ({ params }) => {
    return HttpResponse.json({
      success: true,
      data: { ...mockTheoryLaw, id: params.id },
    });
  }),

  // Content endpoints
  http.get('/api/content/:path*', async () => {
    return HttpResponse.json({
      success: true,
      data: {
        content: '# Test Content\n\nThis is test content.',
        metadata: {
          title: 'Test',
          author: 'Test Author',
        },
      },
    });
  }),

  // WebSocket mock (for testing)
  http.get('/ws', async () => {
    return new HttpResponse(null, {
      status: 101,
      statusText: 'Switching Protocols',
    });
  }),

  // Health check
  http.get('/api/health', async () => {
    return HttpResponse.json({
      success: true,
      status: 'healthy',
      timestamp: Date.now(),
    });
  }),

  // Error simulation
  http.get('/api/error', async () => {
    return new HttpResponse(null, {
      status: 500,
      statusText: 'Internal Server Error',
    });
  }),
];

/**
 * Error handlers for testing error scenarios
 */
export const errorHandlers = [
  http.post('/api/calculations/particle-mass', async () => {
    return HttpResponse.json(mockApiResponses.calculations.error, { status: 500 });
  }),

  http.get('/api/search', async () => {
    return new HttpResponse(null, { status: 500 });
  }),

  http.get('/api/theory/laws/:id', async () => {
    return HttpResponse.json(
      {
        success: false,
        error: 'Not found',
      },
      { status: 404 }
    );
  }),
];
