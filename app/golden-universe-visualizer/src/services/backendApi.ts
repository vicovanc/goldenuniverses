import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001/api';

/**
 * API Client for Golden Universe Backend
 */
class BackendApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Generic request methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  // Theories
  async getTheories() {
    return this.get<ApiResponse<Theory[]>>('/theories');
  }

  async getTheory(id: string, render = false) {
    return this.get<ApiResponse<Theory>>(`/theories/${id}?render=${render}`);
  }

  async searchTheories(query: string) {
    return this.get<ApiResponse<Theory[]>>(`/theories/search?q=${encodeURIComponent(query)}`);
  }

  async getTheoryStats() {
    return this.get<ApiResponse<any>>('/theories/stats');
  }

  // Derivations
  async getDerivations() {
    return this.get<ApiResponse<Derivation[]>>('/derivations');
  }

  async getDerivation(number: number) {
    return this.get<ApiResponse<Derivation>>(`/derivations/${number}`);
  }

  async getDerivationFile(number: number, filename: string) {
    return this.get<ApiResponse<{ filename: string; content: string; extension: string }>>(
      `/derivations/${number}/files/${filename}`
    );
  }

  async getDerivationStats() {
    return this.get<ApiResponse<any>>('/derivations/stats');
  }

  // Equations
  async getEquations(category?: string, render = false) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (render) params.append('render', 'true');
    return this.get<ApiResponse<Equation[]>>(`/equations?${params}`);
  }

  async getEquation(id: number, render = false) {
    return this.get<ApiResponse<Equation>>(`/equations/${id}?render=${render}`);
  }

  async getEquationCategories() {
    return this.get<ApiResponse<Array<{ category: string; count: number }>>>('/equations/categories');
  }

  async searchEquations(query: string) {
    return this.get<ApiResponse<Equation[]>>(`/equations/search?q=${encodeURIComponent(query)}`);
  }

  // Calculations
  async executeCalculation(scriptName: string, parameters?: Record<string, any>) {
    return this.post<ApiResponse<{ jobId: number; status: string; message: string }>>(
      '/calculations',
      { scriptName, parameters }
    );
  }

  async getCalculationStatus(jobId: number) {
    return this.get<ApiResponse<Calculation>>(`/calculations/${jobId}`);
  }

  async getCalculationResult(jobId: number) {
    return this.get<ApiResponse<Calculation>>(`/calculations/${jobId}/result`);
  }

  async getCalculationHistory(limit = 50, offset = 0) {
    return this.get<ApiResponse<Calculation[]>>(`/calculations?limit=${limit}&offset=${offset}`);
  }

  async getCalculationResults() {
    return this.get<ApiResponse<any[]>>('/calculations/results');
  }

  async cancelCalculation() {
    return this.post<ApiResponse<{ message: string }>>('/calculations/cancel');
  }

  // Search
  async search(query: string) {
    return this.get<ApiResponse<SearchResults>>(`/search?q=${encodeURIComponent(query)}`);
  }

  // Health
  async getHealth() {
    return this.get<HealthResponse>('/health');
  }

  async getMetrics() {
    return this.get<any>('/health/metrics');
  }
}

// Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  count?: number;
  pagination?: {
    total: number;
    limit: number;
    offset: number;
    hasMore: boolean;
  };
}

export interface Theory {
  id: number;
  title: string;
  filename: string;
  content: string;
  summary?: string;
  keywords?: string;
  rendered_content?: string;
  equations?: Array<{ latex: string; displayMode: boolean; position: number }>;
  created_at: string;
  updated_at: string;
}

export interface Derivation {
  id: number;
  number: number;
  title: string;
  description?: string;
  folder_path: string;
  files?: string[];
  equations?: any[];
  file_list?: Array<{
    name: string;
    path: string;
    extension: string;
    size: number;
  }>;
  created_at: string;
  updated_at: string;
}

export interface Equation {
  id: number;
  name: string;
  latex: string;
  category?: string;
  description?: string;
  rendered?: string;
  variables?: Array<{ symbol: string; name: string }>;
  derivation_id?: number;
  theory_id?: number;
  created_at: string;
}

export interface Calculation {
  id: number;
  scriptName: string;
  parameters?: Record<string, any>;
  result?: any;
  status: 'pending' | 'running' | 'completed' | 'failed';
  error?: string;
  progress?: number;
  execution_time?: number;
  created_at?: string;
  completed_at?: string;
}

export interface SearchResults {
  query: string;
  results: Array<{
    type: 'theory' | 'equation' | 'derivation';
    id: number;
    title?: string;
    name?: string;
    snippet?: string;
    description?: string;
  }>;
  counts: {
    theories: number;
    equations: number;
    derivations: number;
    total: number;
  };
}

export interface HealthResponse {
  status: 'ok' | 'degraded';
  timestamp: string;
  uptime: number;
  checks: {
    database: boolean;
    filesystem: boolean;
    python: boolean;
  };
}

// Export singleton instance
export const backendApi = new BackendApiClient();
export default backendApi;
