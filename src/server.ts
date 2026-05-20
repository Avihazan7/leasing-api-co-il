import express, { type Request, type Response, type NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import apiRoutes from './routes/api';
import { captureRawBody } from './middleware/hmacAuth';
import { logger } from './lib/logger';

dotenv.config();

const app = express();

// Security & CORS
app.use(helmet());
app.use(cors());

// Body parser with raw-body capture for HMAC verification.
app.use(
  express.json({
    verify: captureRawBody,
    limit: '5mb',
  }),
);

// Health check
app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Minimal OpenAPI descriptor.
app.get('/openapi.json', (_req: Request, res: Response) => {
  res.json({
    openapi: '3.0.0',
    info: { title: 'Leasing.co.il Deal Score Engine API', version: '2.0.0' },
    paths: {
      '/v1/score': { post: { summary: 'Score one or more leasing deals.' } },
    },
  });
});

// Versioned routes
app.use('/v1', apiRoutes);

// 404 handler
app.use((_req: Request, res: Response) => {
  res.status(404).json({ error: { code: 'NOT_FOUND', message: 'Resource not found.' } });
});

// Fallback error handler
app.use((err: unknown, _req: Request, res: Response, _next: NextFunction) => {
  logger.error('Unhandled exception', { err: String(err) });
  res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Internal Server Error' } });
});

// Start a standalone server only when run directly (not under Vercel/tests).
if (require.main === module) {
  const port = Number(process.env.PORT ?? 3000);
  app.listen(port, () => logger.info(`Leasing API listening on port ${port}`));
}

export default app;
