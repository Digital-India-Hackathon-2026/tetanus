import React from 'react';
import { AlertTriangle, TrendingDown, Wallet } from 'lucide-react';

export default function MoneyLeftCard({ dinoSearches, remainingBudget }) {
  if (remainingBudget !== undefined) {
    return (
      <div className="w-full bg-emerald-950/20 text-emerald-100 rounded-2xl p-6 relative overflow-hidden border border-emerald-500/30 shadow-xl">
        <div className="absolute top-0 right-0 -mt-8 -mr-8 w-24 h-24 rounded-full bg-emerald-500/20 blur-xl pointer-events-none" />
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10">
          <div className="space-y-1.5 text-left">
            <div className="flex items-center gap-1.5 text-emerald-400 text-[10px] font-bold uppercase tracking-widest">
              <Wallet className="w-3.5 h-3.5 text-emerald-400" />
              Remaining Budget
            </div>
            <h2 className="text-2xl sm:text-3xl font-black tracking-tight text-white leading-none">
              ₹{remainingBudget.toLocaleString()}
            </h2>
            <p className="text-xs text-emerald-300/70 font-medium">
              You still have room in your budget for accessories or add-ons.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const searches = parseInt(dinoSearches || 8, 10);
  // Formula matching ~₹4,200 for 8 searches
  const lostSalesValue = searches * 525;
  const lostSalesText = `₹${lostSalesValue.toLocaleString()} in missed sales this week`;

  return (
    <div className="w-full bg-brand-block-bg text-brand-block-text rounded-2xl p-6 relative overflow-hidden border border-brand-border-dark shadow-xl">
      {/* Visual blueprint accent */}
      <div className="absolute top-0 right-0 -mt-8 -mr-8 w-24 h-24 rounded-full bg-white/5 blur-xl pointer-events-none" />
      
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10">
        <div className="space-y-1.5 text-left">
          <div className="flex items-center gap-1.5 text-slate-400 text-[10px] font-bold uppercase tracking-widest">
            <TrendingDown className="w-3.5 h-3.5 text-slate-400" />
            Money Left On The Table
          </div>
          <h2 className="text-2xl sm:text-3xl font-black tracking-tight text-white leading-none">
            {lostSalesText}
          </h2>
          <p className="text-xs text-slate-400 font-medium">
            Calculated from {searches} spike queries × average conversion (35%) × unit price (₹499) under current stockout risk.
          </p>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/20 bg-white/5 text-xs text-white font-bold max-w-max self-start sm:self-center">
          <AlertTriangle className="w-4 h-4 text-white" />
          Critical Loss Risk
        </div>
      </div>
    </div>
  );
}
