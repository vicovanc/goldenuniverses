/**
 * IndexedDB Cache Implementation
 * Aggressive caching strategy for calculation results and content
 */

import { openDB, DBSchema, IDBPDatabase } from 'idb';

interface CacheEntry<T = any> {
  key: string;
  value: T;
  timestamp: number;
  expiresAt: number;
  metadata?: Record<string, any>;
}

interface GoldenUniverseCacheDB extends DBSchema {
  calculations: {
    key: string;
    value: CacheEntry;
    indexes: { 'by-timestamp': number; 'by-expires': number };
  };
  content: {
    key: string;
    value: CacheEntry;
    indexes: { 'by-timestamp': number; 'by-expires': number };
  };
  visualizations: {
    key: string;
    value: CacheEntry;
    indexes: { 'by-timestamp': number; 'by-expires': number };
  };
}

const DB_NAME = 'golden-universe-cache';
const DB_VERSION = 1;

// Cache TTL in milliseconds
const CACHE_TTL = {
  CALCULATIONS: 24 * 60 * 60 * 1000, // 24 hours
  CONTENT: 7 * 24 * 60 * 60 * 1000, // 7 days
  VISUALIZATIONS: 60 * 60 * 1000, // 1 hour
};

class CacheManager {
  private db: IDBPDatabase<GoldenUniverseCacheDB> | null = null;
  private initPromise: Promise<void> | null = null;

  /**
   * Initialize IndexedDB
   */
  async init(): Promise<void> {
    if (this.db) return;
    if (this.initPromise) return this.initPromise;

    this.initPromise = (async () => {
      this.db = await openDB<GoldenUniverseCacheDB>(DB_NAME, DB_VERSION, {
        upgrade(db) {
          // Calculations store
          if (!db.objectStoreNames.contains('calculations')) {
            const calcStore = db.createObjectStore('calculations', { keyPath: 'key' });
            calcStore.createIndex('by-timestamp', 'timestamp');
            calcStore.createIndex('by-expires', 'expiresAt');
          }

          // Content store
          if (!db.objectStoreNames.contains('content')) {
            const contentStore = db.createObjectStore('content', { keyPath: 'key' });
            contentStore.createIndex('by-timestamp', 'timestamp');
            contentStore.createIndex('by-expires', 'expiresAt');
          }

          // Visualizations store
          if (!db.objectStoreNames.contains('visualizations')) {
            const vizStore = db.createObjectStore('visualizations', { keyPath: 'key' });
            vizStore.createIndex('by-timestamp', 'timestamp');
            vizStore.createIndex('by-expires', 'expiresAt');
          }
        },
      });

      // Clean expired entries on init
      await this.cleanExpired();
    })();

    return this.initPromise;
  }

  /**
   * Set a cache entry
   */
  async set<T>(
    store: keyof GoldenUniverseCacheDB,
    key: string,
    value: T,
    ttl?: number,
    metadata?: Record<string, any>
  ): Promise<void> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    const now = Date.now();
    const defaultTTL = CACHE_TTL[store.toUpperCase() as keyof typeof CACHE_TTL] || CACHE_TTL.CONTENT;
    const expiresAt = now + (ttl || defaultTTL);

    const entry: CacheEntry<T> = {
      key,
      value,
      timestamp: now,
      expiresAt,
      metadata,
    };

    await this.db.put(store, entry as any);
  }

  /**
   * Get a cache entry
   */
  async get<T>(store: keyof GoldenUniverseCacheDB, key: string): Promise<T | null> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    const entry = await this.db.get(store, key);

    if (!entry) return null;

    // Check if expired
    if (entry.expiresAt < Date.now()) {
      await this.delete(store, key);
      return null;
    }

    return entry.value as T;
  }

  /**
   * Delete a cache entry
   */
  async delete(store: keyof GoldenUniverseCacheDB, key: string): Promise<void> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    await this.db.delete(store, key);
  }

  /**
   * Clear all entries in a store
   */
  async clear(store: keyof GoldenUniverseCacheDB): Promise<void> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    await this.db.clear(store);
  }

  /**
   * Clear all stores
   */
  async clearAll(): Promise<void> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    await Promise.all([
      this.db.clear('calculations'),
      this.db.clear('content'),
      this.db.clear('visualizations'),
    ]);
  }

  /**
   * Get all entries in a store
   */
  async getAll<T>(store: keyof GoldenUniverseCacheDB): Promise<T[]> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    const entries = await this.db.getAll(store);
    const now = Date.now();

    return entries
      .filter(entry => entry.expiresAt > now)
      .map(entry => entry.value as T);
  }

  /**
   * Clean expired entries
   */
  async cleanExpired(): Promise<void> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    const now = Date.now();
    const stores: Array<keyof GoldenUniverseCacheDB> = [
      'calculations',
      'content',
      'visualizations',
    ];

    for (const store of stores) {
      const tx = this.db.transaction(store, 'readwrite');
      const index = tx.store.index('by-expires');

      // Get all expired entries
      const range = IDBKeyRange.upperBound(now);
      let cursor = await index.openCursor(range);

      while (cursor) {
        await cursor.delete();
        cursor = await cursor.continue();
      }

      await tx.done;
    }
  }

  /**
   * Get cache statistics
   */
  async getStats(): Promise<{
    calculations: number;
    content: number;
    visualizations: number;
    total: number;
  }> {
    await this.init();
    if (!this.db) throw new Error('Database not initialized');

    const [calculations, content, visualizations] = await Promise.all([
      this.db.count('calculations'),
      this.db.count('content'),
      this.db.count('visualizations'),
    ]);

    return {
      calculations,
      content,
      visualizations,
      total: calculations + content + visualizations,
    };
  }

  /**
   * Check if cache has entry
   */
  async has(store: keyof GoldenUniverseCacheDB, key: string): Promise<boolean> {
    const value = await this.get(store, key);
    return value !== null;
  }

  /**
   * Get or set pattern (cache-aside)
   */
  async getOrSet<T>(
    store: keyof GoldenUniverseCacheDB,
    key: string,
    factory: () => Promise<T> | T,
    ttl?: number,
    metadata?: Record<string, any>
  ): Promise<T> {
    const cached = await this.get<T>(store, key);

    if (cached !== null) {
      return cached;
    }

    const value = await factory();
    await this.set(store, key, value, ttl, metadata);

    return value;
  }
}

// Singleton instance
let cacheInstance: CacheManager | null = null;

export function getCacheManager(): CacheManager {
  if (!cacheInstance) {
    cacheInstance = new CacheManager();
  }
  return cacheInstance;
}

export { CacheManager, CACHE_TTL };
export type { CacheEntry };
