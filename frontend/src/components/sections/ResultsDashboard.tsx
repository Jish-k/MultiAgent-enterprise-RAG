"use client";

import { useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Target, Activity, Zap, BarChart2 } from "lucide-react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Legend, LineChart, Line, AreaChart, Area 
} from "recharts";

export default function ResultsDashboard({ results }: { results: any }) {
  // Format data for charts
  const stages = ["baseline", "planner", "reasoner", "verifier"];
  
  const chartData = useMemo(() => {
    if (!results) return [];
    return stages.map(stage => ({
      name: stage.charAt(0).toUpperCase() + stage.slice(1),
      accuracy: results[stage]?.accuracy || 0,
      recall: results[stage]?.recall || 0,
      latency: results[stage]?.latency || 0,
    })).filter(data => data.accuracy > 0); // Only show stages that have data
  }, [results]);

  const bestMetrics = useMemo(() => {
    if (!results) return {};
    // Find the most advanced stage that actually has a non-null accuracy value
    for (const stage of [...stages].reverse()) {
      if (results[stage] && results[stage].accuracy) {
        return results[stage];
      }
    }
    return {};
  }, [results, stages]);

  if (!results || Object.keys(results).length === 0) {
    return (
      <section id="results" className="min-h-screen py-24 flex items-center justify-center">
        <div className="text-center space-y-4 text-muted-foreground">
          <BarChart2 className="w-12 h-12 mx-auto opacity-50 animate-pulse" />
          <h2 className="text-2xl font-medium">Awaiting Evaluation Data</h2>
          <p>Run the backend evaluation scripts to populate this dashboard.</p>
        </div>
      </section>
    );
  }

  return (
    <section id="results" className="min-h-screen py-24 flex flex-col">
      <div className="mb-12">
        <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-sm text-primary mb-4">
          <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
          Live Metrics
        </div>
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Results Dashboard</h2>
        <p className="text-xl text-muted-foreground">
          Evaluation metrics streamed directly from the backend JSON artifacts.
        </p>
      </div>

      <div className="space-y-8">
        {/* Top Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-card/40 backdrop-blur-xl border-border/50 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-blue-500/10 rounded-xl">
                  <Target className="h-6 w-6 text-blue-500" />
                </div>
                <Badge variant="outline" className="bg-blue-500/5 text-blue-500 border-blue-500/20">Peak Performance</Badge>
              </div>
              <div className="space-y-1">
                <h3 className="text-3xl font-bold font-mono">{bestMetrics.accuracy ? `${bestMetrics.accuracy}%` : "--"}</h3>
                <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Final Accuracy</p>
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-card/40 backdrop-blur-xl border-border/50 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-emerald-500/10 rounded-xl">
                  <Activity className="h-6 w-6 text-emerald-500" />
                </div>
                <Badge variant="outline" className="bg-emerald-500/5 text-emerald-500 border-emerald-500/20">Retrieval</Badge>
              </div>
              <div className="space-y-1">
                <h3 className="text-3xl font-bold font-mono">{bestMetrics.recall ? `${bestMetrics.recall}%` : "--"}</h3>
                <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Recall@3</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card/40 backdrop-blur-xl border-border/50 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-amber-500/10 rounded-xl">
                  <Zap className="h-6 w-6 text-amber-500" />
                </div>
                <Badge variant="outline" className="bg-amber-500/5 text-amber-500 border-amber-500/20">Performance</Badge>
              </div>
              <div className="space-y-1">
                <h3 className="text-3xl font-bold font-mono">{bestMetrics.latency ? `${bestMetrics.latency}s` : "--"}</h3>
                <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Avg Latency / Query</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Accuracy Evolution */}
          <Card className="bg-card/40 backdrop-blur-xl border-border/50 shadow-lg">
            <CardHeader>
              <CardTitle>Accuracy Evolution</CardTitle>
              <CardDescription>How agentic stages improved reasoning accuracy</CardDescription>
            </CardHeader>
            <CardContent className="h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorAccuracy" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="name" stroke="#888" tick={{ fill: '#888' }} axisLine={false} tickLine={false} />
                  <YAxis stroke="#888" tick={{ fill: '#888' }} axisLine={false} tickLine={false} domain={[0, 100]} tickFormatter={(val) => `${val}%`} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: 'rgba(10, 10, 10, 0.9)', borderColor: '#333', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Area type="monotone" dataKey="accuracy" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorAccuracy)" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Retrieval Recall */}
          <Card className="bg-card/40 backdrop-blur-xl border-border/50 shadow-lg">
            <CardHeader>
              <CardTitle>Retrieval Metrics (Recall@3)</CardTitle>
              <CardDescription>Impact of the multi-query Planner on document retrieval</CardDescription>
            </CardHeader>
            <CardContent className="h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="name" stroke="#888" tick={{ fill: '#888' }} axisLine={false} tickLine={false} />
                  <YAxis stroke="#888" tick={{ fill: '#888' }} axisLine={false} tickLine={false} domain={[0, 100]} tickFormatter={(val) => `${val}%`} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: 'rgba(10, 10, 10, 0.9)', borderColor: '#333', borderRadius: '8px' }}
                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                  />
                  <Bar dataKey="recall" fill="#10b981" radius={[6, 6, 0, 0]} maxBarSize={60} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

        </div>
      </div>
    </section>
  );
}
