// Theory Law Types for Golden Universe

export interface TheoryLaw {
  id: number;
  title: string;
  statement: string;
  equations: string[];
  status: LawStatus;
  category: LawCategory;
  subLaws?: SubLaw[];
  dependencies: number[];
  gaps?: string[];
  pythonImplementations?: string[];
  validationResults?: ValidationResult[];
  content?: string; // Full markdown content
  precision?: string; // Precision in ppm or percentage
}

export interface SubLaw {
  id: string;
  title: string;
  equations: string[];
  description: string;
}

export interface ValidationResult {
  description: string;
  value: string;
  error?: string;
  validated: boolean;
}

export type LawStatus =
  | 'fully-defined'
  | 'partially-defined'
  | 'form-defined'
  | 'schematic'
  | 'derived'
  | 'validated';

export type LawCategory =
  | 'foundation'
  | 'symmetry'
  | 'particles'
  | 'constants'
  | 'cosmology'
  | 'advanced';

export interface LagrangianTerm {
  symbol: string;
  name: string;
  description: string;
  equation: string;
  components?: LagrangianComponent[];
  relatedLaws: number[];
}

export interface LagrangianComponent {
  name: string;
  equation: string;
  description: string;
}

export interface LawDependency {
  from: number;
  to: number;
  type: 'uses' | 'derives' | 'constrains' | 'validates';
}

export interface TheoryDocument {
  id: string;
  title: string;
  content: string;
  sections: DocumentSection[];
}

export interface DocumentSection {
  id: string;
  title: string;
  level: number;
  content: string;
}

export interface BookmarkState {
  lawId: number;
  timestamp: number;
  note?: string;
}

export interface ReadingProgress {
  lawId: number;
  progress: number; // 0-100
  lastRead: number;
}
