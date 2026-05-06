import { PipelineRun } from "../services/api";
import { PipelineVisualizer } from "../components/PipelineVisualizer";
import { UploadBox } from "../components/UploadBox";

type Props = {
  latestRun: PipelineRun | null;
  onUploaded: (run: PipelineRun) => void;
};

export function UploadPage({ latestRun, onUploaded }: Props) {
  return (
    <div className="page-stack">
      <div className="page-heading">
        <h1>Upload e pipeline</h1>
        <p>Envie um CSV no schema esperado para validar, limpar, classificar e persistir as solicitações.</p>
      </div>
      <UploadBox onUploaded={onUploaded} />
      <PipelineVisualizer run={latestRun} />
    </div>
  );
}
