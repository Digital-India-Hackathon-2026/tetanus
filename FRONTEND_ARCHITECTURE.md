# FRONTEND ARCHITECTURE AUDIT

## 1. Framework
- **Core:** React 19
- **Build Tool:** Vite 8
- **Language:** JavaScript (`.jsx` files). No TypeScript detected in `devDependencies`.

## 2. Folder Structure
```
d:/frontend/
├── src/
│   ├── assets/            (Static images, icons, etc.)
│   ├── components/        (11 UI components like FloatingCopilot, SignalFeed, DemandHeatStrip)
│   ├── pages/             (5 view components like ConsumerView, SellerView, LandingPage)
│   ├── services/          (Contains api.js for data fetching and mocks)
│   ├── App.jsx            (Root component with React Router)
│   ├── main.jsx           (Entry point)
│   └── index.css / App.css (Global styles)
├── package.json
└── vite.config.js
```

## 3. Routing
- **Library:** `react-router-dom` (v7.18.1)
- **Implementation:** Client-side routing inside `App.jsx` using `HashRouter`.
- **Routes:** 
  - `/` -> `LandingPage`
  - `/login` -> `LoginPage`
  - `/consumer` -> `ConsumerView`
  - `/seller` -> `SellerView`
  - `*` -> Fallback to `/`

## 4. State Management
- **Local State:** Utilizes React's `useState` and `useEffect`.
- **Global / Persistent State:** Employs `localStorage` directly in `api.js` to persist simulated states like `cos_dino_searches` and `cos_puzzle_stock` across reloads. No Redux, Zustand, or Context API is used for global state management.

## 5. UI Library
- Custom built. Uses `lucide-react` (v1.24.0) for iconography and `recharts` (v3.9.2) for Seller data visualization.

## 6. Styling
- **Engine:** Tailwind CSS v4 (`@tailwindcss/vite` and `tailwindcss` plugins in `package.json`).
- **Methodology:** Utility-first CSS directly on JSX elements. Global variables in `index.css`.

## 7. API Layer
- **Location:** `src/services/api.js`.
- **Implementation:** Currently running in a simulated mode (`USE_MOCK_API = true`). It uses `setTimeout` to mimic network latency (1.5s delay) and returns hardcoded JSON blobs for specific queries (e.g. "dino", "mug"). Contains functions like `postIntent`, `postSellerQuery`, `getIntelligenceLoop`, and `triggerReorder`.

## 8. Existing Pages
- `LandingPage.jsx`: Entry point for navigating to different user flows.
- `LoginPage.jsx`: Authentication shell (clears local storage).
- `ConsumerView.jsx`: The core buyer experience (chat interface, recommendations).
- `SellerView.jsx`: Dashboard for merchants showing analytics, stock alerts, and trends.

## 9. Existing Components
- `AgentActivityLog.jsx`, `CategoryBreakdownChart.jsx`, `DemandHeatStrip.jsx`, `FloatingCopilot.jsx`, `IntelligenceLoop.jsx`, `MoneyLeftCard.jsx`, `ProfitComparisonCard.jsx`, `ReorderSimulator.jsx`, `SalesTrendChart.jsx`, `SignalFeed.jsx`, `TopProductsChart.jsx`.

## 10. Existing Assets
- Expected static icons or SVGs inside `src/assets`. Recharts and Lucide handle most dynamic vector graphics.

## 11. Existing Environment Variables
- None natively loaded currently. `api.js` relies on a hardcoded constant `const API_BASE_URL = 'http://localhost:8000';`. 
- **Missing:** `.env` file containing Vite variables (e.g., `VITE_API_URL`).

## 12. Build System
- **Engine:** Vite 8.
- **Commands:** `npm run dev` (running on `http://localhost:5174/` because 5173 was likely bound). `npm run build` leverages `@rolldown/binding-win32-x64-msvc`.

## 13. Current Problems
- **Hardcoded API URLs:** `API_BASE_URL` is hardcoded in `api.js` instead of using `import.meta.env`.
- **Mock Data Coupling:** The frontend expects response keys like `intent` and `shoppingPlan`, which do not perfectly map to our backend schema (`mission`, `recommendations`, `bundle`).
- **No Global Store:** Prop-drilling or component isolation might become difficult if the Consumer and Seller views need to share real-time Socket/Event data.

## 14. Missing Features
- **API Mapping:** The frontend models need mapping functions to parse our FastAPI backend response into the shapes expected by `ConsumerView.jsx`.
- **Error Handling:** Minimal boundary handling if the backend is down (currently just relies on `console.error` and falls back to mock logic, which needs to be completely removed or restructured for production).
