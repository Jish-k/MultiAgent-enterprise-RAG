"use client";

import { motion } from "framer-motion";
import { ArrowRight, Activity, Target, Zap, Play, BookOpen } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

export default function HomeSection({ projectData, resultsData }: { projectData: any; resultsData: any }) {
  // Use reasoner stats as the highlight if available, else baseline
  const highlightMetrics = resultsData?.reasoner || resultsData?.baseline || {};
  const accuracy = highlightMetrics.accuracy ? `${highlightMetrics.accuracy}%` : "--";
  const recall = highlightMetrics.recall ? `${highlightMetrics.recall}%` : "--";
  const latency = highlightMetrics.latency ? `${highlightMetrics.latency}s` : "--";

  return (
    <section id="home" className="min-h-screen flex flex-col justify-center py-20 relative">
      {/* Background decorations */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px] -z-10" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-secondary/5 rounded-full blur-[120px] -z-10" />

      <div className="max-w-6xl w-full grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        {/* Left Column: Text & CTA */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-8"
        >
          <div className="space-y-4">
            <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-sm text-primary">
              <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
              Live Research Dashboard
            </div>
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-gradient-to-br from-foreground to-foreground/70 bg-clip-text text-transparent">
              {projectData?.title || "Enterprise Agentic RAG"}
            </h1>
            <p className="text-xl md:text-2xl font-medium text-muted-foreground leading-relaxed">
              {projectData?.subtitle || "A multi-stage, reasoning-driven retrieval augmented generation architecture."}
            </p>
          </div>

          <div className="space-y-4 border-l-2 border-primary/20 pl-6">
            <h3 className="text-lg font-semibold">Why this matters</h3>
            <p className="text-muted-foreground">
              {projectData?.goal || "Solving multi-hop reasoning and hallucination in standard RAG pipelines."}
            </p>
          </div>

          <div className="flex flex-wrap gap-4 pt-4">
            <a 
              href="#problem-statement" 
              className="inline-flex items-center justify-center rounded-full bg-primary px-8 py-3 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
            >
              Explore Research
              <ArrowRight className="ml-2 h-4 w-4" />
            </a>
            <a 
              href="#live-demo" 
              className="inline-flex items-center justify-center rounded-full bg-secondary px-8 py-3 text-sm font-medium text-secondary-foreground transition-colors hover:bg-secondary/80 border border-border"
            >
              <Play className="mr-2 h-4 w-4" />
              Live Demo
            </a>
            <a 
              href="#publications" 
              className="inline-flex items-center justify-center rounded-full bg-transparent px-8 py-3 text-sm font-medium transition-colors hover:bg-secondary/50 border border-border"
            >
              <BookOpen className="mr-2 h-4 w-4" />
              Read Paper
            </a>
          </div>
        </motion.div>

        {/* Right Column: Preview & Metrics */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="space-y-6"
        >
          {/* Animated Architecture Preview */}
          <Card className="bg-card/40 backdrop-blur-xl border-border/50 overflow-hidden shadow-2xl shadow-primary/5">
            <CardContent className="p-8">
              <div className="text-sm font-medium text-muted-foreground mb-6 uppercase tracking-wider text-center">
                Pipeline Architecture
              </div>
              <div className="flex flex-col items-center gap-4">
                {["Planner", "Retriever", "Reasoner", "Verifier"].map((stage, i) => (
                  <div key={stage} className="flex flex-col items-center w-full">
                    <motion.div 
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.4 + (i * 0.1) }}
                      className="w-full max-w-[250px] bg-background border border-border rounded-xl p-4 text-center font-medium shadow-sm relative overflow-hidden group"
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-primary/0 via-primary/5 to-primary/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
                      {stage}
                    </motion.div>
                    {i < 3 && (
                      <motion.div 
                        initial={{ height: 0 }}
                        animate={{ height: 24 }}
                        transition={{ duration: 0.3, delay: 0.5 + (i * 0.1) }}
                        className="w-px bg-gradient-to-b from-border to-primary/30"
                      />
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Key Metrics Highlight */}
          <div className="grid grid-cols-3 gap-4">
            <Card className="bg-card/40 backdrop-blur-xl border-border/50">
              <CardContent className="p-4 flex flex-col items-center text-center space-y-1">
                <Target className="h-5 w-5 text-blue-500 mb-1" />
                <span className="text-2xl font-bold font-mono">{accuracy}</span>
                <span className="text-xs text-muted-foreground font-medium">Accuracy</span>
              </CardContent>
            </Card>
            <Card className="bg-card/40 backdrop-blur-xl border-border/50">
              <CardContent className="p-4 flex flex-col items-center text-center space-y-1">
                <Activity className="h-5 w-5 text-emerald-500 mb-1" />
                <span className="text-2xl font-bold font-mono">{recall}</span>
                <span className="text-xs text-muted-foreground font-medium">Recall</span>
              </CardContent>
            </Card>
            <Card className="bg-card/40 backdrop-blur-xl border-border/50">
              <CardContent className="p-4 flex flex-col items-center text-center space-y-1">
                <Zap className="h-5 w-5 text-amber-500 mb-1" />
                <span className="text-2xl font-bold font-mono">{latency}</span>
                <span className="text-xs text-muted-foreground font-medium">Latency</span>
              </CardContent>
            </Card>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
