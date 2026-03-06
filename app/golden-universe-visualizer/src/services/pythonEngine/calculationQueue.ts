/**
 * Queue management for Python calculations
 * Handles prioritization, concurrency, and progress tracking
 */

import type {
  CalculationInput,
  CalculationResult,
  QueuedCalculation,
} from './pythonTypes';

export class CalculationQueue {
  private queue: QueuedCalculation[] = [];
  private running: Map<string, QueuedCalculation> = new Map();
  private completed: Map<string, QueuedCalculation> = new Map();
  private maxConcurrent: number;
  private listeners: Map<string, Set<(calc: QueuedCalculation) => void>> = new Map();

  constructor(maxConcurrent: number = 3) {
    this.maxConcurrent = maxConcurrent;
  }

  /**
   * Add a calculation to the queue
   */
  enqueue(
    input: CalculationInput,
    priority: number = 0,
    id?: string
  ): string {
    const calcId = id || this.generateId();

    const calculation: QueuedCalculation = {
      id: calcId,
      input,
      status: 'queued',
      priority,
      submittedAt: Date.now(),
    };

    // Insert based on priority (higher priority first)
    const insertIndex = this.queue.findIndex(c => c.priority < priority);
    if (insertIndex === -1) {
      this.queue.push(calculation);
    } else {
      this.queue.splice(insertIndex, 0, calculation);
    }

    this.notifyListeners(calcId, calculation);
    this.processQueue();

    return calcId;
  }

  /**
   * Process queued calculations up to max concurrent limit
   */
  private async processQueue(): Promise<void> {
    while (
      this.queue.length > 0 &&
      this.running.size < this.maxConcurrent
    ) {
      const calculation = this.queue.shift();
      if (!calculation) break;

      calculation.status = 'running';
      calculation.startedAt = Date.now();
      this.running.set(calculation.id, calculation);

      this.notifyListeners(calculation.id, calculation);
    }
  }

  /**
   * Mark calculation as completed
   */
  complete(id: string, result: CalculationResult): void {
    const calculation = this.running.get(id);
    if (!calculation) return;

    calculation.status = 'completed';
    calculation.completedAt = Date.now();
    calculation.result = result;

    this.running.delete(id);
    this.completed.set(id, calculation);

    this.notifyListeners(id, calculation);
    this.processQueue(); // Start next queued calculation
  }

  /**
   * Mark calculation as failed
   */
  fail(id: string, error: string): void {
    const calculation = this.running.get(id);
    if (!calculation) return;

    calculation.status = 'failed';
    calculation.completedAt = Date.now();
    calculation.result = {
      success: false,
      error,
      executionTime: Date.now() - (calculation.startedAt || calculation.submittedAt),
      timestamp: Date.now(),
    };

    this.running.delete(id);
    this.completed.set(id, calculation);

    this.notifyListeners(id, calculation);
    this.processQueue();
  }

  /**
   * Update progress for a running calculation
   */
  updateProgress(id: string, progress: number): void {
    const calculation = this.running.get(id);
    if (!calculation) return;

    calculation.progress = Math.min(100, Math.max(0, progress));
    this.notifyListeners(id, calculation);
  }

  /**
   * Cancel a queued or running calculation
   */
  cancel(id: string): boolean {
    // Check if queued
    const queueIndex = this.queue.findIndex(c => c.id === id);
    if (queueIndex !== -1) {
      this.queue.splice(queueIndex, 1);
      return true;
    }

    // Check if running
    if (this.running.has(id)) {
      this.fail(id, 'Calculation cancelled by user');
      return true;
    }

    return false;
  }

  /**
   * Get calculation status
   */
  getStatus(id: string): QueuedCalculation | undefined {
    return (
      this.queue.find(c => c.id === id) ||
      this.running.get(id) ||
      this.completed.get(id)
    );
  }

  /**
   * Get all calculations with given status
   */
  getByStatus(status: QueuedCalculation['status']): QueuedCalculation[] {
    switch (status) {
      case 'queued':
        return [...this.queue];
      case 'running':
        return Array.from(this.running.values());
      case 'completed':
      case 'failed':
        return Array.from(this.completed.values()).filter(
          c => c.status === status
        );
      default:
        return [];
    }
  }

  /**
   * Get queue statistics
   */
  getStats() {
    return {
      queued: this.queue.length,
      running: this.running.size,
      completed: Array.from(this.completed.values()).filter(
        c => c.status === 'completed'
      ).length,
      failed: Array.from(this.completed.values()).filter(
        c => c.status === 'failed'
      ).length,
      total: this.queue.length + this.running.size + this.completed.size,
    };
  }

  /**
   * Clear completed calculations
   */
  clearCompleted(): void {
    this.completed.clear();
  }

  /**
   * Clear all calculations
   */
  clearAll(): void {
    this.queue = [];
    this.running.clear();
    this.completed.clear();
    this.listeners.clear();
  }

  /**
   * Subscribe to calculation updates
   */
  subscribe(
    id: string,
    callback: (calc: QueuedCalculation) => void
  ): () => void {
    if (!this.listeners.has(id)) {
      this.listeners.set(id, new Set());
    }

    this.listeners.get(id)!.add(callback);

    // Return unsubscribe function
    return () => {
      const listeners = this.listeners.get(id);
      if (listeners) {
        listeners.delete(callback);
        if (listeners.size === 0) {
          this.listeners.delete(id);
        }
      }
    };
  }

  /**
   * Notify all listeners for a calculation
   */
  private notifyListeners(id: string, calculation: QueuedCalculation): void {
    const listeners = this.listeners.get(id);
    if (listeners) {
      listeners.forEach(callback => callback(calculation));
    }
  }

  /**
   * Generate unique calculation ID
   */
  private generateId(): string {
    return `calc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Set max concurrent calculations
   */
  setMaxConcurrent(max: number): void {
    this.maxConcurrent = Math.max(1, max);
    this.processQueue();
  }

  /**
   * Get max concurrent calculations
   */
  getMaxConcurrent(): number {
    return this.maxConcurrent;
  }
}

// Singleton instance
let queueInstance: CalculationQueue | null = null;

export function getCalculationQueue(): CalculationQueue {
  if (!queueInstance) {
    queueInstance = new CalculationQueue();
  }
  return queueInstance;
}
