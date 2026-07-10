import React, { useState, useEffect } from 'react';
import { Cpu } from 'lucide-react';

export default function SignalFeed({ searchesCount, stockLeft }) {
  const searches = searchesCount || 8;
  const stock = stockLeft || 5;

  const steps = [
    { time: "14:02", text: "Analyzing search patterns..." },
    { time: "14:02", text: `${searches} searches for 'dinosaur gifts' detected in the last hour` },
    { time: "14:03", text: "Cross-referencing inventory databases..." },
    { time: "14:03", text: `Dinosaur Puzzle Set at ${stock} units, below 30-unit safety threshold` },
    { time: "14:05", text: "Reorder of 25 units recommended" }
  ];

  const [visibleCount, setVisibleCount] = useState(0);

  useEffect(() => {
    if (visibleCount < steps.length) {
      const timer = setTimeout(() => {
        setVisibleCount(prev => prev + 1);
      }, 400); // 400ms stagger between lines
      return () => clearTimeout(timer);
    }
  }, [visibleCount]);

  return (
    <div className="border border-brand-border-dark rounded-2xl p-5 bg-white space-y-4">
      <div className="flex items-center justify-between border-b border-brand-border pb-3">
        <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5">
          <Cpu className="w-4 h-4 text-brand-text animate-pulse" />
          AI Reasoning Trace
        </h3>
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Sequential Log</span>
      </div>

      {/* Monospace Timeline list */}
      <div className="relative pl-4 border-l border-brand-border-dark py-1 space-y-3.5 text-left font-mono">
        {steps.map((step, idx) => {
          const isVisible = idx < visibleCount;
          return (
            <div 
              key={idx}
              className={`text-xs transition-all duration-500 transform ${
                isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-2 pointer-events-none'
              }`}
            >
              <span className="text-slate-400 mr-2 font-semibold">[{step.time}]</span>
              <span className="text-brand-text font-medium">{step.text}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
