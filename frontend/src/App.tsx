import { useEffect, useState } from 'react';
import { Shell } from './components/Shell';
import { api } from './services/api';
import { Overview } from './pages/Overview';
import { RiskMap } from './pages/RiskMap';
import { Prediction } from './pages/Prediction';
import { Explainability } from './pages/Explainability';
import type { FeatureImportance, Statistics } from './types';

function App() {
  const [activePage, setActivePage] = useState('overview');
  const [states, setStates] = useState<string[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [importance, setImportance] = useState<FeatureImportance | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [stateData, statisticsData, importanceData] = await Promise.all([
          api.states(),
          api.statistics(),
          api.featureImportance()
        ]);
        setStates(stateData);
        setStatistics(statisticsData);
        setImportance(importanceData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unable to load dashboard data');
      }
    }
    load();
  }, []);

  function renderPage() {
    if (error) {
      return <div className="rounded-lg border border-red-200 bg-red-50 p-5 text-sm text-red-700">{error}</div>;
    }
    if (!statistics || !importance) {
      return <div className="rounded-lg border border-line bg-white p-8 text-muted shadow-soft">Loading dashboard data...</div>;
    }
    if (activePage === 'map') return <RiskMap points={statistics.map_points} />;
    if (activePage === 'prediction') return <Prediction states={states} />;
    if (activePage === 'explainability') return <Explainability importance={importance} />;
    return <Overview statistics={statistics} />;
  }

  return (
    <Shell activePage={activePage} onPageChange={setActivePage}>
      {renderPage()}
    </Shell>
  );
}

export default App;

