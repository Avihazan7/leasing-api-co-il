import crypto from 'node:crypto';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';

const validDeal = {
  listPrice: 200000,
  sellingPrice: 180000,
  monthlyPayment: 2200,
  downPayment: 10000,
  termMonths: 36,
  residualValue: 120000,
  moneyFactor: 0.001,
};

describe('API (HMAC disabled)', () => {
  let app: typeof import('../server').default;

  beforeAll(async () => {
    process.env.HMAC_DISABLED = 'true';
    app = (await import('../server')).default;
  });

  it('GET /health returns ok', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  it('POST /v1/score scores a single deal', async () => {
    const res = await request(app).post('/v1/score').send(validDeal);
    expect(res.status).toBe(200);
    expect(res.body.count).toBe(1);
    expect(res.body.results[0].score).toBeGreaterThanOrEqual(0);
  });

  it('POST /v1/score scores a batch', async () => {
    const res = await request(app)
      .post('/v1/score')
      .send({ deals: [validDeal, { ...validDeal, reference: 'x' }] });
    expect(res.status).toBe(200);
    expect(res.body.count).toBe(2);
  });

  it('POST /v1/score rejects an invalid body with 400', async () => {
    const res = await request(app).post('/v1/score').send({ listPrice: -1 });
    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });

  it('returns 404 for unknown routes', async () => {
    const res = await request(app).get('/nope');
    expect(res.status).toBe(404);
  });
});

describe('API (HMAC enabled)', () => {
  const secret = 'test-secret';
  let app: typeof import('../server').default;

  beforeAll(async () => {
    process.env.HMAC_DISABLED = 'false';
    process.env.HMAC_SECRET = secret;
    // Re-import a fresh module instance with the new env in place.
    app = (await import('../server')).default;
  });

  afterAll(() => {
    process.env.HMAC_DISABLED = 'true';
  });

  it('rejects requests without a signature', async () => {
    const res = await request(app).post('/v1/score').send(validDeal);
    expect(res.status).toBe(401);
    expect(res.body.error.code).toBe('MISSING_SIGNATURE');
  });

  it('accepts a request with a valid signature', async () => {
    const payload = JSON.stringify(validDeal);
    const digest = crypto.createHmac('sha256', secret).update(payload).digest('hex');
    const res = await request(app)
      .post('/v1/score')
      .set('Content-Type', 'application/json')
      .set('x-signature', `sha256=${digest}`)
      .send(payload);
    expect(res.status).toBe(200);
    expect(res.body.count).toBe(1);
  });
});
