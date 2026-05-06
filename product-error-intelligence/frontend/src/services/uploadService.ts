import { api, PipelineRun } from "./api";
import axios from "axios";

export async function uploadCsv(file: File): Promise<PipelineRun> {
  const form = new FormData();
  form.append("file", file);
  try {
    const response = await api.post<PipelineRun>("/upload", form);
    return response.data;
  } catch (err) {
    if (axios.isAxiosError(err)) {
      const data = err.response?.data as unknown;
      if (data && typeof data === "object" && "detail" in data) {
        const detail = (data as { detail?: unknown }).detail;
        if (typeof detail === "string" && detail.trim()) {
          throw new Error(detail);
        }
      }
      if (typeof data === "string" && data.trim()) {
        throw new Error(data);
      }
      throw new Error(err.message);
    }
    throw err;
  }
}
