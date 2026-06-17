import { recommendationCopy, type Recommendation } from "@/lib/deal"

interface DealScoreProps {
  score: number
  confidence: number
  recommendation: Recommendation
}

export function DealScore({ score, confidence, recommendation }: DealScoreProps) {
  const radius = 84
  const circumference = 2 * Math.PI * radius
  // 270° arc (three-quarter gauge)
  const arcFraction = 0.75
  const arcLength = circumference * arcFraction
  const progress = (score / 100) * arcLength
  const rec = recommendationCopy[recommendation]

  return (
    <section className="mesh-calm relative overflow-hidden rounded-3xl border border-border px-6 pb-8 pt-7">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium uppercase tracking-[0.18em] text-muted-foreground">
          Deal Score
        </span>
        <span className="rounded-full border border-border/70 bg-card/70 px-3 py-1 text-xs font-medium text-muted-foreground backdrop-blur-sm">
          {Math.round(confidence * 100)}% confidence
        </span>
      </div>

      <div className="mt-2 flex flex-col items-center">
        <div className="relative flex items-center justify-center">
          <svg
            width="208"
            height="208"
            viewBox="0 0 208 208"
            className="-rotate-[135deg]"
            role="img"
            aria-label={`Deal score ${score} out of 100`}
          >
            <circle
              cx="104"
              cy="104"
              r={radius}
              fill="none"
              stroke="var(--color-border)"
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={`${arcLength} ${circumference}`}
            />
            <circle
              cx="104"
              cy="104"
              r={radius}
              fill="none"
              stroke="var(--color-primary)"
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={`${progress} ${circumference}`}
            />
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="flex items-baseline gap-0.5">
              <span className="font-sans text-6xl font-semibold tracking-tight text-foreground tabular-nums">
                {score}
              </span>
              <span className="text-lg font-normal text-muted-foreground">/100</span>
            </div>
            <span className="mt-1 text-xs uppercase tracking-[0.16em] text-muted-foreground">
              {rec.title}
            </span>
          </div>
        </div>

        <p className="mt-3 max-w-[16rem] text-balance text-center text-sm leading-relaxed text-muted-foreground">
          {rec.note}
        </p>
      </div>
    </section>
  )
}
