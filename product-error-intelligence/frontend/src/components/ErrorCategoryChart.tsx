import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { ChartItem } from "../services/api";

type Props = {
  data: ChartItem[];
};

export function ErrorCategoryChart({ data }: Props) {
  return (
    <div className="chart-panel">
      <h2>Solicitações por categoria</h2>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} angle={-20} textAnchor="end" height={70} />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="value" fill="#e5484d" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
