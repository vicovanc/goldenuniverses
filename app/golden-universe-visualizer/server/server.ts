import express, { Express, Request, Response, NextFunction } from 'express';
import * as http from 'http';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import bodyParser from 'body-parser';
import swaggerUi from 'swagger-ui-express';
import config from './config/config';
import { corsMiddleware } from './middleware/cors';
import { errorHandler, notFoundHandler } from './middleware/errorHandler';
import { generalLimiter } from './middleware/rateLimiter';
import { initDatabase } from './database/schema';
import websocketService from './services/websocket';
import apiRoutes from './routes';
import swaggerDocument from './swagger.json';

class Server {
  public app: Express;
  private server: http.Server | null = null;

  constructor() {
    this.app = express();
    this.initializeDatabase();
    this.initializeMiddleware();
    this.initializeRoutes();
    this.initializeErrorHandling();
  }

  private initializeDatabase(): void {
    try {
      console.log('Initializing database...');
      initDatabase();
      console.log('Database initialized successfully');
    } catch (error) {
      console.error('Failed to initialize database:', error);
      process.exit(1);
    }
  }

  private initializeMiddleware(): void {
    // Security middleware
    this.app.use(
      helmet({
        contentSecurityPolicy: false, // Disable for API
        crossOriginEmbedderPolicy: false,
      })
    );

    // CORS
    this.app.use(corsMiddleware);

    // Compression
    this.app.use(compression());

    // Logging
    if (config.nodeEnv === 'development') {
      this.app.use(morgan('dev'));
    } else {
      this.app.use(morgan('combined'));
    }

    // Body parsing
    this.app.use(bodyParser.json({ limit: '10mb' }));
    this.app.use(bodyParser.urlencoded({ extended: true, limit: '10mb' }));

    // Rate limiting
    this.app.use('/api', generalLimiter);

    // Request logging
    this.app.use((req: Request, res: Response, next: NextFunction) => {
      console.log(`${req.method} ${req.path}`, {
        query: req.query,
        body: req.method !== 'GET' ? req.body : undefined,
      });
      next();
    });
  }

  private initializeRoutes(): void {
    // API Documentation
    this.app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

    // API routes
    this.app.use('/api', apiRoutes);

    // Root endpoint
    this.app.get('/', (req: Request, res: Response) => {
      res.json({
        message: 'Golden Universe API Server',
        version: '1.0.0',
        documentation: '/api-docs',
        api: '/api',
        health: '/api/health',
      });
    });
  }

  private initializeErrorHandling(): void {
    // 404 handler
    this.app.use(notFoundHandler);

    // Error handler
    this.app.use(errorHandler);
  }

  public start(): void {
    this.server = this.app.listen(config.port, () => {
      console.log('=================================================');
      console.log(`Golden Universe API Server`);
      console.log(`Environment: ${config.nodeEnv}`);
      console.log(`Server running on port ${config.port}`);
      console.log(`API: http://localhost:${config.port}/api`);
      console.log(`Docs: http://localhost:${config.port}/api-docs`);
      console.log(`Health: http://localhost:${config.port}/api/health`);
      console.log('=================================================');
    });

    // Initialize WebSocket
    if (this.server) {
      websocketService.initialize(this.server);
    }

    // Graceful shutdown
    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());
  }

  private shutdown(): void {
    console.log('\nShutting down gracefully...');

    if (this.server) {
      this.server.close(() => {
        console.log('HTTP server closed');
        websocketService.close();
        process.exit(0);
      });

      // Force shutdown after 10 seconds
      setTimeout(() => {
        console.error('Forced shutdown after timeout');
        process.exit(1);
      }, 10000);
    } else {
      process.exit(0);
    }
  }
}

// Create and start server
const server = new Server();
server.start();

export default server;
