import { api, ChartItem, DashboardKpis, PipelineRun, UserErrorRequest } from "./api";

export async function fetchKpis() {
  const response = await api.get<DashboardKpis>("/kpis");
  return response.data;
}

export async function fetchCategoryChart() {
  const response = await api.get<ChartItem[]>("/charts/categories");
  return response.data;
}

export async function fetchSeverityChart() {
  const response = await api.get<ChartItem[]>("/charts/severity");
  return response.data;
}

export async function fetchRequests() {
  const response = await api.get<UserErrorRequest[]>("/requests");
  return response.data;
}

export async function fetchPipelineRuns() {
  const response = await api.get<PipelineRun[]>("/pipeline-runs");
  return response.data;
}
