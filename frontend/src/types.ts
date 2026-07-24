export type RiskLevel = 'Low' | 'Medium' | 'High';

export interface StateCrime {
  state: string;
  crime_count: number;
}

export interface CrimeTrendPoint {
  year: number;
  crime_count: number;
}

export interface MapPoint {
  state: string;
  crime_count: number;
  risk_level: RiskLevel;
  latitude: number;
  longitude: number;
  predicted_crime_count?: number;
  confidence?: number;
}

export interface Statistics {
  total_states: number;
  average_crime: number;
  highest_crime_state: string;
  lowest_crime_state: string;
  latest_year: number;
  statewise_crime: StateCrime[];
  crime_trend: CrimeTrendPoint[];
  map_points: MapPoint[];
}

export interface Prediction {
  state: string;
  year: number;
  predicted_crime_count: number;
  risk_level: RiskLevel;
  confidence: number;
  features: Record<string, number>;
  explanation: Array<{ feature: string; impact: number; direction: string }>;
}

export interface FeatureImportance {
  selected_model: string;
  importance_source?: string;
  features: Array<{ feature: string; importance: number }>;
  metrics: Array<{ model: string; mae: number; rmse: number; r2: number; selected: boolean }>;
}
