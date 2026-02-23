# AI Portfolio Website (React + FastAPI + OpenRouter)

Production-ready personal portfolio with a modern React frontend and a Python FastAPI backend that powers an AI chat assistant grounded only in stored resume data.

## 1) Project Structure

```text
portfolio-ai/
  frontend/
    index.html
    package.json
    tsconfig.json
    tsconfig.node.json
    vite.config.ts
    postcss.config.js
    tailwind.config.ts
    src/
      main.tsx
      App.tsx
      index.css
      types.ts
      api/client.ts
      components/
        Navbar.tsx
        Hero.tsx
        About.tsx
        Skills.tsx
        Projects.tsx
        Experience.tsx
        Contact.tsx
        ChatWidget.tsx
  backend/
    app/
      main.py
      core/
        config.py
        database.py
      models/
        schemas.py
      services/
        portfolio_service.py
        ai_service.py
      routes/
        portfolio.py
        chat.py
    seed.py
    requirements.txt
    .env.example
```

## 2) Key Architecture Decisions

- Frontend and backend are separated for clean deployment and scaling.
- AI calls happen only in backend (`ai_service.py`) to protect API keys.
- Chat responses are grounded using structured resume context fetched from SQLite.
- System prompt enforces "answer only from context" and explicit fallback when data is missing.
- Modular backend layers: routes, services, schemas, and database utilities.
- Typed API contracts on frontend (`types.ts`) improve maintainability.

## 3) Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
```

Edit `.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
DATABASE_URL=sqlite:///./portfolio.db
CORS_ORIGINS=http://localhost:5173
APP_ENV=development
```

Seed sample resume data:

```bash
python seed.py
```

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

## 4) Frontend Setup (React + TypeScript + Tailwind)

```bash
cd frontend
npm install
```

Create `.env` in `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Run frontend:

```bash
npm run dev
```

## 5) API Endpoints

- `GET /api/portfolio` -> returns full portfolio data.
- `POST /api/chat` -> accepts `{ message, history[] }` and returns grounded answer.

## 6) OpenRouter Integration Notes

- Backend sends chat completion request to `https://openrouter.ai/api/v1/chat/completions`.
- `Authorization: Bearer <OPENROUTER_API_KEY>`.
- Model configured via environment variable.
- Prompt includes serialized resume context from DB.

## 7) Deployment Guide

### Frontend to GitHub Pages

1. In `frontend/package.json`, ensure `base` is set in `vite.config.ts` if repo is not root.
2. Install gh-pages:
   ```bash
   npm i -D gh-pages
   ```
3. Add scripts:
   ```json
   "predeploy": "npm run build",
   "deploy": "gh-pages -d dist"
   ```
4. Run:
   ```bash
   npm run deploy
   ```

### Backend on Render (free tier)

1. Push repo to GitHub.
2. Create new Web Service in Render, root directory `backend`.
3. Build command:
   ```bash
   pip install -r requirements.txt
   ```
4. Start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Add env vars from `.env.example`.
6. Set frontend `VITE_API_BASE_URL` to deployed backend URL + `/api`.

### Optional: Cloudflare Tunnel

- Run backend on local VPS/machine.
- Use `cloudflared tunnel --url http://localhost:8000`.
- Set frontend API base URL to tunnel domain.

## 8) Production Hardening Checklist

- Restrict CORS to deployed frontend domain.
- Add request rate limiting for `/api/chat`.
- Add server-side input length checks.
- Add structured logging and error monitoring.
- Optionally persist chat history for analytics.
