import { RequestsTable } from "../components/RequestsTable";
import { UserErrorRequest } from "../services/api";

export function RequestsTablePage({ requests }: { requests: UserErrorRequest[] }) {
  return (
    <div className="page-stack">
      <div className="page-heading">
        <h1>Tabela de Solicitações</h1>
        <p>Registros padronizados com classificação, severidade e score de impacto.</p>
      </div>
      <RequestsTable data={requests} />
    </div>
  );
}
