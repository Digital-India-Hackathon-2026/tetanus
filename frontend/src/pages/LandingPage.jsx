import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { User, Package, Warehouse, Box, Route, Archive, Gift, Shirt, Coffee, Headphones, Book, Camera, Watch, Layers } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();
  const containerRef = useRef(null);
  
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  const yUnderstand = useTransform(scrollYProgress, [0, 1], [300, -200]);
  const yThe = useTransform(scrollYProgress, [0, 1], [400, -300]);
  const yMission = useTransform(scrollYProgress, [0, 1], [500, -400]);
  const heroParallax = useTransform(scrollYProgress, [0, 1], [0, -100]);

  return (
    <div ref={containerRef} className="w-full bg-[#F5F6F8] text-[#252525] overflow-hidden relative font-sans selection:bg-[#D8E7FF]">
      
      {/* Header / Nav */}
      <div className="fixed top-6 left-8 z-50">
        <div className="flex items-center justify-center w-12 h-12 bg-[#252525] text-white text-[11px] font-bold tracking-widest" style={{ clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)' }}>
          CIN
        </div>
      </div>

      <nav className="fixed top-6 left-1/2 -translate-x-1/2 bg-white/95 backdrop-blur-md px-10 py-[12px] rounded-[30px] shadow-sm flex gap-8 z-50 text-[13px] font-medium text-[#252525]">
        <button onClick={() => navigate('/')} className="hover:opacity-60 transition-opacity">Values</button>
        <button onClick={() => navigate('/login')} className="hover:opacity-60 transition-opacity">Projects</button>
        <button onClick={() => navigate('/login')} className="hover:opacity-60 transition-opacity">History</button>
        <button onClick={() => navigate('/login')} className="hover:opacity-60 transition-opacity">Community</button>
      </nav>

      <div className="fixed top-6 right-8 z-50">
        <button onClick={() => navigate('/login')} className="bg-[#252525] text-white px-6 py-[12px] rounded-[30px] text-[13px] font-medium hover:bg-black transition-colors">
          Contact Us
        </button>
      </div>

      {/* Hero Section - 100% FROZEN */}
      <section className="min-h-screen w-full relative z-10 pt-[15vh] pb-[10vh] px-8 flex flex-col justify-center">
        
        {/* Sculpted Organic Background */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#ffffff] via-[#F5F6F8] to-[#F5F6F8] opacity-60 pointer-events-none z-0" />
        
        <motion.svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" className="absolute top-[-15%] left-[-15%] w-[45vw] min-w-[500px] h-auto z-0 opacity-90 pointer-events-none" animate={{ rotate: [0, 5, 0], scale: [1, 1.02, 1] }} transition={{ duration: 30, repeat: Infinity, ease: "easeInOut" }}>
          <defs>
            <radialGradient id="gradTopLeft" cx="30%" cy="30%" r="70%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
              <stop offset="40%" stopColor="#e8eaf6" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#d4d9ea" stopOpacity="0.4" />
            </radialGradient>
          </defs>
          <path fill="url(#gradTopLeft)" d="M48.8,-74.6C62.1,-67.2,71,-51.6,76.5,-35.1C82.1,-18.6,84.4,-1.2,80.7,14.6C77,30.4,67.3,44.6,54.5,55.1C41.7,65.6,25.8,72.4,9.4,75.4C-7,78.4,-23.9,77.6,-38.3,69.9C-52.7,62.2,-64.5,47.6,-73,31.3C-81.5,15,-86.6,-3.1,-82.1,-19.2C-77.6,-35.3,-63.5,-49.4,-48.1,-56.3C-32.7,-63.2,-16.3,-62.9,1.1,-64.4C18.5,-65.9,35.5,-82,48.8,-74.6Z" transform="translate(100 100) scale(1.1)"/>
        </motion.svg>

        <motion.svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" className="absolute bottom-[-10%] right-[-5%] w-[40vw] min-w-[450px] h-auto z-0 opacity-80 pointer-events-none" animate={{ rotate: [0, -5, 0], scale: [1, 1.03, 1] }} transition={{ duration: 35, repeat: Infinity, ease: "easeInOut" }}>
          <defs>
            <radialGradient id="gradBottomRight" cx="70%" cy="30%" r="70%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
              <stop offset="40%" stopColor="#f0eef6" stopOpacity="0.7" />
              <stop offset="100%" stopColor="#e2dcf2" stopOpacity="0.3" />
            </radialGradient>
          </defs>
          <path fill="url(#gradBottomRight)" d="M43.1,-58.5C54.8,-46.8,62.5,-30.9,67.6,-13.6C72.7,3.7,75.3,22.4,67.1,36.5C58.9,50.6,39.9,60.1,22.2,64.3C4.5,68.5,-12,67.4,-27.1,60.8C-42.2,54.2,-55.9,42.1,-65.1,26.5C-74.3,10.9,-79,-8.3,-73.4,-24.1C-67.8,-39.9,-51.9,-52.3,-36.5,-61.6C-21.1,-70.9,-6.2,-77.1,7.2,-73C20.6,-68.9,31.4,-70.2,43.1,-58.5Z" transform="translate(100 100) scale(1.2)"/>
        </motion.svg>

        {/* Giant Background Word */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 0.12, y: 0 }}
          transition={{ duration: 2, ease: "easeOut" }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-0 pointer-events-none w-full text-center"
        >
          <h1 className="text-[16vw] font-black text-[#111111] leading-none tracking-tighter mix-blend-multiply">CONNECTED</h1>
        </motion.div>

        {/* Exact Layout Container */}
        <motion.div style={{ y: heroParallax }} className="w-full max-w-[1500px] mx-auto relative z-10 flex flex-col gap-2">
          
          {/* Row 1: Commerce */}
          <div className="relative w-full">
            <div className="w-fit relative ml-[36%]">
              <div className="absolute bottom-[90%] right-[10%] text-[14px] font-serif text-[#4F4F4F] whitespace-nowrap">
                Natural language
              </div>
              <h1 className="text-[10vw] font-medium text-[#252525] leading-[0.95] tracking-tighter">Commerce</h1>
            </div>
          </div>

          {/* Row 2: understands */}
          <div className="relative w-full">
            <div className="w-fit relative ml-[5%]">
              <div className="absolute bottom-[95%] left-[25%] text-[14px] font-serif text-[#4F4F4F] whitespace-nowrap">
                AI reasoning
              </div>
              <h1 className="text-[10vw] font-medium text-[#252525] leading-[0.95] tracking-tighter">understands</h1>
            </div>
          </div>

          {/* Row 3: Intent + Paragraph */}
          <div className="relative w-full">
            <div className="w-fit relative ml-[34%]">
              <div className="absolute bottom-[95%] left-[5%] text-[14px] font-serif text-[#4F4F4F] whitespace-nowrap">
                Graph mapping
              </div>
              <h1 className="text-[10vw] font-medium text-[#252525] leading-[0.95] tracking-tighter">Intent</h1>
            </div>
            
            {/* Paragraph */}
            <div className="absolute right-[8%] top-[20%] max-w-[320px] hidden lg:block">
              <p className="text-[15px] leading-[1.6] text-[#4F4F4F] font-normal text-left tracking-tight">
                Rethinking how users interact with commerce to prioritise exact intent. A visionary new AI platform, generating curated carts dynamically to support frictionless discovery.
              </p>
            </div>
          </div>

          {/* Row 4: without */}
          <div className="relative w-full">
            <div className="w-fit relative ml-[45%]">
              <div className="absolute bottom-[95%] left-[8%] text-[14px] font-serif text-[#4F4F4F] whitespace-nowrap">
                Context aware
              </div>
              <h1 className="text-[8.5vw] font-light italic text-[#4F4F4F] leading-[0.95] tracking-tighter">without</h1>
            </div>
          </div>

          {/* Row 5: search */}
          <div className="relative w-full">
            <div className="w-fit relative ml-[60%]">
              <h1 className="text-[10vw] font-medium text-[rgba(37,37,37,0.12)] leading-[0.95] tracking-tighter mix-blend-multiply">search</h1>
            </div>
          </div>

        </motion.div>
      </section>

      {/* SECTION 2 (Manifesto) - 100% FROZEN */}
      <div className="relative w-full overflow-hidden">
        
        {/* The Animated Knowledge Graph Background */}
        <div className="absolute inset-0 z-0 pointer-events-none opacity-[0.06] hidden md:block mt-[20vh]">
          <svg viewBox="0 0 1000 1000" preserveAspectRatio="none" className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
            <motion.path d="M 100,200 Q 300,500 500,400 T 900,700" stroke="#111111" strokeWidth="3" fill="none" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 4, repeat: Infinity, ease: "linear" }} />
            <motion.path d="M 200,800 Q 400,600 600,800 T 800,300" stroke="#111111" strokeWidth="3" fill="none" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 5, repeat: Infinity, ease: "linear" }} />
            <motion.path d="M 100,200 L 200,800 M 500,400 L 800,300 M 900,700 L 800,300" stroke="#111111" strokeWidth="1" strokeDasharray="5,5" fill="none" opacity="0.5" />
          </svg>
          
          <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 4, repeat: Infinity }} className="absolute left-[10%] top-[20%] -translate-x-1/2 -translate-y-1/2 bg-[#F5F6F8] p-2 rounded-full">
            <User size={32} className="text-[#111111]" strokeWidth={1.5} />
          </motion.div>
          <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 4, delay: 1, repeat: Infinity }} className="absolute left-[50%] top-[40%] -translate-x-1/2 -translate-y-1/2 bg-[#F5F6F8] p-2 rounded-full">
            <Warehouse size={32} className="text-[#111111]" strokeWidth={1.5} />
          </motion.div>
          <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 4, delay: 2, repeat: Infinity }} className="absolute left-[90%] top-[70%] -translate-x-1/2 -translate-y-1/2 bg-[#F5F6F8] p-2 rounded-full">
            <Package size={32} className="text-[#111111]" strokeWidth={1.5} />
          </motion.div>
          <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 4, delay: 1.5, repeat: Infinity }} className="absolute left-[20%] top-[80%] -translate-x-1/2 -translate-y-1/2 bg-[#F5F6F8] p-2 rounded-full">
            <Box size={32} className="text-[#111111]" strokeWidth={1.5} />
          </motion.div>
          <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 4, delay: 2.5, repeat: Infinity }} className="absolute left-[80%] top-[30%] -translate-x-1/2 -translate-y-1/2 bg-[#F5F6F8] p-2 rounded-full">
            <Route size={32} className="text-[#111111]" strokeWidth={1.5} />
          </motion.div>
        </div>

        <section className="min-h-[180vh] w-full relative z-10 mt-32">
          <div className="w-full relative h-full flex flex-col justify-center">
            <motion.h2 style={{ y: yUnderstand }} className="text-[9vw] leading-[0.85] font-light tracking-tighter uppercase text-right pr-[8%] mb-[4vh] text-[rgba(0,0,0,0.28)]">Understand</motion.h2>
            <motion.h2 style={{ y: yThe }} className="text-[10vw] leading-[0.85] font-medium tracking-tighter uppercase text-right pr-[15%] mb-[4vh]">The</motion.h2>
            <motion.h2 style={{ y: yMission }} className="text-[11vw] leading-[0.85] font-extrabold tracking-tighter uppercase text-right pr-[5%]">Mission.</motion.h2>

            <div className="absolute top-[60vh] left-[8%] space-y-6 md:space-y-10 text-[6vw] md:text-[5vw] font-medium tracking-tighter leading-none">
              {['Products.', 'Warehouses.', 'Customers.', 'Connected.'].map((word, i) => (
                <motion.div key={word} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: "-10%" }} transition={{ delay: i * 0.15, duration: 1, ease: [0.16, 1, 0.3, 1] }} className={i === 3 ? "text-[#111111] mt-8" : "text-[#4F4F4F]"}>
                  {word}
                </motion.div>
              ))}
            </div>

            <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true, margin: "-20%" }} className="absolute bottom-[20vh] right-[5%] text-[10px] font-bold uppercase tracking-[0.25em] text-[#4F4F4F] max-w-[220px] text-right leading-relaxed">
              [ 02 ] <br /><br />
              Graph Intelligence mapping relationships across the entire commerce ecosystem in real-time.
            </motion.div>
          </div>
        </section>

        {/* SECTION 3 (CIN Assembles) - Massive AI Glass Orb Installation */}
        <section className="min-h-screen w-full relative z-20 flex flex-col justify-center pb-[15vh] pt-[15vh] overflow-hidden">
          
          <div className="w-full relative flex flex-col items-start justify-center min-h-[800px] pointer-events-none">
            
            {/* Massive Installation Visual (Absolute and extending across the screen) */}
            <div className="absolute top-1/2 -translate-y-1/2 left-0 right-0 h-[1000px] w-full min-w-[1500px] z-10">
              
              {/* Background Cloud Gradients (Scaled up) */}
              <div className="absolute inset-0 z-0 opacity-[0.25] overflow-visible">
                <motion.div 
                  animate={{ x: [0, 40, 0], y: [0, -60, 0] }} 
                  transition={{ duration: 25, repeat: Infinity, ease: "easeInOut" }}
                  className="absolute top-[10%] left-[30%] w-[600px] h-[600px] bg-[#DCE8FF] rounded-full blur-[120px] mix-blend-multiply" 
                />
                <motion.div 
                  animate={{ x: [0, -40, 0], y: [0, 60, 0] }} 
                  transition={{ duration: 28, repeat: Infinity, ease: "easeInOut" }}
                  className="absolute bottom-[10%] right-[10%] w-[500px] h-[500px] bg-[#E7DFFF] rounded-full blur-[140px] mix-blend-multiply" 
                />
              </div>

              {/* The Glass Orb Sequence Container */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1500px] h-[1000px]">
                
                {/* 1. The Elegant Curved SVG Path */}
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 1500 1000">
                  <motion.path 
                    d="M 200 450 Q 800 -50 1200 550" 
                    stroke="rgba(0,0,0,0.06)" 
                    strokeWidth="1.5" 
                    fill="none" 
                    strokeLinecap="round"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 5, ease: "easeInOut", repeat: Infinity, repeatDelay: 10 }}
                  />
                </svg>

                {/* 2. Floating Minimal Product Glyphs travelling the path */}
                {[
                  { Icon: Shirt, delay: 0 },
                  { Icon: Coffee, delay: 0.8 },
                  { Icon: Headphones, delay: 1.6 },
                  { Icon: Book, delay: 2.4 },
                  { Icon: Camera, delay: 3.2 },
                  { Icon: Watch, delay: 4.0 }
                ].map((item, i) => (
                  <motion.div
                    key={i}
                    className="absolute text-[#888888] z-20"
                    animate={{ 
                      left: [200, 487.5, 750, 987.5, 1200], 
                      top: [450, 268.75, 225, 318.75, 550], 
                      opacity: [0, 1, 1, 1, 0], 
                      scale: [0.6, 0.9, 0.9, 0.9, 0.3],
                    }}
                    transition={{ 
                      duration: 5, 
                      delay: item.delay,
                      repeat: Infinity, 
                      repeatDelay: 10, // 5s active + 10s delay = 15s total loop
                      ease: "easeInOut" 
                    }}
                  >
                    <div className="absolute -translate-x-1/2 -translate-y-1/2">
                      <item.Icon size={24} strokeWidth={1} />
                    </div>
                  </motion.div>
                ))}

                {/* 3. The Central Frosted Glass Orb */}
                <div className="absolute left-[1200px] top-[550px] -translate-x-1/2 -translate-y-1/2 z-30">
                  <motion.div 
                    className="w-56 h-56 rounded-full backdrop-blur-xl bg-white/30 border border-white/60 flex items-center justify-center relative overflow-hidden"
                    animate={{ 
                      boxShadow: [
                        "0px 8px 32px rgba(0,0,0,0.02)", 
                        "0px 8px 32px rgba(0,0,0,0.02)", 
                        "0px 8px 32px rgba(0,0,0,0.02)", 
                        "0px 30px 60px rgba(0,0,0,0.15)", 
                        "0px 8px 32px rgba(0,0,0,0.02)"
                      ]
                    }}
                    transition={{ duration: 15, times: [0, 0.5, 0.6, 0.75, 1], repeat: Infinity, ease: "easeInOut" }}
                  >
                    {/* Inner highlight for premium glass effect */}
                    <div className="absolute inset-0 bg-gradient-to-tr from-white/10 to-white/40 rounded-full" />
                    
                    {/* Inside Orb: The final clean "Mission Bundle" package */}
                    <motion.div
                      className="text-[#111111] z-10"
                      animate={{ opacity: [0, 0, 0, 1, 1, 0, 0], scale: [0.8, 0.8, 0.8, 1, 1, 0.8, 0.8] }}
                      transition={{ duration: 15, times: [0, 0.5, 0.6, 0.65, 0.85, 0.9, 1], repeat: Infinity, ease: "easeInOut" }}
                    >
                      <Package size={48} strokeWidth={1.2} />
                    </motion.div>
                  </motion.div>
                </div>
              </div>
            </div>

            {/* Left Side: Typography (Overlaps the animation canvas) */}
            <div className="w-full lg:w-1/2 flex flex-col relative z-40 pointer-events-auto pl-[10%]">
              <div className="text-[2vw] leading-[1.2] font-medium tracking-widest uppercase text-[#888888] mb-[8vh]">
                We Do Not <br />
                Browse <br />
                Anymore.
              </div>
              
              <div className="text-[4.8vw] leading-[1.3] tracking-tighter uppercase text-[#111111] py-[4vh] flex flex-col gap-6">
                <span className="font-medium text-[#4F4F4F]">CIN</span>
                <span className="font-medium text-[#4F4F4F]">Assembles</span>
                <span className="font-medium text-[#4F4F4F]">The Perfect</span>
                <span className="font-black text-[#111111]">Cart.</span>
              </div>
            </div>

          </div>

          {/* Horizontal Intelligence Timeline Sequence */}
          <div className="w-full mt-[10vh] px-[10%] flex flex-wrap items-center justify-start gap-4 md:gap-8 overflow-hidden pt-16 border-t border-[rgba(0,0,0,0.05)]">
            {['Mission', 'Understanding', 'Knowledge Graph', 'Reasoning', 'Bundle', 'Checkout'].map((step, i) => (
              <React.Fragment key={step}>
                <motion.div 
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, margin: "-10%" }}
                  transition={{ delay: i * 0.15, duration: 1.2, ease: "easeOut" }}
                  className="text-[11px] md:text-[13px] uppercase tracking-widest font-serif text-[#4F4F4F]"
                >
                  {step}
                </motion.div>
                {i < 5 && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 0.2 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.15 + 0.1, duration: 1 }}
                    className="text-[#111111]"
                  >
                    →
                  </motion.div>
                )}
              </React.Fragment>
            ))}
          </div>

        </section>

      </div>
    </div>
  );
}
