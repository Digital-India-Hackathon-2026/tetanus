import React, { useState, useEffect } from 'react';
import { Bell, AlertTriangle, CheckCircle, TrendingUp, ShoppingBag } from 'lucide-react';
import { getIntelligenceLoop } from '../services/api';

// Sub-components
import IntelligenceLoop from '../components/IntelligenceLoop';
import MoneyLeftCard from '../components/MoneyLeftCard';
import SignalFeed from '../components/SignalFeed';
import SalesTrendChart from '../components/SalesTrendChart';
import TopProductsChart from '../components/TopProductsChart';
import DemandHeatStrip from '../components/DemandHeatStrip';
import ReorderSimulator from '../components/ReorderSimulator';
import AgentActivityLog from '../components/AgentActivityLog';
import ProfitComparisonCard from '../components/ProfitComparisonCard';
import CategoryBreakdownChart from '../components/CategoryBreakdownChart';
import FloatingCopilot from '../components/FloatingCopilot';

export default function SellerView() {
  const [stats, setStats] = useState({
    todaySales: "₹23,800",
    salesChange: "▲ 7.2%",
    activeOrders: 38,
    lowStockCount: 1,
    puzzleStock: 5,
    dinoSearches: 8
  });

  const [refreshKey, setRefreshKey] = useState(0);

  // Staged loading animation states
  const [showCharts, setShowCharts] = useState(false);
  const [showTerminal, setShowTerminal] = useState(false);

  const fetchDashboardStats = async () => {
    try {
      const loopData = await getIntelligenceLoop();
      const stockVal = parseInt(loopData.stockLeft, 10);
      const searchVal = parseInt(loopData.searchesCount, 10);
      
      setStats({
        todaySales: stockVal >= 30 ? "₹28,500" : "₹23,800",
        salesChange: stockVal >= 30 ? "▲ 9.8%" : "▲ 7.2%",
        activeOrders: stockVal >= 30 ? 39 : 38,
        lowStockCount: stockVal <= 5 ? 1 : 0,
        puzzleStock: stockVal,
        dinoSearches: searchVal
      });
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchDashboardStats();
  }, [refreshKey]);

  useEffect(() => {
    // Stage 2: Fade in charts and simulators at 2.0s
    const chartsTimer = setTimeout(() => {
      setShowCharts(true);
    }, 2000);

    // Stage 3: Trigger typewriter Terminal Log at 3.5s
    const terminalTimer = setTimeout(() => {
      setShowTerminal(true);
    }, 3500);

    return () => {
      clearTimeout(chartsTimer);
      clearTimeout(terminalTimer);
    };
  }, []);

  const handleStateChange = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 bg-white text-brand-text select-none">
      
      {/* 1. Intelligence Loop Header */}
      <IntelligenceLoop onStateChange={handleStateChange} />

      {/* 2. Primary Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Metric 1 */}
        <div className="border border-brand-border-dark rounded-2xl p-5 bg-white text-left space-y-1 hover:shadow-sm transition-all duration-300">
          <div className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Today's Sales</div>
          <div className="flex items-baseline justify-between">
            <span className="text-2xl font-black text-brand-text">{stats.todaySales}</span>
            <span className="text-xs font-bold text-slate-650">{stats.salesChange}</span>
          </div>
        </div>

        {/* Metric 2 */}
        <div className="border border-brand-border-dark rounded-2xl p-5 bg-white text-left space-y-1 hover:shadow-sm transition-all duration-300">
          <div className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Active Orders</div>
          <div className="flex items-baseline justify-between">
            <span className="text-2xl font-black text-brand-text">{stats.activeOrders}</span>
            <span className="text-xs font-semibold text-slate-400">▲ 2 today</span>
          </div>
        </div>

        {/* Metric 3 */}
        <div className="border border-brand-border-dark rounded-2xl p-5 bg-white text-left space-y-1 hover:shadow-sm transition-all duration-300">
          <div className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Low Stock Alerts</div>
          <div className="flex items-baseline justify-between">
            <span className={`text-2xl font-black ${stats.puzzleStock <= 5 ? 'text-red-655 font-extrabold' : 'text-brand-text'}`}>
              {stats.lowStockCount}
            </span>
            <span className="text-xs font-bold text-slate-400">
              {stats.puzzleStock <= 5 ? "▼ needs action" : "▲ stable"}
            </span>
          </div>
        </div>

      </div>

      {/* 3. Core "AI-in-Action" Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column (5 columns width): Signal Feed & Alerts */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Signal Feed (Reasoning steps staggered on mount) */}
          <SignalFeed searchesCount={stats.dinoSearches} stockLeft={stats.puzzleStock} />

          {/* Live Alerts Panel (Monochrome layouts, warm red ONLY for stock warnings) */}
          <div className="border border-brand-border-dark rounded-2xl p-5 space-y-4 bg-white">
            <div className="flex items-center justify-between border-b border-brand-border pb-3">
              <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5 leading-none">
                <Bell className="w-4 h-4 text-brand-text" />
                Live Alerts
              </h3>
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-slate-900 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-slate-900"></span>
              </span>
            </div>
            
            <div className="space-y-3">
              {/* Critical Alert with reserved Warm Red */}
              {stats.puzzleStock <= 5 ? (
                <div className="flex gap-3 bg-red-50 border border-red-600 rounded-xl p-3.5 text-xs text-red-650">
                  <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0" />
                  <div className="text-left leading-normal">
                    <span className="font-extrabold block mb-0.5 uppercase tracking-wide">Stockout Risk Critical</span>
                    Dinosaur Puzzle Set inventory is down to {stats.puzzleStock} units. Spiked demand has outrun available warehouse stocks.
                  </div>
                </div>
              ) : (
                <div className="flex gap-3 bg-slate-50 border border-brand-border rounded-xl p-3.5 text-xs text-slate-700">
                  <CheckCircle className="w-5 h-5 text-slate-650 flex-shrink-0" />
                  <div className="text-left leading-normal">
                    <span className="font-extrabold text-brand-text block mb-0.5 uppercase tracking-wide">Alert Resolved</span>
                    Dinosaur Puzzle Set reordered. Stock replenishing to safety limits.
                  </div>
                </div>
              )}

              {/* Spikes / Other Alerts - Strictly Monochrome */}
              {stats.dinoSearches > 0 && (
                <div className="flex gap-3 bg-slate-50 border border-brand-border rounded-xl p-3.5 text-xs text-slate-650">
                  <TrendingUp className="w-5 h-5 text-brand-text flex-shrink-0" />
                  <div className="text-left leading-normal">
                    <span className="font-extrabold text-brand-text block mb-0.5 uppercase tracking-wide text-left">Traffic Spike</span>
                    Search counts for 'dinosaur gifts' saw a 300% volume increase today.
                  </div>
                </div>
              )}

              <div className="flex gap-3 bg-slate-50 border border-brand-border rounded-xl p-3.5 text-xs text-slate-400">
                <ShoppingBag className="w-5 h-5 text-slate-455 flex-shrink-0" />
                <div className="text-left leading-normal">
                  <span className="font-bold text-slate-600 block mb-0.5 uppercase tracking-wide">Sync Status</span>
                  External integrations and listings are in sync.
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Right Column (7 columns width): Hero Loss Card & Simulator */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Hero Money Left Card */}
          <MoneyLeftCard dinoSearches={stats.dinoSearches} />

          {/* Reorder Simulator */}
          <ReorderSimulator 
            isVisible={showCharts} 
            puzzleStock={stats.puzzleStock} 
            onStateChange={handleStateChange} 
          />

        </div>

      </div>

      {/* 4. Chart Row (Two Columns, fades in at 2s) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <SalesTrendChart isVisible={showCharts} />
        <TopProductsChart isVisible={showCharts} puzzleStock={stats.puzzleStock} />
      </div>

      {/* 5. Demand Heat Strip (Full Width, fades in at 2s) */}
      <DemandHeatStrip isVisible={showCharts} />

      {/* 6. Agent Activity Log (Bottom Terminal log, types out character-by-character starting at 3.5s) */}
      <AgentActivityLog isVisible={showTerminal} />

      {/* 7. Secondary cards (Profit vs last period, category share progress bars) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <ProfitComparisonCard isVisible={showCharts} />
        <CategoryBreakdownChart isVisible={showCharts} />
      </div>

      {/* 8. Collapsible Floating AI Assistant Button (Collapses to right drawer overlay) */}
      <FloatingCopilot />

    </div>
  );
}
