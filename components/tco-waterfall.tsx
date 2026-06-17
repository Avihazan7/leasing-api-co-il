"use client"

import { useState } from "react"
import { formatCurrency, type WaterfallStep } from "@/lib/deal"

interface TcoWaterfallProps {
  steps: WaterfallStep[]
  currency: string
}

const toneFill: Record<WaterfallStep["tone"], string> = {
  anchor: "var(--color-anchor)",
  depreciation: "var(--color-depreciation)",
  interest: "var(--color-interest)",
  tco: "var(--color-tco)",
}

export function TcoWaterfall({ steps, currency }: TcoWaterfallProps) {
  const [selected, setSelected] = useState<string>("tco")
  const max = Math.max(...steps.map((s) => s.value))
  const active = steps.find((s) => s.id === selected) ?? steps[steps.length - 1]

  const anchor = steps.find((s) => s.id === "anchor")
  const tco = steps.find((s) => s.id === "tco")
  const savings = anchor && tco ? anchor.value - tco.value : 0

  return (
    <section className="rounded-3xl border border-border bg-card p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-base font-semibold tracking-tight text-card-foreground">
            Total Cost of Ownership
          </h2>
          <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
            What the deal actually costs — past the anchor.
          </p>
        </div>
        {savings > 0 && (
          <div className="shrink-0 text-right">
            <div className="font-mono text-sm font-medium text-foreground tabular-nums">
              −{formatCurrency(savings, currency)}
            </div>
            <div className="text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
              vs. anchor
            </div>
          </div>
        )}
      </div>

      {/* Chart */}
      <div className="mt-7 flex h-56 items-end justify-between gap-3">
        {steps.map((step) => {
          const heightPct = (step.value / max) * 100
          const isAnchor = step.tone === "anchor"
          const isActive = step.id === selected
          return (
            <button
              key={step.id}
              type="button"
              onClick={() => setSelected(step.id)}
              aria-pressed={isActive}
              className="group flex h-full flex-1 flex-col items-center justify-end gap-2 focus:outline-none"
            >
              <span className="font-mono text-[11px] font-medium text-muted-foreground tabular-nums">
                {formatCurrency(step.value, currency)}
              </span>
              <div className="flex w-full flex-1 items-end">
                <div
                  className="w-full origin-bottom rounded-t-md transition-[filter,box-shadow] duration-300"
                  style={{
                    height: `${heightPct}%`,
                    backgroundColor: toneFill[step.tone],
                    opacity: isAnchor ? (isActive ? 0.5 : 0.32) : isActive ? 1 : 0.82,
                    border: isAnchor ? "1px dashed var(--color-border)" : "none",
                    boxShadow: isActive && !isAnchor ? "0 6px 18px -8px var(--color-tco)" : "none",
                    animation: "rise 0.7s cubic-bezier(0.22,1,0.36,1) both",
                  }}
                />
              </div>
              <span
                className={`text-center text-[11px] leading-tight transition-colors ${
                  isActive ? "font-medium text-foreground" : "text-muted-foreground"
                }`}
              >
                {step.label}
              </span>
            </button>
          )
        })}
      </div>

      {/* Detail panel */}
      <div className="mt-6 rounded-2xl border border-border bg-muted/60 p-4">
        <div className="flex items-center gap-2">
          <span
            className="h-2.5 w-2.5 rounded-full"
            style={{ backgroundColor: toneFill[active.tone] }}
            aria-hidden
          />
          <h3 className="text-sm font-medium text-foreground">{active.label}</h3>
          <span className="ml-auto font-mono text-sm font-medium text-foreground tabular-nums">
            {formatCurrency(active.value, currency)}
          </span>
        </div>
        <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{active.detail}</p>
      </div>
    </section>
  )
}
