---
marp: true
theme: default
class: lead

# LearnLog — Code Walkthrough

**Presenter:** Project Team • **Duration:** 20–30 min

---

## Project Overview & Objectives

- **What is LearnLog?** A learning platform to create and enroll in courses, track progress, and leave reviews.
- **Objectives for this walkthrough:** Understand core architecture, auth flow, API surface, data model, and frontend integration.

---

## Tech Stack

- **Backend:** Flask, Flask-RESTful, Flask-JWT-Extended, Flask-CORS, SQLAlchemy
- **Frontend:** React + Vite, React Router, custom hooks and context for auth
- **DB & Dev tooling:** SQLite (dev), SQLAlchemy models, `seed.py` for demo data, optional Flask-Migrate

---

## Core Architecture (High level)

- Browser UI (React) -> REST API (Flask) -> Database (SQLAlchemy)
- Auth: JWT access & refresh tokens stored in localStorage; `AuthContext` manages state
- Routes grouped by domain in `backend/app/routes/` (auth, courses, enrollments, reviews, stats)

---

## Data Flow (mermaid)

```mermaid
flowchart LR
  A[Browser / React UI] -->|HTTP JSON| B(API: Flask Restful)
  B --> C[Auth Routes (auth.py)]
  B --> D[Course Routes (courses.py)]
  B --> E[Enrollments (enrollments.py)]
  B --> F[Reviews (reviews.py)]
  B --> G[(Database via SQLAlchemy)]
```

---

## Important API Routes — Mapping

- `POST /auth/register` & `POST /auth/login` — backend/app/routes/auth.py
- `GET /courses`, `GET /courses/<id>`, `POST /courses` — backend/app/routes/courses.py
- `POST /courses/<id>/enroll`, `PUT /enrollments/<id>` — backend/app/routes/enrollments.py
- `GET /reviews`, `GET /reviews/<id>` — backend/app/routes/reviews.py
- `GET /dashboard/stats`, `GET /instructors/top` — backend/app/routes/stats.py

---

## Auth Flow (high-level)

1. User logs in via frontend form -> `AuthContext.login()` posts to `/auth/login`.
2. Server validates credentials, issues JWT `access_token`, `refresh_token` and returns user payload.
3. Frontend stores tokens and user in `localStorage` and sets context state.
4. Protected API routes use `@jwt_required()` to authorize requests.

See code in: frontend/src/context/AuthContext.jsx and backend/app/routes/auth.py.

---

## Database Models — Overview

- Key models are in backend/app/models.py: `User`, `Profile`, `Course`, `Lesson`, `Enrollment`, `Review`.
- Notable patterns:
  - Relationships: `Course.lessons`, `Course.reviews`, `Course.enrollments` (cascade deletes)
  - Convenience methods: `Course.average_rating()`, `Course.to_dict(include_details=False)`

---

## Data Seeding & Demo Data

- Seeding script: backend/app/seed.py
  - Drops and recreates DB, creates demo users (students, instructors, admin), profiles, courses, lessons, enrollments, and reviews.
  - Use `python backend/app/seed.py` (or run it directly) in dev to populate `learnlog_dev.db`.

---

## Frontend Structure

- Root: `frontend/src/` — `App.jsx` wires routes and `AuthProvider`.
- `context/AuthContext.jsx` handles login/logout and token storage.
- `hooks/useFetch.jsx` abstracts GET calls to API endpoints.
- Pages: `CourseList`, `CourseDetail`, `CourseCreate`, `Dashboard`, `Login`, `Register`.

---

## Key Implementation Notes — Backend

- `create_app()` in backend/app/__init__.py initializes Flask, SQLAlchemy, JWT, CORS, and registers API resources.
- JWT config and token lifetimes are in backend/app/config.py.
- Example useful snippet to show during demo: `Course.to_dict()` and `average_rating()` in backend/app/models.py.

---

## Key Implementation Notes — Frontend

- `AuthContext.login()` (frontend/src/context/AuthContext.jsx) posts credentials, saves `access_token`, `refresh_token`, and `user` to `localStorage`, sets context state.
- `ProtectedRoute` guards routes by checking auth context.
- `useFetch` is used to load dashboard stats and course data (examples: frontend/src/pages/Dashboard.jsx, frontend/src/pages/CourseDetail.jsx).

---

## Demo Plan (live)

1. Show repo layout quickly (backend/ and frontend/).
2. Start server (explain environment variables in backend/app/config.py).
3. Run `seed.py` to populate DB and show sample accounts (email/passwords in UI login page).
4. Show login flow and Dashboard (frontend) -> inspect network calls to `/auth/login` and `/dashboard/stats`.
5. Inspect `CourseDetail` page and backend `Course.to_dict()` mapping.

---

## Summary & Q&A

- Recap: small, clear separation between frontend and backend; JWT auth; SQLAlchemy models with helpful helper methods; seed data for demos.
- Open for technical questions or deeper code walkthroughs.

---

<!-- End of slides -->
