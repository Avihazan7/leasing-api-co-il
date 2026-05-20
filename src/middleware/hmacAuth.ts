import crypto from 'node:crypto';
import type { Request, Response, NextFunction } from 'express';
import { logger } from '../lib/logger';

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Express {
    interface Request {
      rawBody?: Buffer;
    }
  }
}

/**
 * Express body-parser `verify` hook that stores the raw request bytes so the
 * HMAC signature can be checked against the exact payload that was sent.
 */
export function captureRawBody(req: Request, _res: Response, buf: Buffer): void {
  if (buf?.length) {
    req.rawBody = Buffer.from(buf);
  }
}

const SIGNATURE_HEADER = 'x-signature';

function safeEqual(a: string, b: string): boolean {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
}

/**
 * Verifies an `X-Signature: sha256=<hex>` header against the raw body using a
 * shared secret (HMAC-SHA256). Set `HMAC_DISABLED=true` to bypass in local dev.
 */
export function verifyHmac(req: Request, res: Response, next: NextFunction): void {
  if (process.env.HMAC_DISABLED === 'true') {
    return next();
  }

  const secret = process.env.HMAC_SECRET ?? '';
  if (!secret) {
    logger.error('HMAC_SECRET is not configured; rejecting signed request.');
    res.status(500).json({
      error: { code: 'CONFIG_ERROR', message: 'Server signing secret not configured.' },
    });
    return;
  }

  const provided = req.get(SIGNATURE_HEADER);
  if (!provided) {
    res.status(401).json({
      error: { code: 'MISSING_SIGNATURE', message: `Missing ${SIGNATURE_HEADER} header.` },
    });
    return;
  }

  const payload = req.rawBody ?? Buffer.alloc(0);
  const digest = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  const expected = `sha256=${digest}`;

  if (!safeEqual(provided, expected)) {
    res.status(401).json({
      error: { code: 'INVALID_SIGNATURE', message: 'Signature verification failed.' },
    });
    return;
  }

  next();
}
