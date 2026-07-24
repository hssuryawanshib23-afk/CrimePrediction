import Plot from 'react-plotly.js';
import { Card } from '../components/Card';
import { MetricCard } from '../components/MetricCard';
import type { Statistics } from '../types';
import { formatNumber, plotConfig, plotLayout } from '../utils';

interface OverviewProps {
  statistics: Statistics;
}

export function Overview({ statistics }: OverviewProps) {
  const topStates = statistics.statewise_crime.slice(0, 12).reverse();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-muted">Overview</p>
        <h2 className="mt-2 text-3xl font-semibold">State-wise crime risk signals</h2>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Total States / UTs" value={String(statistics.total_states)} detail={`Latest year: ${statistics.latest_year}`} />
        <MetricCard label="Average Crime Count" value={formatNumber(statistics.average_crime)} />
        <MetricCard label="Highest Crime State" value={statistics.highest_crime_state} />
        <MetricCard label="Lowest Crime State" value={statistics.lowest_crime_state} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card className="p-5">
          <h3 className="text-lg font-semibold">Top states by crime count</h3>
          <Plot
            data={[
              {
                type: 'bar',
                orientation: 'h',
                y: topStates.map((row) => row.state),
                x: topStates.map((row) => row.crime_count),
                marker: { color: '#2563eb' }
              }
            ]}
            layout={plotLayout({ height: 420, margin: { l: 140, r: 20, t: 20, b: 40 } })}
            config={plotConfig}
            className="w-full"
          />
        </Card>

        <Card className="p-5">
          <h3 className="text-lg font-semibold">Crime trend over years</h3>
          <Plot
            data={[
              {
                type: 'scatter',
                mode: 'lines+markers',
                x: statistics.crime_trend.map((row) => row.year),
                y: statistics.crime_trend.map((row) => row.crime_count),
                line: { color: '#0f766e', width: 3 },
                marker: { size: 6 }
              }
            ]}
            layout={plotLayout({ height: 420, margin: { l: 60, r: 20, t: 20, b: 40 } })}
            config={plotConfig}
            className="w-full"
          />
        </Card>
      </div>
    </div>
  );
}

