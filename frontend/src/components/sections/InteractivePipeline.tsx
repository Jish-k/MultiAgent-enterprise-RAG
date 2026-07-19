"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, Search, BrainCircuit, ShieldCheck, Check, ArrowRight, Loader2, Play } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const STEPS = [
  { id: "planner", title: "Planner Agent", icon: <Bot className="w-5 h-5" />, color: "text-blue-500", bg: "bg-blue-500/10", border: "border-blue-500/30" },
  { id: "retriever", title: "Retriever", icon: <Search className="w-5 h-5" />, color: "text-purple-500", bg: "bg-purple-500/10", border: "border-purple-500/30" },
  { id: "reasoner", title: "Reasoner Agent", icon: <BrainCircuit className="w-5 h-5" />, color: "text-amber-500", bg: "bg-amber-500/10", border: "border-amber-500/30" },
  { id: "verifier", title: "Verifier Agent", icon: <ShieldCheck className="w-5 h-5" />, color: "text-emerald-500", bg: "bg-emerald-500/10", border: "border-emerald-500/30" },
];

const MOCK_DATA_LIST = [
  {
    question: "Who was born first, Percy Clifford Mills or Nigel Graham Pearson?",
    planner: [
      "Percy Clifford Mills birth date",
      "Nigel Graham Pearson birth date",
    ],
    retriever: [
      "...Percy Clifford Mills (born 1909) was an English footballer...",
      "...Nigel Graham Pearson (born 21 August 1963) is an English football manager..."
    ],
    reasoner: "Based on the retrieved context, Percy Clifford Mills was born in 1909. Nigel Graham Pearson was born in 1963. Since 1909 is earlier than 1963, Percy Clifford Mills was born first.",
    verifier: "The reasoning trace logically follows from the retrieved context. The birth years match exactly. The conclusion is factually correct."
  },
  {
    question: "Which magazine was first started, Arthur's Magazine or First for Women?",
    planner: [
      "When was Arthur's Magazine first started?",
      "When was First for Women first started?"
    ],
    retriever: [
      "[Doc 1] Arthur's Magazine (1844–1846) was an American literary magazine published in Philadelphia.",
      "[Doc 2] First for Women is a woman's magazine published by Bauer Media Group in the USA. It was started in 1989."
    ],
    reasoner: "1. Arthur's Magazine was started in 1844.\n2. First for Women was started in 1989.\n3. 1844 is earlier than 1989.\nConclusion: Arthur's Magazine was started first.",
    verifier: "[PASS] Context verifies Arthur's Magazine began publication in 1844 and First for Women in 1989. The temporal reasoning holds."
  },
  {
    question: "What is the English translation of Telemundo?",
    planner: [
      "What does 'Telemundo' mean in English?",
      "Translate 'Telemundo' to English."
    ],
    retriever: [
      "[Doc 1] Telemundo (Spanish pronunciation: [teleˈmundo]; English: World TV) is an American Spanish-language terrestrial television network."
    ],
    reasoner: "1. The context provides the English translation for Telemundo.\n2. It translates to 'World TV'.",
    verifier: "[PASS] The provided context explicitly contains the English translation 'World TV'. No hallucination detected."
  }
];

export default function InteractivePipeline() {
  const [activeStep, setActiveStep] = useState(-1);
  const [isRunning, setIsRunning] = useState(false);
  const [typedQuestion, setTypedQuestion] = useState("");
  const [dataIndex, setDataIndex] = useState(0);

  const startSimulation = () => {
    if (isRunning) return;
    
    // Determine the next question to show
    const nextIndex = activeStep === -1 ? dataIndex : (dataIndex + 1) % MOCK_DATA_LIST.length;
    setDataIndex(nextIndex);
    const currentData = MOCK_DATA_LIST[nextIndex];
    
    setIsRunning(true);
    setActiveStep(-1);
    setTypedQuestion("");

    // Simulate typing the question
    let i = 0;
    const typeInterval = setInterval(() => {
      setTypedQuestion(currentData.question.slice(0, i + 1));
      i++;
      if (i === currentData.question.length) {
        clearInterval(typeInterval);
        // Start pipeline execution
        setTimeout(() => setActiveStep(0), 600); // Start Planner
        setTimeout(() => setActiveStep(1), 2500); // Start Retriever
        setTimeout(() => setActiveStep(2), 4500); // Start Reasoner
        setTimeout(() => setActiveStep(3), 7500); // Start Verifier
        setTimeout(() => setActiveStep(4), 10000); // Complete
        setTimeout(() => setIsRunning(false), 10500);
      }
    }, 40);
  };
  
  const activeData = MOCK_DATA_LIST[dataIndex];

  return (
    <section id="interactive-pipeline" className="min-h-screen py-24 flex flex-col">
      <div className="mb-12">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Interactive Pipeline</h2>
        <p className="text-xl text-muted-foreground">
          Watch the Agentic architecture process a complex reasoning query in real-time.
        </p>
      </div>

      <div className="flex-1 max-w-5xl w-full mx-auto space-y-8 relative">
        
        {/* Search Bar Simulation */}
        <div className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-primary/0 blur-xl opacity-50 rounded-3xl" />
          <Card className="relative bg-background/80 backdrop-blur-xl border-border shadow-2xl rounded-3xl overflow-hidden">
            <CardContent className="p-2 flex items-center">
              <div className="pl-4 pr-2 text-muted-foreground">
                <Search className="w-6 h-6" />
              </div>
              <input 
                type="text" 
                value={typedQuestion} 
                readOnly
                placeholder="Ask a complex multi-hop question..."
                className="flex-1 bg-transparent border-none outline-none text-xl md:text-2xl py-4 font-medium"
              />
              <Button 
                onClick={startSimulation}
                disabled={isRunning}
                className="rounded-2xl h-14 px-8 text-lg ml-2 transition-all"
              >
                {isRunning ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <>
                    <Play className="w-5 h-5 mr-2 fill-current" />
                    Run Pipeline
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Pipeline Execution Flow */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-12">
          {STEPS.map((step, index) => {
            const isActive = activeStep === index;
            const isCompleted = activeStep > index;
            const isPending = activeStep < index;

            return (
              <div key={step.id} className="relative flex flex-col">
                <Card className={`h-full transition-all duration-500 relative overflow-hidden ${
                  isActive ? 'border-primary shadow-[0_0_30px_-5px] shadow-primary/30 scale-105 z-10' : 
                  isCompleted ? `${step.border} bg-card/50` : 
                  'border-border/40 bg-card/20 opacity-50'
                }`}>
                  {isActive && (
                    <motion.div 
                      layoutId="active-glow" 
                      className="absolute inset-0 bg-gradient-to-b from-primary/10 to-transparent pointer-events-none" 
                    />
                  )}
                  <CardContent className="p-6 flex flex-col items-center text-center gap-4">
                    <div className={`p-4 rounded-full transition-colors ${
                      isCompleted ? step.bg + " " + step.color :
                      isActive ? 'bg-primary text-primary-foreground animate-pulse' :
                      'bg-secondary text-muted-foreground'
                    }`}>
                      {isCompleted ? <Check className="w-6 h-6" /> : isActive ? <Loader2 className="w-6 h-6 animate-spin" /> : step.icon}
                    </div>
                    <div>
                      <h4 className={`font-bold ${isActive ? 'text-foreground' : 'text-muted-foreground'}`}>{step.title}</h4>
                      <div className="h-1 w-full bg-secondary rounded-full mt-3 overflow-hidden">
                        {isActive && (
                          <motion.div 
                            className="h-full bg-primary" 
                            initial={{ width: "0%" }}
                            animate={{ width: "100%" }}
                            transition={{ duration: index === 0 ? 1.9 : index === 1 ? 2 : index === 2 ? 3 : 2.5 }}
                          />
                        )}
                        {isCompleted && <div className="h-full w-full bg-primary/50" />}
                      </div>
                    </div>
                  </CardContent>
                </Card>
                {/* Connecting Arrow */}
                {index < 3 && (
                  <div className="hidden md:flex absolute top-1/2 -right-4 -translate-y-1/2 z-20 text-border">
                    <ArrowRight className="w-6 h-6" />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Live Execution Output Area */}
        <Card className="min-h-[300px] border-border/50 bg-card/30 backdrop-blur-sm relative overflow-hidden mt-8">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
          <CardContent className="p-8">
            <AnimatePresence mode="popLayout">
              {activeStep === -1 && !isRunning && (
                <motion.div 
                  initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="h-full flex items-center justify-center text-muted-foreground font-medium"
                >
                  Click "Run Pipeline" to watch the agents interact.
                </motion.div>
              )}
              
              {activeStep >= 0 && (
                <motion.div 
                  key="planner"
                  initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  <div>
                    <h5 className="text-sm font-bold text-blue-500 uppercase tracking-wider mb-3 flex items-center"><Bot className="w-4 h-4 mr-2"/> Planner Queries Generated</h5>
                    <div className="flex gap-3 flex-wrap">
                      {activeData.planner.map((q, i) => (
                        <span key={i} className="px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-lg text-sm font-mono text-blue-400">"{q}"</span>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}

              {activeStep >= 1 && (
                <motion.div 
                  key="retriever"
                  initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                  className="space-y-6 pt-6 mt-6 border-t border-border/50"
                >
                  <div>
                    <h5 className="text-sm font-bold text-purple-500 uppercase tracking-wider mb-3 flex items-center"><Search className="w-4 h-4 mr-2"/> Top Retrieved Context</h5>
                    <div className="space-y-3">
                      {activeData.retriever.map((chunk, i) => (
                        <div key={i} className="p-4 bg-purple-500/5 border border-purple-500/20 rounded-xl text-sm leading-relaxed text-muted-foreground italic">
                          {chunk}
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}

              {activeStep >= 2 && (
                <motion.div 
                  key="reasoner"
                  initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                  className="space-y-6 pt-6 mt-6 border-t border-border/50"
                >
                  <div>
                    <h5 className="text-sm font-bold text-amber-500 uppercase tracking-wider mb-3 flex items-center"><BrainCircuit className="w-4 h-4 mr-2"/> CoT Reasoning Trace</h5>
                    <div className="p-5 bg-amber-500/10 border border-amber-500/30 rounded-xl font-medium leading-relaxed text-amber-900 dark:text-amber-100 whitespace-pre-line">
                      {activeData.reasoner}
                    </div>
                  </div>
                </motion.div>
              )}

              {activeStep >= 3 && (
                <motion.div 
                  key="verifier"
                  initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                  className="space-y-6 pt-6 mt-6 border-t border-border/50"
                >
                  <div>
                    <h5 className="text-sm font-bold text-emerald-500 uppercase tracking-wider mb-3 flex items-center"><ShieldCheck className="w-4 h-4 mr-2"/> Verifier Critique</h5>
                    <div className="p-5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl font-medium text-emerald-900 dark:text-emerald-400">
                      {activeData.verifier}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </CardContent>
        </Card>

      </div>
    </section>
  );
}
