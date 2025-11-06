# React + FastAPI + SQLite Starter

A tiny full‑stack starter you can demo in an interview: **React (Vite)** UI, **FastAPI** backend, **SQLite** persistent DB.
Runs with **Docker Compose** (zero local installs) or locally with Node + Python.

## Quick Start (no installs, just Docker)
1. Ensure Docker is running.
2. In a terminal at this folder:  
   ```bash
   docker compose up --build
   ```
3. Open: http://localhost:5173
   - API: http://localhost:8000/docs (interactive Swagger)
   - DB file persists under `./backend/data/app.db`

## Local (no Docker)
Terminal 1:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Terminal 2:
```bash
cd frontend
npm install
npm run dev -- --port 5173
```
Open http://localhost:5173

## Online (minimal install)
**Option A: GitHub Codespaces (recommended)**
1. Push this folder to a new GitHub repo.
2. Click **Code → Create codespace on main**.
3. In the codespace terminal: `docker compose up --build`
4. Use forwarded ports (5173 and 8000).

**Option B: Replit (single workspace)**
- Create a new Repl with “Python” template for the backend; add `FastAPI` and `uvicorn` in `poetry.toml` or `requirements.txt`.
- Add a React Vite project as a subfolder and run `npm run build`; serve the built assets via FastAPI’s `StaticFiles` or a simple Replit web server. (See comment in `backend/app/main.py` for static file serving option.)

**Option C: Gitpod**
- Create a repo from this folder, then open in Gitpod and run `docker compose up --build`.

## What’s included
- **CRUD for Items**: title (str), done (bool). Endpoints prefixed with `/api`.
- **SQLite** for persistence via SQLAlchemy. File: `backend/data/app.db`.
- **Vite proxy**: Frontend calls `/api/...` locally without CORS issues.
- **Swagger UI**: http://localhost:8000/docs

## Useful commands
Recreate DB from scratch:
```bash
rm -f backend/data/app.db && docker compose up --build
```

Good luck with the interview!
