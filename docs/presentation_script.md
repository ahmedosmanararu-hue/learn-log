# Presentation Script — LearnLog Code Walkthrough

Slide 1 — Title
- Quick intro: your name, role, and purpose of walkthrough.

Slide 2 — Project Overview & Objectives
- Say: "LearnLog is a minimal learning platform allowing users to browse courses, enroll, and leave reviews." 
- Emphasize demo goal: show architecture, auth, and key code paths.

Slide 3 — Tech Stack
- Call out backend stack: Flask + Flask-RESTful, JWT for auth, SQLAlchemy for ORM.
- Frontend: React + Vite, React Router; mention `AuthContext` as central piece.

Slide 4 — Core Architecture
- Explain the separation: React UI issues JSON calls to Flask endpoints; server returns JSON DTOs from `to_dict()` helpers.
- Mention CORS in `create_app()` that allows the frontend dev server to call the backend.
  - File to highlight: `backend/app/__init__.py` (show `db.init_app(app)`, `JWTManager(app)`, `CORS(app)`, and `api.add_resource(...)`).

Slide 5 — Data Flow (diagram)
- Walk through a common flow: user clicks a course -> frontend GET `/courses/<id>` -> backend `CourseDetail` resource loads models and returns a `course.to_dict()` payload.

Slide 6 — Important API Routes
- Quickly open these files (or point at editor tabs):
  - `backend/app/routes/auth.py` — registration & login flow
  - `backend/app/routes/courses.py` — course CRUD and enrollment endpoint
  - `backend/app/routes/enrollments.py` — enrollment updates/status
  - `backend/app/routes/stats.py` — user dashboard stats (show `@jwt_required()` usage)

Slide 7 — Auth Flow
- Show the login form: `frontend/src/pages/Login.jsx` (point to test accounts shown in the UI)
- Show `AuthContext.login()` (frontend/src/context/AuthContext.jsx): highlight the fetch to `http://localhost:5000/auth/login`, storing tokens and user in `localStorage`.
- Show `@jwt_required()` on protected endpoints in the backend to explain server-side checks.

Slide 8 — Database Models
- Open `backend/app/models.py` and point out:
  - `Course` relationships: `lessons`, `reviews`, `enrollments` and cascade behavior
  - `Course.average_rating()` and `to_dict()` — explain how the API shapes JSON returned to the frontend

Slide 9 — Seeding & Demo Data
- Open `backend/app/seed.py` and explain steps: creates users, profiles, courses, lessons, enrollments, and reviews.
- Mention how to run the script locally and that it populates `learnlog_dev.db`.

Slide 10 — Frontend Structure
- Point to `frontend/src/App.jsx` — show route composition and `ProtectedRoute` usage.
- Highlight `CourseDetail.jsx` (how it renders `course.lessons` and reviews) and `Dashboard.jsx` (how it displays `data` from `/dashboard/stats`).

Slide 11 — Key Code Snippets to Show Live
- Backend: `Course.to_dict()` and `create_app()` in `backend/app/__init__.py`.
- Frontend: `AuthContext.login()` and `ProtectedRoute` component.
- Stats: `backend/app/routes/stats.py` — show `DashboardStats.get()` implementation and `TopInstructors` aggregation.

Slide 12 — Demo Plan (live)
- Quick commands to run locally (paste in terminal):

```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
# seed DB
python backend/app/seed.py
# start backend (example)
FLASK_APP=backend/app/run.py flask run --port 5000
# start frontend
cd frontend && npm install && npm run dev
```

Note: Replace commands with your preferred environment management. Explain `JWT_SECRET_KEY` in `backend/app/config.py` and how to set it as env var for production.

Slide 13 — Summary & Q&A
- Walk through key takeaways: clear separation of concerns, JWT auth pattern, helpful model helpers and seed script for demos.
- Invite questions and suggest deeper dives (e.g., adding migrations, production DB, unit tests, or CI).

---

Speaker tips & lines to highlight in code during demo:
- `backend/app/__init__.py`: registration of resources and CORS/JWT setup.
- `backend/app/models.py`: `Course.to_dict()` and `average_rating()` (show how UI displays `average_rating`).
- `frontend/src/context/AuthContext.jsx`: the `login()` fetch and `localStorage` writes.
- `backend/app/routes/stats.py`: demonstrate `@jwt_required()` and how `average_grade` is calculated.

End of script.
