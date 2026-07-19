"use client";

import { motion } from "framer-motion";
import { XCircle, ArrowDown, Lightbulb, CheckCircle2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const steps = [
  {
    id: "traditional-rag",
    title: "Traditional RAG",
    icon: <div className="p-3 bg-secondary/50 rounded-full"><span className="text-xl">🔍</span></div>,
    description: "Fetches chunks based purely on semantic similarity and passes them to an LLM.",
    status: "neutral"
  },
  {
    id: "failure",
    title: "Why it fails",
    icon: <XCircle className="w-8 h-8 text-destructive" />,
    description: "Struggles with multi-hop questions. Irrelevant chunks distract the LLM, leading to severe hallucinations.",
    status: "negative"
  },
  {
    id: "gap",
    title: "The Research Gap",
    icon: <Lightbulb className="w-8 h-8 text-amber-500" />,
    description: "LLMs need active reasoning paths and verifiable facts, not just a passive dump of unstructured text.",
    status: "warning"
  },
  {
    id: "solution",
    title: "Our Solution",
    icon: <CheckCircle2 className="w-8 h-8 text-emerald-500" />,
    description: "Enterprise Agentic RAG: An autonomous multi-agent pipeline that plans, retrieves, reasons, and verifies.",
    status: "positive"
  }
];

export default function ProblemStatement() {
  return (
    <section id="problem-statement" className="min-h-screen py-24 relative flex flex-col justify-center">
      <div className="max-w-4xl mx-auto w-full space-y-16">
        
        <div className="text-center space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold tracking-tight">The Problem with RAG</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Why simply gluing a vector database to an LLM isn't enough for enterprise-grade reasoning.
          </p>
        </div>

        <div className="relative">
          {/* Vertical Connecting Line */}
          <div className="absolute left-8 md:left-1/2 top-8 bottom-8 w-px bg-border -translate-x-1/2 hidden md:block" />

          <div className="space-y-12">
            {steps.map((step, index) => {
              const isEven = index % 2 === 0;
              return (
                <motion.div 
                  key={step.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-100px" }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  className={`flex flex-col md:flex-row items-center gap-8 ${isEven ? 'md:flex-row' : 'md:flex-row-reverse'}`}
                >
                  {/* Content Card */}
                  <div className={`w-full md:w-1/2 flex ${isEven ? 'md:justify-end' : 'md:justify-start'}`}>
                    <Card className={`max-w-[400px] w-full shadow-lg ${step.status === 'negative' ? 'border-destructive/30 bg-destructive/5' : step.status === 'positive' ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-border/50 bg-card/50'}`}>
                      <CardContent className="p-6 space-y-3">
                        <div className="flex items-center gap-4">
                          {step.icon}
                          <h3 className="text-xl font-bold">{step.title}</h3>
                        </div>
                        <p className="text-muted-foreground leading-relaxed">
                          {step.description}
                        </p>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Center Node (Hidden on Mobile) */}
                  <div className="hidden md:flex absolute left-1/2 -translate-x-1/2 w-12 h-12 bg-background border-2 border-border rounded-full items-center justify-center z-10">
                    <span className="text-sm font-bold text-muted-foreground">{index + 1}</span>
                  </div>

                  {/* Empty Spacer */}
                  <div className="hidden md:block w-1/2" />
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Transition to next section */}
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 1 }}
          className="flex justify-center pt-8"
        >
          <div className="flex flex-col items-center text-muted-foreground animate-bounce">
            <span className="text-sm mb-2 font-medium">See how it works</span>
            <ArrowDown className="w-5 h-5" />
          </div>
        </motion.div>

      </div>
    </section>
  );
}
