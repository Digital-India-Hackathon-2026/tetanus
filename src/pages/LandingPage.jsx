import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Cpu } from 'lucide-react';

function FloatingCube({ halfSize = 48, position = "", color = "rgba(10, 10, 10, 0.03)", borderColor = "rgba(10, 10, 10, 0.15)", delay = "0s" }) {
  return (
    <div 
      className={`absolute preserve-3d ${position}`} 
      style={{ 
        width: halfSize * 2, 
        height: halfSize * 2,
        animationDelay: delay,
        transformStyle: 'preserve-3d'
      }}
    >
      <div 
        className="cube preserve-3d animate-spin-slow"
        style={{
          width: '100%',
          height: '100%',
          transformStyle: 'preserve-3d',
        }}
      >
        {/* Front */}
        <div 
          className="cube-face" 
          style={{ 
            border: `1px solid ${borderColor}`, 
            background: color, 
            transform: `rotateY(0deg) translateZ(${halfSize}px)` 
          }}
        />
        {/* Back */}
        <div 
          className="cube-face" 
          style={{ 
            border: `1px solid ${borderColor}`, 
            background: color, 
            transform: `rotateY(180deg) translateZ(${halfSize}px)` 
          }}
        />
        {/* Left */}
        <div 
          className="cube-face" 
          style={{ 
            border: `1px solid ${borderColor}`, 
            background: color, 
            transform: `rotateY(-90deg) translateZ(${halfSize}px)` 
          }}
        />
        {/* Right */}
        <div 
          className="cube-face" 
          style={{ 
            border: `1px solid ${borderColor}`, 
            background: color, 
            transform: `rotateY(90deg) translateZ(${halfSize}px)` 
          }}
        />
        {/* Top */}
        <div 
          className="cube-face" 
          style={{ 
            border: `1px solid ${borderColor}`, 
            background: color, 
            transform: `rotateX(90deg) translateZ(${halfSize}px)` 
          }}
        />
        {/* Bottom */}
        <div 
          className="cube-face" 
          style={{ 
            border: `1px solid ${borderColor}`, 
            background: color, 
            transform: `rotateX(-90deg) translateZ(${halfSize}px)` 
          }}
        />
      </div>
    </div>
  );
}

export default function LandingPage() {
  const navigate = useNavigate();
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const [activeTextIndex, setActiveTextIndex] = useState(0);

  // Parallax mouse tilt effect
  useEffect(() => {
    const handleMouseMove = (e) => {
      const xVal = (e.clientX / window.innerWidth - 0.5) * 35; // max 17.5deg tilt
      const yVal = (e.clientY / window.innerHeight - 0.5) * -35;
      setTilt({ x: xVal, y: yVal });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Text animation slideshow for the dual-sided transaction thesis
  const phrases = [
    "Understands intent, finds it instantly.",
    "Buyers get matched with product plans.",
    "Sellers get analytics answers instantly."
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveTextIndex((prev) => (prev + 1) % phrases.length);
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative min-h-[calc(100vh-4rem)] w-full bg-transparent flex flex-col md:flex-row items-center justify-center px-6 md:px-16 lg:px-24 py-12 overflow-hidden select-none">
      
      {/* Visual background lines (Blueprint aesthetic) */}
      <div className="absolute inset-0 grid grid-cols-12 pointer-events-none opacity-[0.03] border-b border-white/10">
        {[...Array(12)].map((_, i) => (
          <div key={i} className="border-r border-white/10 h-full" />
        ))}
      </div>

      {/* Left Column: Thesis & Headline (60% width on md+) */}
      <div className="w-full md:w-1/2 flex flex-col justify-center space-y-8 z-10 text-left">
        {/* Wordmark logo */}
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-lg shadow-[0_0_15px_rgba(139,92,246,0.4)]">
            <Cpu className="w-4 h-4" />
          </div>
          <span className="font-bold text-xs uppercase tracking-widest text-zinc-300">
            CommerceOS
          </span>
        </div>

        {/* Dynamic alive Headline */}
        <div className="space-y-4">
          <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tighter text-white uppercase leading-none">
            Commerce <br />
            <span className="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">Connected.</span>
          </h1>
          <div className="h-12 overflow-hidden relative">
            {phrases.map((phrase, idx) => (
              <div
                key={idx}
                className="absolute inset-x-0 transition-all duration-700 ease-in-out text-sm sm:text-base lg:text-lg font-bold tracking-tight text-zinc-200 flex items-center gap-2"
                style={{
                  transform: `translateY(${(idx - activeTextIndex) * 100}%)`,
                  opacity: idx === activeTextIndex ? 1 : 0
                }}
              >
                <span className="h-1.5 w-1.5 rounded-full bg-violet-400 inline-block animate-pulse shadow-[0_0_8px_rgba(139,92,246,0.6)]" />
                {phrase}
              </div>
            ))}
          </div>
        </div>

        {/* Subhead */}
        <p className="text-sm lg:text-base text-zinc-400 max-w-md font-medium leading-relaxed">
          CommerceOS links both sides of the transaction. Buyers query natural intent to receive structured purchasing maps, while sellers query analytics to capture real-time demand alerts.
        </p>

        {/* CTA button */}
        <div>
          <button
            onClick={() => navigate('/login')}
            className="group px-7 py-4 rounded-full bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white border-2 border-transparent text-sm font-bold flex items-center gap-2.5 shadow-lg shadow-violet-500/20 hover:shadow-violet-500/30 transition-all duration-300 transform active:scale-95 cursor-pointer"
          >
            Get Started
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>

      {/* Right Column: 3D centerpiece (40% width on md+) */}
      <div className="w-full md:w-1/2 flex items-center justify-center mt-12 md:mt-0 relative h-[380px] lg:h-[480px]">
        {/* Outer Perspective Box */}
        <div className="w-full h-full flex items-center justify-center perspective-1000">
          
          {/* Parallax Rotate Wrapper */}
          <div 
            className="relative w-64 h-64 preserve-3d transition-transform duration-300 ease-out"
            style={{
              transform: `rotateX(${tilt.y}deg) rotateY(${tilt.x}deg)`,
              transformStyle: 'preserve-3d'
            }}
          >
            {/* Center Main Cube */}
            <FloatingCube 
              halfSize={64} 
              position="top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-float" 
              borderColor="rgba(10, 10, 10, 0.4)"
              color="rgba(10, 10, 10, 0.05)"
              delay="0s"
            />

            {/* Small Top-Right Cube */}
            <div 
              className="absolute preserve-3d animate-float" 
              style={{ 
                transform: 'translate3d(120px, -90px, 60px)', 
                animationDelay: '1s',
                transformStyle: 'preserve-3d'
              }}
            >
              <FloatingCube 
                halfSize={32} 
                borderColor="rgba(10, 10, 10, 0.25)"
                color="rgba(10, 10, 10, 0.02)"
                delay="-4s"
              />
            </div>

            {/* Small Bottom-Left Cube */}
            <div 
              className="absolute preserve-3d animate-float" 
              style={{ 
                transform: 'translate3d(-130px, 90px, -60px)', 
                animationDelay: '2s',
                transformStyle: 'preserve-3d'
              }}
            >
              <FloatingCube 
                halfSize={40} 
                borderColor="rgba(10, 10, 10, 0.3)"
                color="rgba(10, 10, 10, 0.03)"
                delay="-8s"
              />
            </div>
            
          </div>
        </div>
      </div>
      
    </div>
  );
}
