import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';
import { MessageSquare, X, Send, Sparkles, AlertTriangle, CheckCircle, RefreshCw } from 'lucide-react';
import { postSellerQuery } from '../services/api';

export default function FloatingCopilot() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'copilot',
      text: "Hello! I am your CommerceOS Seller Copilot. I cross-reference natural query spikes with real-time stock levels. Ask me about store revenue drops or reorder recommendations by clicking one of the templates below:",
      chartType: null
    }
  ]);

  const presetQueries = [
    { label: "📉 Sales drop", text: "Why did my sales drop yesterday?" },
    { label: "📦 Reorder check", text: "What should I reorder?" }
  ];

  const handleQuerySubmit = async (e, textOverride = null) => {
    if (e) e.preventDefault();
    const queryText = textOverride || query;
    if (!queryText.trim()) return;

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

  return (
    <>
      {/* 1. Floating Circular Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 p-4 rounded-full bg-brand-block-bg hover:bg-slate-800 text-white shadow-xl hover:scale-105 transition-all duration-300 z-50 flex items-center justify-center cursor-pointer group"
      >
        {/* Pulsing ring indicator */}
        <span className="absolute inset-0 rounded-full border border-black group-hover:animate-ping opacity-45 pointer-events-none" />
        
        {isOpen ? (
          <X className="w-6 h-6" />
        ) : (
          <MessageSquare className="w-6 h-6" />
        )}
      </button>

      {/* 2. Floating Compact Chat Drawer */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-[360px] sm:w-[380px] h-[500px] border border-brand-border-dark bg-white rounded-3xl shadow-2xl flex flex-col overflow-hidden z-50 animate-slide-up">
          
          {/* Header */}
          <div className="px-5 py-3.5 border-b border-brand-border bg-slate-50 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-brand-block-bg text-white rounded-lg">
                <Sparkles className="w-4 h-4" />
              </div>
              <div className="text-left">
                <h4 className="font-extrabold text-xs text-brand-text uppercase tracking-wider leading-none">Seller Copilot</h4>
                <span className="text-[8px] text-slate-400 font-bold uppercase tracking-widest block mt-0.5">Neural assistant connected</span>
              </div>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="text-slate-400 hover:text-brand-text transition-all"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Chat message space */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white">
            {chatHistory.map((msg, index) => (
              <div
                key={index}
                className={`flex gap-2 max-w-[90%] ${
                  msg.sender === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'
                }`}
              >
                {/* Bubble card */}
                <div className={`p-3 rounded-xl text-xs text-left leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-slate-100 border border-brand-border text-brand-text rounded-tr-none'
                    : 'bg-brand-block-bg text-white rounded-tl-none font-medium'
                }`}>
                  <p className="whitespace-pre-line">
                    {msg.text.split('**').map((part, pIdx) => 
                      pIdx % 2 === 1 ? <strong key={pIdx} className="font-extrabold underline">{part}</strong> : part
                    )}
                  </p>

                  {/* Inline Recharts within bubble */}
                  {msg.chartType && msg.chartData && (
                    <div className="w-full h-40 bg-white border border-brand-border rounded-lg p-2 mt-2.5">
                      {msg.chartType === 'area' && (
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart data={msg.chartData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                            <defs>
                              <linearGradient id="copilotGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#0a0a0a" stopOpacity={0.15}/>
                                <stop offset="95%" stopColor="#0a0a0a" stopOpacity={0.0}/>
                              </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#f4f4f5" />
                            <XAxis dataKey="day" stroke="#a1a1aa" fontSize={8} tickLine={false} />
                            <YAxis stroke="#a1a1aa" fontSize={8} tickLine={false} />
                            <Tooltip 
                              contentStyle={{ backgroundColor: '#ffffff', borderColor: '#0a0a0a', borderRadius: 4, fontSize: 9 }}
                            />
                            <Area 
                              type="monotone" 
                              dataKey="sales" 
                              stroke="#0a0a0a" 
                              strokeWidth={1.5}
                              fillOpacity={1} 
                              fill="url(#copilotGrad)" 
                            />
                          </AreaChart>
                        </ResponsiveContainer>
                      )}

                      {msg.chartType === 'bar' && (
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={msg.chartData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#f4f4f5" />
                            <XAxis dataKey="name" stroke="#a1a1aa" fontSize={8} tickLine={false} />
                            <YAxis stroke="#a1a1aa" fontSize={8} tickLine={false} />
                            <Tooltip 
                              contentStyle={{ backgroundColor: '#ffffff', borderColor: '#0a0a0a', borderRadius: 4, fontSize: 9 }}
                            />
                            <Bar dataKey="stock" fill="#0a0a0a" radius={[2, 2, 0, 0]}>
                              {msg.chartData.map((entry, index) => (
                                <Cell 
                                  key={`cell-${index}`} 
                                  fill={entry.stock <= entry.safety ? '#666666' : '#0a0a0a'} 
                                />
                              ))}
                            </Bar>
                          </BarChart>
                        </ResponsiveContainer>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex gap-2 max-w-[85%] mr-auto text-left animate-pulse">
                <div className="bg-slate-50 border border-brand-border rounded-xl rounded-tl-none p-3.5 flex-1 min-w-[200px] space-y-2">
                  <div className="h-2 w-3/4 bg-slate-350 rounded shimmer" />
                  <div className="h-2 w-5/6 bg-slate-350 rounded shimmer" />
                </div>
              </div>
            )}
          </div>

          {/* Quick Action Suggestion Chips */}
          <div className="px-4 py-2 bg-slate-50 border-t border-brand-border">
            <div className="flex flex-wrap gap-1.5 items-center">
              <span className="text-[8px] text-slate-400 font-bold uppercase tracking-wider">Ask:</span>
              {presetQueries.map((preset, idx) => (
                <button
                  key={idx}
                  onClick={() => handleQuerySubmit(null, preset.text)}
                  disabled={loading}
                  className="px-2 py-0.5 rounded-md text-[10px] border border-brand-border bg-white text-slate-700 hover:border-brand-border-dark transition-all cursor-pointer font-semibold"
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>

          {/* Input field footer */}
          <form 
            onSubmit={handleQuerySubmit}
            className="p-3 border-t border-brand-border bg-slate-50 flex gap-2 items-center"
          >
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a query..."
              className="flex-1 bg-white border border-brand-border-dark focus:border-brand-border-dark focus:ring-1 focus:ring-brand-border-dark rounded-lg px-3 py-2 text-xs text-brand-text placeholder-slate-400 focus:outline-none"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="p-2 rounded-lg bg-brand-block-bg text-white hover:bg-slate-800 disabled:opacity-40"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>

        </div>
      )}
    </>
  );
}
