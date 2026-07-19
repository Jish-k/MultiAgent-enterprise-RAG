"use client";

import { motion } from "framer-motion";
import { Check, X, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const comparisonData = [
  {
    category: "Multi-query Planning",
    basePaper: false,
    myWork: true,
    description: "The base paper relies on a single semantic search vector. My work uses an LLM to deconstruct complex questions into parallel search queries, drastically increasing recall."
  },
  {
    category: "Multi-hop Reasoning",
    basePaper: false,
    myWork: true,
    description: "Standard RAG passes all chunks to an LLM at once. My architecture enforces Chain of Thought (CoT) reasoning, establishing logical links across disjointed documents."
  },
  {
    category: "Verification",
    basePaper: false,
    myWork: true,
    description: "The base paper assumes the LLM's answer is correct. My work introduces an autonomous Verifier Agent that checks the final answer against the raw retrieved facts to prevent hallucinations."
  },
  {
    category: "Enterprise Dataset",
    basePaper: false,
    myWork: true,
    description: "Evaluated strictly on HotpotQA (Wikipedia). My implementation extends the evaluation to complex enterprise-grade data with structured/unstructured hybrid formats."
  },
  {
    category: "Interactive Demo",
    basePaper: false,
    myWork: true,
    description: "The base paper provides only terminal scripts. This platform provides a fully interactive, live visualization of the reasoning pipeline."
  }
];

export default function BasePaperComparison() {
  return (
    <section id="comparison" className="min-h-screen py-24 flex flex-col justify-center relative">
      <div className="absolute left-0 top-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[100px] pointer-events-none" />
      
      <div className="max-w-5xl mx-auto w-full space-y-12">
        <div className="text-center space-y-4">
          <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-sm text-primary mb-2">
            Research Contributions
          </div>
          <h2 className="text-4xl md:text-5xl font-bold tracking-tight">Base Paper vs. My Work</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Highlighting the architectural leaps made beyond traditional RAG literature.
          </p>
        </div>

        {/* Comparison Table */}
        <Card className="bg-card/40 backdrop-blur-xl border-border/50 shadow-2xl overflow-hidden">
          <CardContent className="p-0">
            <Table>
              <TableHeader className="bg-secondary/30">
                <TableRow>
                  <TableHead className="w-[300px] text-lg font-bold py-6 px-8">Category</TableHead>
                  <TableHead className="text-center text-lg font-bold py-6 text-muted-foreground">Base Paper</TableHead>
                  <TableHead className="text-center text-lg font-bold py-6 text-primary">Enterprise Agentic RAG</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {comparisonData.map((row, index) => (
                  <TableRow key={index} className="border-border/20 transition-colors hover:bg-secondary/10">
                    <TableCell className="font-medium px-8 py-6">{row.category}</TableCell>
                    <TableCell className="text-center py-6">
                      {row.basePaper ? (
                        <Check className="w-6 h-6 text-emerald-500 mx-auto" />
                      ) : (
                        <X className="w-6 h-6 text-destructive/50 mx-auto" />
                      )}
                    </TableCell>
                    <TableCell className="text-center py-6 bg-primary/5">
                      {row.myWork ? (
                        <Check className="w-6 h-6 text-primary mx-auto" />
                      ) : (
                        <X className="w-6 h-6 text-destructive/50 mx-auto" />
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Explanations Grid */}
        <div className="pt-12">
          <h3 className="text-2xl font-bold mb-8 text-center">Why these additions matter</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {comparisonData.map((item, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
              >
                <Card className="h-full bg-card/20 border-border/40 hover:border-primary/30 hover:bg-card/40 transition-colors">
                  <CardContent className="p-6">
                    <h4 className="font-bold text-lg mb-2 flex items-center">
                      <ArrowRight className="w-4 h-4 mr-2 text-primary" />
                      {item.category}
                    </h4>
                    <p className="text-muted-foreground leading-relaxed text-sm">
                      {item.description}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
