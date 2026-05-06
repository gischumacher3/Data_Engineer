import { Upload } from "lucide-react";
import { useRef, useState } from "react";
import { uploadCsv } from "../services/uploadService";
import { PipelineRun } from "../services/api";

type UploadBoxProps = {
  onUploaded: (run: PipelineRun) => void;
};

export function UploadBox({ onUploaded }: UploadBoxProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleFile(file: File | undefined) {
    if (!file) return;
    setIsUploading(true);
    setError(null);
    try {
      const run = await uploadCsv(file);
      onUploaded(run);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao processar CSV.");
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section className="upload-box">
      <input
        ref={inputRef}
        type="file"
        accept=".csv,text/csv"
        onChange={(event) => handleFile(event.target.files?.[0])}
      />
      <button type="button" onClick={() => inputRef.current?.click()} disabled={isUploading}>
        <Upload size={18} />
        {isUploading ? "Processando" : "Enviar CSV"}
      </button>
      {error && <p className="inline-error">{error}</p>}
    </section>
  );
}
