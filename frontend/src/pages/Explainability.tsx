import Plot from 'react-plotly.js';
import { Card } from '../components/Card';
import type { FeatureImportance } from '../types';
import { plotConfig, plotLayout } from '../utils';

interface ExplainabilityProps {
  importance: FeatureImportance;
}

export function Explainability({ importance }: ExplainabilityProps) {
  const features = [...importance.features].reverse();
  const selected = importance.metrics.find((metric) => metric.selected);

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-muted">Explainability</p>
        <h2 className="mt-2 text-3xl font-semibold">Why the model predicts risk</h2>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_380px]">
        <Card className="p-5">
          <h3 className="text-lg font-semibold">Feature importance</h3>
          <Plot
            data={[
              {
                type: 'bar',
                orientation: 'h',
                y: features.map((row) => row.feature.replaceAll('_', ' ')),
                x: features.map((row) => row.importance),
                marker: { color: '#7c3aed' }
              }
            ]}
            layout={plotLayout({ height: 460, margin: { l: 150, r: 20, t: 20, b: 40 } })}
            config={plotConfig}
            className="w-full"
          />
        </Card>

        <Card className="p-5">
          <h3 className="text-lg font-semibold">Model comparison</h3>
          <div className="mt-4 space-y-3">
            {importance.metrics.map((metric) => (
              <div
                key={metric.model}
                className={`rounded-md border p-4 ${metric.selected ? 'border-slate-900 bg-slate-50' : 'border-line bg-white'}`}
              >
                <div className="flex items-center justify-between gap-3">
                  <p className="font-semibold">{metric.model}</p>
                  {metric.selected ? <span className="rounded-md bg-slate-900 px-2 py-1 text-xs font-semibold text-white">Selected</span> : null}
                </div>
                <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
                  <span>MAE<br /><strong>{metric.mae}</strong></span>
                  <span>RMSE<br /><strong>{metric.rmse}</strong></span>
                  <span>R2<br /><strong>{metric.r2}</strong></span>
                </div>
              </div>
            ))}
          </div>
          {selected ? (
            <p className="mt-5 text-sm leading-6 text-muted">
              The API uses {selected.model} because it produced the lowest RMSE on the 2020-2023 holdout window.
            </p>
          ) : null}
        </Card>
      </div>

      <Card className="p-5">
        <h3 className="text-lg font-semibold">Interpretation</h3>
        <p className="mt-3 max-w-4xl text-sm leading-6 text-muted">
          Source: {importance.importance_source ?? 'SHAP mean absolute value'}. The model is mostly driven by recent crime volume, growth rate, and the three-year rolling average. Population,
          literacy, and urbanization provide context so the forecast is not based only on raw historical counts.
        </p>
      </Card>
    </div>
  );
}
