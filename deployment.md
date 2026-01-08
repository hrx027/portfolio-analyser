# Deployment Guide

This guide provides instructions for deploying the Portfolio Analyzer application using Docker Compose (recommended), Manual Deployment, or Cloud Platforms (Render & Vercel).

## Option 1: Docker Compose (Recommended for VPS/Local)

This method builds both the backend and frontend into containers and orchestrates them together.

### 1. Configure Environment Variables
Open `docker-compose.yml` and update the environment variables for the `backend` service if needed.

### 2. Build and Run
Run the following command in the project root directory:

```bash
docker-compose up -d --build
```

### 3. Access the Application
- **Frontend**: `http://localhost`
- **Backend API**: `http://localhost:8000/docs`

---

## Option 2: Render (Backend) & Vercel (Frontend)

This is the easiest way to deploy for free/cheap without managing a server.

### Part 1: Deploy Backend on Render

1.  **Push your code to GitHub**.
2.  **Create a Web Service on Render**:
    - Connect your GitHub repo.
    - **Root Directory**: `backend`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3.  **Environment Variables**:
    - Add `JWT_SECRET_KEY` (generate a secure random string).
    - Add `DATABASE_URL` (see Database section below).
    - Add `PYTHON_VERSION` = `3.9.0` (optional, but good for stability).
4.  **Database**:
    - **Recommended**: Create a **PostgreSQL** database on Render. Copy the "Internal Database URL" and paste it as the `DATABASE_URL` environment variable in your Web Service.
    - *Note*: If you don't provide a `DATABASE_URL`, it will default to SQLite, but your data will be lost every time the server restarts (ephemeral storage).
5.  **Deploy**: Click "Create Web Service".
6.  **Copy Backend URL**: Once deployed, copy the URL (e.g., `https://my-api.onrender.com`).

### Part 2: Deploy Frontend on Vercel

1.  **Import Project in Vercel**:
    - Connect your GitHub repo.
    - Select the `frontend` directory as the **Root Directory**.
    - **Framework Preset**: Vite (should be detected automatically).
2.  **Environment Variables**:
    - Add `VITE_API_URL` with the value of your Render Backend URL (e.g., `https://my-api.onrender.com`).
    - **Important**: Do not add a trailing slash.
3.  **Deploy**: Click "Deploy".
4.  **Visit**: Your app is now live!

### Notes

- **CORS**: The backend is configured to allow all origins (`allow_origins=["*"]`) in `main.py` by default. This is fine for testing but should be restricted to your Vercel domain in production.
- **Database Migrations**: When using PostgreSQL, the app will automatically create tables on startup if they don't exist (via `models.Base.metadata.create_all(bind=engine)` in `main.py`).

---

## Option 3: Manual Deployment

If you prefer running services directly on a server (e.g., Ubuntu VPS).

### Backend
1.  **Install Python 3.9+** and `pip`.
2.  **Navigate to backend**: `cd backend`
3.  **Create venv**: `python3 -m venv venv`
4.  **Activate venv**: `source venv/bin/activate`
5.  **Install dependencies**: `pip install -r requirements.txt`
6.  **Run with Gunicorn**:
    ```bash
    pip install gunicorn
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
    ```

### Frontend
1.  **Install Node.js 18+**.
2.  **Navigate to frontend**: `cd frontend`
3.  **Install dependencies**: `npm install`
4.  **Build**: `npm run build`
5.  **Serve**: Use Nginx/Apache to serve `dist/`.
    - **Nginx Config**: Proxy `/api` requests to `http://localhost:8000`.
