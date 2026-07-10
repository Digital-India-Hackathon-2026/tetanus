import React, { useState, useEffect } from 'react';
import { Search, Info, Package, Star, ShoppingBag, BrainCircuit } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { postIntent } from '../services/api';
import MoneyLeftCard from '../components/MoneyLeftCard';

export default function ConsumerView() {
  const defaultQuery = "Birthday gift for a 10-year-old who loves dinosaurs, budget ₹1500";
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadingStatus, setLoadingStatus] = useState("Extracting intent...");
  const [results, setResults] = useState(null);
  const [failedImages, setFailedImages] = useState({});
  
  const [nearbyProducts, setNearbyProducts] = useState([]);
  const [nearbyLoading, setNearbyLoading] = useState(true);

  const quickSelectChips = [
    { label: "Dinosaur Gift (₹1500)", text: "Birthday gift for a 10-year-old who loves dinosaurs, budget ₹1500" },
    { label: "Developer Desk", text: "Smart coffee mug for developer workspace, budget ₹4000" },
    { label: "Workout Gear", text: "Cozy running shoes under ₹5000" }
  ];

  const handleImageError = (id) => setFailedImages(prev => ({ ...prev, [id]: true }));

  useEffect(() => {
    const fetchNearbyProducts = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
        const response = await fetch(`${apiUrl}/api/products/nearby`);
        if (!response.ok) throw new Error("Failed");
        const data = await response.json();
        setNearbyProducts(data.products || []);
      } catch (err) {
        setNearbyProducts([]);
      } finally {
        setNearbyLoading(false);
      }
    };
    fetchNearbyProducts();
  }, []);

  const handleSearchSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResults(null);
    setError(null);
    setLoadingStatus("Extracting intent...");

    const statusInterval = setInterval(() => {
      setLoadingStatus(prev => prev === "Extracting intent..." ? "Querying graph..." : "Assembling bundle...");
    }, 800);

    try {
      const data = await postIntent(query);
      if (!data) throw new Error("Invalid response received from the backend.");
      setResults(data);
    } catch (err) {
      setError(err.message || "Failed to process your request. Ensure backend is running.");
    } finally {
      clearInterval(statusInterval);
      setLoading(false);
    }
  };

  return (
    <div className="w-full bg-[#F8F7F5] min-h-screen text-[#171717] pb-32">
      
      {/* 1. HERO SEARCH AREA */}
      <section className="pt-24 pb-12 px-6">
        <div className="max-w-[800px] mx-auto text-center space-y-12">
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            <h1 className="text-4xl md:text-5xl tracking-tight font-medium">
              What is your mission?
            </h1>
            <p className="text-[#6F6F73] text-lg font-light">
              Describe your goal naturally. CIN handles the rest.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="w-full"
          >
            <form onSubmit={handleSearchSubmit} className="relative group">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. Birthday gift for a 10-year-old who loves dinosaurs..."
                className="w-full bg-white border border-black/5 shadow-xl shadow-black/[0.03] rounded-3xl py-6 pl-8 pr-20 text-lg md:text-xl font-medium focus:outline-none focus:ring-1 focus:ring-black/10 transition-all placeholder-[#6F6F73]/50"
              />
              <button
                type="submit"
                className="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-[#171717] text-white rounded-2xl flex items-center justify-center hover:bg-black transition-transform hover:scale-105"
              >
                <Search className="w-5 h-5" />
              </button>
            </form>
            
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              {quickSelectChips.map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => setQuery(chip.text)}
                  className="px-5 py-2 rounded-full border border-black/5 bg-white/50 hover:bg-white text-sm font-medium text-[#6F6F73] hover:text-[#171717] transition-all"
                >
                  {chip.label}
                </button>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* 2. LOADING STATE */}
      <AnimatePresence>
        {loading && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="max-w-[600px] mx-auto py-12 flex flex-col items-center gap-6"
          >
            <div className="w-16 h-16 rounded-2xl bg-white border border-black/5 shadow-2xl shadow-black/5 flex items-center justify-center relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-[#8B5CF6]/20 to-[#D946EF]/20 animate-pulse" />
              <BrainCircuit className="w-6 h-6 text-[#171717] animate-bounce" />
            </div>
            <span className="text-sm tracking-widest uppercase font-medium text-[#6F6F73] animate-pulse">
              {loadingStatus}
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 3. ERROR STATE */}
      {error && !loading && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="max-w-[800px] mx-auto mt-12 p-6 bg-red-50 border border-red-100 rounded-3xl text-center text-red-600"
        >
          {error}
        </motion.div>
      )}

      {/* 4. RESULTS VIEW */}
      {!loading && results && !error && (
        <div className="max-w-[1200px] mx-auto px-6 mt-12 space-y-12">
          
          {/* Agent Windows (Intent & Reasoning) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="luxury-card p-8 flex flex-col gap-6"
            >
              <div className="flex items-center gap-2">
                <Info className="w-5 h-5 text-[#8B5CF6]" />
                <h3 className="text-sm uppercase tracking-widest font-semibold text-[#171717]">Extracted Intent</h3>
              </div>
              <div className="flex flex-wrap gap-3">
                {Object.entries(results.intent || {}).map(([key, val]) => (
                  <div key={key} className="px-4 py-2 rounded-xl bg-white/60 border border-black/5 text-sm">
                    <span className="text-[#6F6F73] mr-2 capitalize">{key}:</span>
                    <span className="font-medium text-[#171717]">{val}</span>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="luxury-card p-8 flex flex-col gap-6"
            >
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-5 h-5 text-[#D946EF]" />
                <h3 className="text-sm uppercase tracking-widest font-semibold text-[#171717]">Copilot Reasoning</h3>
              </div>
              <p className="text-[#171717] font-medium leading-relaxed">
                {results.summary}
              </p>
            </motion.div>
          </div>

          {/* Bundle Information (if any) */}
          {results.bundle && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="w-full max-w-[600px] mx-auto"
            >
              <MoneyLeftCard remainingBudget={results.bundle.remaining_budget || 0} />
            </motion.div>
          )}

          {/* Products Grid */}
          <div className="space-y-8">
            <motion.h2 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-2xl font-medium tracking-tight text-center"
            >
              Curated Selection
            </motion.h2>

            {results.shoppingPlan && results.shoppingPlan.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.shoppingPlan.map((product, idx) => (
                  <motion.div
                    key={product.id}
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 + (idx * 0.1) }}
                    className="luxury-card p-4 group"
                  >
                    <div className="aspect-[4/3] bg-[#F2F1EE] rounded-2xl overflow-hidden mb-6 relative">
                      {product.image_url && !failedImages[product.id] ? (
                        <img 
                          src={product.image_url} 
                          alt={product.name} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out" 
                          onError={() => handleImageError(product.id)}
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <ShoppingBag className="w-8 h-8 text-[#6F6F73]/30" />
                        </div>
                      )}
                      
                      <div className="absolute top-4 right-4 bg-white/80 backdrop-blur px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1 shadow-sm">
                        <Star className="w-3 h-3 text-[#171717]" />
                        {product.rating}
                      </div>
                    </div>
                    
                    <div className="px-2 space-y-4">
                      <div>
                        <h3 className="font-medium text-lg leading-tight mb-2 line-clamp-2 text-[#171717]">
                          {product.name}
                        </h3>
                        <p className="text-xl font-semibold text-[#8B5CF6]">
                          {product.price}
                        </p>
                      </div>

                      {product.whyWePickedThis && (
                        <p className="text-sm text-[#6F6F73] italic border-l-2 border-[#8B5CF6]/30 pl-3">
                          "{product.whyWePickedThis}"
                        </p>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center py-20 text-[#6F6F73]">
                No specific products matched.
              </div>
            )}
          </div>
        </div>
      )}

      {/* 5. INITIAL STATE: NEARBY */}
      {!loading && !results && !error && nearbyProducts.length > 0 && (
        <div className="max-w-[1200px] mx-auto px-6 mt-32 space-y-8">
          <div className="text-center">
            <h2 className="text-sm uppercase tracking-widest font-semibold text-[#6F6F73]">Available Locally</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {nearbyProducts.map((prod, idx) => (
              <motion.div 
                key={prod.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05 }}
                className="group cursor-pointer"
              >
                <div className="aspect-square bg-[#F2F1EE] rounded-2xl mb-4 overflow-hidden relative">
                  {prod.image_url && !failedImages[prod.id] ? (
                    <img 
                      src={prod.image_url} 
                      alt={prod.name} 
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out" 
                      onError={() => handleImageError(prod.id)}
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <ShoppingBag className="w-6 h-6 text-[#6F6F73]/30" />
                    </div>
                  )}
                </div>
                <h3 className="text-sm font-medium text-[#171717] line-clamp-1 group-hover:text-[#8B5CF6] transition-colors">
                  {prod.name}
                </h3>
                <p className="text-sm font-semibold text-[#6F6F73] mt-1">{prod.price}</p>
              </motion.div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
