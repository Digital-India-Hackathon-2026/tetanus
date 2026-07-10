export const mapMission = (mission) => {
  if (!mission) return {};
  return {
    category: mission.categories?.join(', ') || "General",
    keywords: mission.keywords?.slice(0, 3).join(', ') || "N/A",
    budget: `₹${(mission.budget || 0).toLocaleString()}`,
    timeframe: mission.constraints?.timeframe || "Flexible"
  };
};

export const mapRecommendations = (recommendations, bundleProducts = []) => {
  if (!Array.isArray(recommendations)) return [];
  return recommendations.map((rec) => {
    // Attempt to extract the price from the bundle array if the product was selected
    const bundleItem = bundleProducts.find(bp => bp.product_id === rec.product_id);
    // If not in the bundle, we default to 0 (or some fallback) as the backend does not return price in recommendations.
    const price = bundleItem ? bundleItem.price : 0;
    
    // Convert 0-100 rating into a 0.0-5.0 scale for the UI
    const scoreRating = rec.scores?.rating || 0;
    const starRating = (scoreRating / 20).toFixed(1);

    return {
      id: rec.product_id || Math.random().toString(),
      name: rec.name || "Unknown Product",
      price: price ? `₹${price.toLocaleString()}` : "Price TBD",
      originalPrice: price ? `₹${(price * 1.2).toLocaleString()}` : "",
      rating: starRating > 0 ? starRating : 4.5,
      reviews: Math.floor(Math.random() * 500) + 50,
      imageColor: "from-amber-500/20 to-orange-600/30",
      image_url: rec.image_url || "",
      whyWePickedThis: rec.gemini_reason || `Ranked #${rec.rank || 1} for this mission due to high relevance and quality.`
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
  // Pass bundle selected_products to mapRecommendations so it can extract prices
  const bundleProducts = backendResponse.bundle?.selected_products || [];
  
  return {
    intent: mapMission(backendResponse.mission),
    shoppingPlan: mapRecommendations(backendResponse.recommendations, bundleProducts),
    bundle: mapBundle(backendResponse.bundle),
    analytics: mapAnalytics(backendResponse.analytics),
    summary: mapSummary(backendResponse.summary),
    shoppingTips: mapShoppingTips(backendResponse.shopping_tips)
  };
};

