"use client";

import { Card } from "@/components/ui/card";

export default function ArchitectureExplorer() {
  return (
    <section id="architecture" className="min-h-screen py-24 flex flex-col">
      <div className="mb-12 text-center">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Architecture Explorer</h2>
        <p className="text-xl text-muted-foreground">
          A high-level view of the Multi-Agent RAG Pipeline
        </p>
      </div>

      <div className="flex-1 flex justify-center items-center px-4 w-full max-w-5xl mx-auto">
        <Card className="w-full overflow-hidden border-border/50 bg-black shadow-2xl shadow-primary/10">
          {/* Terminal Header */}
          <div className="h-10 bg-zinc-900 border-b border-zinc-800 flex items-center px-4 gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
            <span className="ml-4 text-xs font-mono text-zinc-500">architecture.txt</span>
          </div>
          
          {/* ASCII Diagram */}
          <div className="p-8 overflow-x-auto">
            <pre className="font-mono text-sm md:text-base leading-snug text-green-400">
{`                        ┌──────────────────────────────┐
                        │        User Question         │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │        Planner Agent                │
                    │-------------------------------------│
                    │ • Intent Detection                  │
                    │ • Query Decomposition               │
                    │ • Retrieval Planning                │
                    └──────────────┬──────────────────────┘
                                   │
                    Multiple Retrieval Queries
                                   │
                                   ▼
                    ┌─────────────────────────────────────┐
                    │     Evidence Retrieval Agent        │
                    │-------------------------------------│
                    │ • ChromaDB Search                  │
                    │ • Semantic Similarity Ranking      │
                    │ • Evidence Merging                 │
                    │ • Duplicate Removal                │
                    └──────────────┬──────────────────────┘
                                   │
                           Ranked Evidence
                                   │
                                   ▼
                    ┌─────────────────────────────────────┐
                    │        Reasoner Agent              │
                    │-------------------------------------│
                    │ • Evidence Analysis               │
                    │ • Multi-hop Reasoning             │
                    │ • Answer Synthesis                │
                    └──────────────┬──────────────────────┘
                                   │
                             Draft Answer
                                   │
                                   ▼
                    ┌─────────────────────────────────────┐
                    │        Verifier Agent              │
                    │-------------------------------------│
                    │ • Claim Validation                │
                    │ • Evidence Sufficiency            │
                    │ • Hallucination Detection         │
                    │ • Citation Verification           │
                    └──────────────┬──────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────────────┐
                    │        Final Response              │
                    │-------------------------------------│
                    │ Answer + Citations + Confidence    │
                    └─────────────────────────────────────┘`}
            </pre>
          </div>
        </Card>
      </div>
    </section>
  );
}
