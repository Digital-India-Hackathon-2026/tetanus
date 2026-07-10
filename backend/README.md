# CommerceOS FastAPI Backend

FastAPI backend server configured for automatic database introspection and Supabase PostgreSQL integration.

---

## 🚀 Setup Instructions

Follow these steps to run the server on your local machine:

### 1. Create a Python Virtual Environment
Navigate to the `backend/` directory and run:
```bash
python -m venv venv
```

### 2. Activate the Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Copy the `.env.example` file to create a local `.env` configuration:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your Supabase database password in the `DB_PASSWORD` variable.

### 5. Launch the Server
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload --port 8000
```
The server will start up and run at: [http://localhost:8000/](http://localhost:8000/)

---

## 🔍 Database Introspection & Schema Discovery
On startup, the server dynamically scans the `public` schema in the Supabase instance:
1. It searches for base tables containing catalog-like keywords: `products`, `items`, `inventory`, `catalog`.
2. Once found, it automatically maps target data fields (ID, Name, Price, Category, Rating, Stock) by checking column synonyms.
3. If database credentials are missing or the connection fails, the server falls back to returning local mock product data automatically.
