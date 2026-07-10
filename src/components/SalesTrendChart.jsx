import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';

export default function SalesTrendChart({ isVisible }) {
  // 14 days actual + 7 days projected sales data
  const data = [
    { name: 'Jul 10', actual: 23800, projected: null },
    { name: 'Jul 11', actual: 24200, projected: null },
    { name: 'Jul 12', actual: 25000, projected: null },
    { name: 'Jul 13', actual: 26100, projected: null },
    { name: 'Jul 14', actual: 24800, projected: null },
    { name: 'Jul 15', actual: 25500, projected: null },
    { name: 'Jul 16', actual: 27200, projected: null },
    { name: 'Jul 17', actual: 26800, projected: null },
    { name: 'Jul 18', actual: 27900, projected: null },
    { name: 'Jul 19', actual: 28400, projected: null },
    { name: 'Jul 20', actual: 21500, projected: null }, // Drop day
    { name: 'Jul 21', actual: 23800, projected: 23800 }, // Merge connection
    { name: 'Jul 22', actual: null, projected: 25100 },
    { name: 'Jul 23', actual: null, projected: 26500 },
    { name: 'Jul 24', actual: null, projected: 28000 },
    { name: 'Jul 25', actual: null, projected: 29500 },
    { name: 'Jul 26', actual: null, projected: 31000 },
    { name: 'Jul 27', actual: null, projected: 32200 },
    { name: 'Jul 28', actual: null, projected: 33500 },
  ];

  return (
    <div className={`border border-brand-border-dark rounded-2xl p-5 bg-white space-y-4 transition-all duration-700 transform ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      <div className="flex items-center justify-between border-b border-brand-border pb-3">
        <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5">
          <TrendingUp className="w-4 h-4 text-brand-text" />
          Sales Trend & Forecast
        </h3>
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Line Chart</span>
      </div>

      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f1f1" />
            <XAxis dataKey="name" stroke="#a1a1aa" fontSize={10} tickLine={false} />
            <YAxis stroke="#a1a1aa" fontSize={10} tickLine={false} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#ffffff', borderColor: '#0a0a0a', borderRadius: 8, color: '#0a0a0a', fontSize: 11 }}
              labelStyle={{ fontWeight: 'bold' }}
            />
            <Legend 
              wrapperStyle={{ fontSize: 10, fontWeight: 'bold', paddingTop: 10 }}
              iconType="plainline"
            />
            {/* Actual sales: Solid Black Line */}
            <Line 
              type="monotone" 
              name="Actual Sales"
              dataKey="actual" 
              stroke="#0a0a0a" 
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
              connectNulls
            />
            {/* Projected sales: Dashed Black Line */}
            <Line 
              type="monotone" 
              name="Projected Sales"
              dataKey="projected" 
              stroke="#0a0a0a" 
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
              connectNulls
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
