import { WebSocketServer, WebSocket } from 'ws';
import { Server } from 'http';
import config from '../config/config';
import pythonExecutor from './pythonExecutor';

export interface WSMessage {
  type: string;
  data: any;
}

export class WebSocketService {
  private wss: WebSocketServer | null = null;
  private clients: Set<WebSocket> = new Set();

  initialize(server: Server): void {
    if (!config.websocket.enabled) {
      console.log('WebSocket is disabled');
      return;
    }

    this.wss = new WebSocketServer({ server });

    this.wss.on('connection', (ws: WebSocket) => {
      console.log('WebSocket client connected');
      this.clients.add(ws);

      // Send welcome message
      this.send(ws, {
        type: 'connected',
        data: { message: 'Connected to Golden Universe API' },
      });

      ws.on('message', (message: string) => {
        try {
          const data = JSON.parse(message.toString());
          this.handleMessage(ws, data);
        } catch (error) {
          console.error('WebSocket message parse error:', error);
          this.send(ws, {
            type: 'error',
            data: { message: 'Invalid message format' },
          });
        }
      });

      ws.on('close', () => {
        console.log('WebSocket client disconnected');
        this.clients.delete(ws);
      });

      ws.on('error', (error) => {
        console.error('WebSocket error:', error);
        this.clients.delete(ws);
      });

      // Ping interval to keep connection alive
      const pingInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.ping();
        } else {
          clearInterval(pingInterval);
        }
      }, config.websocket.pingInterval);
    });

    // Subscribe to Python executor events
    this.subscribeToPythonEvents();

    console.log('WebSocket server initialized');
  }

  private handleMessage(ws: WebSocket, message: WSMessage): void {
    switch (message.type) {
      case 'ping':
        this.send(ws, { type: 'pong', data: {} });
        break;

      case 'subscribe':
        // Handle subscription to specific events
        this.send(ws, {
          type: 'subscribed',
          data: { channel: message.data.channel },
        });
        break;

      default:
        console.log('Unknown message type:', message.type);
    }
  }

  private subscribeToPythonEvents(): void {
    pythonExecutor.on('job-queued', (job) => {
      this.broadcast({
        type: 'calculation-queued',
        data: { jobId: job.id, scriptName: job.scriptName },
      });
    });

    pythonExecutor.on('job-started', (job) => {
      this.broadcast({
        type: 'calculation-started',
        data: { jobId: job.id, scriptName: job.scriptName },
      });
    });

    pythonExecutor.on('job-completed', (job) => {
      this.broadcast({
        type: 'calculation-completed',
        data: {
          jobId: job.id,
          scriptName: job.scriptName,
          result: job.result,
        },
      });
    });

    pythonExecutor.on('job-failed', (job) => {
      this.broadcast({
        type: 'calculation-failed',
        data: {
          jobId: job.id,
          scriptName: job.scriptName,
          error: job.error,
        },
      });
    });

    pythonExecutor.on('progress', (data) => {
      this.broadcast({
        type: 'calculation-progress',
        data,
      });
    });
  }

  send(ws: WebSocket, message: WSMessage): void {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    }
  }

  broadcast(message: WSMessage): void {
    this.clients.forEach((client) => {
      this.send(client, message);
    });
  }

  close(): void {
    if (this.wss) {
      this.wss.close();
    }
  }
}

export default new WebSocketService();
