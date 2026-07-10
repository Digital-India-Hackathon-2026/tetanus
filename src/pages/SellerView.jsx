import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';
import { MessageSquare, ArrowRight, AlertTriangle, TrendingUp, ShoppingBag, Bell, RefreshCw, Send, Sparkles, CheckCircle } from 'lucide-react';
import { postSellerQuery, getIntelligenceLoop } from '../services/api';
import IntelligenceLoop from '../components/IntelligenceLoop';

export default function SellerView() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'copilot',
      text: "Hello! I am your CommerceOS Seller Copilot. I cross-reference natural query spikes with real-time stock levels. Ask me about store revenue drops or reorder recommendations by clicking one of the templates below:",
      chartType: null
    }
  ]);
  
  // Dashboard stats state
  const [stats, setStats] = useState({
    todaySales: "₹23,800",
    salesChange: "▲ 7.2%",
    activeOrders: 38,
    lowStockCount: 1,
    puzzleStock: 5,
    dinoSearches: 3
  });

  const [refreshKey, setRefreshKey] = useState(0);

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

  // Handle local state updates from the Intelligence Loop action
  const handleStateChange = () => {
    setRefreshKey(prev => prev + 1);
    
    // Inject a system notification in the copilot chat showing the flow is resolved
    setChatHistory(prev => [
      ...prev,
      {
        sender: 'copilot',
        text: "⚡ **System Update**: Replenishment invoice generated! 25 units of Dinosaur Puzzle Set ordered. Current warehouse count has updated to 30.",
        isSystem: true
      }
    ]);
  };

  const handleQuerySubmit = async (e, textOverride = null) => {
    if (e) e.preventDefault();
    const queryText = textOverride || query;
    if (!queryText.trim()) return;

    // Add user query to chat history
    setChatHistory(prev => [...prev, { sender: 'user', text: queryText }]);
    setQuery("");
    setLoading(true);

    try {
      const response = await postSellerQuery(queryText);
      setChatHistory(prev => [
        ...prev,
        {
          sender: 'copilot',
          text: response.answer,
          chartType: response.chartType,
          chartData: response.chartData,
          chartConfig: response.chartConfig
        }
      ]);
    } catch (err) {
      setChatHistory(prev => [
        ...prev,
        {
          sender: 'copilot',
          text: "Error fetching data from neural indexing. Check API rules.",
          isError: true
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Preset queries
  const presetQueries = [
    { label: "📉 Sales drop query", text: "Why did my sales drop yesterday?" },
    { label: "📦 Inventory reorder check", text: "What should I reorder?" }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 bg-white text-brand-text">
      
      {/* Top Banner Area: The Intelligence Loop (restyled in black and white) */}
      <IntelligenceLoop onStateChange={handleStateChange} />

      {/* Main Grid Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Stats & Alerts (4 Columns) */}
        <div className="lg:col-span-4 space-y-6">
          
          {/* Store Performance cards (white cards with black borders, black numerals, unicode glyphs) */}
          <div className="border border-brand-border-dark rounded-2xl p-5 space-y-4 bg-white">
            <h3 className="text-xs font-bold text-slate-400 tracking-widest uppercase text-left">Store Metrics</h3>
            <div className="grid grid-cols-1 gap-4">
              
              {/* Stat 1 */}
              <div className="border border-brand-border rounded-xl p-4 text-left space-y-1 bg-white">
                <div className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider">Today's Sales</div>
                <div className="flex items-baseline justify-between">
                  <span className="text-2xl font-black text-brand-text">{stats.todaySales}</span>
                  <span className="text-xs font-bold text-slate-600">{stats.salesChange}</span>
                </div>
              </div>

              {/* Stat 2 */}
              <div className="border border-brand-border rounded-xl p-4 text-left space-y-1 bg-white">
                <div className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider">Active Orders</div>
                <div className="flex items-baseline justify-between">
                  <span className="text-2xl font-black text-brand-text">{stats.activeOrders}</span>
                  <span className="text-xs font-semibold text-slate-400">▲ 2 today</span>
                </div>
              </div>

              {/* Stat 3 */}
              <div className="border border-brand-border rounded-xl p-4 text-left space-y-1 bg-white">
                <div className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider">Low Stock Items</div>
                <div className="flex items-baseline justify-between">
                  <span className="text-2xl font-black text-brand-text">
                    {stats.lowStockCount}
                  </span>
                  <span className="text-xs font-bold text-slate-400">
                    {stats.lowStockCount > 0 ? "▼ needs action" : "▲ stable"}
                  </span>
                </div>
              </div>

            </div>
          </div>

          {/* Live Alerts Panel (monochrome icons, warm red ONLY for critical alerts) */}
          <div className="border border-brand-border-dark rounded-2xl p-5 space-y-4 bg-white">
            <div className="flex items-center justify-between border-b border-brand-border pb-2.5">
              <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5">
                <Bell className="w-4 h-4 text-brand-text" />
                Live Alerts
              </h3>
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-slate-900 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-slate-900"></span>
              </span>
            </div>
            
            <div className="space-y-3">
              {/* CRITICAL STOCK ALERT: Highlighted strictly with warm red accent */}
              {stats.puzzleStock <= 5 ? (
                <div className="flex gap-3 bg-red-50 border border-red-600 rounded-xl p-3.5 text-xs text-red-600">
                  <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0" />
                  <div className="text-left">
                    <span className="font-extrabold block mb-0.5 uppercase tracking-wide">Critical Stock Warning</span>
                    Dinosaur Puzzle Set inventory is critical at {stats.puzzleStock} units.
                  </div>
                </div>
              ) : (
                <div className="flex gap-3 bg-slate-50 border border-brand-border rounded-xl p-3.5 text-xs text-slate-700">
                  <CheckCircle className="w-5 h-5 text-slate-600 flex-shrink-0" />
                  <div className="text-left">
                    <span className="font-extrabold block mb-0.5 uppercase tracking-wide text-brand-text">Restock Fulfilled</span>
                    Dinosaur Puzzle Set inventory has been stabilized to {stats.puzzleStock} units.
                  </div>
                </div>
              )}

              {/* DEMAND SPIKE: Strictly monochrome/slate */}
              {stats.dinoSearches > 0 && (
                <div className="flex gap-3 bg-slate-50 border border-brand-border rounded-xl p-3.5 text-xs text-slate-600">
                  <TrendingUp className="w-5 h-5 text-brand-text flex-shrink-0" />
                  <div className="text-left">
                    <span className="font-extrabold text-brand-text block mb-0.5 uppercase tracking-wide">Demand Influx</span>
                    Search volumes for "dinosaur gifts" increased by 300% today.
                  </div>
                </div>
              )}

              {/* NETWORK CHANNEL: Strictly monochrome/slate */}
              <div className="flex gap-3 bg-slate-50 border border-brand-border rounded-xl p-3.5 text-xs text-slate-400">
                <ShoppingBag className="w-5 h-5 text-slate-400 flex-shrink-0" />
                <div className="text-left">
                  <span className="font-bold text-slate-500 block mb-0.5 uppercase tracking-wide">Sync Status</span>
                  External sales channels and listings are fully synchronized.
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Right Column: Copilot Workspace (8 Columns) */}
        <div className="lg:col-span-8 space-y-6">
          <div className="border border-brand-border-dark rounded-2xl flex flex-col h-[600px] bg-white relative overflow-hidden">
            
            {/* Copilot Chat Header */}
            <div className="px-6 py-4 border-b border-brand-border flex items-center justify-between bg-slate-50">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-brand-block-bg text-white rounded-xl">
                  <MessageSquare className="w-4 h-4" />
                </div>
                <div className="text-left">
                  <h2 className="font-extrabold text-brand-text text-sm uppercase">Seller AI Copilot</h2>
                  <p className="text-[9px] text-slate-500 flex items-center gap-1 font-bold">
                    <span className="h-1.5 w-1.5 rounded-full bg-brand-block-bg animate-pulse" />
                    Store Analytics Terminal Active
                  </p>
                </div>
              </div>
            </div>

            {/* Chat Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-white">
              {chatHistory.map((msg, index) => (
                <div
                  key={index}
                  className={`flex gap-3 max-w-[85%] ${
                    msg.sender === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'
                  }`}
                >
                  {/* Avatar */}
                  <div className={`w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center text-[10px] font-bold ${
                    msg.sender === 'user'
                      ? 'bg-slate-100 border border-brand-border-dark text-brand-text'
                      : 'bg-brand-block-bg text-white'
                  }`}>
                    {msg.sender === 'user' ? 'U' : <Sparkles className="w-3.5 h-3.5" />}
                  </div>

                  {/* Bubble content */}
                  <div className={`space-y-4 rounded-2xl p-4 text-xs sm:text-sm text-left ${
                    msg.sender === 'user'
                      ? 'bg-slate-100 text-brand-text rounded-tr-none border border-brand-border'
                      : msg.isSystem
                        ? 'bg-slate-50 border-2 border-dashed border-brand-border-dark text-brand-text rounded-tl-none font-bold'
                        : 'bg-brand-block-bg text-white rounded-tl-none'
                  }`}>
                    <div className="leading-relaxed whitespace-pre-line">
                      {msg.text.split('**').map((part, pIdx) => 
                        pIdx % 2 === 1 ? <strong key={pIdx} className="font-extrabold underline">{part}</strong> : part
                      )}
                    </div>

                    {/* Render Charts if applicable - STYLED IN STRICT MONOCHROME */}
                    {msg.chartType && msg.chartData && (
                      <div className="w-full h-64 bg-white border border-brand-border rounded-xl p-4 mt-2">
                        {msg.chartType === 'area' && (
                          <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={msg.chartData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                              <defs>
                                <linearGradient id="monochromeGrad" x1="0" y1="0" x2="0" y2="1">
                                  <stop offset="5%" stopColor="#0a0a0a" stopOpacity={0.2}/>
                                  <stop offset="95%" stopColor="#0a0a0a" stopOpacity={0.0}/>
                                </linearGradient>
                              </defs>
                              <CartesianGrid strokeDasharray="3 3" stroke="#f1f1f1" />
                              <XAxis dataKey="day" stroke="#a1a1aa" fontSize={10} tickLine={false} />
                              <YAxis stroke="#a1a1aa" fontSize={10} tickLine={false} />
                              <Tooltip 
                                contentStyle={{ backgroundColor: '#ffffff', borderColor: '#0a0a0a', borderRadius: 8, color: '#0a0a0a', fontSize: 11 }}
                                labelStyle={{ fontWeight: 'bold' }}
                              />
                              <Area 
                                type="monotone" 
                                dataKey="sales" 
                                stroke="#0a0a0a" 
                                strokeWidth={2}
                                fillOpacity={1} 
                                fill="url(#monochromeGrad)" 
                              />
                            </AreaChart>
                          </ResponsiveContainer>
                        )}

                        {msg.chartType === 'bar' && (
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={msg.chartData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                              <CartesianGrid strokeDasharray="3 3" stroke="#f1f1f1" />
                              <XAxis dataKey="name" stroke="#a1a1aa" fontSize={9} tickLine={false} />
                              <YAxis stroke="#a1a1aa" fontSize={10} tickLine={false} />
                              <Tooltip 
                                contentStyle={{ backgroundColor: '#ffffff', borderColor: '#0a0a0a', borderRadius: 8, fontSize: 11 }}
                                itemStyle={{ color: '#0a0a0a' }}
                              />
                              <Bar dataKey="stock" fill="#0a0a0a" radius={[2, 2, 0, 0]}>
                                {msg.chartData.map((entry, index) => (
                                  <Cell 
                                    key={`cell-${index}`} 
                                    fill={entry.stock <= entry.safety ? '#666666' : '#0a0a0a'} 
                                  />
                                ))}
                              </Bar>
                              <Bar dataKey="safety" fill="#e5e5e5" radius={[2, 2, 0, 0]} />
                            </BarChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Chat Loader skeletons */}
              {loading && (
                <div className="flex gap-3 max-w-[80%] mr-auto text-left">
                  <div className="w-7 h-7 rounded-full bg-slate-200 shimmer flex-shrink-0" />
                  <div className="space-y-3 border border-brand-border rounded-2xl rounded-tl-none p-5 flex-1 min-w-[260px] bg-slate-50">
                    <div className="h-3 w-3/4 bg-slate-300 rounded shimmer" />
                    <div className="h-3 w-5/6 bg-slate-300 rounded shimmer" />
                    <div className="h-32 w-full bg-white border border-brand-border rounded-xl shimmer mt-2" />
                  </div>
                </div>
              )}
            </div>

            {/* Template queries */}
            <div className="px-6 py-2 bg-slate-50 border-t border-brand-border">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wider">Suggested:</span>
                {presetQueries.map((preset, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuerySubmit(null, preset.text)}
                    disabled={loading}
                    className="px-2.5 py-1 rounded-lg text-xs border border-brand-border hover:border-brand-border-dark bg-white text-slate-700 hover:text-brand-text transition-all cursor-pointer font-semibold"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Footer Input form */}
            <form 
              onSubmit={handleQuerySubmit} 
              className="p-4 border-t border-brand-border bg-slate-50 flex gap-3 items-center"
            >
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask your query about stock counts, reorders, or sales..."
                className="flex-1 bg-white border border-brand-border-dark focus:border-brand-border-dark focus:ring-1 focus:ring-brand-border-dark rounded-xl px-4 py-2.5 text-xs sm:text-sm text-brand-text placeholder-slate-400 focus:outline-none transition-all"
              />
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="p-2.5 rounded-xl bg-brand-block-bg hover:bg-slate-800 disabled:opacity-40 text-white transition-all duration-200"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>

          </div>
        </div>

      </div>

    </div>
  );
}
