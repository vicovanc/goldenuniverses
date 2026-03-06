/**
 * Type definitions for Results Dashboard
 * GU-036 through GU-040
 */

export type ParticleCategory = 'leptons' | 'quarks' | 'bosons' | 'constants';

export type PrecisionLevel = 'excellent' | 'very-good' | 'good' | 'fair' | 'poor';

export interface ResultData {
  id: string;
  name: string;
  category: ParticleCategory;
  theoretical: number;
  experimental: number;
  unit: string;
  formula?: string;
  derivation?: string;
  errorPpm: number;
  errorPercent: number;
  precision: PrecisionLevel;
  references?: string[];
  discoveryDate?: string;
  breakthrough?: boolean;
  codataYear?: number;
}

export interface CODATAValue {
  name: string;
  value: number;
  uncertainty: number;
  unit: string;
  year: number;
  source?: string;
  doi?: string;
}

export interface AchievementData {
  title: string;
  description: string;
  precision: number;
  badge: 'gold' | 'silver' | 'bronze';
  date: string;
  category: ParticleCategory;
  resultId: string;
}

export interface ExportFormat {
  type: 'csv' | 'excel' | 'json' | 'latex';
  filename: string;
  includeMetadata?: boolean;
}

export interface FilterOptions {
  categories: ParticleCategory[];
  precisionLevels: PrecisionLevel[];
  minPrecision?: number;
  maxPrecision?: number;
  searchTerm?: string;
}

export interface ChartDataPoint {
  name: string;
  theoretical: number;
  experimental: number;
  error: number;
  category: ParticleCategory;
}
