type KPICardProps = {
  label: string;
  value: string | number;
  tone?: "default" | "critical" | "success";
};

export function KPICard({ label, value, tone = "default" }: KPICardProps) {
  return (
    <div className={`kpi-card kpi-card--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
