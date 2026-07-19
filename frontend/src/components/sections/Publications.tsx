"use client";

import { motion } from "framer-motion";
import { FileText, Image as ImageIcon, Presentation, GitBranch, Download } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const publications = [
  {
    title: "IEEE Research Paper",
    description: "Full manuscript detailing the Agentic RAG architecture, mathematical formulations, and evaluation results. Submitted to IEEE Transactions on Knowledge and Data Engineering.",
    icon: <FileText className="w-8 h-8 text-blue-500" />,
    filename: "enterprise_agentic_rag_ieee.pdf",
    color: "bg-blue-500/10 border-blue-500/30",
    hoverColor: "hover:bg-blue-500/20"
  },
  {
    title: "Conference Poster",
    description: "A1 size poster summarizing the problem statement, proposed methodology, and key experimental graphs for conference presentation.",
    icon: <ImageIcon className="w-8 h-8 text-purple-500" />,
    filename: "research_poster_a1.pdf",
    color: "bg-purple-500/10 border-purple-500/30",
    hoverColor: "hover:bg-purple-500/20"
  },
  {
    title: "M.Tech Defense PPT",
    description: "The complete 25-slide presentation deck used for the final M.Tech project defense, including speaker notes.",
    icon: <Presentation className="w-8 h-8 text-amber-500" />,
    filename: "defense_presentation.pptx",
    color: "bg-amber-500/10 border-amber-500/30",
    hoverColor: "hover:bg-amber-500/20"
  },
  {
    title: "GitHub Repository",
    description: "Open-source implementation containing the FastAPI backend, Next.js frontend, and all evaluation scripts used in this research.",
    icon: <GitBranch className="w-8 h-8 text-emerald-500" />,
    filename: "Source Code",
    color: "bg-emerald-500/10 border-emerald-500/30",
    hoverColor: "hover:bg-emerald-500/20"
  }
];

export default function Publications() {
  return (
    <section id="publications" className="min-h-screen py-24 flex flex-col justify-center">
      <div className="mb-12 text-center">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Publications & Assets</h2>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Download the complete research materials, presentations, and source code.
        </p>
      </div>

      <div className="max-w-6xl w-full mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {publications.map((item, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
          >
            <Card className={`h-full border transition-all cursor-pointer group ${item.color} ${item.hoverColor}`}>
              <CardContent className="p-8 flex flex-col h-full">
                <div className="flex items-start justify-between mb-6">
                  <div className="p-4 bg-background/50 rounded-2xl backdrop-blur-sm border border-border/50">
                    {item.icon}
                  </div>
                  <div className="p-3 bg-background/30 rounded-full text-foreground/50 group-hover:text-foreground transition-colors group-hover:bg-background/80">
                    <Download className="w-5 h-5" />
                  </div>
                </div>
                
                <h3 className="text-2xl font-bold mb-3">{item.title}</h3>
                <p className="text-muted-foreground leading-relaxed flex-1 mb-6">
                  {item.description}
                </p>
                
                <div className="text-sm font-mono text-muted-foreground bg-background/50 px-4 py-2 rounded-lg border border-border/50 inline-block w-fit">
                  {item.filename}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
