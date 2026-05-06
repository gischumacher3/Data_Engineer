import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000"
});

export type PipelineRun = {
  id: string;
  file_name: string | null;
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  duplicate_rows: number;
  completeness_rate: number | null;
  duplicate_rate: number | null;
  ingestion_success_rate: number | null;
  pipeline_latency_seconds: number | null;
  status: string;
  started_at: string;
  finished_at: string | null;
};

export type UserErrorRequest = {
  id: string;
  client_name: string | null;
  email: string | null;
  company: string | null;
  problem_description: string;
  request_date: string | null;
  is_finished: boolean | null;
  problem_category: string | null;
  severity: string | null;
  customer_profile: string | null;
  business_impact_score: number | null;
};

export type DashboardKpis = {
  total_requests: number;
  finished_rate: number;
  critical_errors: number;
  average_business_impact: number;
  top_category: string | null;
  data_completeness: number;
  duplicate_rate: number;
  ingestion_success_rate: number;
  pipeline_latency_seconds: number;
  throughput_per_minute: number;
  top_error_coverage: number;
};

export type ChartItem = {
  name: string;
  value: number;
};
