"use client";

import { motion } from "framer-motion";
import { Settings2, Database, Brain, AlignLeft, CalendarClock, PlaySquare, AlertCircle, CheckCircle2, Server } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function SystemAppendix() {
  return (
    <section id="appendix" className="min-h-screen py-24 flex flex-col gap-16 relative">
      
      {/* 1. Configuration Viewer */}
      <div>
        <div className="mb-12">
          <h2 className="text-4xl font-bold tracking-tight mb-4 flex items-center">
            <Settings2 className="w-8 h-8 mr-4 text-primary" /> System Configuration
          </h2>
          <p className="text-lg text-muted-foreground">The exact hyper-parameters and models used during the final evaluation.</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="bg-card/40 backdrop-blur-xl border-border/50">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
              <Brain className="w-8 h-8 text-blue-500 mb-2" />
              <div className="text-sm text-muted-foreground uppercase tracking-wider font-bold">LLM Engine</div>
              <div className="text-lg font-mono">gpt-4o-mini</div>
            </CardContent>
          </Card>
          <Card className="bg-card/40 backdrop-blur-xl border-border/50">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
              <Database className="w-8 h-8 text-purple-500 mb-2" />
              <div className="text-sm text-muted-foreground uppercase tracking-wider font-bold">Vector Store</div>
              <div className="text-lg font-mono">ChromaDB</div>
            </CardContent>
          </Card>
          <Card className="bg-card/40 backdrop-blur-xl border-border/50">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
              <Server className="w-8 h-8 text-amber-500 mb-2" />
              <div className="text-sm text-muted-foreground uppercase tracking-wider font-bold">Embeddings</div>
              <div className="text-lg font-mono">all-MiniLM-L6-v2</div>
            </CardContent>
          </Card>
          <Card className="bg-card/40 backdrop-blur-xl border-border/50">
            <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
              <AlignLeft className="w-8 h-8 text-emerald-500 mb-2" />
              <div className="text-sm text-muted-foreground uppercase tracking-wider font-bold">Chunk Strategy</div>
              <div className="text-lg font-mono">1024 / 100 overlap</div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* 2. Metric History */}
      <div>
        <div className="mb-12">
          <h2 className="text-4xl font-bold tracking-tight mb-4 flex items-center">
            <CalendarClock className="w-8 h-8 mr-4 text-primary" /> Historical Progress
          </h2>
          <p className="text-lg text-muted-foreground">Tracking the evolution of accuracy over the project lifecycle.</p>
        </div>
        
        <div className="relative">
          <div className="absolute top-1/2 left-0 w-full h-1 bg-border -translate-y-1/2 hidden md:block" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 relative z-10">
            {[
              { date: "June 05", acc: "49%", note: "Naive Baseline" },
              { date: "June 12", acc: "62%", note: "Planner Added" },
              { date: "June 20", acc: "76%", note: "Reasoner Added" },
              { date: "July 02", acc: "92%", note: "Verifier Added" }
            ].map((milestone, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}
                className="flex flex-col items-center text-center"
              >
                <Badge variant="outline" className="mb-4 bg-background">{milestone.date}</Badge>
                <div className="w-4 h-4 bg-primary rounded-full mb-4 shadow-[0_0_10px_0] shadow-primary/50" />
                <div className="p-4 bg-card/60 backdrop-blur-md border border-border/50 rounded-xl w-full">
                  <div className="text-2xl font-bold font-mono text-primary mb-1">{milestone.acc}</div>
                  <div className="text-sm text-muted-foreground">{milestone.note}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* 3. Experiment Replay */}
      <div>
        <div className="mb-12">
          <h2 className="text-4xl font-bold tracking-tight mb-4 flex items-center">
            <PlaySquare className="w-8 h-8 mr-4 text-primary" /> Experiment Replay
          </h2>
          <p className="text-lg text-muted-foreground">Side-by-side comparison of how different architectures answer the exact same question.</p>
        </div>

        <Card className="bg-background/50 border-border/50 overflow-hidden">
          <CardHeader className="bg-secondary/30 border-b border-border/50">
            <div className="text-sm font-bold text-muted-foreground uppercase tracking-wider mb-2">The Control Question</div>
            <CardTitle className="text-xl font-medium">"Who was born first, Percy Clifford Mills or Nigel Graham Pearson?"</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="grid grid-cols-1 lg:grid-cols-3 divide-y lg:divide-y-0 lg:divide-x divide-border/50">
              
              <div className="p-6 space-y-4">
                <Badge variant="destructive" className="bg-destructive/10 text-destructive border-destructive/20">Baseline RAG</Badge>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  "Percy Clifford Mills was born in 1909. The context does not provide information about Nigel Graham Pearson's birth date."
                </p>
                <div className="flex items-center text-xs text-destructive mt-4 font-medium">
                  <AlertCircle className="w-4 h-4 mr-1" /> Failed retrieval (Missing Pearson)
                </div>
              </div>

              <div className="p-6 space-y-4">
                <Badge variant="secondary" className="bg-blue-500/10 text-blue-500 border-blue-500/20">Planner + Standard LLM</Badge>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  "Percy Clifford Mills was born in 1909 and Nigel Graham Pearson was born in 1963. They are both English football managers."
                </p>
                <div className="flex items-center text-xs text-amber-500 mt-4 font-medium">
                  <AlertCircle className="w-4 h-4 mr-1" /> Retrieved both, but failed to answer the question explicitly
                </div>
              </div>

              <div className="p-6 space-y-4 bg-primary/5">
                <Badge variant="default" className="bg-primary/20 text-primary border-primary/30">Full Agentic Pipeline</Badge>
                <p className="text-sm leading-relaxed font-medium">
                  "Percy Clifford Mills was born first. Mills was born in 1909, whereas Nigel Graham Pearson was born in 1963."
                </p>
                <div className="flex items-center text-xs text-emerald-500 mt-4 font-bold">
                  <CheckCircle2 className="w-4 h-4 mr-1" /> Perfect retrieval & reasoning
                </div>
              </div>

            </div>
          </CardContent>
        </Card>
      </div>

    </section>
  );
}
