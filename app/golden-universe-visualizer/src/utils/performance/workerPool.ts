/**
 * WebWorker Pool Manager
 * Manages a pool of workers for parallel computation
 */

interface WorkerTask<T = any> {
  id: string;
  type: string;
  payload: any;
  priority: number;
  resolve: (value: T) => void;
  reject: (error: any) => void;
  timestamp: number;
}

interface WorkerInstance {
  worker: Worker;
  busy: boolean;
  currentTask: WorkerTask | null;
}

class WorkerPool {
  private workers: WorkerInstance[] = [];
  private queue: WorkerTask[] = [];
  private workerCount: number;
  private workerFactory: () => Worker;

  constructor(workerFactory: () => Worker, workerCount: number = navigator.hardwareConcurrency || 4) {
    this.workerFactory = workerFactory;
    this.workerCount = Math.min(workerCount, 8); // Cap at 8 workers
    this.initializeWorkers();
  }

  /**
   * Initialize worker pool
   */
  private initializeWorkers(): void {
    for (let i = 0; i < this.workerCount; i++) {
      const worker = this.workerFactory();
      const instance: WorkerInstance = {
        worker,
        busy: false,
        currentTask: null,
      };

      worker.onmessage = (event) => this.handleWorkerMessage(instance, event);
      worker.onerror = (error) => this.handleWorkerError(instance, error);

      this.workers.push(instance);
    }
  }

  /**
   * Handle worker message
   */
  private handleWorkerMessage(instance: WorkerInstance, event: MessageEvent): void {
    const { currentTask } = instance;
    if (!currentTask) return;

    const { type, payload } = event.data;

    if (type === 'result') {
      currentTask.resolve(payload);
      this.markWorkerFree(instance);
    } else if (type === 'error') {
      currentTask.reject(new Error(payload.error));
      this.markWorkerFree(instance);
    }
  }

  /**
   * Handle worker error
   */
  private handleWorkerError(instance: WorkerInstance, error: ErrorEvent): void {
    const { currentTask } = instance;
    if (currentTask) {
      currentTask.reject(error);
    }
    this.markWorkerFree(instance);
  }

  /**
   * Mark worker as free and process next task
   */
  private markWorkerFree(instance: WorkerInstance): void {
    instance.busy = false;
    instance.currentTask = null;
    this.processQueue();
  }

  /**
   * Execute task on worker
   */
  async execute<T>(type: string, payload: any, priority: number = 0): Promise<T> {
    return new Promise((resolve, reject) => {
      const task: WorkerTask<T> = {
        id: this.generateId(),
        type,
        payload,
        priority,
        resolve,
        reject,
        timestamp: Date.now(),
      };

      this.queue.push(task);
      this.sortQueue();
      this.processQueue();
    });
  }

  /**
   * Sort queue by priority
   */
  private sortQueue(): void {
    this.queue.sort((a, b) => {
      if (a.priority !== b.priority) {
        return b.priority - a.priority; // Higher priority first
      }
      return a.timestamp - b.timestamp; // FIFO for same priority
    });
  }

  /**
   * Process queued tasks
   */
  private processQueue(): void {
    if (this.queue.length === 0) return;

    const freeWorker = this.workers.find(w => !w.busy);
    if (!freeWorker) return;

    const task = this.queue.shift();
    if (!task) return;

    freeWorker.busy = true;
    freeWorker.currentTask = task;

    freeWorker.worker.postMessage({
      type: task.type,
      id: task.id,
      payload: task.payload,
    });

    // Continue processing if more tasks and workers available
    this.processQueue();
  }

  /**
   * Generate unique ID
   */
  private generateId(): string {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Get pool statistics
   */
  getStats(): {
    totalWorkers: number;
    busyWorkers: number;
    freeWorkers: number;
    queueLength: number;
  } {
    const busyWorkers = this.workers.filter(w => w.busy).length;
    return {
      totalWorkers: this.workerCount,
      busyWorkers,
      freeWorkers: this.workerCount - busyWorkers,
      queueLength: this.queue.length,
    };
  }

  /**
   * Terminate all workers
   */
  terminate(): void {
    this.workers.forEach(({ worker }) => worker.terminate());
    this.workers = [];
    this.queue = [];
  }
}

export { WorkerPool };
export type { WorkerTask, WorkerInstance };
