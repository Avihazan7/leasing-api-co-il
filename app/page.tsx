import { DealScore } from "@/components/deal-score"
import { TcoWaterfall } from "@/components/tco-waterfall"
import { SubScores } from "@/components/sub-scores"
import { deal, formatCurrency } from "@/lib/deal"

export default function Page() {
  return (
    <main className="mx-auto flex min-h-dvh w-full max-w-md flex-col gap-5 px-4 pb-12 pt-6">
      {/* Brand bar */}
      <header className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2.5">
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary">
            <span className="h-2.5 w-2.5 rounded-sm bg-primary-foreground" aria-hidden />
          </span>
          <span className="text-sm font-semibold tracking-tight text-foreground">
            Leasing<span className="text-muted-foreground">.co.il</span>
          </span>
        </div>
        <span className="text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
          Mobility OS
        </span>
      </header>

      {/* Vehicle context */}
      <div className="px-1">
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">{deal.vehicle}</h1>
        <div className="mt-1 flex items-center gap-2 text-sm text-muted-foreground">
          <span>{deal.trim}</span>
          <span aria-hidden>·</span>
          <span>{deal.durationMonths} mo</span>
          <span aria-hidden>·</span>
          <span className="font-mono tabular-nums">
            {formatCurrency(deal.monthlyPayment, deal.currency)}/mo
          </span>
        </div>
      </div>

      <DealScore
        score={deal.score}
        confidence={deal.confidence}
        recommendation={deal.recommendation}
      />

      <TcoWaterfall steps={deal.waterfall} currency={deal.currency} />

      <SubScores scores={deal.subScores} />

      <footer className="px-1 pt-1">
        <p className="text-pretty text-xs leading-relaxed text-muted-foreground">
          Computed by the ULease intelligence engine. Figures are modeled estimates derived from
          market anchors and the proposed payment schedule — not financial advice.
        </p>
      </footer>
    </main>
  )
}
