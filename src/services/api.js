import { mapBackendResponseToFrontend } from './mapper';

const USE_MOCK_API = false; // Set to false to connect to FastAPI backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Initialize localStorage values for simulation if not set
if (!localStorage.getItem('cos_dino_searches')) {
  localStorage.setItem('cos_dino_searches', '3');
}
if (!localStorage.getItem('cos_puzzle_stock')) {
  localStorage.setItem('cos_puzzle_stock', '5');
}
if (!localStorage.getItem('cos_search_history')) {
  localStorage.setItem('cos_search_history', JSON.stringify([]));
}

// Helper to delay simulation (polishing skeleton loading states)
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const postIntent = async (query) => {
  if (!USE_MOCK_API) {
    try {
      const response = await fetch(`${API_BASE_URL}/mission`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mission: query }),
      });
      if (!response.ok) throw new Error(`Backend error: ${response.status}`);
      const rawData = await response.json();
      return mapBackendResponseToFrontend(rawData);
    } catch (error) {
      console.error('API Error, falling back to mock:', error);
      // Fallback if backend is down
    }
  }

  // Stateful Simulation logic
  await delay(1500); // 1.5s skeleton loading simulation

  const lowerQuery = query.toLowerCase();
  
  // Record search history
  const history = JSON.parse(localStorage.getItem('cos_search_history') || '[]');
  history.push({ query, timestamp: new Date().toISOString() });
  localStorage.setItem('cos_search_history', JSON.stringify(history));

  // If search involves dinosaurs, increment count
  if (lowerQuery.includes('dino') || lowerQuery.includes('dinosaur')) {
    const current = parseInt(localStorage.getItem('cos_dino_searches') || '3', 10);
    localStorage.setItem('cos_dino_searches', (current + 1).toString());
  }

  // Response mapping based on queries
  if (lowerQuery.includes('dino') || lowerQuery.includes('dinosaur')) {
    const searchCount = localStorage.getItem('cos_dino_searches');
    return {
      intent: {
        category: "Toys & Games",
        occasion: "10th Birthday Gift",
        budget: "₹1,500",
        interest: "Dinosaurs",
        volume: `${searchCount} Shoppers Today`
      },
      shoppingPlan: [
        {
          id: "dino-1",
          name: "DinoBuilder Jurassic LEGO Set",
          price: "₹1,299",
          originalPrice: "₹1,599",
          rating: 4.8,
          reviews: 128,
          imageColor: "from-amber-500/20 to-orange-600/30",
          whyWePickedThis: "Perfect fit for dinosaur lovers. Combines building blocks with high play value, and sits comfortably under the ₹1,500 limit."
        },
        {
          id: "dino-2",
          name: "Glow-in-the-Dark T-Rex Skeleton 3D Puzzle",
          price: "₹499",
          originalPrice: "₹799",
          rating: 4.5,
          reviews: 84,
          imageColor: "from-emerald-500/20 to-teal-600/30",
          whyWePickedThis: "Interactive 3D puzzle that glows at night. Great high-scoring budget option, leaving room to spare."
        },
        {
          id: "dino-3",
          name: "National Geographic Big Book of Dinosaurs",
          price: "₹799",
          originalPrice: "₹999",
          rating: 4.9,
          reviews: 320,
          imageColor: "from-indigo-500/20 to-purple-600/30",
          whyWePickedThis: "Enriching educational facts with colorful visual page layouts. Ideal reading choice for a 10-year-old child."
        }
      ]
    };
  } else if (lowerQuery.includes('mug') || lowerQuery.includes('coffee') || lowerQuery.includes('developer')) {
    return {
      intent: {
        category: "Office & Electronics",
        occasion: "Desk Upgrade",
        budget: "₹4,000",
        interest: "Software Engineering",
        volume: "12 Shoppers This Week"
      },
      shoppingPlan: [
        {
          id: "mug-1",
          name: "ThermaSmart App-Controlled Heated Mug",
          price: "₹3,499",
          originalPrice: "₹3,999",
          rating: 4.6,
          reviews: 43,
          imageColor: "from-zinc-700/30 to-slate-900/30",
          whyWePickedThis: "Keep beverages at target temperature (50-65°C) during long coding sprints. Syncs with developer's phone app."
        },
        {
          id: "mug-2",
          name: "Minimalist Double-Wall Borosilicate Mug",
          price: "₹899",
          originalPrice: "₹1,200",
          rating: 4.4,
          reviews: 79,
          imageColor: "from-cyan-500/20 to-blue-600/30",
          whyWePickedThis: "Heat resistant glass design prevents condensation on work surfaces. Elegant shape looks clean on any developer setup."
        }
      ]
    };
  } else {
    // General fallback response
    return {
      intent: {
        category: "General Retail",
        occasion: "Self Purchase",
        budget: "Flexible",
        interest: "Custom Search",
        volume: "1 Shopper"
      },
      shoppingPlan: [
        {
          id: "gen-1",
          name: "Premium Wireless Desk Charger Pad",
          price: "₹1,899",
          originalPrice: "₹2,499",
          rating: 4.7,
          reviews: 215,
          imageColor: "from-purple-500/20 to-pink-600/30",
          whyWePickedThis: "Elegant charging pad matching standard workspaces. Supports fast wireless charging for multiple devices."
        },
        {
          id: "gen-2",
          name: "Organized Felt Desk Organizer Mat",
          price: "₹1,200",
          originalPrice: "₹1,500",
          rating: 4.8,
          reviews: 96,
          imageColor: "from-zinc-500/20 to-neutral-600/30",
          whyWePickedThis: "Eco-friendly wool felt desk mat to protect surfaces and dampen mouse noises, creating a clean workspace."
        }
      ]
    };
  }
};

export const postSellerQuery = async (query) => {
  if (!USE_MOCK_API) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/seller-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      if (!response.ok) throw new Error('Backend error');
      return await response.json();
    } catch (error) {
      console.error('API Error, falling back to mock:', error);
    }
  }

  await delay(1200); // 1.2s seller query processing time

  const lowerQuery = query.toLowerCase();

  if (lowerQuery.includes('drop') || lowerQuery.includes('sales') || lowerQuery.includes('yesterday')) {
    return {
      answer: "Your aggregate sales dropped by **18%** yesterday. This was driven by a temporary **30% drop in traffic** in the **Electronics** category (primarily affecting Smart Coffee Mugs). However, your **Toys & Games** category remained resilient, with a spike in search volume. Here is your daily revenue trend for the past week:",
      chartType: "area",
      chartData: [
        { day: "Mon", sales: 24200 },
        { day: "Tue", sales: 26800 },
        { day: "Wed", sales: 25100 },
        { day: "Thu", sales: 27900 },
        { day: "Fri", sales: 28400 },
        { day: "Sat (Yesterday)", sales: 21500, isHighlight: true },
        { day: "Sun (Today)", sales: 23800 }
      ],
      chartConfig: {
        dataKey: "sales",
        name: "Sales Volume (₹)"
      }
    };
  } else if (lowerQuery.includes('reorder') || lowerQuery.includes('inventory') || lowerQuery.includes('stock')) {
    const dinoSearches = parseInt(localStorage.getItem('cos_dino_searches') || '3', 10);
    const puzzleStock = parseInt(localStorage.getItem('cos_puzzle_stock') || '5', 10);
    
    return {
      answer: `Inventory analysis shows critical stock levels for items experiencing search spikes. Specifically, **${dinoSearches} shoppers** searched for dinosaur products today, resulting in the **Dinosaur Puzzle Set** dropping to **${puzzleStock} units** (well below safety threshold of 30). I suggest raising a purchase order of **25 units** to replenish. Current versus safety stock comparisons:`,
      chartType: "bar",
      chartData: [
        { name: "Dino Puzzle", stock: puzzleStock, safety: 30, reorder: 25 },
        { name: "Dino LEGO", stock: 8, safety: 20, reorder: 12 },
        { name: "Smart Mug", stock: 45, safety: 25, reorder: 0 }
      ],
      chartConfig: {
        keys: ["stock", "safety"],
        names: ["Current Stock", "Safety Stock"]
      }
    };
  } else {
    return {
      answer: "I am ready to analyze your inventory levels, traffic patterns, and order history. To see charts and advanced insights, you can try asking: \n- *'Why did my sales drop yesterday?'*\n- *'What should I reorder?'*",
      chartType: null,
      chartData: null
    };
  }
};

export const getIntelligenceLoop = async () => {
  if (!USE_MOCK_API) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/intelligence-loop`);
      if (!response.ok) throw new Error('Backend error');
      return await response.json();
    } catch (error) {
      console.error('API Error, falling back to mock:', error);
    }
  }

  // Read live search state
  const dinoSearches = localStorage.getItem('cos_dino_searches') || '3';
  const puzzleStock = localStorage.getItem('cos_puzzle_stock') || '5';

  return {
    searchesCount: dinoSearches,
    stockLeft: puzzleStock,
    productName: "Dinosaur Puzzle Set",
    searchQuery: "dinosaur gifts",
    suggestedReorder: 25
  };
};

export const triggerReorder = async () => {
  // Simulates ordering stock, which resolves the stock alert!
  await delay(1000);
  localStorage.setItem('cos_puzzle_stock', '30'); // Reset stock to safety
  localStorage.setItem('cos_dino_searches', '0'); // Reset searches
  return { success: true };
};

export const resetDemoState = () => {
  localStorage.setItem('cos_dino_searches', '3');
  localStorage.setItem('cos_puzzle_stock', '5');
  localStorage.setItem('cos_search_history', JSON.stringify([]));
  return true;
};
