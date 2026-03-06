import * as dotenv from 'dotenv';
import * as path from 'path';

dotenv.config();

export interface Config {
  port: number;
  nodeEnv: string;
  database: {
    filename: string;
  };
  cors: {
    origin: string[];
    credentials: boolean;
  };
  rateLimit: {
    windowMs: number;
    max: number;
  };
  python: {
    executable: string;
    scriptsPath: string;
    timeout: number;
  };
  content: {
    basePath: string;
    derivationsPath: string;
    theoriesPath: string;
  };
  cache: {
    ttl: number;
    checkPeriod: number;
  };
  websocket: {
    enabled: boolean;
    pingInterval: number;
  };
}

const config: Config = {
  port: parseInt(process.env.PORT || '3001', 10),
  nodeEnv: process.env.NODE_ENV || 'development',

  database: {
    filename: process.env.DB_PATH || path.join(__dirname, '../../data/golden-universe.db'),
  },

  cors: {
    origin: process.env.CORS_ORIGIN?.split(',') || ['http://localhost:5173', 'http://localhost:3000'],
    credentials: true,
  },

  rateLimit: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
  },

  python: {
    executable: process.env.PYTHON_PATH || 'python3',
    scriptsPath: process.env.PYTHON_SCRIPTS_PATH || path.join(__dirname, '../../../pipeline'),
    timeout: parseInt(process.env.PYTHON_TIMEOUT || '300000', 10), // 5 minutes default
  },

  content: {
    basePath: process.env.CONTENT_PATH || path.join(__dirname, '../../../'),
    derivationsPath: process.env.DERIVATIONS_PATH || path.join(__dirname, '../../../derivations'),
    theoriesPath: process.env.THEORIES_PATH || path.join(__dirname, '../../../Theory Development'),
  },

  cache: {
    ttl: parseInt(process.env.CACHE_TTL || '3600', 10), // 1 hour default
    checkPeriod: parseInt(process.env.CACHE_CHECK_PERIOD || '600', 10), // 10 minutes
  },

  websocket: {
    enabled: process.env.WS_ENABLED !== 'false',
    pingInterval: parseInt(process.env.WS_PING_INTERVAL || '30000', 10),
  },
};

export default config;
