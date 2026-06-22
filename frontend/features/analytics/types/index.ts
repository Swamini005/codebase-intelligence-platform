export interface MetricValue {
  name: string;
  value: number;
  unit?: string;
}

export interface AnalyticsReport {
  repository_id: number;
  metrics: MetricValue[];
  insights: string[];
}
