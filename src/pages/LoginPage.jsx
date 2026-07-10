import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layers, Mail, Lock, User, Briefcase, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

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
    <div className="bg-white rounded-3xl p-8 border border-black/5 shadow-xl shadow-black/[0.02] flex flex-col justify-between h-full hover:shadow-2xl hover:shadow-black/[0.04] transition-shadow duration-500">
      <div className="space-y-8">
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="p-3 bg-[#F2F1EE] text-[#171717] rounded-2xl">
            <Icon className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-medium text-[#171717] text-lg tracking-tight">
              {title}
            </h3>
            <span className="text-sm text-[#6F6F73] mt-1 block">
              Access {roleLabel} workspace
            </span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2 text-left">
            <label className="text-xs font-semibold text-[#6F6F73] uppercase tracking-widest">
              Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-10 pr-4 py-3 bg-[#F8F7F5] border border-transparent focus:border-black/10 focus:bg-white focus:ring-1 focus:ring-black/5 rounded-xl text-sm font-medium focus:outline-none text-[#171717] transition-all"
              />
              <Mail className="w-4 h-4 text-[#6F6F73] absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          <div className="space-y-2 text-left">
            <label className="text-xs font-semibold text-[#6F6F73] uppercase tracking-widest">
              Password
            </label>
            <div className="relative">
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-3 bg-[#F8F7F5] border border-transparent focus:border-black/10 focus:bg-white focus:ring-1 focus:ring-black/5 rounded-xl text-sm font-medium focus:outline-none text-[#171717] transition-all"
              />
              <Lock className="w-4 h-4 text-[#6F6F73] absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={!isFormValid || loading}
              className="w-full py-3.5 rounded-xl bg-[#171717] hover:bg-black text-white text-sm font-medium flex items-center justify-center gap-2 transition-all disabled:opacity-30 active:scale-[0.98]"
            >
              {loading ? (
                <div className="w-4 h-4 rounded-full border-2 border-white/20 border-t-white animate-spin" />
              ) : (
                <>
                  {buttonText}
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
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

    setTimeout(() => {
      setSubmitting(false);
      const targetPath = role === 'seller' ? '/seller' : '/consumer';
      navigate(targetPath);
    }, 600);
  };

  return (
    <div className="min-h-screen w-full bg-[#F8F7F5] flex flex-col items-center justify-center px-6 py-12 relative overflow-hidden selection:bg-[#8B5CF6]/20 selection:text-[#8B5CF6]">
      
      {/* Background Ornaments */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-b from-[#8B5CF6]/5 to-transparent blur-3xl pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-4xl z-10 text-center space-y-12"
      >
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 bg-[#171717] rounded-full flex items-center justify-center shadow-lg">
            <Layers className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-3xl font-medium tracking-tight text-[#171717]">
            Select Workspace
          </h2>
          <p className="text-[#6F6F73] text-lg max-w-md mx-auto">
            Authorize access to the commerce network.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch max-w-3xl mx-auto">
          <LoginBlock 
            title="Consumer Terminal"
            roleLabel="customer"
            icon={User}
            buttonText="Enter Network"
            onSubmit={(data) => handleLoginSubmit(data, 'customer')}
          />
          <LoginBlock 
            title="Seller Copilot"
            roleLabel="seller"
            icon={Briefcase}
            buttonText="Access Analytics"
            onSubmit={(data) => handleLoginSubmit(data, 'seller')}
          />
        </div>
      </motion.div>
    </div>
  );
}
