import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Cpu, Mail, Lock, User, Briefcase, ArrowRight } from 'lucide-react';

function LoginBlock({ title, roleLabel, icon: Icon, onSubmit, buttonText }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) return;

    setLoading(true);
    onSubmit({ email, password, setSubmitting: setLoading });
  };

  const isFormValid = email.trim() !== "" && password.trim() !== "";

  return (
    <div className="border border-brand-border-dark bg-white rounded-3xl p-6 md:p-8 flex flex-col justify-between h-full hover:shadow-lg transition-all duration-300">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-brand-block-bg text-brand-block-text rounded-xl">
            <Icon className="w-5 h-5" />
          </div>
          <div className="text-left">
            <h3 className="font-bold text-brand-text text-lg uppercase tracking-tight leading-none">
              {title}
            </h3>
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mt-1">
              Access Terminal
            </span>
          </div>
        </div>

        {/* Inputs */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5 text-left">
            <label className="text-[10px] font-bold text-brand-text uppercase tracking-wider">
              Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-9 pr-4 py-2.5 bg-white border border-brand-border focus:border-brand-border-dark focus:ring-1 focus:ring-brand-border-dark rounded-xl text-xs font-semibold focus:outline-none transition-colors"
              />
              <Mail className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          <div className="space-y-1.5 text-left">
            <label className="text-[10px] font-bold text-brand-text uppercase tracking-wider">
              Password
            </label>
            <div className="relative">
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-4 py-2.5 bg-white border border-brand-border focus:border-brand-border-dark focus:ring-1 focus:ring-brand-border-dark rounded-xl text-xs font-semibold focus:outline-none transition-colors"
              />
              <Lock className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          {/* Progress loader or submit button */}
          <div className="pt-2">
            {loading ? (
              <div className="space-y-2 py-2">
                <span className="text-[9px] font-extrabold text-slate-500 uppercase tracking-widest block text-center animate-pulse">
                  Authenticating {roleLabel}...
                </span>
                <div className="w-full h-1 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-brand-block-bg animate-progress rounded-full" />
                </div>
              </div>
            ) : (
              <button
                type="submit"
                disabled={!isFormValid}
                className="w-full py-3 rounded-xl bg-brand-block-bg hover:bg-white text-white hover:text-brand-text border border-brand-block-bg hover:border-brand-border-dark text-xs font-extrabold flex items-center justify-center gap-1.5 transition-all disabled:opacity-30 disabled:hover:bg-brand-block-bg disabled:hover:text-white disabled:hover:border-brand-block-bg cursor-pointer"
              >
                {buttonText}
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}

export default function LoginPage() {
  const navigate = useNavigate();

  const handleLoginSubmit = ({ email, password, setSubmitting }, role) => {
    localStorage.setItem('cos_user_role', role);
    localStorage.setItem('cos_user_email', email);
    localStorage.setItem('cos_user_name', email.split('@')[0]);

    // Simulated short authentication bar (<1s)
    setTimeout(() => {
      setSubmitting(false);
      
      // Redirect directly to view based on login card clicked
      const targetPath = role === 'seller' ? '/seller' : '/consumer';
      navigate(targetPath);
    }, 750);
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] w-full bg-white flex flex-col items-center justify-center px-4 py-8 relative">
      
      {/* Background grids */}
      <div className="absolute inset-0 grid grid-cols-12 pointer-events-none opacity-[0.02] border-b border-brand-text/10">
        {[...Array(12)].map((_, i) => (
          <div key={i} className="border-r border-brand-text h-full" />
        ))}
      </div>

      <div className="w-full max-w-4xl space-y-8 z-10 text-center">
        
        {/* Header Block */}
        <div className="space-y-3">
          <div className="inline-flex p-3 bg-brand-block-bg text-brand-block-text rounded-2xl">
            <Cpu className="w-6 h-6 animate-pulse" />
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight text-brand-text uppercase leading-none">
            CommerceOS Gate
          </h2>
          <p className="text-xs text-slate-500 font-semibold max-w-md mx-auto leading-relaxed">
            Select your role terminal to authorize connection. Whichever channel you access directly specifies your workspace authorization.
          </p>
        </div>

        {/* Side-by-side Dual Login Panels */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch max-w-3xl mx-auto">
          
          {/* Customer Panel */}
          <LoginBlock 
            title="Customer Terminal"
            roleLabel="customer"
            icon={User}
            buttonText="Access Marketplace"
            onSubmit={(data) => handleLoginSubmit(data, 'customer')}
          />

          {/* Seller Panel */}
          <LoginBlock 
            title="Seller Copilot"
            roleLabel="seller"
            icon={Briefcase}
            buttonText="Access Dashboard"
            onSubmit={(data) => handleLoginSubmit(data, 'seller')}
          />

        </div>

      </div>

    </div>
  );
}
