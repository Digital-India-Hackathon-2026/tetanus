import React, { useState, useEffect } from 'react';
import { Terminal } from 'lucide-react';

export default function AgentActivityLog({ isVisible }) {
  const logLines = [
    "[14:02] Recommendation Agent flagged dinosaur search query spike",
    "[14:03] Inventory Agent cross-checked warehouse stock status",
    "[14:05] Copilot compiled automated purchase reorder proposal"
  ];

  const [visibleLines, setVisibleLines] = useState([]);
  const [currentLineIdx, setCurrentLineIdx] = useState(-1);
  const [currentText, setCurrentText] = useState("");

  useEffect(() => {
    if (isVisible) {
      // Delay terminal print sequence until charts have loaded (3.2 seconds)
      const delayTimer = setTimeout(() => {
        setCurrentLineIdx(0);
      }, 3200);
      return () => clearTimeout(delayTimer);
    }
  }, [isVisible]);

  useEffect(() => {
    if (currentLineIdx < 0 || currentLineIdx >= logLines.length) return;

    let charIdx = 0;
    const fullText = logLines[currentLineIdx];
    setCurrentText("");

    const typingTimer = setInterval(() => {
      if (charIdx < fullText.length) {
        setCurrentText(prev => prev + fullText.charAt(charIdx));
        charIdx++;
      } else {
        clearInterval(typingTimer);
        setVisibleLines(prev => [...prev, fullText]);
        setCurrentText("");
        setCurrentLineIdx(prev => prev + 1);
      }
    }, 20); // 20ms typing tick

    return () => clearInterval(typingTimer);
  }, [currentLineIdx]);

  return (
    <div className={`border border-brand-border-dark rounded-2xl p-5 bg-white space-y-3.5 transition-all duration-700 transform ${
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-brand-border pb-2.5">
        <h3 className="text-xs font-bold text-brand-text tracking-widest uppercase flex items-center gap-1.5 leading-none">
          <Terminal className="w-4 h-4 text-brand-text" />
          Agent Activity Log
        </h3>
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider font-mono">Terminal Outputs</span>
      </div>

      {/* Terminal Block */}
      <div className="bg-black text-green-400 p-4 rounded-xl font-mono text-xs text-left h-28 overflow-y-auto space-y-1.5 shadow-inner">
        {visibleLines.map((line, idx) => (
          <div key={idx} className="leading-tight flex items-start gap-1">
            <span className="text-green-600 select-none">&gt;</span>
            <span>{line}</span>
          </div>
        ))}
        {currentLineIdx >= 0 && currentLineIdx < logLines.length && (
          <div className="leading-tight flex items-start gap-1">
            <span className="text-green-600 select-none">&gt;</span>
            <span>
              {currentText}
              <span className="inline-block w-1.5 h-3.5 bg-green-400 ml-0.5 animate-pulse" />
            </span>
          </div>
        )}
        {currentLineIdx === -1 && (
          <div className="text-slate-600 text-[10px] italic">
            Connecting to agent terminal sync loop...
          </div>
        )}
        {currentLineIdx === logLines.length && (
          <div className="leading-tight flex items-start gap-1 text-slate-500 animate-pulse text-[10px]">
            <span className="select-none">&gt;</span>
            <span>Terminal Idle. Ready for incoming signal streams.</span>
          </div>
        )}
      </div>
    </div>
  );
}
