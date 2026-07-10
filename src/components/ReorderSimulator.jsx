import React, { useState } from 'react';
import { ArrowRight, RefreshCw, CheckCircle, Calculator } from 'lucide-react';
import { triggerReorder } from '../services/api';

export default function ReorderSimulator({ isVisible, puzzleStock, onStateChange }) {
  const [quantity, setQuantity] = useState(25);
  const [loading, setLoading] = useState(false);
  const [actionSuccess, setActionSuccess] = useState(false);

  const stock = parseInt(puzzleStock || 5, 10);
  const isResolved = stock >= 30;

  // Simple math simulation
  // 1 unit orders avoid stockouts and save ₹320 in lost demand
  const dailyDemandRate = 3.5; // units/day
  const coverDays = Math.floor((stock + quantity) / dailyDemandRate);
  
  // Calculate target date
  const targetDate = new Date();
  targetDate.setDate(targetDate.getDate() + coverDays);
  const targetDateStr = targetDate.toLocaleDateString('en-IN', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  const lostSalesAvoided = quantity * 320;

  const handleReorder = async () => {
    setLoading(true);
    try {
      await triggerReorder();
      setActionSuccess(true);
      if (onStateChange) onStateChange();
      setTimeout(() => {
        setActionSuccess(false);
      }, 3000);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`border border-brand-border-dark rounded-2xl p-5 bg-white space-y-5 transition-all duration-700 transform ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-brand-border pb-3">
        <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5">
          <Calculator className="w-4 h-4 text-brand-text" />
          "What-If" Reorder Simulator
        </h3>
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider font-mono">Live Projections</span>
      </div>

      {/* Simulator Inputs */}
      <div className="space-y-4 text-left">
        <div className="flex justify-between items-center text-xs font-bold">
          <span className="text-slate-500 uppercase tracking-wide">Reorder Quantity</span>
          <span className="text-brand-text font-mono text-sm bg-slate-100 px-2 py-0.5 rounded">
            {quantity} units
          </span>
        </div>

        <input 
          type="range" 
          min="0" 
          max="100" 
          step="5"
          value={quantity} 
          disabled={isResolved}
          onChange={(e) => setQuantity(parseInt(e.target.value, 10))}
          className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-brand-block-bg disabled:opacity-30"
        />
        
        <div className="grid grid-cols-2 gap-4 pt-2">
          {/* Output 1: Days of Cover */}
          <div className="border border-brand-border rounded-xl p-3 bg-slate-50">
            <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wider block">Stockout Postponed Until</span>
            <span className="text-xs sm:text-sm font-black text-brand-text block mt-1">
              {isResolved ? "Stock Stable" : `${targetDateStr} (${coverDays} days cover)`}
            </span>
          </div>

          {/* Output 2: Lost Sales Prevented */}
          <div className="border border-brand-border rounded-xl p-3 bg-slate-50">
            <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wider block">Lost Sales Prevented</span>
            <span className="text-xs sm:text-sm font-black text-brand-text block mt-1">
              {isResolved ? "₹0 (Stocked)" : `₹${lostSalesAvoided.toLocaleString()}`}
            </span>
          </div>
        </div>

      </div>

      {/* Approve Reorder Button mirroring banner */}
      <div className="pt-2">
        {isResolved ? (
          <div className="w-full py-3 rounded-xl border border-brand-border-dark bg-slate-50 text-slate-500 text-xs font-extrabold flex items-center justify-center gap-1.5">
            <CheckCircle className="w-4 h-4 text-slate-500" />
            Inventory Fulfills Projected Cover
          </div>
        ) : actionSuccess ? (
          <div className="w-full py-3 rounded-xl bg-brand-block-bg text-white text-xs font-extrabold flex items-center justify-center gap-1.5 animate-pulse">
            <CheckCircle className="w-4 h-4 text-white" />
            Reorder Dispatched Successfully
          </div>
        ) : (
          <button
            onClick={handleReorder}
            disabled={loading || quantity <= 0}
            className="w-full py-3 rounded-xl bg-brand-block-bg hover:bg-slate-800 text-white text-xs font-extrabold flex items-center justify-center gap-1.5 transition-all cursor-pointer"
          >
            {loading ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <>
                Approve Reorder of {quantity} Units
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        )}
      </div>

    </div>
  );
}
