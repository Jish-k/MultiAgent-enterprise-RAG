"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { History, ArrowRight, Lightbulb, TrendingUp } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const EXPERIMENTS = [
  {
    id: "baseline",
    title: "Stage 0: Baseline RAG",
    date: "Experiment 1",
    changed: "Implemented standard naive RAG architecture using ChromaDB and a single LLM call.",
    why: "To establish a performance floor and understand exactly where traditional methods fail on complex multi-hop queries.",
    insights: "Retrieval recall was terrible (40%). The LLM hallucinated wildly because the retrieved chunks often missed the 'bridge' entity required to connect two separate facts.",
    metrics: { accuracy: "42.0%", recall: "45.0%", latency: "1.2s" }
  },
  {
    id: "planner",
    title: "Stage 1: + Planner Agent",
    date: "Experiment 2",
    changed: "Added an autonomous Planner that intercepts the user question and breaks it down into 2-4 parallel search queries.",
    why: "Because semantic search fails on complex questions. We needed to explicitly search for the sub-components of a multi-hop query.",
    insights: "Recall sky-rocketed to 85%. By explicitly querying for 'Percy Mills birth date' AND 'Nigel Pearson birth date', the vector database finally returned the correct chunks. However, the LLM still struggled to synthesize them properly.",
    metrics: { accuracy: "58.5%", recall: "85.2%", latency: "2.8s" }
  },
  {
    id: "reasoner",
    title: "Stage 2: + Reasoner Agent",
    date: "Experiment 3",
    changed: "Replaced the standard LLM generation prompt with a strict Chain-of-Thought (CoT) Reasoner agent.",
    why: "Even with the right documents, the LLM would get confused by the sheer volume of text. It needed a structured way to 'think' step-by-step.",
    insights: "Accuracy jumped significantly. The Reasoner was able to extract the two distinct facts and compare them logically. Latency increased due to the longer token generation required for the reasoning trace.",
    metrics: { accuracy: "76.4%", recall: "85.2%", latency: "5.4s" }
  },
  {
    id: "verifier",
    title: "Stage 3: + Verifier Agent",
    date: "Experiment 4",
    changed: "Added a final Verification loop that critiques the Reasoner's output against the raw retrieved facts.",
    why: "The Reasoner still occasionally hallucinated dates or names in its final conclusion. We needed an adversarial agent to double-check the work.",
    insights: "Highest accuracy achieved. The Verifier caught and corrected 15% of the errors made by the Reasoner. The pipeline is now highly robust for complex reasoning, at the cost of maximum latency.",
    metrics: { accuracy: "92.1%", recall: "85.2%", latency: "8.1s" }
  }
];

export default function ExperimentTimeline() {
  const [activeId, setActiveId] = useState(EXPERIMENTS[0].id);

  const activeExp = EXPERIMENTS.find(e => e.id === activeId)!;

  return (
    <section id="experiments" className="min-h-screen py-24 flex flex-col">
      <div className="mb-12">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Experiment Timeline</h2>
        <p className="text-xl text-muted-foreground">
          Trace the evolutionary journey of the architecture and the insights gathered at each stage.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 flex-1">
        
        {/* Timeline Navigation (Left) */}
        <div className="lg:col-span-4 relative border-l border-border/50 ml-4 pl-8 py-4 space-y-12">
          {EXPERIMENTS.map((exp, index) => {
            const isActive = activeId === exp.id;
            return (
              <div 
                key={exp.id} 
                className="relative cursor-pointer group"
                onClick={() => setActiveId(exp.id)}
              >
                {/* Timeline Dot */}
                <div className={`absolute -left-[41px] top-2 w-4 h-4 rounded-full border-2 transition-colors ${
                  isActive ? 'bg-primary border-primary shadow-[0_0_10px_0] shadow-primary/50' : 'bg-background border-border group-hover:border-primary/50'
                }`} />
                
                <div className={`transition-colors ${isActive ? 'opacity-100' : 'opacity-50 group-hover:opacity-80'}`}>
                  <Badge variant="outline" className="mb-2 text-xs font-mono">{exp.date}</Badge>
                  <h3 className={`text-xl font-bold ${isActive ? 'text-primary' : 'text-foreground'}`}>{exp.title}</h3>
                </div>
              </div>
            );
          })}
        </div>

        {/* Experiment Details (Right) */}
        <div className="lg:col-span-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeId}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Card className="bg-card/40 backdrop-blur-xl border-border/50 shadow-2xl h-full">
                <CardContent className="p-8 space-y-8">
                  
                  <div>
                    <h3 className="text-3xl font-bold mb-6">{activeExp.title}</h3>
                    <div className="grid grid-cols-3 gap-4 mb-8">
                      <div className="p-4 bg-background rounded-xl border border-border">
                        <div className="text-sm text-muted-foreground mb-1 uppercase tracking-wider">Accuracy</div>
                        <div className="text-2xl font-mono font-bold text-blue-500">{activeExp.metrics.accuracy}</div>
                      </div>
                      <div className="p-4 bg-background rounded-xl border border-border">
                        <div className="text-sm text-muted-foreground mb-1 uppercase tracking-wider">Recall@3</div>
                        <div className="text-2xl font-mono font-bold text-emerald-500">{activeExp.metrics.recall}</div>
                      </div>
                      <div className="p-4 bg-background rounded-xl border border-border">
                        <div className="text-sm text-muted-foreground mb-1 uppercase tracking-wider">Latency</div>
                        <div className="text-2xl font-mono font-bold text-amber-500">{activeExp.metrics.latency}</div>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <div className="space-y-2">
                      <h4 className="text-sm font-bold text-primary uppercase tracking-wider flex items-center">
                        <ArrowRight className="w-4 h-4 mr-2" /> What Changed
                      </h4>
                      <p className="text-lg leading-relaxed">{activeExp.changed}</p>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-sm font-bold text-amber-500 uppercase tracking-wider flex items-center">
                        <Lightbulb className="w-4 h-4 mr-2" /> Why it Changed
                      </h4>
                      <p className="text-lg leading-relaxed text-muted-foreground">{activeExp.why}</p>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-sm font-bold text-emerald-500 uppercase tracking-wider flex items-center">
                        <TrendingUp className="w-4 h-4 mr-2" /> Key Insights
                      </h4>
                      <div className="p-5 bg-emerald-500/5 border border-emerald-500/20 rounded-xl leading-relaxed">
                        {activeExp.insights}
                      </div>
                    </div>
                  </div>

                </CardContent>
              </Card>
            </motion.div>
          </AnimatePresence>
        </div>

      </div>
    </section>
  );
}
