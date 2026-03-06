/**
 * Health Check Service
 * Provides application health monitoring
 */

interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  uptime: number;
  checks: {
    api: boolean;
    database: boolean;
    memory: boolean;
  };
}

class HealthCheckService {
  private startTime: number;

  constructor() {
    this.startTime = Date.now();
  }

  /**
   * Get application health status
   */
  async getHealthStatus(): Promise<HealthStatus> {
    const checks = await this.runHealthChecks();
    const allHealthy = Object.values(checks).every((check) => check);

    return {
      status: allHealthy ? 'healthy' : 'degraded',
      timestamp: new Date().toISOString(),
      version: import.meta.env.VITE_APP_VERSION || '1.0.0',
      uptime: Date.now() - this.startTime,
      checks,
    };
  }

  /**
   * Run health checks
   */
  private async runHealthChecks(): Promise<{
    api: boolean;
    database: boolean;
    memory: boolean;
  }> {
    const apiCheck = await this.checkAPI();
    const dbCheck = await this.checkDatabase();
    const memoryCheck = this.checkMemory();

    return {
      api: apiCheck,
      database: dbCheck,
      memory: memoryCheck,
    };
  }

  /**
   * Check API connectivity
   */
  private async checkAPI(): Promise<boolean> {
    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      if (!apiUrl) return true; // No API configured

      const response = await fetch(`${apiUrl}/health`, {
        method: 'GET',
        cache: 'no-cache',
      });

      return response.ok;
    } catch (error) {
      console.error('API health check failed:', error);
      return false;
    }
  }

  /**
   * Check database (IndexedDB)
   */
  private async checkDatabase(): Promise<boolean> {
    try {
      if (!window.indexedDB) return false;

      const request = indexedDB.open('health-check', 1);

      return new Promise((resolve) => {
        request.onsuccess = () => {
          request.result.close();
          resolve(true);
        };
        request.onerror = () => resolve(false);
      });
    } catch (error) {
      console.error('Database health check failed:', error);
      return false;
    }
  }

  /**
   * Check memory usage
   */
  private checkMemory(): boolean {
    try {
      if (!('memory' in performance)) return true; // Not supported

      const memory = (performance as any).memory;
      const usageRatio = memory.usedJSHeapSize / memory.jsHeapSizeLimit;

      // Alert if using more than 90% of available heap
      return usageRatio < 0.9;
    } catch (error) {
      console.error('Memory health check failed:', error);
      return true; // Assume healthy if can't check
    }
  }

  /**
   * Get uptime in human-readable format
   */
  getUptime(): string {
    const uptime = Date.now() - this.startTime;
    const seconds = Math.floor(uptime / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ${hours % 24}h`;
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  }
}

export const healthCheck = new HealthCheckService();
