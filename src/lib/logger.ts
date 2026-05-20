type Meta = Record<string, unknown> | undefined;

function format(meta: Meta): string {
  if (!meta) return '';
  try {
    return JSON.stringify(meta);
  } catch {
    return '[unserializable meta]';
  }
}

export const logger = {
  info: (msg: string, meta?: Meta) => console.log(`[INFO] ${msg}`, format(meta)),
  warn: (msg: string, meta?: Meta) => console.warn(`[WARN] ${msg}`, format(meta)),
  error: (msg: string, meta?: Meta) => console.error(`[ERROR] ${msg}`, format(meta)),
  debug: (msg: string, meta?: Meta) => {
    if (process.env.NODE_ENV !== 'production') {
      console.debug(`[DEBUG] ${msg}`, format(meta));
    }
  },
};
