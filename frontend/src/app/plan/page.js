"use client";

import { useEffect, useState } from "react";
import { createPlan } from "@/lib/api";
import type { PlanResponse } from "@/lib/api";

export default function PlanPage() {
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [source, setSource] = useState<"backend" | "fallback" | "unknown">("unknown");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function fetchPlan(goal = "Build TaskPilot workflow") {
    setLoading(true);
    setError(null);
    try {
      const data = await createPlan(goal);
      setPlan(data);
      setSource("backend");
    } catch (err) {
      console.error(err);
      setError("Failed to fetch plan, using fallback data.");
      setPlan({
        goal: "Demo: Build TaskPilot agentic workflow",
        goal_id: 0,
        milestones: [
          {
            title: "Day 1 – Backend & agentic flow",
            tasks: [
              { id: 1, title: "Design task schema & /plan endpoint", status: "pending" },
              { id: 2, title: "Implement dummy AI planning service", status: "pending" },
            ],
          },
        ],
      });
      setSource("fallback");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchPlan();
  }, []);

  if (loading) return <p>Loading plan…</p>;
  if (!plan) return <p>No plan available</p>;

  return (
    <section className="space-y-4">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h2 className="text-xl font-semibold mb-1">Your execution plan</h2>
          <p className="text-sm text-slate-400">
            Goal: <span className="text-slate-100">{plan.goal}</span>
          </p>
        </div>

        <span
          className={`text-[10px] px-2 py-1 rounded-full border ${
            source === "backend"
              ? "bg-emerald-500/10 border-emerald-500/60 text-emerald-300"
              : "bg-slate-900 border-slate-600 text-slate-300"
          }`}
        >
          {source === "backend" ? "Live from backend" : "Using demo data"}
        </span>
      </div>

      <button
        onClick={() => fetchPlan("New Goal Name")}
        className="px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600"
      >
        Generate New Plan
      </button>

      <div className="grid gap-4 md:grid-cols-2">
        {plan.milestones.map((m, idx) => (
          <article key={idx} className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 space-y-2">
            <h3 className="font-semibold text-sm md:text-base">{m.title}</h3>
            <ul className="text-xs md:text-sm list-disc list-inside space-y-1 text-slate-300">
              {m.tasks.map((t) => (
                <li key={t.id}>{t.title}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>

      {error && <p className="text-red-400">{error}</p>}
    </section>
  );
}