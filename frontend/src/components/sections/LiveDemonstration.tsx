"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, Search, BrainCircuit, ShieldCheck, CheckCircle2, Loader2, Play } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function LiveDemonstration() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/demo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      
      // Artificial delay for presentation effect
      setTimeout(() => {
        setResult(data);
        setLoading(false);
      }, 1500);
      
    } catch (error) {
      console.error("Demo API error:", error);
      setLoading(false);
    }
  };

  return (
    <section id="live-demo" className="min-h-screen py-24 flex flex-col justify-center">
      <div className="mb-12 text-center">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 flex items-center justify-center gap-4">
          <Play className="w-10 h-10 text-primary fill-primary" /> Live Demonstration
        </h2>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Test the Enterprise Agentic RAG pipeline interactively. Connects directly to the FastAPI backend.
        </p>
      </div>

      <div className="max-w-4xl mx-auto w-full space-y-8">
        
        {/* Input Form */}
        <form onSubmit={handleSubmit} className="relative group">
          <div className="absolute inset-0 bg-primary/20 blur-xl opacity-50 rounded-3xl" />
          <Card className="relative bg-background/80 backdrop-blur-xl border-primary/30 shadow-2xl rounded-3xl overflow-hidden">
            <CardContent className="p-3 flex items-center">
              <input 
                type="text" 
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask any complex multi-hop question..."
                className="flex-1 bg-transparent border-none outline-none text-xl md:text-2xl py-4 px-6 font-medium placeholder:text-muted-foreground/50"
                disabled={loading}
              />
              <Button 
                type="submit"
                disabled={loading || !question.trim()}
                className="rounded-2xl h-14 w-14 p-0 shrink-0 bg-primary hover:bg-primary/90 text-primary-foreground ml-2"
              >
                {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Send className="w-6 h-6" />}
              </Button>
            </CardContent>
          </Card>
        </form>

        {/* Loading State */}
        <AnimatePresence mode="wait">
          {loading && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
              className="flex flex-col items-center justify-center py-20 text-muted-foreground space-y-4"
            >
              <div className="relative">
                <div className="w-16 h-16 border-4 border-primary/20 rounded-full" />
                <div className="w-16 h-16 border-4 border-primary rounded-full border-t-transparent animate-spin absolute inset-0" />
              </div>
              <p className="text-lg font-medium animate-pulse text-primary">Agents are thinking...</p>
            </motion.div>
          )}

          {/* Results Output */}
          {result && !loading && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* 1. Planner */}
              <Card className="border-blue-500/30 bg-blue-500/5">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-blue-500 uppercase tracking-wider flex items-center">
                    <Bot className="w-4 h-4 mr-2" /> Planner Sub-Queries
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc list-inside space-y-1 text-muted-foreground font-mono text-sm">
                    {result.planner_queries?.map((q: string, i: number) => (
                      <li key={i}>{q}</li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* 2. Retriever */}
              <Card className="border-purple-500/30 bg-purple-500/5">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-purple-500 uppercase tracking-wider flex items-center">
                    <Search className="w-4 h-4 mr-2" /> Retrieved Context
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {result.retrieved_chunks?.map((chunk: string, i: number) => (
                      <div key={i} className="p-3 bg-background rounded border border-border/50 text-sm text-muted-foreground italic border-l-4 border-l-purple-500/50">
                        {chunk}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* 3. Reasoner */}
              <Card className="border-amber-500/30 bg-amber-500/5">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-amber-500 uppercase tracking-wider flex items-center">
                    <BrainCircuit className="w-4 h-4 mr-2" /> Chain of Thought Reasoning
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="leading-relaxed font-medium text-amber-100">{result.reasoning}</p>
                </CardContent>
              </Card>

              {/* 4. Verifier */}
              <Card className="border-emerald-500/30 bg-emerald-500/5">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-emerald-500 uppercase tracking-wider flex items-center">
                    <ShieldCheck className="w-4 h-4 mr-2" /> Verification
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="leading-relaxed text-emerald-400 font-medium">{result.verification}</p>
                </CardContent>
              </Card>

              {/* 5. Final Answer */}
              <Card className="border-primary bg-primary/10 shadow-lg shadow-primary/10 scale-[1.02]">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm text-primary uppercase tracking-wider flex items-center">
                    <CheckCircle2 className="w-5 h-5 mr-2" /> Final Verified Answer
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xl font-bold leading-relaxed">{result.final_answer}</p>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}
