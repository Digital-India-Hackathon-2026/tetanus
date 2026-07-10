import React, { useState, useEffect } from 'react';
import { getIntelligenceLoop } from '../services/api';
import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { ArrowUpRight, ArrowDownRight, Package, AlertCircle } from 'lucide-react';

// Fake Data for Minimal Charts
const salesData = [
  { name: 'Mon', value: 4000 },
  { name: 'Tue', value: 3000 },
  { name: 'Wed', value: 5000 },
  { name: 'Thu', value: 2780 },
  { name: 'Fri', value: 8900 },
  { name: 'Sat', value: 12000 },
  { name: 'Sun', value: 14000 },
];

const demandData = [
  { name: 'Toys', value: 85 },
  { name: 'Tech', value: 65 },
  { name: 'Home', value: 45 },
  { name: 'Apparel', value: 30 },
];

export default function SellerView() {
  const [stats, setStats] = useState({
    todaySales: "₹0",
    salesChange: "0%",
    activeOrders: 0,
    puzzleStock: 0,
    dinoSearches: 0
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        const loopData = await getIntelligenceLoop();
        const stockVal = parseInt(loopData.stockLeft, 10);
        const searchVal = parseInt(loopData.searchesCount, 10);
        
        setStats({
          todaySales: stockVal >= 30 ? "₹28,500" : "₹23,800",
          salesChange: stockVal >= 30 ? "+9.8%" : "+7.2%",
          activeOrders: stockVal >= 30 ? 39 : 38,
          puzzleStock: stockVal,
          dinoSearches: searchVal
        });
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardStats();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F8F7F5] flex items-center justify-center">
        <div className="w-6 h-6 rounded-full border-2 border-black/20 border-t-black animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F8F7F5] text-[#171717] pb-32">
      
      {/* HEADER */}
      <header className="pt-24 pb-12 px-6">
        <div className="max-w-[1000px] mx-auto">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-4xl tracking-tight font-medium">Overview</h1>
            <p className="text-[#6F6F73] mt-2">Real-time network intelligence</p>
          </motion.div>
        </div>
      </header>

      {/* METRICS ROW */}
      <section className="px-6 mb-12">
        <div className="max-w-[1000px] mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-3xl p-8 border border-black/5 shadow-sm flex flex-col justify-between"
          >
            <div className="text-sm font-medium text-[#6F6F73] mb-4 uppercase tracking-widest">Gross Volume</div>
            <div className="text-5xl font-medium tracking-tighter">{stats.todaySales}</div>
            <div className="mt-4 flex items-center gap-1 text-sm font-medium text-emerald-600 bg-emerald-50 w-fit px-2 py-1 rounded-md">
              <ArrowUpRight className="w-4 h-4" />
              {stats.salesChange} today
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-3xl p-8 border border-black/5 shadow-sm flex flex-col justify-between"
          >
            <div className="text-sm font-medium text-[#6F6F73] mb-4 uppercase tracking-widest">Active Orders</div>
            <div className="text-5xl font-medium tracking-tighter">{stats.activeOrders}</div>
            <div className="mt-4 flex items-center gap-1 text-sm font-medium text-[#6F6F73]">
              Fulfillment running
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className={`rounded-3xl p-8 border shadow-sm flex flex-col justify-between ${
              stats.puzzleStock <= 5 ? 'bg-red-50 border-red-100' : 'bg-white border-black/5'
            }`}
          >
            <div className={`text-sm font-medium mb-4 uppercase tracking-widest ${stats.puzzleStock <= 5 ? 'text-red-600' : 'text-[#6F6F73]'}`}>
              Inventory Alert
            </div>
            <div className={`text-5xl font-medium tracking-tighter ${stats.puzzleStock <= 5 ? 'text-red-700' : '#171717'}`}>
              {stats.puzzleStock} <span className="text-2xl text-opacity-50 font-light tracking-normal">units</span>
            </div>
            <div className={`mt-4 flex items-center gap-2 text-sm font-medium ${stats.puzzleStock <= 5 ? 'text-red-600' : 'text-[#6F6F73]'}`}>
              {stats.puzzleStock <= 5 ? (
                <>
                  <AlertCircle className="w-4 h-4" />
                  Dinosaur Puzzle Set requires restocking.
                </>
              ) : (
                <>
                  <Package className="w-4 h-4" />
                  Stock levels nominal.
                </>
              )}
            </div>
          </motion.div>

        </div>
      </section>

      {/* CHARTS ROW */}
      <section className="px-6">
        <div className="max-w-[1000px] mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Main Chart */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-3xl p-8 border border-black/5 shadow-sm"
          >
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-sm font-semibold uppercase tracking-widest text-[#171717]">Volume Trajectory</h2>
            </div>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={salesData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#171717" stopOpacity={0.1}/>
                      <stop offset="95%" stopColor="#171717" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <Tooltip 
                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}
                    itemStyle={{ color: '#171717', fontWeight: 600 }}
                    cursor={{ stroke: '#171717', strokeWidth: 1, strokeDasharray: '4 4' }}
                  />
                  <Area type="monotone" dataKey="value" stroke="#171717" strokeWidth={2} fillOpacity={1} fill="url(#colorValue)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Secondary Chart */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-white rounded-3xl p-8 border border-black/5 shadow-sm"
          >
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-sm font-semibold uppercase tracking-widest text-[#171717]">Intent Demand</h2>
            </div>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={demandData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#6F6F73', fontSize: 12 }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fill: '#6F6F73', fontSize: 12 }} />
                  <Tooltip 
                    cursor={{ fill: 'transparent' }} 
                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }} 
                  />
                  <Bar dataKey="value" fill="#8B5CF6" radius={[4, 4, 0, 0]} barSize={32} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

        </div>
      </section>

    </div>
  );
}
