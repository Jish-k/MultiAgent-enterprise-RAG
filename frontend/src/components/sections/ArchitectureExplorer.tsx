"use client";

import { useState, useCallback, useMemo } from "react";
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
import { Brain, Search, GitBranch, CheckSquare, MessageSquare, Database } from "lucide-react";

// --- Custom Node Component ---
const CustomNode = ({ data, selected }: any) => {
  return (
    <div className={`px-6 py-4 shadow-xl rounded-2xl border-2 bg-background flex flex-col items-center justify-center min-w-[180px] transition-all ${selected ? 'border-primary shadow-primary/20 scale-105' : 'border-border/50 hover:border-primary/50 hover:shadow-primary/10'}`}>
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-primary" />
      <div className={`p-3 rounded-full mb-3 ${selected ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
        {data.icon}
      </div>
      <div className="font-bold text-lg">{data.label}</div>
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-primary" />
    </div>
  );
};

// --- Data & Definitions ---
const nodeTypes = { custom: CustomNode };

const initialNodes: Node[] = [
  { id: "question", type: "custom", position: { x: 250, y: 0 }, data: { label: "User Question", icon: <MessageSquare className="w-6 h-6" /> } },
  { id: "planner", type: "custom", position: { x: 250, y: 150 }, data: { label: "Planner Agent", icon: <GitBranch className="w-6 h-6" /> } },
  { id: "retriever", type: "custom", position: { x: 250, y: 300 }, data: { label: "Retriever", icon: <Search className="w-6 h-6" /> } },
  { id: "chroma", type: "custom", position: { x: 50, y: 300 }, data: { label: "ChromaDB", icon: <Database className="w-6 h-6" /> } },
  { id: "reasoner", type: "custom", position: { x: 250, y: 450 }, data: { label: "Reasoner Agent", icon: <Brain className="w-6 h-6" /> } },
  { id: "verifier", type: "custom", position: { x: 250, y: 600 }, data: { label: "Verifier Agent", icon: <CheckSquare className="w-6 h-6" /> } },
  { id: "answer", type: "custom", position: { x: 250, y: 750 }, data: { label: "Final Answer", icon: <MessageSquare className="w-6 h-6" /> } },
];

const initialEdges: Edge[] = [
  { id: "e-q-p", source: "question", target: "planner", animated: true },
  { id: "e-p-r", source: "planner", target: "retriever", animated: true },
  { id: "e-c-r", source: "chroma", target: "retriever", animated: false, type: "step" },
  { id: "e-r-rs", source: "retriever", target: "reasoner", animated: true },
  { id: "e-rs-v", source: "reasoner", target: "verifier", animated: true },
  { id: "e-v-a", source: "verifier", target: "answer", animated: true },
];

const nodeDetails: Record<string, any> = {
  question: {
    purpose: "The entry point of the pipeline.",
    inputs: "String (Raw User Text)",
    outputs: "String",
    algorithm: "N/A",
    codeLocation: "frontend/src/components/...",
    example: '"Who was born first, Percy Clifford Mills or Nigel Graham Pearson?"'
  },
  planner: {
    purpose: "Deconstructs complex multi-hop questions into multiple parallel search queries to maximize recall.",
    inputs: "User Question (String)",
    outputs: "List of Strings (Sub-queries)",
    algorithm: "Few-shot prompting with an LLM to generate orthogonal search vectors.",
    codeLocation: "backend/agent/planner.py",
    example: '["Percy Clifford Mills birth date", "Nigel Graham Pearson birth date"]'
  },
  retriever: {
    purpose: "Fetches the top-k most semantically relevant paragraphs for every generated sub-query.",
    inputs: "List of Sub-queries",
    outputs: "List of Document Chunks",
    algorithm: "Dense vector retrieval (Cosine Similarity) using all-MiniLM-L6-v2 embeddings.",
    codeLocation: "backend/rag/retriever.py",
    example: '"Percy Clifford Mills (born 1909)..." | "Nigel Graham Pearson (born 1963)..."'
  },
  chroma: {
    purpose: "Persistent vector storage for the enterprise dataset.",
    inputs: "Embeddings",
    outputs: "Nearest Neighbors",
    algorithm: "HNSW (Hierarchical Navigable Small World) Indexing",
    codeLocation: "backend/ingestion/loader.py",
    example: "Returns distance scores < 1.0"
  },
  reasoner: {
    purpose: "Synthesizes the retrieved chunks and establishes a logical chain of thought to arrive at an answer.",
    inputs: "User Question + Retrieved Chunks",
    outputs: "Reasoning Trace (Chain of Thought)",
    algorithm: "CoT Prompting (LLM analyzes step-by-step)",
    codeLocation: "backend/agent/reasoner.py",
    example: '"Mills was born in 1909. Pearson was born in 1963. Therefore, Mills was born first."'
  },
  verifier: {
    purpose: "Critiques the reasoner's output against the raw retrieved facts to catch and correct hallucinations.",
    inputs: "Reasoning Trace + Retrieved Chunks",
    outputs: "Final Verified Answer",
    algorithm: "Critique and Revise loop (Self-Correction)",
    codeLocation: "backend/agent/verifier.py",
    example: '"Verified: The birth dates match the provided context exactly."'
  },
  answer: {
    purpose: "The final output delivered back to the user.",
    inputs: "Verified Output",
    outputs: "String",
    algorithm: "N/A",
    codeLocation: "N/A",
    example: '"Percy Clifford Mills was born first (1909 vs 1963)."'
  }
};

export default function ArchitectureExplorer() {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [selectedNode, setSelectedNode] = useState<string>("planner");

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
      <div className="mb-12">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Architecture Explorer</h2>
        <p className="text-xl text-muted-foreground">
          Click on any node in the pipeline to explore its purpose, algorithms, and implementation details.
        </p>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8 min-h-[600px] h-[800px] lg:h-auto">
        
        {/* Interactive Graph */}
        <Card className="lg:col-span-2 overflow-hidden border-border/50 bg-background/50 shadow-xl shadow-primary/5">
          <div className="h-full w-full bg-grid-white/[0.02]">
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
                Selected Component
              </Badge>
            </div>
            <CardTitle className="text-3xl font-bold capitalize mt-2 flex items-center gap-3">
              {selectedNode}
            </CardTitle>
          </CardHeader>
          
          <CardContent className="p-6 space-y-8">
            {details ? (
              <>
                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Purpose</h4>
                  <p className="text-lg leading-relaxed">{details.purpose}</p>
                </div>

                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Algorithm</h4>
                  <div className="p-4 bg-secondary/50 rounded-xl border border-border/50 font-medium">
                    {details.algorithm}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Inputs</h4>
                    <Badge variant="secondary" className="px-3 py-1 font-mono text-xs whitespace-normal break-words h-auto text-left leading-relaxed">{details.inputs}</Badge>
                  </div>
                  <div className="space-y-2">
                    <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Outputs</h4>
                    <Badge variant="outline" className="px-3 py-1 font-mono text-xs whitespace-normal break-words h-auto text-left leading-relaxed">{details.outputs}</Badge>
                  </div>
                </div>

                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Example I/O</h4>
                  <div className="p-4 bg-muted/50 rounded-xl border border-border/50 font-mono text-sm break-words whitespace-pre-wrap">
                    {details.example}
                  </div>
                </div>

                <div className="space-y-2 pt-4 border-t border-border/50">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Code Location</h4>
                  <code className="text-xs text-primary px-2 py-1 bg-primary/10 rounded font-mono">
                    {details.codeLocation}
                  </code>
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
