import React, { useState, useEffect } from 'react';
import { Search, Sparkles, Tag, Star, Gift, ShoppingBag, Info, Compass, HelpCircle } from 'lucide-react';
import { postIntent } from '../services/api';

export default function ConsumerView() {
  const defaultQuery = "Birthday gift for a 10-year-old who loves dinosaurs, budget ₹1500";
  const [query, setQuery] = useState(defaultQuery);
  const [loading, setLoading] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState("Understanding your request...");
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

  // Seed data for the initial "Near You" display
  const nearYouProducts = [
    { id: "ny-1", name: "Stark Matte Black Backpack", price: "₹4,500", rating: 4.8, category: "Luggage" },
    { id: "ny-2", name: "Minimalist Mechanical Keyboard", price: "₹6,800", rating: 4.9, category: "Electronics" },
    { id: "ny-3", name: "Studio Noise Cancelling Headset", price: "₹12,999", rating: 4.7, category: "Audio" },
    { id: "ny-4", name: "Wool Felt Sleeve Organizer", price: "₹1,499", rating: 4.5, category: "Office" },
    { id: "ny-5", name: "Aluminum Desk Phone Dock", price: "₹899", rating: 4.6, category: "Accessories" }
  ];

  // Dynamic nearby products loading states
  const [nearbyProducts, setNearbyProducts] = useState([]);
  const [nearbyLoading, setNearbyLoading] = useState(true);

  const handleSearchSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResults(null);
    setLoadingStatus("Understanding your request...");

    // Status switching simulation at 900ms of a 1.8s load
    const statusTimeout = setTimeout(() => {
      setLoadingStatus("Finding matches...");
    }, 900);

    try {
      const data = await postIntent(query);
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      clearTimeout(statusTimeout);
      setLoading(false);
    }
  };

  useEffect(() => {
    setQuery(defaultQuery);

    // Fetch dynamic nearby items from the FastAPI DB catalog
    const fetchNearbyProducts = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/products/nearby");
        if (!response.ok) throw new Error("Failed to load products from endpoint");
        const data = await response.json();
        setNearbyProducts(data.products || []);
        console.log(`[CommerceOS] Discovered product source: ${data.source}`);
      } catch (err) {
        console.warn("[CommerceOS] DB endpoint down, rendering local mock fallback:", err);
        setNearbyProducts(nearYouProducts);
      } finally {
        setNearbyLoading(false);
      }
    };

    fetchNearbyProducts();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-12 bg-transparent text-[#1f2937]">
      
      {/* Header Block */}
      <div className="text-center space-y-3">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-amber-600 via-orange-500 to-amber-500 bg-clip-text text-transparent uppercase leading-none pb-2">
          AI Personal Shopper
        </h1>
        <p className="text-slate-500 max-w-xl mx-auto text-xs md:text-sm font-medium">
          Enter what you're seeking. We parse the intent, explore local warehouse databases, and provide a tailored purchasing plan.
        </p>
      </div>

      {/* Query input card */}
      <div className="max-w-3xl mx-auto border border-amber-500/10 rounded-3xl p-6 md:p-8 bg-white/80 backdrop-blur-md shadow-[0_8px_30px_rgba(217,119,6,0.03)]">
        <form onSubmit={handleSearchSubmit} className="space-y-6">
          
          <div className="space-y-2 text-left">
            <label className="text-xs font-bold tracking-widest text-[#1f2937] uppercase">
              What are you looking for?
            </label>
            <div className="relative flex items-center">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Describe your search query..."
                className="w-full pl-5 pr-14 py-4 bg-white border border-amber-500/15 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 rounded-xl text-[#1f2937] placeholder-slate-400 focus:outline-none transition-all duration-300 text-sm md:text-base font-medium"
              />
              <button
                type="submit"
                className="absolute right-3 p-2.5 rounded-lg bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white transition-all hover:scale-105 shadow-[0_4px_12px_rgba(217,119,6,0.2)]"
              >
                <Search className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Preset Chips */}
          <div className="space-y-2 text-left">
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Example queries:</span>
            <div className="flex flex-wrap gap-2">
              {quickSelectChips.map((chip, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setQuery(chip.text)}
                  className="px-3.5 py-1.5 rounded-full text-xs font-semibold border border-amber-500/15 hover:border-amber-500/50 bg-white hover:bg-amber-50/50 text-slate-700 hover:text-amber-800 transition-all cursor-pointer"
                >
                  {chip.label}
                </button>
              ))}
            </div>
          </div>

        </form>
      </div>

      {/* Horizontal Loading Progress State */}
      {loading && (
        <div className="max-w-md mx-auto space-y-3 py-12 text-center">
          <div className="w-full h-2 bg-slate-200/50 rounded-full overflow-hidden">
            {/* Animates over 1.8 seconds using progress keyframe */}
            <div className="h-full bg-gradient-to-r from-amber-400 via-orange-400 to-amber-600 animate-progress rounded-full" />
          </div>
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest animate-pulse">
            {loadingStatus}
          </p>
        </div>
      )}

      {/* INITIAL / NO-SEARCH VIEW: Popular Nearby Row */}
      {!loading && !results && (
        <div className="space-y-6 text-left">
          <div className="flex items-center gap-2 border-b border-amber-500/15 pb-3">
            <Compass className="w-5 h-5 text-amber-500" />
            <h2 className="text-lg font-extrabold uppercase tracking-tight text-[#1f2937]">
              Popular Nearby You
            </h2>
            <span className="text-[10px] bg-amber-500/10 text-amber-700 border border-amber-500/20 px-2 py-0.5 rounded-md font-semibold tracking-wide uppercase">
              Immediate Pickup
            </span>
          </div>

          {nearbyLoading ? (
            /* Black-bordered skeleton cards while request is in flight */
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {[1, 2, 3, 4, 5].map((n) => (
                <div key={n} className="border border-brand-border rounded-2xl p-4 space-y-3 flex flex-col justify-between bg-white shimmer">
                  <div className="space-y-2 animate-pulse">
                    <div className="w-full aspect-square bg-slate-100 rounded-xl shimmer" />
                    <div className="h-3 w-10 bg-slate-200 rounded shimmer" />
                    <div className="h-4 w-5/6 bg-slate-200 rounded shimmer" />
                  </div>
                  <div className="h-4 w-1/3 bg-slate-200 rounded shimmer mt-1" />
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-5">
              {nearbyProducts.map((prod) => (
                <div 
                  key={prod.id} 
                  className="light-panel light-panel-hover rounded-2xl p-4 flex flex-col justify-between group transition-all duration-300"
                >
                  <div className="space-y-3">
                    {/* Stark monochrome placeholder box / image */}
                    <div className="w-full aspect-square bg-amber-50/20 border border-amber-500/10 rounded-xl flex items-center justify-center relative overflow-hidden transition-all duration-300">
                      {prod.image_url && !failedImages[prod.id] ? (
                        <img 
                          src={prod.image_url} 
                          alt={prod.name} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                          onError={() => handleImageError(prod.id)}
                        />
                      ) : (
                        <ShoppingBag className="w-8 h-8 text-amber-600/40 group-hover:scale-110 transition-transform duration-300" />
                      )}
                      <div className="absolute top-2 right-2 flex items-center gap-1 bg-white border border-amber-500/15 px-1.5 py-0.5 rounded text-[8px] font-bold text-amber-600 shadow-sm">
                        <Star className="w-2.5 h-2.5 fill-current text-amber-500" />
                        {prod.rating}
                      </div>
                    </div>
                    
                    <div className="space-y-1">
                      <span className="text-[9px] font-extrabold text-slate-400 uppercase tracking-widest block">
                        {prod.category}
                      </span>
                      <h3 className="text-xs font-bold text-[#1f2937] line-clamp-1 group-hover:text-amber-600 transition-colors duration-300">
                        {prod.name}
                      </h3>
                      {prod.description && (
                        <p className="text-[10px] text-slate-500 line-clamp-2 leading-relaxed">
                          {prod.description}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="text-xs font-black text-[#1f2937] pt-2 mt-2 border-t border-amber-500/10 flex items-center justify-between">
                    <span className="text-amber-600 font-extrabold">{prod.price}</span>
                    <span className="text-[9px] text-slate-450 font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center gap-0.5">
                      View Detail &rarr;
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* RESULTS VIEW */}
      {!loading && results && (
        <div className="space-y-8 animate-fade-in text-left">
          
          {/* Extracted Intent Tags */}
          <div className="flex flex-col items-center gap-3 border-t border-b border-amber-500/15 py-6">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-500 uppercase tracking-widest">
              <Info className="w-4 h-4 text-amber-500" />
              Extracted Intent Parameters
            </div>
            
            <div className="flex flex-wrap justify-center gap-2">
              {Object.entries(results.intent).map(([key, val]) => (
                <div
                  key={key}
                  className="px-3.5 py-1.5 rounded-full border border-amber-500/20 bg-amber-500/5 text-xs font-semibold text-amber-700 shadow-[0_2px_8px_rgba(217,119,6,0.03)]"
                >
                  <span className="opacity-50 capitalize mr-1">{key}:</span>
                  <span>{val}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Dynamic Suggestion Plan Cards */}
          <div className="space-y-5">
            <h2 className="text-xl font-extrabold uppercase tracking-tight text-[#1f2937] flex items-center gap-2">
              <Gift className="w-5 h-5 text-amber-500" />
              Recommended Purchasing Plan
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {results.shoppingPlan.map((product) => (
                <div
                  key={product.id}
                  className="border border-amber-500/10 hover:border-amber-500/35 rounded-2xl p-5 flex flex-col justify-between bg-white/70 backdrop-blur-md transition-all duration-300 group shadow-sm hover:shadow-[0_8px_30px_rgba(217,119,6,0.08)] hover:-translate-y-1"
                >
                  <div className="space-y-4">
                    {/* Image block */}
                    <div className="w-full aspect-video bg-amber-50/20 border border-amber-500/10 rounded-xl flex items-center justify-center relative overflow-hidden">
                      {product.image_url && !failedImages[product.id] ? (
                        <img 
                          src={product.image_url} 
                          alt={product.name} 
                          className="w-full h-full object-cover" 
                          onError={() => handleImageError(product.id)}
                        />
                      ) : (
                        <ShoppingBag className="w-10 h-10 text-amber-600/40 group-hover:scale-110 transition-transform" />
                      )}
                      <div className="absolute top-2 right-2 flex items-center gap-1 bg-white border border-amber-500/15 px-2 py-0.5 rounded-md text-[9px] text-amber-600 font-bold shadow-sm">
                        <Star className="w-3.5 h-3.5 fill-current text-amber-500" />
                        {product.rating}
                      </div>
                    </div>

                    {/* Metadata & Title */}
                    <div className="space-y-1">
                      <h3 className="font-extrabold text-[#1f2937] group-hover:text-amber-600 transition-colors text-sm md:text-base line-clamp-1">
                        {product.name}
                      </h3>
                      <div className="text-base font-black text-amber-600">
                        {product.price}
                      </div>
                    </div>

                    {/* Reason block */}
                    <div className="pt-3 border-t border-amber-500/10">
                      <p className="text-xs text-slate-500 italic pl-3 border-l-2 border-amber-500">
                        "{product.whyWePickedThis}"
                      </p>
                    </div>
                  </div>

                  {/* Action button */}
                  <button className="mt-5 w-full py-2.5 rounded-lg border border-amber-500/20 bg-amber-500/5 hover:bg-gradient-to-r hover:from-amber-500 hover:to-orange-500 text-amber-700 hover:text-white text-xs font-black transition-all duration-300 shadow-sm">
                    Select & Configure
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
