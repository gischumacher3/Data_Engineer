import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { ChartItem } from "../services/api";

const colors = ["#b42318", "#e5484d", "#f59e0b", "#16a34a"];

export function SeverityChart({ data }: { data: ChartItem[] }) {
  return (
    <div className="chart-panel">
      <h2>Erros por severidade</h2>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" outerRadius={88} label>
            {data.map((item, index) => (
              <Cell key={item.name} fill={colors[index % colors.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
