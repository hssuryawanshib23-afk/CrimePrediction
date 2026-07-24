import type { RiskLevel } from './types';

export const plotConfig = {
  displayModeBar: false,
  responsive: true
};

export function plotLayout(options: Record<string, unknown>) {
  return {
    autosize: true,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'Inter, system-ui, sans-serif', color: '#172033' },
    xaxis: { gridcolor: '#edf1f7', zerolinecolor: '#edf1f7' },
    yaxis: { gridcolor: '#edf1f7', zerolinecolor: '#edf1f7' },
    ...options
  };
}

export function formatNumber(value: number) {
  return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(value);
}

export function riskColor(risk: RiskLevel) {
  if (risk === 'Low') return '#1f9d62';
  if (risk === 'Medium') return '#d99a16';
  return '#c24135';
}

export function riskClasses(risk: RiskLevel) {
  if (risk === 'Low') return 'bg-emerald-50 text-emerald-700';
  if (risk === 'Medium') return 'bg-amber-50 text-amber-700';
  return 'bg-red-50 text-red-700';
}

