export const mapMission = (missionString) => {
  if (!missionString) return {};
  return {
    category: "AI Recommended",
    occasion: "Custom Mission",
    budget: "Flexible",
    interest: missionString,
    volume: "Live Data"
  };
};

export const mapRecommendations = (products) => {
  if (!Array.isArray(products)) return [];
  
  const gradients = [
    "from-amber-500/20 to-orange-600/30",
    "from-emerald-500/20 to-teal-600/30",
    "from-indigo-500/20 to-purple-600/30",
    "from-cyan-500/20 to-blue-600/30",
    "from-purple-500/20 to-pink-600/30",
    "from-zinc-500/20 to-neutral-600/30"
  ];

  return products.map((rec, index) => {
    return {
      id: rec.product_id || Math.random().toString(),
      name: rec.name || "Unknown Product",
      price: rec.price ? `₹${rec.price.toLocaleString()}` : "Price TBD",
      originalPrice: rec.price ? `₹${(Math.round(rec.price * 1.2)).toLocaleString()}` : "",
      rating: rec.rating || 4.5,
      reviews: Math.floor(Math.random() * 500) + 50,
      imageColor: gradients[index % gradients.length],
      image_url: rec.image_url || "",
      whyWePickedThis: rec.justification || "Recommended by CIN."
    };
  });
};

export const mapBundle = (bundle) => {
  if (!bundle) return { remaining_budget: 0, readiness_score: 0 };
  return {
    ...bundle,
    remaining_budget: bundle.remaining_budget || 0,
    readiness_score: bundle.readiness_score || 0
  };
};

export const mapAnalytics = (analytics) => {
  if (!analytics) return {};
  
  // Flatten strategy array into a clean string for the UI
  let strategyStr = "";
  if (Array.isArray(analytics.shopping_strategy)) {
    strategyStr = analytics.shopping_strategy.join(" ");
  } else if (typeof analytics.shopping_strategy === 'string') {
    strategyStr = analytics.shopping_strategy;
  }

  return {
    ...analytics,
    shopping_strategy: strategyStr
  };
};

export const mapSummary = (summary) => {
  return summary || "We have analyzed your request and prepared the following purchasing plan.";
};

export const mapShoppingTips = (tips) => {
  if (!Array.isArray(tips)) return [];
  return tips;
};

export const mapBackendResponseToFrontend = (backendResponse) => {
  return {
    intent: mapMission(backendResponse.mission),
    shoppingPlan: mapRecommendations(backendResponse.products),
    bundle: backendResponse.bundles && backendResponse.bundles.length > 0 ? backendResponse.bundles[0] : null,
    analytics: {},
    summary: backendResponse.explanation || "CIN has assembled your cart.",
    shoppingTips: []
  };
};

