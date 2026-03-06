/**
 * Performance Monitoring Dashboard
 * Real-time display of bundle size, load time, memory, and FPS metrics
 */

import { useState, useEffect } from 'react';
import { getPerformanceMonitor, PerformanceMetrics } from '@utils/performance/metrics';
import { getCacheManager } from '@utils/performance/cache';
import './PerformanceDashboard.scss';

const PerformanceDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [cacheStats, setCacheStats] = useState<{
    calculations: number;
    content: number;
    visualizations: number;
    total: number;
  } | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    const monitor = getPerformanceMonitor();
    const cacheManager = getCacheManager();

    // Initial load
    setMetrics(monitor.getMetrics());
    cacheManager.getStats().then(setCacheStats);

    // Subscribe to updates
    const unsubscribe = monitor.onUpdate((newMetrics) => {
      setMetrics(newMetrics);
    });

    // Update cache stats periodically
    const cacheInterval = setInterval(() => {
      cacheManager.getStats().then(setCacheStats);
    }, 5000);

    return () => {
      unsubscribe();
      clearInterval(cacheInterval);
    };
  }, []);

  if (!metrics) {
    return null;
  }

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
  };

  const formatTime = (ms: number): string => {
    if (ms < 1000) return `${ms.toFixed(0)} ms`;
    return `${(ms / 1000).toFixed(2)} s`;
  };

  const getFPSColor = (fps: number): string => {
    if (fps >= 55) return 'good';
    if (fps >= 30) return 'warning';
    return 'bad';
  };

  const getLoadTimeColor = (ms: number): string => {
    if (ms < 1000) return 'good';
    if (ms < 3000) return 'warning';
    return 'bad';
  };

  return (
    <div className={`performance-dashboard ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <button
        className="dashboard-toggle"
        onClick={() => setIsExpanded(!isExpanded)}
        aria-label={isExpanded ? 'Collapse dashboard' : 'Expand dashboard'}
      >
        <span className="toggle-icon">📊</span>
        {isExpanded && <span className="toggle-text">Performance</span>}
      </button>

      {isExpanded && (
        <div className="dashboard-content">
          {/* Bundle Size Section */}
          <section className="metric-section">
            <h3 className="section-title">Bundle Size</h3>
            <div className="metric-grid">
              <div className="metric-card">
                <div className="metric-label">Total</div>
                <div className="metric-value">
                  {formatBytes(metrics.bundleSize.total)}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">JavaScript</div>
                <div className="metric-value">
                  {formatBytes(metrics.bundleSize.js)}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">CSS</div>
                <div className="metric-value">
                  {formatBytes(metrics.bundleSize.css)}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Chunks</div>
                <div className="metric-value">
                  {metrics.bundleSize.chunks.length}
                </div>
              </div>
            </div>
          </section>

          {/* Load Time Section */}
          <section className="metric-section">
            <h3 className="section-title">Load Time</h3>
            <div className="metric-grid">
              <div className="metric-card">
                <div className="metric-label">DOM Ready</div>
                <div className={`metric-value ${getLoadTimeColor(metrics.loadTime.domContentLoaded)}`}>
                  {formatTime(metrics.loadTime.domContentLoaded)}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Load Complete</div>
                <div className={`metric-value ${getLoadTimeColor(metrics.loadTime.loadComplete)}`}>
                  {formatTime(metrics.loadTime.loadComplete)}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">FCP</div>
                <div className={`metric-value ${getLoadTimeColor(metrics.loadTime.firstContentfulPaint)}`}>
                  {formatTime(metrics.loadTime.firstContentfulPaint)}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">LCP</div>
                <div className={`metric-value ${getLoadTimeColor(metrics.loadTime.largestContentfulPaint)}`}>
                  {formatTime(metrics.loadTime.largestContentfulPaint)}
                </div>
              </div>
            </div>
          </section>

          {/* Memory Section */}
          {metrics.memory.used > 0 && (
            <section className="metric-section">
              <h3 className="section-title">Memory Usage</h3>
              <div className="metric-grid">
                <div className="metric-card">
                  <div className="metric-label">Used</div>
                  <div className="metric-value">
                    {formatBytes(metrics.memory.used)}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Total</div>
                  <div className="metric-value">
                    {formatBytes(metrics.memory.total)}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Limit</div>
                  <div className="metric-value">
                    {formatBytes(metrics.memory.limit)}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Usage</div>
                  <div className="metric-value">
                    {((metrics.memory.used / metrics.memory.limit) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* FPS Section */}
          <section className="metric-section">
            <h3 className="section-title">Frame Rate (FPS)</h3>
            <div className="metric-grid">
              <div className="metric-card">
                <div className="metric-label">Current</div>
                <div className={`metric-value ${getFPSColor(metrics.fps.current)}`}>
                  {metrics.fps.current}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Average</div>
                <div className={`metric-value ${getFPSColor(metrics.fps.average)}`}>
                  {metrics.fps.average}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Min</div>
                <div className={`metric-value ${getFPSColor(metrics.fps.min)}`}>
                  {metrics.fps.min}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Max</div>
                <div className="metric-value good">
                  {metrics.fps.max}
                </div>
              </div>
            </div>
          </section>

          {/* Cache Section */}
          {cacheStats && (
            <section className="metric-section">
              <h3 className="section-title">Cache Statistics</h3>
              <div className="metric-grid">
                <div className="metric-card">
                  <div className="metric-label">Calculations</div>
                  <div className="metric-value">
                    {cacheStats.calculations}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Content</div>
                  <div className="metric-value">
                    {cacheStats.content}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Visualizations</div>
                  <div className="metric-value">
                    {cacheStats.visualizations}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Total Cached</div>
                  <div className="metric-value">
                    {cacheStats.total}
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* Chunk Details */}
          {metrics.bundleSize.chunks.length > 0 && (
            <section className="metric-section">
              <h3 className="section-title">Bundle Chunks</h3>
              <div className="chunk-list">
                {metrics.bundleSize.chunks
                  .sort((a, b) => b.size - a.size)
                  .slice(0, 10)
                  .map((chunk, index) => (
                    <div key={index} className="chunk-item">
                      <span className="chunk-name">{chunk.name}</span>
                      <span className="chunk-size">{formatBytes(chunk.size)}</span>
                    </div>
                  ))}
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
};

export default PerformanceDashboard;
