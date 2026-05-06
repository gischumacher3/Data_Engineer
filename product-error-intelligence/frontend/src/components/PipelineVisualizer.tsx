import { Check, Clock, Loader2 } from "lucide-react";
import { PipelineRun } from "../services/api";

const steps = [
  "Upload CSV",
  "Validação de Schema",
  "Limpeza dos Dados",
  "Padronização",
  "Classificação",
  "Cálculo de KPIs",
  "Análise com IA",
  "Dados Prontos"
];

type PipelineVisualizerProps = {
  run?: PipelineRun | null;
};

export function PipelineVisualizer({ run }: PipelineVisualizerProps) {
  const status = run?.status ?? "pending";
  return (
    <section className="pipeline">
      {steps.map((step, index) => {
        const isDone = status === "success";
        const isRunning = status === "running" && index < 5;
        return (
          <div className={`pipeline-step ${isDone ? "success" : isRunning ? "running" : "pending"}`} key={step}>
            {isDone ? <Check size={16} /> : isRunning ? <Loader2 size={16} /> : <Clock size={16} />}
            <span>{step}</span>
          </div>
        );
      })}
    </section>
  );
}
