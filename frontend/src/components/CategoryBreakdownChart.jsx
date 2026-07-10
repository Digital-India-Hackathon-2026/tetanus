import React from 'react';
import { Layers } from 'lucide-react';

export default function CategoryBreakdownChart({ isVisible }) {
  const categories = [
    { name: "Toys & Games", percentage: 45, count: "₹82,890" },
    { name: "Electronics", percentage: 25, count: "₹46,050" },
    { name: "Audio Systems", percentage: 15, count: "₹27,630" },
    { name: "Office Stationery", percentage: 10, count: "₹18,420" },
    { name: "Accessories", percentage: 5, count: "₹9,210" }
  ];

  return (
    <div className={`border border-brand-border-dark rounded-2xl p-5 bg-white space-y-4 text-left transition-all duration-700 transform ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      <div className="flex items-center justify-between border-b border-brand-border pb-2.5">
        <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5 leading-none">
          <Layers className="w-4 h-4 text-brand-text" />
          Category Breakdown
        </h3>
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Revenue Share</span>
      </div>

      <div className="space-y-3">
        {categories.map((cat, idx) => (
          <div key={idx} className="space-y-1.5">
            <div className="flex justify-between text-xs font-bold">
              <span className="text-slate-700">{cat.name}</span>
              <span className="text-brand-text">{cat.count} ({cat.percentage}%)</span>
            </div>
            
            {/* Progress Bar visual indicator */}
            <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div 
                className="h-full bg-brand-block-bg rounded-full transition-all duration-1000"
                style={{ 
                  width: isVisible ? `${cat.percentage}%` : '0%',
                  transitionDelay: `${idx * 100}ms`
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
