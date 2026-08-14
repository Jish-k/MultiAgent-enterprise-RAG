"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, Search, BrainCircuit, ShieldCheck, CheckCircle2, Loader2, Play, Settings } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BACKEND_URL } from "@/lib/api";

export default function LiveDemonstration() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [showConnectors, setShowConnectors] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [anthropicApiKey, setAnthropicApiKey] = useState("");
  const [llmProvider, setLlmProvider] = useState("openai");

  useEffect(() => {
    const savedOpenAI = localStorage.getItem("openai_api_key");
    const savedAnthropic = localStorage.getItem("anthropic_api_key");
    const savedProvider = localStorage.getItem("llm_provider");
    if (savedOpenAI) setApiKey(savedOpenAI);
    if (savedAnthropic) setAnthropicApiKey(savedAnthropic);
    if (savedProvider) setLlmProvider(savedProvider);
  }, []);

  const handleOpenAiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setApiKey(e.target.value);
    localStorage.setItem("openai_api_key", e.target.value);
  };

  const handleAnthropicKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAnthropicApiKey(e.target.value);
    localStorage.setItem("anthropic_api_key", e.target.value);
  };

  const handleProviderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLlmProvider(e.target.value);
    localStorage.setItem("llm_provider", e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const token = localStorage.getItem("token");
      const body: any = { question };
      if (llmProvider === "openai" && apiKey.trim()) {
        body.api_key = apiKey.trim();
        body.llm_provider = "openai";
      } else if (llmProvider === "anthropic" && anthropicApiKey.trim()) {
        body.anthropic_api_key = anthropicApiKey.trim();
        body.llm_provider = "anthropic";
      }
      
      const response = await fetch(`${BACKEND_URL}/api/demo`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          ...(token ? { "Authorization": `Bearer ${token}` } : {})
        },
        body: JSON.stringify(body)
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
          Test the Agentic RAG pipeline interactively. Connects directly to the FastAPI backend.
        </p>
      </div>

      <div className="max-w-4xl mx-auto w-full space-y-8 relative">
        
        {/* Connectors / Settings Button */}
        <div className="flex justify-end mb-4 relative z-50">
          <Button 
            type="button"
            variant="outline" 
            className="rounded-full bg-background/50 backdrop-blur"
            onClick={() => setShowConnectors(!showConnectors)}
          >
            <Settings className="w-4 h-4 mr-2" /> Connectors
          </Button>

          {/* Connectors Dropdown */}
          <AnimatePresence>
            {showConnectors && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute top-12 right-0 w-80 p-5 rounded-xl border border-border/50 bg-background/95 backdrop-blur-xl shadow-2xl z-50 text-left"
              >
                <h4 className="font-semibold text-sm mb-2">API Connectors</h4>
                <p className="text-xs text-muted-foreground mb-4">
                  Add your API key to bypass mock results and run the live Agentic RAG pipeline dynamically.
                </p>
                <div className="space-y-2">
                  <label className="text-xs font-medium uppercase tracking-wider">LLM Provider</label>
                  <select
                    value={llmProvider}
                    onChange={handleProviderChange}
                    className="w-full bg-background border border-border/50 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 mb-3"
                  >
                    <option value="openai">ChatGPT (OpenAI)</option>
                    <option value="anthropic">Claude (Anthropic)</option>
                  </select>

                  {llmProvider === "openai" && (
                    <>
                      <label className="text-xs font-medium uppercase tracking-wider block mt-3 mb-1">OpenAI API Key</label>
                      <input
                        type="password"
                        value={apiKey}
                        onChange={handleOpenAiKeyChange}
                        placeholder="sk-..."
                        className="w-full bg-background border border-border/50 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 mb-4"
                      />
                    </>
                  )}

                  {llmProvider === "anthropic" && (
                    <>
                      <label className="text-xs font-medium uppercase tracking-wider block mt-3 mb-1">Anthropic API Key</label>
                      <input
                        type="password"
                        value={anthropicApiKey}
                        onChange={handleAnthropicKeyChange}
                        placeholder="sk-ant-..."
                        className="w-full bg-background border border-border/50 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 mb-4"
                      />
                    </>
                  )}

                  <hr className="border-border/40 my-4" />

                  <label className="text-xs font-medium uppercase tracking-wider block mb-2">Integrations</label>
                  <Button 
                    variant="outline" 
                    className="w-full justify-start text-muted-foreground"
                    onClick={() => alert("Google Drive integration requires GCP OAuth setup and is currently a mock UI.")}
                  >
                    <img src="https://upload.wikimedia.org/wikipedia/commons/1/12/Google_Drive_icon_%282020%29.svg" alt="Google Drive" className="w-4 h-4 mr-2" />
                    Connect Google Drive
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

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
                  <p className="leading-relaxed font-medium text-amber-900 dark:text-amber-100">{result.reasoning}</p>
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
                  <p className="leading-relaxed text-emerald-900 dark:text-emerald-400 font-medium">{result.verification}</p>
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
