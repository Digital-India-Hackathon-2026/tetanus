import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ShoppingBag } from 'lucide-react';

export default function TopProductsChart({ isVisible, puzzleStock }) {
  const stock = parseInt(puzzleStock || 5, 10);

  // Top 5 products by search/purchase demand
  const data = [
    { name: 'Dino Puzzle Set', demand: 45, currentStock: stock },
    { name: 'DinoBuilder LEGO', demand: 32, currentStock: 8 },
    { name: 'Smart Coffee Mug', demand: 24, currentStock: 45 },
    { name: 'Charger Pad', demand: 18, currentStock: 215 },
    { name: 'Desk Organizer', demand: 12, currentStock: 96 }
  ];

  return (
    <div className={`border border-brand-border-dark rounded-2xl p-5 bg-white space-y-4 transition-all duration-700 transform ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      <div className="flex items-center justify-between border-b border-brand-border pb-3">
        <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5">
          <ShoppingBag className="w-4 h-4 text-brand-text" />
          Top Products by Demand
        </h3>
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Bar Chart</span>
      </div>

      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart 
            data={data} 
            layout="vertical"
            margin={{ top: 10, right: 10, left: 10, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f1f1" horizontal={false} />
            <XAxis type="number" stroke="#a1a1aa" fontSize={10} tickLine={false} />
            <YAxis 
              dataKey="name" 
              type="category" 
              stroke="#a1a1aa" 
              fontSize={10} 
              tickLine={false}
              width={100}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: '#ffffff', borderColor: '#0a0a0a', borderRadius: 8, fontSize: 11 }}
              itemStyle={{ color: '#0a0a0a' }}
            />
            {/* Horizontal Bar: Solid Black Fill */}
            <Bar dataKey="demand" name="Daily Demand Units" fill="#0a0a0a" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
