import rateLimit from 'express-rate-limit';
import config from '../config/config';

export const generalLimiter = rateLimit({
  windowMs: config.rateLimit.windowMs,
  max: config.rateLimit.max,
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

export const calculationLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 5, // 5 calculations per minute
  message: 'Too many calculation requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

export const searchLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 30, // 30 searches per minute
  message: 'Too many search requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});
