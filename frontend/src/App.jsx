import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import { LogOut, RefreshCw, Layers } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import ConsumerView from './pages/ConsumerView';
import SellerView from './pages/SellerView';
import { resetDemoState } from './services/api';

function NavigationHeader() {
  const location = useLocation();
  const currentPath = location.pathname;

  if (currentPath === '/' || currentPath === '/login') {
    return null;
  }

  const handleReset = () => {
    resetDemoState();
    window.location.reload();
  };

  const isSellerView = currentPath === '/seller';
  const roleLabel = isSellerView ? "Seller" : "Consumer";

  return (
    <motion.header 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      className="sticky top-0 z-50 bg-[#F8F7F5]/80 backdrop-blur-xl border-b border-black/5"
    >
      <div className="max-w-[1400px] mx-auto px-6 h-20 flex items-center justify-between">
        
        {/* Minimal Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 bg-[#171717] rounded-full flex items-center justify-center">
            <Layers className="w-4 h-4 text-white" />
          </div>
          <span className="font-medium text-lg tracking-tight text-[#171717]">
            CIN.
          </span>
        </Link>

        {/* Actions */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-[#6F6F73]">Active Mode:</span>
            <span className="text-sm font-semibold text-[#171717]">{roleLabel}</span>
          </div>

          <div className="h-4 w-px bg-black/10"></div>

          <button
            onClick={handleReset}
            className="flex items-center gap-2 text-sm font-medium text-[#6F6F73] hover:text-[#171717] transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Reset Demo</span>
          </button>

          <Link
            to="/login"
            onClick={() => localStorage.clear()}
            className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#171717] text-white text-sm font-medium hover:bg-black transition-transform hover:scale-105 active:scale-95"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </Link>
        </div>

      </div>
    </motion.header>
  );
}

function Footer() {
  const location = useLocation();
  const currentPath = location.pathname;

  if (currentPath === '/') return null;

  return (
    <footer className="py-12 mt-auto border-t border-black/5">
      <div className="max-w-[1400px] mx-auto px-6 flex items-center justify-between">
        <div className="flex items-center gap-2 text-[#6F6F73] text-sm">
          <Layers className="w-4 h-4" />
          <span>Commerce Intelligence Network</span>
        </div>
        <p className="text-[#6F6F73] text-sm">
          Running AI Loop
        </p>
      </div>
    </footer>
  );
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col justify-between selection:bg-[#8B5CF6]/20 selection:text-[#8B5CF6]">
        <div className="flex-1 flex flex-col">
          <NavigationHeader />
          <main className="flex-1 flex flex-col">
            <AnimatePresence mode="wait">
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/consumer" element={<ConsumerView />} />
                <Route path="/seller" element={<SellerView />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AnimatePresence>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
}
