import React, { useState } from 'react';
import { Clock } from 'lucide-react';

export default function DemandHeatStrip({ isVisible }) {
  // Mock search volumes per hour of the day
  const hoursData = [
    { hour: "00:00", count: 0 }, { hour: "01:00", count: 1 }, { hour: "02:00", count: 0 }, { hour: "03:00", count: 0 },
    { hour: "04:00", count: 0 }, { hour: "05:00", count: 1 }, { hour: "06:00", count: 2 }, { hour: "07:00", count: 3 },
    { hour: "08:00", count: 5 }, { hour: "09:00", count: 4 }, { hour: "10:00", count: 6 }, { hour: "11:00", count: 8 },
    { hour: "12:00", count: 10 }, { hour: "13:00", count: 12 }, { hour: "14:00", count: 15 }, { hour: "15:00", count: 9 },
    { hour: "16:00", count: 6 }, { hour: "17:00", count: 5 }, { hour: "18:00", count: 4 }, { hour: "19:00", count: 5 },
    { hour: "20:00", count: 3 }, { hour: "21:00", count: 2 }, { hour: "22:00", count: 1 }, { hour: "23:00", count: 0 }
  ];

  const [hoveredIndex, setHoveredIndex] = useState(null);

  const getShadeClass = (count) => {
    if (count === 0) return 'bg-slate-50 border border-slate-100';
    if (count <= 2) return 'bg-slate-200 border border-slate-300';
    if (count <= 5) return 'bg-slate-400 border border-slate-400';
    if (count <= 8) return 'bg-slate-650 border border-slate-650';
    if (count <= 11) return 'bg-slate-800 border border-slate-800';
    return 'bg-[#0A0A0A] border border-[#0A0A0A]';
  };

  return (
    <div className={`border border-brand-border-dark rounded-2xl p-5 bg-white space-y-4 transition-all duration-700 transform ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      <div className="flex items-center justify-between border-b border-brand-border pb-3">
        <div className="text-left space-y-0.5">
          <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5 leading-none">
            <Clock className="w-4 h-4 text-brand-text" />
            Today's Demand Pulse
          </h3>
          <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block">
            Hourly searches for "dinosaur gifts"
          </span>
        </div>
        
        {/* Heat Map Legend */}
        <div className="flex items-center gap-1 text-[9px] text-slate-400 font-bold uppercase tracking-wider">
          <span>Less</span>
          <div className="w-2.5 h-2.5 bg-slate-50 border border-slate-200 rounded-sm" />
          <div className="w-2.5 h-2.5 bg-slate-200 rounded-sm" />
          <div className="w-2.5 h-2.5 bg-slate-400 rounded-sm" />
          <div className="w-2.5 h-2.5 bg-slate-600 rounded-sm" />
          <div className="w-2.5 h-2.5 bg-[#0a0a0a] rounded-sm" />
          <span>More</span>
        </div>
      </div>

      {/* Hour blocks row with custom tooltip */}
      <div className="relative pt-4 pb-2">
        <div 
          className="grid gap-1 md:gap-1.5" 
          style={{ gridTemplateColumns: 'repeat(24, minmax(0, 1fr))' }}
        >
          {hoursData.map((data, idx) => (
            <div
              key={idx}
              className={`aspect-square w-full rounded-md cursor-pointer transition-all duration-200 transform hover:scale-110 relative ${getShadeClass(data.count)}`}
              onMouseEnter={() => setHoveredIndex(idx)}
              onMouseLeave={() => setHoveredIndex(null)}
            />
          ))}
        </div>

        {/* Dynamic Tooltip */}
        {hoveredIndex !== null && (
          <div 
            className="absolute top-[-32px] transform -translate-x-1/2 bg-[#0A0A0A] text-white text-[10px] font-bold py-1 px-2.5 rounded-lg shadow-lg pointer-events-none z-30 transition-all border border-white/20 whitespace-nowrap"
            style={{
              left: `${((hoveredIndex + 0.5) / 24) * 100}%`
            }}
          >
            {hoursData[hoveredIndex].hour} — {hoursData[hoveredIndex].count} search queries
          </div>
        )}
      </div>

      {/* X Axis Labels */}
      <div className="flex justify-between text-[9px] text-slate-400 font-bold uppercase tracking-wider pt-1">
        <span>12 AM</span>
        <span>6 AM</span>
        <span>12 PM</span>
        <span>6 PM</span>
        <span>11 PM</span>
      </div>
    </div>
  );
}
