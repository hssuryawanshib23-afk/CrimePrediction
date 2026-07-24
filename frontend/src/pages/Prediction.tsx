import { useMemo, useState } from 'react';
import { Card } from '../components/Card';
import { api } from '../services/api';
import type { Prediction as PredictionResult } from '../types';
import { formatNumber, riskClasses } from '../utils';

interface PredictionProps {
  states: string[];
}

export function Prediction({ states }: PredictionProps) {
  const [state, setState] = useState(states[0] ?? '');
  const [year, setYear] = useState(2024);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const years = useMemo(() => Array.from({ length: 12 }, (_, index) => 2024 + index), []);

  async function submit() {
    setLoading(true);
    setError('');
    try {
      setResult(await api.predict(state, year));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Prediction failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-muted">Prediction</p>
        <h2 className="mt-2 text-3xl font-semibold">Forecast next-year crime count</h2>
      </div>

      <div className="grid gap-6 xl:grid-cols-[420px_1fr]">
        <Card className="p-5">
          <div className="space-y-4">
            <label className="block">
              <span className="text-sm font-medium text-muted">State / UT</span>
              <select
                className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-sm outline-none focus:border-slate-500"
                value={state}
                onChange={(event) => setState(event.target.value)}
              >
                {states.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </label>

            <label className="block">
              <span className="text-sm font-medium text-muted">Forecast year</span>
              <select
                className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-sm outline-none focus:border-slate-500"
                value={year}
                onChange={(event) => setYear(Number(event.target.value))}
              >
                {years.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </label>

            <button
              className="w-full rounded-md bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-400"
              disabled={loading || !state}
              onClick={submit}
              type="button"
            >
              {loading ? 'Predicting...' : 'Run prediction'}
            </button>

            {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
          </div>
        </Card>

        <Card className="p-6">
          {result ? (
            <div>
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-medium text-muted">{result.state} · {result.year}</p>
                  <p className="mt-2 text-5xl font-semibold">{formatNumber(result.predicted_crime_count)}</p>
                  <p className="mt-2 text-sm text-muted">Predicted crime count</p>
                </div>
                <span className={`rounded-md px-3 py-2 text-sm font-semibold ${riskClasses(result.risk_level)}`}>
                  {result.risk_level} Risk
                </span>
              </div>

              <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                <div className="rounded-md bg-slate-50 p-4">
                  <p className="text-sm text-muted">Prediction confidence</p>
                  <p className="mt-1 text-2xl font-semibold">{Math.round(result.confidence * 100)}%</p>
                </div>
                {Object.entries(result.features).map(([key, value]) => (
                  <div key={key} className="rounded-md bg-slate-50 p-4">
                    <p className="text-sm text-muted">{key.replaceAll('_', ' ')}</p>
                    <p className="mt-1 text-xl font-semibold">{formatNumber(value)}</p>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="flex min-h-[260px] items-center justify-center text-center text-muted">
              Select a state and forecast year to generate the risk estimate.
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
