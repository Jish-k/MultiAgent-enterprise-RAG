"use client";

import { useEffect, useState } from "react";
import { useState, useEffect } from "react";
import { fetchProjectOverview, fetchResults } from "@/lib/api";
import { Loader2, MonitorPlay, GraduationCap, Microscope } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import HomeSection from "@/components/sections/HomeSection";
import ProblemStatement from "@/components/sections/ProblemStatement";
import ArchitectureExplorer from "@/components/sections/ArchitectureExplorer";
import InteractivePipeline from "@/components/sections/InteractivePipeline";
import ResultsDashboard from "@/components/sections/ResultsDashboard";
import BasePaperComparison from "@/components/sections/BasePaperComparison";
import ExperimentTimeline from "@/components/sections/ExperimentTimeline";
import LiveDemonstration from "@/components/sections/LiveDemonstration";
import Publications from "@/components/sections/Publications";
import SystemAppendix from "@/components/sections/SystemAppendix";





export default function ResearchDashboard() {
  const [projectData, setProjectData] = useState<any>(null);
  const [resultsData, setResultsData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [displayMode, setDisplayMode] = useState<"research" | "professor" | "conference">("research");

  useEffect(() => {
    async function loadData() {
      try {
        const [project, results] = await Promise.all([
          fetchProjectOverview(),
          fetchResults()
        ]);
        setProjectData(project);
        setResultsData(results);
      } catch (e) {
        console.error("Failed to load backend data", e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  const sections = [
    { id: "home", title: "Home" },
    { id: "problem-statement", title: "Problem Statement" },
    { id: "existing-work", title: "Existing Work" },
    { id: "proposed-method", title: "Proposed Method" },
    { id: "interactive-pipeline", title: "Interactive Pipeline" },
    { id: "datasets", title: "Dataset Explorer" },
    { id: "experiments", title: "Experiment Timeline" },
    { id: "results", title: "Results Dashboard" },
    { id: "ablation", title: "Ablation Study" },
    { id: "comparison", title: "Base Paper vs My Work" },
    { id: "live-demo", title: "Live Demonstration" },
    { id: "architecture", title: "Architecture Explorer" },
    { id: "code", title: "Code Explorer" },
    { id: "evaluation", title: "Evaluation Dashboard" },
    { id: "publications", title: "Publications" },
    { id: "future-work", title: "Future Work" },
  ];

  const filteredSections = sections.filter(section => {
    if (displayMode === "professor") {
      return ["home", "problem-statement", "architecture", "results", "live-demo", "publications"].includes(section.id);
    }
    return true; // Research and Conference modes show everything
  });
  
  // Add the appendix to the navigation for Research and Conference mode
  if (displayMode !== "professor" && !sections.find(s => s.id === "appendix")) {
    sections.push({ id: "appendix", title: "System Appendix" });
  }

  return (
    <div className={`flex min-h-screen bg-background text-foreground selection:bg-primary/30 transition-all duration-500 ${displayMode === "conference" ? "text-lg md:text-xl" : ""}`}>
      {/* Sticky Sidebar Navigation */}
      <nav className={`w-64 fixed h-screen overflow-y-auto border-r border-border/40 p-6 hidden lg:flex flex-col bg-background/50 backdrop-blur-3xl z-50 transition-transform ${displayMode === "conference" ? "-translate-x-full" : ""}`}>
        <div className="font-bold text-lg mb-8 bg-gradient-to-br from-primary to-primary/50 bg-clip-text text-transparent">
          Agentic RAG
        </div>

        {/* Mode Switcher */}
        <div className="mb-8 space-y-2">
          <p className="text-xs font-bold text-muted-foreground uppercase tracking-wider mb-3">Display Mode</p>
          <Button 
            variant={displayMode === "research" ? "default" : "ghost"} 
            className="w-full justify-start" 
            onClick={() => setDisplayMode("research")}
          >
            <Microscope className="w-4 h-4 mr-2" /> Research
          </Button>
          <Button 
            variant={displayMode === "professor" ? "default" : "ghost"} 
            className="w-full justify-start" 
            onClick={() => setDisplayMode("professor")}
          >
            <GraduationCap className="w-4 h-4 mr-2" /> Professor
          </Button>
          <Button 
            variant={displayMode === "conference" ? "default" : "ghost"} 
            className="w-full justify-start" 
            onClick={() => setDisplayMode("conference")}
          >
            <MonitorPlay className="w-4 h-4 mr-2" /> Conference
          </Button>
        </div>

        <ul className="space-y-3 flex-1">
          {filteredSections.map((section) => (
            <li key={section.id}>
              <a 
                href={`#${section.id}`}
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors block py-1"
              >
                {section.title}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {/* Main Content Area */}
      <main className={`flex-1 transition-all duration-500 px-8 md:px-24 ${displayMode === "conference" ? "lg:ml-0 max-w-7xl mx-auto" : "lg:ml-64"}`}>
        {/* Conference Mode Exit Button */}
        {displayMode === "conference" && (
          <div className="fixed top-6 right-6 z-50">
            <Button variant="outline" onClick={() => setDisplayMode("research")} className="backdrop-blur-xl bg-background/50">
              Exit Conference Mode
            </Button>
          </div>
        )}

        {filteredSections.some(s => s.id === "home") && <HomeSection projectData={projectData || {}} resultsData={resultsData || {}} />}
        {filteredSections.some(s => s.id === "problem-statement") && <ProblemStatement />}
        {filteredSections.some(s => s.id === "architecture") && <ArchitectureExplorer />}
        {filteredSections.some(s => s.id === "interactive-pipeline") && <InteractivePipeline />}
        {filteredSections.some(s => s.id === "results") && <ResultsDashboard results={resultsData || {}} />}
        {filteredSections.some(s => s.id === "comparison") && <BasePaperComparison />}
        {filteredSections.some(s => s.id === "experiments") && <ExperimentTimeline />}
        {filteredSections.some(s => s.id === "live-demo") && <LiveDemonstration />}
        {filteredSections.some(s => s.id === "publications") && <Publications />}
        {filteredSections.some(s => s.id === "appendix") && <SystemAppendix />}
      </main>
    </div>
  );
}
