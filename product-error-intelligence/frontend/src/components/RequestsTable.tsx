import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { UserErrorRequest } from "../services/api";

const columnHelper = createColumnHelper<UserErrorRequest>();

const columns = [
  columnHelper.accessor("client_name", { header: "Cliente" }),
  columnHelper.accessor("company", { header: "Empresa" }),
  columnHelper.accessor("problem_category", { header: "Categoria" }),
  columnHelper.accessor("severity", { header: "Severidade" }),
  columnHelper.accessor("business_impact_score", {
    header: "Impacto",
    cell: (info) => info.getValue()?.toFixed(1) ?? "-"
  }),
  columnHelper.accessor("is_finished", {
    header: "Status",
    cell: (info) => (info.getValue() ? "Finalizada" : "Aberta")
  })
];

export function RequestsTable({ data }: { data: UserErrorRequest[] }) {
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() });

  return (
    <div className="table-panel">
      <h2>Tabela de solicitações tratadas</h2>
      <div className="table-scroll">
        <table>
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id}>{flexRender(header.column.columnDef.header, header.getContext())}</th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
