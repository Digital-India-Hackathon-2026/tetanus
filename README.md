# CommerceOS — AI-Powered Commerce Platform

Developed by **Team Tetanus** for the Digital India Hackathon 2026.

CommerceOS is a next-generation decentralized commerce platform that bridges natural language purchase intent with local availability and real-time merchant analytics. 

---

## 🌟 Key Features

1. **Thesis Landing Portal**: Minimalist entrance featuring a dynamic, animated typography title and an interactive monochrome 3D package cluster using CSS 3D transforms that respond to mouse parallax tilt.
2. **Multi-Role Login Terminal**: Explicit side-by-side Customer and Seller authentication card gates with validation states and simulated progress loaders.
3. **AI-Powered Consumer Storefront**:
   - Lists local "Popular Nearby" items on load.
   - Natural language search console ("What are you looking for?") with step-by-step progress tracking loaders.
   - Outputs extracted structured intents (Category, Occasion, Budget, Interest) and shopping plans with contextual reasoning.
4. **Seller Intelligence Console**:
   - Real-time performance indicators (sales totals, order volumes, stock alerts) using clean monochrome deltas.
   - Dynamic AI Copilot Chat offering answers and custom-rendered monochrome visualizations (weekly Area and inventory Bar charts via Recharts).
   - "Live Alerts" sidebar with a dedicated warm red indicator reserved exclusively for critical stock levels.
   - **Cross-Channel Intelligence Loop**: A visual banner showing incoming buyer queries linking to stock counts and recommending single-click reorder actions.

---

## 🛠️ Technology Stack

- **Frontend Core**: React 19 (Functional Components + Hooks)
- **Styling Layout**: Tailwind CSS v4 (Glassmorphism interfaces)
- **Navigation & Routing**: React Router (HashRouter configuration)
- **Data Visualization**: Recharts (Custom monochrome themes)
- **Icons**: Lucide React
- **Development Tooling**: Vite 8 + Rolldown

---

## 🚀 How to Run Locally

### 1. Install Dependencies
Make sure you have Node.js installed, then install packages:
```bash
npm install
```

### 2. Start the Development Server
Launch the local server:
```bash
npm run dev
```
Open [http://localhost:5173/](http://localhost:5173/) in your web browser.

### 3. Build for Production
To bundle optimized client assets:
```bash
npm run build
```
The output directory will be created under `dist/`.
