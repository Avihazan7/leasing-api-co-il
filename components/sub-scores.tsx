interface SubScore {
  label: string
  value: number
}

export function SubScores({ scores }: { scores: SubScore[] }) {
  return (
    <section className="rounded-3xl border border-border bg-card p-6">
      <h2 className="text-base font-semibold tracking-tight text-card-foreground">
        Score Composition
      </h2>
      <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
        The deterministic factors behind the headline number.
      </p>

      <ul className="mt-5 flex flex-col gap-4">
        {scores.map((s) => (
          <li key={s.label} className="flex items-center gap-4">
            <span className="w-20 shrink-0 text-sm text-muted-foreground">{s.label}</span>
            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full rounded-full bg-primary"
                style={{ width: `${s.value}%` }}
              />
            </div>
            <span className="w-8 shrink-0 text-right font-mono text-sm font-medium text-foreground tabular-nums">
              {s.value}
            </span>
          </li>
        ))}
      </ul>
    </section>
  )
}
