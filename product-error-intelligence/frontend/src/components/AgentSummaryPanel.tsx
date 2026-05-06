import { BrainCircuit } from "lucide-react";
import { Fragment } from "react";
import { AgentAnalysis } from "../services/agentService";

function normalizeMarkdownInput(value: string): string {
  return value
    .replace(/\r\n/g, "\n")
    .replace(/\s+(#{2,6}\s)/g, "\n$1")
    .replace(/\s+(\d+\.\s)/g, "\n$1")
    .replace(/\s+([-*]\s)/g, "\n$1")
    .trim();
}

function renderInline(text: string) {
  const parts = text.split("**");
  if (parts.length === 1) return text;
  return parts.map((part, index) => {
    const key = `${index}-${part}`;
    if (index % 2 === 1) return <strong key={key}>{part}</strong>;
    return <Fragment key={key}>{part}</Fragment>;
  });
}

function renderMarkdown(text: string) {
  const normalized = normalizeMarkdownInput(text);
  const lines = normalized.split("\n");
  const blocks: Array<
    | { type: "h2" | "h3" | "h4"; text: string }
    | { type: "p"; text: string }
    | { type: "ol" | "ul"; items: string[] }
  > = [];

  let paragraph: string[] = [];
  let listType: "ol" | "ul" | null = null;
  let listItems: string[] = [];

  const flushParagraph = () => {
    const content = paragraph.join(" ").trim();
    if (content) blocks.push({ type: "p", text: content });
    paragraph = [];
  };

  const flushList = () => {
    if (listType && listItems.length) blocks.push({ type: listType, items: listItems });
    listType = null;
    listItems = [];
  };

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      flushParagraph();
      flushList();
      continue;
    }

    if (line.startsWith("### ")) {
      flushParagraph();
      flushList();
      blocks.push({ type: "h4", text: line.slice(4).trim() });
      continue;
    }

    if (line.startsWith("## ")) {
      flushParagraph();
      flushList();
      blocks.push({ type: "h3", text: line.slice(3).trim() });
      continue;
    }

    if (line.startsWith("# ")) {
      flushParagraph();
      flushList();
      blocks.push({ type: "h2", text: line.slice(2).trim() });
      continue;
    }

    const ordered = line.match(/^\d+\.\s+(.*)$/);
    if (ordered) {
      flushParagraph();
      if (listType && listType !== "ol") flushList();
      listType = "ol";
      listItems.push(ordered[1].trim());
      continue;
    }

    const unordered = line.match(/^[-*]\s+(.*)$/);
    if (unordered) {
      flushParagraph();
      if (listType && listType !== "ul") flushList();
      listType = "ul";
      listItems.push(unordered[1].trim());
      continue;
    }

    if (listType) {
      listItems[listItems.length - 1] = `${listItems[listItems.length - 1]} ${line}`.trim();
      continue;
    }

    paragraph.push(line);
  }

  flushParagraph();
  flushList();

  return blocks.map((block, index) => {
    switch (block.type) {
      case "h2":
        return <h2 key={index}>{renderInline(block.text)}</h2>;
      case "h3":
        return <h3 key={index}>{renderInline(block.text)}</h3>;
      case "h4":
        return <h4 key={index}>{renderInline(block.text)}</h4>;
      case "p":
        return <p key={index}>{renderInline(block.text)}</p>;
      case "ol":
        return (
          <ol key={index}>
            {block.items.map((item: string, itemIndex: number) => (
              <li key={`${itemIndex}-${item}`}>{renderInline(item)}</li>
            ))}
          </ol>
        );
      case "ul":
        return (
          <ul key={index}>
            {block.items.map((item: string, itemIndex: number) => (
              <li key={`${itemIndex}-${item}`}>{renderInline(item)}</li>
            ))}
          </ul>
        );
    }
  });
}

export function AgentSummaryPanel({ analysis }: { analysis: AgentAnalysis | null }) {
  return (
    <section className="agent-panel">
      <div className="panel-title">
        <BrainCircuit size={20} />
        <h2>Insights IA</h2>
      </div>
      <div className="markdown">
        {analysis?.analysis ? renderMarkdown(analysis.analysis) : <p>Execute uma análise para gerar recomendações de produto.</p>}
      </div>
      <ul>
        {(analysis?.recommendations ?? []).map((recommendation) => (
          <li key={recommendation}>{recommendation}</li>
        ))}
      </ul>
    </section>
  );
}
