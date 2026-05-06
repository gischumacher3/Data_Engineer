import { Sparkles } from "lucide-react";
import { AgentSummaryPanel } from "../components/AgentSummaryPanel";
import { AgentAnalysis } from "../services/agentService";

type Props = {
  analysis: AgentAnalysis | null;
  onAnalyze: () => void;
  isLoading: boolean;
};

export function InsightsPage({ analysis, onAnalyze, isLoading }: Props) {
  return (
    <div className="page-stack">
      <div className="page-heading with-action">
        <div>
          <h1>Insights IA</h1>
          <p>Resumo executivo e recomendações para priorização de backlog.</p>
        </div>
        <button type="button" onClick={onAnalyze} disabled={isLoading}>
          <Sparkles size={18} />
          {isLoading ? "Analisando" : "Analisar"}
        </button>
      </div>
      <AgentSummaryPanel analysis={analysis} />
    </div>
  );
}
