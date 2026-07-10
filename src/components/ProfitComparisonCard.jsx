import React from 'react';
import { ArrowUpRight } from 'lucide-react';

export default function ProfitComparisonCard({ isVisible }) {
  return (
    <div className={`border border-brand-border-dark rounded-2xl p-5 bg-white space-y-4 text-left transition-all duration-700 transform ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      <div className="flex items-center justify-between border-b border-brand-border pb-2.5">
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Performance Log</span>
        <span className="text-[9px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-extrabold uppercase">30-Day Window</span>
      </div>

      <div className="space-y-2">
        <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block">Net Profit Margin</span>
        <div className="flex items-baseline justify-between">
          <span className="text-2xl font-black text-brand-text">₹1,84,200</span>
          <span className="text-xs font-black text-brand-text flex items-center">
            ▲ 14.2%
            <ArrowUpRight className="w-3 h-3 ml-0.5" />
          </span>
        </div>
        <p className="text-[10px] text-slate-400 font-medium leading-normal pt-1">
          Margins increased due to strong performance in high-ticket segments and lower bulk shipping expenses.
        </p>
      </div>
    </div>
  );
}
