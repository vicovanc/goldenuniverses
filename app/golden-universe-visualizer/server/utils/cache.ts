import { getDatabase } from '../database/schema';
import config from '../config/config';

export class Cache {
  /**
   * Get value from cache
   */
  static get<T>(key: string): T | null {
    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        SELECT value FROM results_cache
        WHERE key = ? AND expires_at > datetime('now')
      `);

      const row = stmt.get(key) as { value: string } | undefined;

      if (row) {
        return JSON.parse(row.value) as T;
      }

      return null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    } finally {
      db.close();
    }
  }

  /**
   * Set value in cache
   */
  static set(key: string, value: any, ttl: number = config.cache.ttl): void {
    const db = getDatabase();

    try {
      const expiresAt = new Date(Date.now() + ttl * 1000).toISOString();

      const stmt = db.prepare(`
        INSERT OR REPLACE INTO results_cache (key, value, expires_at)
        VALUES (?, ?, ?)
      `);

      stmt.run(key, JSON.stringify(value), expiresAt);
    } catch (error) {
      console.error('Cache set error:', error);
    } finally {
      db.close();
    }
  }

  /**
   * Delete value from cache
   */
  static delete(key: string): void {
    const db = getDatabase();

    try {
      const stmt = db.prepare('DELETE FROM results_cache WHERE key = ?');
      stmt.run(key);
    } catch (error) {
      console.error('Cache delete error:', error);
    } finally {
      db.close();
    }
  }

  /**
   * Clear all cache
   */
  static clear(): void {
    const db = getDatabase();

    try {
      db.prepare('DELETE FROM results_cache').run();
    } catch (error) {
      console.error('Cache clear error:', error);
    } finally {
      db.close();
    }
  }

  /**
   * Clear expired cache entries
   */
  static clearExpired(): void {
    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        DELETE FROM results_cache WHERE expires_at <= datetime('now')
      `);
      const result = stmt.run();
      console.log(`Cleared ${result.changes} expired cache entries`);
    } catch (error) {
      console.error('Cache clearExpired error:', error);
    } finally {
      db.close();
    }
  }
}

// Auto-clear expired cache periodically
setInterval(() => {
  Cache.clearExpired();
}, config.cache.checkPeriod * 1000);

export default Cache;
