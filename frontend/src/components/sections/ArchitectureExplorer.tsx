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
import { Brain, Search, GitBranch, CheckSquare, MessageSquare } from "lucide-react";

// --- Custom Node Component ---
const CustomNode = ({ data, selected }: any) => {
  return (
    <div className={`px-6 py-4 shadow-xl rounded-2xl border-2 bg-background flex flex-col items-center justify-center min-w-[240px] transition-all ${selected ? 'border-primary shadow-primary/20 scale-105' : 'border-border/50 hover:border-primary/50 hover:shadow-primary/10'}`}>
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-primary" />
      <div className={`p-3 rounded-full mb-3 ${selected ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
        {data.icon}
      </div>
      <div className="font-bold text-lg text-center">{data.label}</div>
      {data.subtext && <div className="text-xs text-muted-foreground mt-1 text-center whitespace-pre-wrap">{data.subtext}</div>}
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-primary" />
    </div>
  );
};

// --- Data & Definitions ---
const nodeTypes = { custom: CustomNode };

const initialNodes: Node[] = [
  { id: "question", type: "custom", position: { x: 250, y: 0 }, data: { label: "User Question", icon: <MessageSquare className="w-6 h-6" /> } },
  { id: "planner", type: "custom", position: { x: 250, y: 150 }, data: { label: "Planner Agent", icon: <GitBranch className="w-6 h-6" /> } },
  { id: "retriever", type: "custom", position: { x: 250, y: 300 }, data: { label: "Evidence Retrieval Agent", icon: <Search className="w-6 h-6" /> } },
  { id: "reasoner", type: "custom", position: { x: 250, y: 450 }, data: { label: "Reasoner Agent", icon: <Brain className="w-6 h-6" /> } },
  { id: "verifier", type: "custom", position: { x: 250, y: 600 }, data: { label: "Verifier Agent", icon: <CheckSquare className="w-6 h-6" /> } },
  { id: "answer", type: "custom", position: { x: 250, y: 750 }, data: { label: "Final Response", subtext: "Answer + Citations + Confidence", icon: <MessageSquare className="w-6 h-6" /> } },
];

// Reusing tailwind classes for the label text for a sleek dark mode look
const edgeLabelStyle = { fill: '#fff', fontWeight: 600, fontSize: 12 };
const edgeLabelBgStyle = { fill: '#18181b', color: '#fff', fillOpacity: 0.9, stroke: '#3f3f46', strokeWidth: 1 };

const initialEdges: Edge[] = [
  { id: "e-q-p", source: "question", target: "planner", animated: true },
  { 
    id: "e-p-r", source: "planner", target: "retriever", animated: true, 
    label: "Multiple Retrieval Queries", 
    labelBgPadding: [8, 4], labelBgBorderRadius: 4, labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-r-rs", source: "retriever", target: "reasoner", animated: true, 
    label: "Ranked Evidence", 
    labelBgPadding: [8, 4], labelBgBorderRadius: 4, labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { 
    id: "e-rs-v", source: "reasoner", target: "verifier", animated: true, 
    label: "Draft Answer", 
    labelBgPadding: [8, 4], labelBgBorderRadius: 4, labelBgStyle: edgeLabelBgStyle, labelStyle: edgeLabelStyle 
  },
  { id: "e-v-a", source: "verifier", target: "answer", animated: true },
];

const nodeDetails: Record<string, any> = {
  question: {
    purpose: "The entry point of the pipeline.",
    capabilities: [
      "Accepts raw user text"
    ],
    inputs: "String (Raw User Text)",
    outputs: "String",
  },
  planner: {
    purpose: "Deconstructs complex multi-hop questions into multiple parallel search queries to maximize recall.",
    capabilities: [
      "Intent Detection",
      "Query Decomposition",
      "Retrieval Planning"
    ],
    inputs: "User Question (String)",
    outputs: "Multiple Retrieval Queries",
  },
  retriever: {
    purpose: "Fetches the top-k most semantically relevant paragraphs for every generated sub-query and deduplicates them.",
    capabilities: [
      "ChromaDB Search",
      "Semantic Similarity Ranking",
      "Evidence Merging",
      "Duplicate Removal"
    ],
    inputs: "Multiple Retrieval Queries",
    outputs: "Ranked Evidence",
  },
  reasoner: {
    purpose: "Synthesizes the retrieved chunks and establishes a logical chain of thought to arrive at an answer.",
    capabilities: [
      "Evidence Analysis",
      "Multi-hop Reasoning",
      "Answer Synthesis"
    ],
    inputs: "Ranked Evidence",
    outputs: "Draft Answer",
  },
  verifier: {
    purpose: "Critiques the reasoner's output against the raw retrieved facts to catch and correct hallucinations.",
    capabilities: [
      "Claim Validation",
      "Evidence Sufficiency",
      "Hallucination Detection",
      "Citation Verification"
    ],
    inputs: "Draft Answer",
    outputs: "Final Response",
  },
  answer: {
    purpose: "The final output delivered back to the user.",
    capabilities: [
      "Answer Formatting",
      "Citation Injection",
      "Confidence Scoring"
    ],
    inputs: "Final Response",
    outputs: "Answer + Citations + Confidence",
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
      <div className="mb-12 text-center md:text-left">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Architecture Explorer</h2>
        <p className="text-xl text-muted-foreground">
          Click on any node in the pipeline to explore its purpose, capabilities, and data flow.
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
              {initialNodes.find(n => n.id === selectedNode)?.data.label}
            </CardTitle>
          </CardHeader>
          
          <CardContent className="p-6 space-y-8">
            {details ? (
              <>
                <div className="space-y-4">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Capabilities</h4>
                  <ul className="space-y-2">
                    {details.capabilities.map((cap: string, i: number) => (
                      <li key={i} className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                        <span className="font-medium">{cap}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Purpose</h4>
                  <p className="text-lg leading-relaxed">{details.purpose}</p>
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
