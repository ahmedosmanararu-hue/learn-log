# Running LearnLog locally

Prerequisites:
- Python 3.10+ and pip
- Node.js 18+ and npm

Backend (from repository root):

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
```

2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Copy the example env and adjust if needed:

```bash
cp .env.example .env
```

4. Run the backend:

```bash
python3 backend/run.py
```

Frontend:

1. Install dependencies and run dev server:

```bash
cd frontend
npm install
npm run dev
```

Notes:
- By default the frontend will point to `http://localhost:5001` for the API. Override with `VITE_API_URL` in your frontend environment.
- The backend auto-creates an SQLite database (`learnlog_dev.db`) and seeds example users and courses on first run.
