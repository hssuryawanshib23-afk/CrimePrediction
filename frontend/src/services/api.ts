import type { FeatureImportance, Prediction, Statistics } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {})
    },
    ...options
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  states: () => request<string[]>('/states'),
  statistics: () => request<Statistics>('/statistics'),
  featureImportance: () => request<FeatureImportance>('/feature-importance'),
  predict: (state: string, year: number) =>
    request<Prediction>('/predict', {
      method: 'POST',
      body: JSON.stringify({ state, year })
    })
};

