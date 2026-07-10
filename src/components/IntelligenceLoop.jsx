import React, { useState, useEffect } from 'react';
import { Sparkles, RefreshCw, CheckCircle, ArrowRight, AlertTriangle } from 'lucide-react';
import { getIntelligenceLoop, triggerReorder } from '../services/api';

export default function IntelligenceLoop({ onStateChange }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [actionSuccess, setActionSuccess] = useState(false);

  const fetchLoopData = async () => {
    try {
      const result = await getIntelligenceLoop();
      setData(result);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchLoopData();
    const interval = setInterval(fetchLoopData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleReorder = async () => {
    setLoading(true);
    try {
      await triggerReorder();
      setActionSuccess(true);
      if (onStateChange) onStateChange();
      setTimeout(() => {
        setActionSuccess(false);
        fetchLoopData();
      }, 3000);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (!data) return null;

  const isResolved = parseInt(data.stockLeft, 10) >= 30;

  return (
    <div className={`relative overflow-hidden rounded-2xl border-2 p-5 transition-all duration-500 bg-white ${
      isResolved 
        ? 'border-slate-200' 
        : 'animate-border-bw border-brand-border-dark'
    }`}>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 relative z-10">
        
        {/* Signal content flow */}
        <div className="flex flex-col sm:flex-row sm:items-center gap-3">
          {/* Black bar badge with white text */}
          <div className="flex-shrink-0 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-brand-block-bg text-white text-xs font-extrabold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5 animate-pulse" />
            AI Loop Signal
          </div>
          
          {/* Stark black text describing intent-to-inventory link */}
          <div className="flex flex-wrap items-center gap-1.5 text-xs sm:text-sm text-brand-text font-bold text-left">
            <span>📈 {data.searchesCount} shoppers</span>
            <span className="text-slate-500">searched for</span>
            <span>"{data.searchQuery}"</span>
            <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
            <span>{data.productName} is at {data.stockLeft} units</span>
            <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
            <span className="underline decoration-slate-400">Reorder suggested ({data.suggestedReorder} units)</span>
          </div>
        </div>

        {/* Action Button */}
        <div className="flex items-center">
          {isResolved ? (
            <div className="flex items-center gap-1.5 text-brand-text bg-slate-100 px-4 py-2 rounded-full border border-brand-border-dark text-xs font-extrabold">
              <CheckCircle className="w-3.5 h-3.5" />
              Replenished
            </div>
          ) : actionSuccess ? (
            <div className="flex items-center gap-1.5 text-white bg-brand-block-bg px-4 py-2 rounded-full text-xs font-extrabold animate-pulse">
              <CheckCircle className="w-3.5 h-3.5" />
              Ordered
            </div>
          ) : (
            <button
              onClick={handleReorder}
              disabled={loading}
              className="w-full md:w-auto px-5 py-2.5 rounded-full bg-brand-block-bg hover:bg-slate-800 text-white text-xs font-extrabold tracking-wider transition-all duration-300 disabled:opacity-50 flex items-center justify-center gap-1 cursor-pointer"
            >
              {loading ? (
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <>
                  Approve Reorder
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
