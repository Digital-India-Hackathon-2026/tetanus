import React, { useState, useEffect } from 'react';
import { Search, Sparkles, Tag, Star, Gift, ShoppingCart, Info, Clock } from 'lucide-react';
import { postIntent } from '../services/api';

export default function CustomerView() {
  const defaultQuery = "Birthday gift for a 10-year-old who loves dinosaurs, budget ₹1500";
  const [query, setQuery] = useState(defaultQuery);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [failedImages, setFailedImages] = useState({});

  const handleImageError = (id) => {
    setFailedImages(prev => ({ ...prev, [id]: true }));
  };

  const quickSelectChips = [
    { label: "🦕 Dinosaur Gift (₹1500)", text: "Birthday gift for a 10-year-old who loves dinosaurs, budget ₹1500" },
    { label: "☕ Tech Mug", text: "Smart coffee mug for developer workspace, budget ₹4000" },
    { label: "👟 Workout Gear", text: "Cozy running shoes under ₹5000" }
  ];

  const handleSearchSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResults(null);
    try {
      const data = await postIntent(query);
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Pre-fill search field, but don't auto-submit so the presenter can control the flow
  useEffect(() => {
    setQuery(defaultQuery);
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-12">
      {/* Header Section */}
      <div className="text-center space-y-3">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-slate-100 via-slate-200 to-indigo-300 bg-clip-text text-transparent">
          AI Personal Shopper
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto text-sm md:text-base">
          Describe what you are looking for in natural language. Our neural agent will extract your intent and construct a tailored shopping plan.
        </p>
      </div>

      {/* Main Command Center Card */}
      <div className="max-w-3xl mx-auto glass-panel rounded-3xl p-6 md:p-8 shadow-2xl border-brand-indigo/15 relative overflow-hidden">
        {/* Decorative corner glows */}
        <div className="absolute top-0 left-0 -mt-10 -ml-10 w-24 h-24 rounded-full bg-brand-indigo/10 blur-xl pointer-events-none" />
        
        <form onSubmit={handleSearchSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-xs font-semibold tracking-widest text-brand-indigo uppercase">
              What are you looking for?
            </label>
            <div className="relative group">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., Cozy running shoes under ₹5000"
                className="w-full pl-5 pr-14 py-4 md:py-5 bg-brand-dark-bg/60 border border-brand-dark-border group-hover:border-brand-indigo/30 focus:border-brand-indigo focus:ring-1 focus:ring-brand-indigo rounded-2xl text-slate-100 placeholder-slate-500 focus:outline-none transition-all duration-300 text-sm md:text-base"
              />
              <button
                type="submit"
                className="absolute right-3 top-1/2 -translate-y-1/2 p-2.5 rounded-xl bg-brand-indigo hover:bg-brand-indigo-dark text-white shadow-md shadow-brand-indigo/20 transition-all duration-300 hover:scale-105"
              >
                <Search className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Quick Select Chips */}
          <div className="space-y-2.5">
            <span className="text-xs text-slate-500">Quick suggestions:</span>
            <div className="flex flex-wrap gap-2">
              {quickSelectChips.map((chip, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setQuery(chip.text)}
                  className="px-3.5 py-1.5 rounded-full text-xs font-medium border border-brand-dark-border bg-brand-dark-card/50 hover:bg-brand-indigo/10 hover:border-brand-indigo/35 text-slate-300 hover:text-slate-100 transition-all duration-200 cursor-pointer"
                >
                  {chip.label}
                </button>
              ))}
            </div>
          </div>
        </form>
      </div>

      {/* Loading Skeleton State */}
      {loading && (
        <div className="space-y-8 animate-pulse">
          {/* Skeleton Chips */}
          <div className="flex justify-center gap-2 max-w-xl mx-auto">
            <div className="h-7 w-24 bg-brand-dark-card rounded-full shimmer" />
            <div className="h-7 w-28 bg-brand-dark-card rounded-full shimmer" />
            <div className="h-7 w-20 bg-brand-dark-card rounded-full shimmer" />
          </div>
          {/* Skeleton Product Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((n) => (
              <div key={n} className="glass-panel border-brand-dark-border/40 rounded-2xl p-5 space-y-4">
                <div className="w-full aspect-video rounded-xl shimmer" />
                <div className="h-5 w-2/3 bg-brand-dark-border/60 rounded shimmer" />
                <div className="h-4 w-1/4 bg-brand-dark-border/60 rounded shimmer" />
                <div className="space-y-2 pt-2">
                  <div className="h-3 w-full bg-brand-dark-border/60 rounded shimmer" />
                  <div className="h-3 w-5/6 bg-brand-dark-border/60 rounded shimmer" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && !results && (
        <div className="text-center py-12 space-y-4 max-w-md mx-auto">
          <div className="inline-flex p-4 bg-brand-dark-card border border-brand-dark-border rounded-2xl text-slate-500">
            <Sparkles className="w-8 h-8" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-semibold text-slate-200">No Shopping Plan Generated</h3>
            <p className="text-xs text-slate-500">
              Submit the query above or select a suggestion chip to let the AI build your shopping recommendation flow.
            </p>
          </div>
        </div>
      )}

      {/* Results View */}
      {!loading && results && (
        <div className="space-y-8 transition-all duration-500 ease-in-out">
          
          {/* Extracted Intent Section */}
          <div className="flex flex-col items-center gap-3">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-widest">
              <Info className="w-3.5 h-3.5 text-brand-teal" />
              Extracted Intent
            </div>
            <div className="flex flex-wrap justify-center gap-2 max-w-2xl">
              {Object.entries(results.intent).map(([key, value]) => (
                <div
                  key={key}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-brand-teal/20 bg-brand-teal/5 text-xs text-brand-teal font-medium"
                >
                  <span className="opacity-60 capitalize">{key}:</span>
                  <span>{value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Shopping Plan Products Grid */}
          <div className="space-y-4">
            <h2 className="text-xl md:text-2xl font-bold text-slate-100 flex items-center gap-2">
              <Gift className="w-5 h-5 text-brand-indigo" />
              Suggested Shopping Plan
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {results.shoppingPlan.map((product) => (
                <div
                  key={product.id}
                  className="glass-panel glass-panel-hover border-brand-dark-border/40 rounded-2xl p-5 flex flex-col justify-between group transition-all duration-300 relative"
                >
                  <div className="space-y-4">
                    {/* Visual Placeholder */}
                    <div className="w-full aspect-video rounded-xl bg-slate-800 flex items-center justify-center relative overflow-hidden group-hover:scale-[1.02] transition-transform duration-300">
                      {product.image_url && !failedImages[product.id] ? (
                        <img 
                          src={product.image_url} 
                          alt={product.name} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                          onError={() => handleImageError(product.id)}
                        />
                      ) : (
                        <div className={`w-full h-full bg-gradient-to-br ${product.imageColor} flex items-center justify-center`}>
                          <Gift className="w-10 h-10 text-slate-400 opacity-60 absolute group-hover:rotate-6 group-hover:scale-110 transition-all duration-300" />
                        </div>
                      )}
                      <div className="absolute top-2 right-2 flex items-center gap-1 bg-brand-dark-bg/85 px-2 py-0.5 rounded-md text-[10px] text-brand-indigo font-bold border border-brand-indigo/20">
                        <Star className="w-3.5 h-3.5 fill-current" />
                        {product.rating}
                      </div>
                    </div>

                    {/* Metadata & Title */}
                    <div className="space-y-1">
                      <h3 className="font-bold text-slate-100 group-hover:text-brand-indigo transition-colors line-clamp-1">
                        {product.name}
                      </h3>
                      <div className="flex items-baseline gap-2">
                        <span className="text-lg font-extrabold text-slate-100">{product.price}</span>
                        {product.originalPrice && (
                          <span className="text-xs text-slate-500 line-through">{product.originalPrice}</span>
                        )}
                      </div>
                    </div>

                    {/* AI Pick Explanation */}
                    <div className="pt-2 border-t border-brand-dark-border/30">
                      <p className="text-xs text-slate-400 italic pl-3 border-l-2 border-brand-teal/40 line-clamp-3">
                        "{product.whyWePickedThis}"
                      </p>
                    </div>
                  </div>

                  {/* Add To Cart Demo Button */}
                  <button className="mt-5 w-full py-2.5 rounded-xl border border-brand-indigo/20 bg-brand-indigo/5 group-hover:bg-brand-indigo text-slate-200 group-hover:text-white text-xs font-semibold flex items-center justify-center gap-1.5 transition-all duration-300">
                    <ShoppingCart className="w-3.5 h-3.5" />
                    Select & Customize
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
