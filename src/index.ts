/**
 * AI Stories Sharing - Main Application Entry Point
 */

import express, { Request, Response, NextFunction } from 'express';
import { apiRouter } from './api/index';
import { AppError } from './models/errors';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API routes
app.use(apiRouter);

// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      error: err.code,
      message: err.message
    });
  } else {
    console.error('Unexpected error:', err);
    res.status(500).json({
      error: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    });
  }
});

// Start server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`AI Stories Sharing server running on port ${PORT}`);
  });
}

export { app };
