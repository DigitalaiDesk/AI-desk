import React from "react";

export default function IntelligenceDashboard() {
  return (
    <div className="p-6 grid grid-cols-2 gap-4">
      <section className="rounded-2xl border p-4"><h2>Crawl Monitoring</h2><div id="crawl-chart" /></section>
      <section className="rounded-2xl border p-4"><h2>SEO Issues</h2><div id="seo-issues" /></section>
      <section className="rounded-2xl border p-4"><h2>AI Visibility</h2><div id="ai-vis" /></section>
      <section className="rounded-2xl border p-4"><h2>Entity Graph</h2><div id="entity-graph" /></section>
      <section className="rounded-2xl border p-4"><h2>Competitors</h2><div id="competitor" /></section>
      <section className="rounded-2xl border p-4"><h2>Chunk Analysis</h2><div id="chunks" /></section>
    </div>
  );
}
