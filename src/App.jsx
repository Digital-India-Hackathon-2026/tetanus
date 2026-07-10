import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import { LogOut, Cpu, Layers, RefreshCw, User, Briefcase } from 'lucide-react';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import ConsumerView from './pages/ConsumerView';
import SellerView from './pages/SellerView';
import { resetDemoState } from './services/api';

function NavigationHeader() {
  const location = useLocation();
  const currentPath = location.pathname;

  // Hide header on Landing page and Login page
  if (currentPath === '/' || currentPath === '/login') {
    return null;
  }

  const handleReset = () => {
    resetDemoState();
    window.location.reload();
  };

  const isSellerView = currentPath === '/seller';
  const roleLabel = isSellerView ? "Seller Copilot" : "Customer";
  const RoleIcon = isSellerView ? Briefcase : User;

  return (
    <header className="border-b border-amber-500/10 bg-[#fcfbfa]/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo / Wordmark */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="p-1.5 bg-amber-600 text-white rounded-lg">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-sm tracking-tight text-brand-text uppercase">
                CommerceOS
              </span>
              <span className="h-1.5 w-1.5 rounded-full bg-amber-600 animate-pulse" title="Connected" />
            </div>
            <span className="text-[9px] font-bold text-slate-400 tracking-wider uppercase block leading-none mt-0.5">
              Platform Terminal
            </span>
          </div>
        </Link>

        {/* Active Role Label & Sign Out */}
        <div className="flex items-center gap-3.5">
          {/* Static Active Role Indicator (No Toggle) */}
          <div className="flex items-center gap-2 px-3 py-1.5 border border-amber-500/10 bg-amber-500/5 rounded-xl">
            <div className="p-1 bg-amber-600 text-white rounded-lg">
              <RoleIcon className="w-3.5 h-3.5" />
            </div>
            <div className="text-left">
              <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block leading-none">Active Role</span>
              <span className="text-xs font-black text-brand-text block mt-0.5">{roleLabel}</span>
            </div>
          </div>

          {/* Reset Demo Button */}
          <button
            onClick={handleReset}
            className="flex items-center gap-1 px-3 py-2 rounded-xl border border-amber-500/10 text-slate-600 hover:text-amber-700 hover:border-amber-500/30 transition-all text-xs font-semibold cursor-pointer"
            title="Reset Demo State"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Reset</span>
          </button>

          {/* Log Out Link */}
          <Link
            to="/login"
            onClick={() => {
              localStorage.clear();
            }}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-amber-600 hover:bg-amber-750 text-white text-xs font-bold transition-all"
            title="Log Out"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Sign Out</span>
          </Link>
        </div>

      </div>
    </header>
  );
}

function Footer() {
  const location = useLocation();
  const currentPath = location.pathname;

  // Hide footer on Landing page to keep it clean and single-screen
  if (currentPath === '/') {
    return null;
  }

  return (
    <footer className="border-t border-amber-500/10 py-8 bg-[#fcfbfa]/50 mt-auto">
      <div className="max-w-7xl mx-auto px-4 text-center space-y-2">
        <div className="flex items-center justify-center gap-2 text-slate-500 text-xs font-medium">
          <Layers className="w-4 h-4 text-brand-text" />
          CommerceOS v1.0 • System Terminal
        </div>
        <p className="text-[10px] text-slate-400 font-semibold tracking-wider uppercase">
          Decentralized Purchase & Inventory Loop Running
        </p>
      </div>
    </footer>
  );
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-transparent flex flex-col justify-between">
        <div>
          <NavigationHeader />
          <main>
            <Routes>
              {/* Landing Page */}
              <Route path="/" element={<LandingPage />} />
              
              {/* Login Page */}
              <Route path="/login" element={<LoginPage />} />
              
              {/* Consumer View */}
              <Route path="/consumer" element={<ConsumerView />} />
              
              {/* Seller View */}
              <Route path="/seller" element={<SellerView />} />
              
              {/* Fallback to Landing */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
}
