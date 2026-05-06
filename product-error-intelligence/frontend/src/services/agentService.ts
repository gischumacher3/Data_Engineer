import { api } from "./api";

export type AgentAnalysis = {
  provider: string;
  analysis: string;
  recommendations: string[];
};

export async function analyzeWithAgent() {
  const response = await api.post<AgentAnalysis>("/agent/analyze");
  return response.data;
}
