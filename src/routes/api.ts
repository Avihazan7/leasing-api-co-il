import { Router, type Request, type Response } from 'express';
import { ZodError } from 'zod';
import { ScoreRequestSchema } from '../schemas';
import { scoreDeals } from '../scoring/dealScore';
import { verifyHmac } from '../middleware/hmacAuth';
import { logger } from '../lib/logger';

const router = Router();

/**
 * POST /v1/score
 * Body: a single leasing deal, or { deals: [...] } for a batch.
 * Returns a 0-100 score with a breakdown for each deal.
 */
router.post('/score', verifyHmac, (req: Request, res: Response) => {
  try {
    const parsed = ScoreRequestSchema.parse(req.body);
    const deals = 'deals' in parsed ? parsed.deals : [parsed];
    const results = scoreDeals(deals);

    res.json({
      count: results.length,
      results,
    });
  } catch (err) {
    if (err instanceof ZodError) {
      res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request body.',
          issues: err.issues,
        },
      });
      return;
    }
    logger.error('Failed to score deal', { err: String(err) });
    res.status(500).json({
      error: { code: 'INTERNAL_ERROR', message: 'Failed to score deal.' },
    });
  }
});

export default router;
