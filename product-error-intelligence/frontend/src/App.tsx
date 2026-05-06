import { BarChart3, BrainCircuit, Database, FileUp, Table2 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DashboardPage } from "./pages/DashboardPage";
import { InsightsPage } from "./pages/InsightsPage";
import { RequestsTablePage } from "./pages/RequestsTablePage";
import { UploadPage } from "./pages/UploadPage";
import { AgentAnalysis, analyzeWithAgent } from "./services/agentService";
import { ChartItem, DashboardKpis, PipelineRun, UserErrorRequest } from "./services/api";
import { fetchCategoryChart, fetchKpis, fetchPipelineRuns, fetchRequests, fetchSeverityChart } from "./services/kpiService";

type Page = "upload" | "pipeline" | "requests" | "kpis" | "insights";

const navItems = [
  { id: "upload", label: "Upload", icon: FileUp },
  { id: "pipeline", label: "Pipeline", icon: Database },
  { id: "requests", label: "Tabela", icon: Table2 },
  { id: "kpis", label: "KPIs", icon: BarChart3 },
  { id: "insights", label: "Insights IA", icon: BrainCircuit }
] satisfies Array<{ id: Page; label: string; icon: typeof FileUp }>;

export function App() {
  const [page, setPage] = useState<Page>("upload");
  const [kpis, setKpis] = useState<DashboardKpis | null>(null);
  const [categories, setCategories] = useState<ChartItem[]>([]);
  const [severities, setSeverities] = useState<ChartItem[]>([]);
  const [requests, setRequests] = useState<UserErrorRequest[]>([]);
  const [pipelineRuns, setPipelineRuns] = useState<PipelineRun[]>([]);
  const [analysis, setAnalysis] = useState<AgentAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const latestRun = pipelineRuns[0] ?? null;
  const lastAnalysisDate = useMemo(() => new Date().toLocaleDateString("pt-BR"), []);

  async function refreshData() {
    const [nextKpis, nextCategories, nextSeverities, nextRequests, nextRuns] = await Promise.all([
      fetchKpis(),
      fetchCategoryChart(),
      fetchSeverityChart(),
      fetchRequests(),
      fetchPipelineRuns()
    ]);
    setKpis(nextKpis);
    setCategories(nextCategories);
    setSeverities(nextSeverities);
    setRequests(nextRequests);
    setPipelineRuns(nextRuns);
  }

  async function handleAnalyze() {
    setIsAnalyzing(true);
    try {
      setAnalysis(await analyzeWithAgent());
    } finally {
      setIsAnalyzing(false);
    }
  }

  useEffect(() => {
    refreshData().catch(() => undefined);
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <img className="brand-mark" src="/favicon.svg" alt="Product Error Intelligence" />
          <strong>Product Error Intelligence</strong>
        </div>
        <nav>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button className={page === item.id ? "active" : ""} key={item.id} onClick={() => setPage(item.id)}>
                <Icon size={18} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <strong>Product Error Intelligence Pipeline</strong>
            <span>Status do último pipeline: {latestRun?.status ?? "sem execução"}</span>
          </div>
          <span>Última análise: {lastAnalysisDate}</span>
        </header>
        {page === "upload" && <UploadPage latestRun={latestRun} onUploaded={() => refreshData()} />}
        {page === "pipeline" && <UploadPage latestRun={latestRun} onUploaded={() => refreshData()} />}
        {page === "requests" && <RequestsTablePage requests={requests} />}
        {page === "kpis" && <DashboardPage kpis={kpis} categories={categories} severities={severities} />}
        {page === "insights" && <InsightsPage analysis={analysis} onAnalyze={handleAnalyze} isLoading={isAnalyzing} />}
      </main>
    </div>
  );
}
