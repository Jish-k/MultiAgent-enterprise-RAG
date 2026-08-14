"use client";

import { useState, useCallback } from "react";
import {
  ReactFlow,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  NodeChange,
  EdgeChange,
  Node,
  Edge,
  Handle,
  Position,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Database, FileText, LayoutList, Layers, HelpCircle, GitBranch, Search, Brain, PenTool, Cpu, ShieldCheck, CheckSquare } from "lucide-react";

// --- Custom Node Component ---
const getCategoryStyles = (category: string) => {
  if (category === "data" || category === "infra") return { bg: "#DCE6F1", border: "#2E5090" };
  if (category === "agent" || category === "input" || category === "output") return { bg: "#F2F2F2", border: "#4D4D4D" };
  if (category === "verification") return { bg: "#F8D7DA", border: "#A94442" };
  return { bg: "#ffffff", border: "#cccccc" };
};

const CustomNode = ({ data, selected }: any) => {
  const { bg, border } = getCategoryStyles(data.category);
  return (
    <div 
      className={`px-4 py-3 shadow-md rounded-xl border-2 flex flex-col items-center justify-center min-w-[220px] max-w-[240px] transition-all ${selected ? 'shadow-xl scale-105 ring-4 ring-primary/20' : 'hover:shadow-lg'}`}
      style={{ backgroundColor: bg, borderColor: border }}
    >
      <Handle type="target" position={Position.Top} id="top" className="w-2 h-2 bg-slate-500 border-none opacity-0" />
      <Handle type="target" position={Position.Left} id="left" className="w-2 h-2 bg-slate-500 border-none opacity-0" />
      <Handle type="target" position={Position.Right} id="right" className="w-2 h-2 bg-slate-500 border-none opacity-0" />
      
      {data.icon && (
        <div className="mb-2 text-[#4D4D4D]">
          {data.icon}
        </div>
      )}
      <div className="font-bold text-sm text-center text-[#111111] leading-tight">{data.label}</div>
      {data.subtext && <div className="text-[10px] mt-1 text-center text-[#4D4D4D] leading-tight opacity-70 group-hover:opacity-100">{data.subtext}</div>}
      
      <Handle type="source" position={Position.Bottom} id="bottom" className="w-2 h-2 bg-slate-500 border-none opacity-0" />
      <Handle type="source" position={Position.Left} id="left-src" className="w-2 h-2 bg-slate-500 border-none opacity-0" />
      <Handle type="source" position={Position.Right} id="right-src" className="w-2 h-2 bg-slate-500 border-none opacity-0" />
    </div>
  );
};

// --- Data & Definitions ---
const nodeTypes = { custom: CustomNode };

const initialNodes: Node[] = [
  { id: "corpus", type: "custom", position: { x: 50, y: 0 }, data: { label: "HotpotQA Corpus", subtext: "Wikipedia passages used as the retrieval corpus.", category: "data", icon: <Database className="w-5 h-5" /> } },
  { id: "chunking", type: "custom", position: { x: 50, y: 140 }, data: { label: "Passage Chunking", subtext: "Splits documents into overlapping semantic chunks.", category: "data", icon: <Layers className="w-5 h-5" /> } },
  { id: "embedding", type: "custom", position: { x: 50, y: 280 }, data: { label: "Dense Embedding (MiniLM)", subtext: "Encodes chunks into vector embeddings via all-MiniLM-L6-v2.", category: "data", icon: <LayoutList className="w-5 h-5" /> } },
  { id: "vector_index", type: "custom", position: { x: 50, y: 420 }, data: { label: "Vector Index", subtext: "ChromaDB collection storing embeddings and chunk metadata.", category: "data", icon: <Database className="w-5 h-5" /> } },

  { id: "query", type: "custom", position: { x: 350, y: 0 }, data: { label: "Multi-hop Query", subtext: "Incoming user question from the HotpotQA dev/test split.", category: "input", icon: <HelpCircle className="w-5 h-5" /> } },
  { id: "decomposition", type: "custom", position: { x: 350, y: 140 }, data: { label: "Query Decomposition", subtext: "Planner Agent breaks the query into targeted sub-queries.", category: "agent", icon: <GitBranch className="w-5 h-5" /> } },
  
  { id: "retrieval", type: "custom", position: { x: 200, y: 420 }, data: { label: "Evidence Retrieval", subtext: "Retrieval Agent fetches and ranks the most relevant passages.", category: "agent", icon: <Search className="w-5 h-5" /> } },
  { id: "synthesis", type: "custom", position: { x: 200, y: 560 }, data: { label: "Fact Synthesis", subtext: "Reasoner Agent extracts atomic key facts from retrieved evidence.", category: "agent", icon: <Brain className="w-5 h-5" /> } },
  { id: "generation", type: "custom", position: { x: 200, y: 700 }, data: { label: "Answer Generation", subtext: "Reasoner Agent drafts an answer grounded strictly in the key facts.", category: "agent", icon: <PenTool className="w-5 h-5" /> } },
  
  { id: "llm", type: "custom", position: { x: 550, y: 700 }, data: { label: "Pluggable LLM Backend", subtext: "Swappable LLM provider (OpenAI, Anthropic, Groq, or Ollama).", category: "infra", icon: <Cpu className="w-5 h-5" /> } },

  { id: "verification", type: "custom", position: { x: 200, y: 840 }, data: { label: "Claim Verification", subtext: "Verifier Agent checks each claim against evidence and computes ESS = supported claims / total claims.", category: "verification", icon: <ShieldCheck className="w-5 h-5" /> } },
  { id: "answer", type: "custom", position: { x: 200, y: 980 }, data: { label: "Verified Answer", subtext: "Final answer with citations and Evidence Sufficiency Score.", category: "output", icon: <CheckSquare className="w-5 h-5" /> } },
];

const edgeLabelStyle = { fill: '#ffffff', fontWeight: 600, fontSize: 11 };
const edgeLabelBgStyle = { fill: '#4D4D4D', color: '#fff', fillOpacity: 1, stroke: '#4D4D4D', strokeWidth: 1, rx: 4, ry: 4 };

const initialEdges: Edge[] = [
  { id: "e-c-ch", source: "corpus", target: "chunking", animated: true, style: { stroke: '#4D4D4D', strokeWidth: 2 } },
  { id: "e-ch-emb", source: "chunking", target: "embedding", animated: true, style: { stroke: '#4D4D4D', strokeWidth: 2 } },
  { id: "e-emb-vi", source: "embedding", target: "vector_index", animated: true, style: { stroke: '#4D4D4D', strokeWidth: 2 } },
  { id: "e-q-qd", source: "query", target: "decomposition", animated: true, style: { stroke: '#4D4D4D', strokeWidth: 2 } },
  { 
    id: "e-qd-er", source: "decomposition", target: "retrieval", sourceHandle: "bottom", targetHandle: "top", animated: true, 
    label: "sub-queries", style: { stroke: '#4D4D4D', strokeWidth: 2 },
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-vi-er", source: "vector_index", target: "retrieval", sourceHandle: "right-src", targetHandle: "left", animated: true, 
    label: "top-k passages", style: { stroke: '#4D4D4D', strokeWidth: 2 },
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-er-fs", source: "retrieval", target: "synthesis", animated: true, 
    label: "evidence", style: { stroke: '#4D4D4D', strokeWidth: 2 },
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-fs-ag", source: "synthesis", target: "generation", animated: true, 
    label: "key facts", style: { stroke: '#4D4D4D', strokeWidth: 2 },
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-llm-ag", source: "llm", target: "generation", sourceHandle: "left-src", targetHandle: "right", animated: true, 
    label: "generation", style: { stroke: '#4D4D4D', strokeWidth: 2 },
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-ag-cv", source: "generation", target: "verification", animated: true, 
    label: "draft answer", style: { stroke: '#4D4D4D', strokeWidth: 2 },
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-cv-va", source: "verification", target: "answer", animated: true, 
    label: "citations + ESS", style: { stroke: '#4D4D4D', strokeWidth: 2 },
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-cv-fs", source: "verification", target: "synthesis", sourceHandle: "right-src", targetHandle: "right", animated: true, 
    style: { stroke: '#4D4D4D', strokeWidth: 2, strokeDasharray: '5,5' },
    label: "unsupported claim", 
    labelBgPadding: [6, 4], labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle,
    type: 'smoothstep'
  },
];

const nodeDetails: Record<string, any> = {
  corpus: { purpose: "Wikipedia passages used as the retrieval corpus.", category: "data" },
  chunking: { purpose: "Splits documents into overlapping semantic chunks.", category: "data" },
  embedding: { purpose: "Encodes chunks into vector embeddings via all-MiniLM-L6-v2.", category: "data" },
  vector_index: { purpose: "ChromaDB collection storing embeddings and chunk metadata.", category: "data" },
  query: { purpose: "Incoming user question from the HotpotQA dev/test split.", category: "input" },
  decomposition: { purpose: "Planner Agent breaks the query into targeted sub-queries.", category: "agent" },
  retrieval: { purpose: "Retrieval Agent fetches and ranks the most relevant passages.", category: "agent" },
  synthesis: { purpose: "Reasoner Agent extracts atomic key facts from retrieved evidence.", category: "agent" },
  generation: { purpose: "Reasoner Agent drafts an answer grounded strictly in the key facts.", category: "agent" },
  llm: { purpose: "Swappable LLM provider (OpenAI, Anthropic, Groq, or Ollama).", category: "infra" },
  verification: { purpose: "Verifier Agent checks each claim against evidence and computes ESS = supported claims / total claims.", category: "verification" },
  answer: { purpose: "Final answer with citations and Evidence Sufficiency Score.", category: "output" }
};

export default function ArchitectureExplorer() {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [selectedNode, setSelectedNode] = useState<string>("verification");

  const onNodesChange = useCallback(
    (changes: NodeChange<Node>[]) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes: EdgeChange<Edge>[]) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onNodeClick = (_: any, node: Node) => {
    setSelectedNode(node.id);
  };

  const details = nodeDetails[selectedNode] || null;

  return (
    <section id="architecture" className="min-h-screen py-24 flex flex-col">
      <div className="mb-12 text-center md:text-left">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Pipeline Architecture</h2>
        <p className="text-lg text-muted-foreground max-w-4xl">
          This pipeline answers multi-hop questions from HotpotQA by decomposing the query, 
          retrieving supporting passages from a Wikipedia vector index, synthesizing evidence 
          into key facts, and generating a draft answer via a pluggable LLM backend. Before the 
          answer is returned, a dedicated Verifier Agent cross-checks every claim against the 
          retrieved evidence and computes an Evidence Sufficiency Score (ESS), flagging or 
          correcting any unsupported statements. This deterministic verification step is what 
          distinguishes the system from standard single-pass RAG.
        </p>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8 min-h-[600px] h-[800px] lg:h-auto">
        
        {/* Interactive Graph */}
        <Card className="lg:col-span-2 overflow-hidden border-border/50 bg-background/50 shadow-xl shadow-primary/5">
          <div className="h-full w-full bg-grid-white/[0.02] min-h-[600px]">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onNodeClick={onNodeClick}
              fitView
              attributionPosition="bottom-left"
              className="bg-transparent"
            >
              <Background gap={24} size={2} className="opacity-20" />
              <Controls className="bg-background border-border/50 fill-foreground shadow-lg" />
            </ReactFlow>
          </div>
        </Card>

        {/* Node Details Panel */}
        <Card className="bg-card border-border/50 shadow-xl overflow-y-auto">
          <CardHeader className="bg-secondary/30 border-b border-border/50 sticky top-0 z-10 backdrop-blur-xl pb-6">
            <div className="flex items-center gap-3">
              <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20 uppercase tracking-wider">
                Selected Node
              </Badge>
            </div>
            <CardTitle className="text-2xl font-bold mt-2 flex items-center gap-3 text-foreground">
              {initialNodes.find(n => n.id === selectedNode)?.data.label}
            </CardTitle>
          </CardHeader>
          
          <CardContent className="p-6 space-y-8">
            {details ? (
              <>
                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Category</h4>
                  <Badge variant="secondary" className="px-3 py-1 font-mono text-xs capitalize">{details.category}</Badge>
                </div>
                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Description</h4>
                  <p className="text-lg leading-relaxed">{details.purpose}</p>
                </div>
              </>
            ) : (
              <div className="h-full flex items-center justify-center text-muted-foreground">
                Select a node to view details
              </div>
            )}
          </CardContent>
        </Card>

      </div>
    </section>
  );
}
