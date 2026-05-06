import { ErrorCategoryChart } from "../components/ErrorCategoryChart";
import { KPICard } from "../components/KPICard";
import { SeverityChart } from "../components/SeverityChart";
import { ChartItem, DashboardKpis } from "../services/api";

type Props = {
  kpis: DashboardKpis | null;
  categories: ChartItem[];
  severities: ChartItem[];
};

export function DashboardPage({ kpis, categories, severities }: Props) {
  return (
    <div className="page-stack">
      <div className="page-heading">
        <h1>KPIs</h1>
        <p>Qualidade da ingestão, concentração de erros e impacto de produto.</p>
      </div>
      <section className="kpi-grid">
        <KPICard label="Total de Solicitações" value={kpis?.total_requests ?? 0} />
        <KPICard label="Taxa de Completude" value={`${kpis?.data_completeness ?? 0}%`} tone="success" />
        <KPICard label="Taxa de Duplicidade" value={`${kpis?.duplicate_rate ?? 0}%`} />
        <KPICard label="Taxa de Finalização" value={`${kpis?.finished_rate ?? 0}%`} />
        <KPICard label="Categoria Mais Frequente" value={kpis?.top_category ?? "-"} />
        <KPICard label="Erros Críticos" value={kpis?.critical_errors ?? 0} tone="critical" />
        <KPICard label="Business Impact Médio" value={kpis?.average_business_impact ?? 0} />
        <KPICard label="Latência do Pipeline" value={`${kpis?.pipeline_latency_seconds ?? 0}s`} />
      </section>
      <section className="charts-grid">
        <ErrorCategoryChart data={categories} />
        <SeverityChart data={severities} />
      </section>
    </div>
  );
}
