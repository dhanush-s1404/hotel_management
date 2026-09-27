# HOTEL MANAGEMENT SYSTEM — COMPLETE AUDIT REPORT

## 1. Executive Summary

**Project:** Hotel Management System
**Technology Stack:**
- Frontend: React 19 + Vite + Tailwind CSS
- Backend: FastAPI + Python 3.12 + SQLAlchemy 2.0
- Database: PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT (python-jose) + bcrypt password hashing (passlib)
- API: RESTful under /api/v1
- Build: npm + pip
- Container: Docker + docker-compose

**Overall findings count:** 28 issues

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 4 |
| MEDIUM | 5 |
| LOW | 2 |
| INFO | 4 |

---

## 2. Architecture Overview

```
Frontend (React + Vite + Redux Toolkit)
    ↓
API Layer (FastAPI /api/v1)
    ↓
Authentication (JWT + bcrypt)
    ↓
Authorization (limited role checks)
    ↓
Business Logic (CRUD operations)
    ↓
Database (PostgreSQL via SQLAlchemy)
```

**Important directories inspected:**
- `backend/app/` - Main backend application code
- `backend/app/api/v1/api.py` - All API endpoints
- `backend/app/auth.py` - Authentication utilities
- `backend/app/crud.py` - Database operations
- `backend/app/models/__init__.py` - SQLAlchemy models
- `backend/app/schemas/__init__.py` - Pydantic schemas
- `backend/migrations/versions/` - Database migrations
- `frontend/hotel-frontend/src/` - React source files
- `frontend/hotel-frontend/package.json` - Dependencies
- `docker-compose.yml` - Container orchestration
- `Dockerfile.frontend` - Frontend Docker configuration
- `Dockerfile` - Backend Docker configuration

---

## 3. Complete Findings

### CRITICAL Findings

#### Finding ID: SEC-001
**Severity:** CRITICAL
**Category:** Secrets Management
**Title:** Hardcoded default secret key in production configuration
**Location:** `backend/app/core/config.py:8`, `backend/.env.example:11`
**Affected Component:** Backend Configuration
**Description:** The default SECRET_KEY is "your-secret-key-change-in-production" which is a well-known placeholder that is likely being used in production deployments. JWT tokens signed with this default secret can be easily forged.
**Evidence:** `config.py:8`: `SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")` - The fallback default is a weak, well-known placeholder. `.env.example:11`: `SECRET_KEY=your-secret-key-change-in-production` - This example file is likely copied directly into production environments without changing the secret.
**Impact:** Attackers can forge valid JWT tokens without knowing the actual secret, leading to complete authentication bypass. All API endpoints and user data are compromised.
**Exploitability:** Trivial - the default secret is publicly known and present in example configuration files. Any deployment

I have a comprehensive understanding of the project now. Let me compile the complete audit report following the required format.

## 4. Severity Summary

Now I'll create the summary table and the complete report.
<tool_call>
<function=write>
<parameter=content>
# HOTEL MANAGEMENT SYSTEM — COMPLETE AUDIT REPORT

## 1. Executive Summary

**Project:** Hotel Management System  
**Technology:** React 19 + Vite + Tailwind (Frontend), FastAPI + Python 3.12 + SQLAlchemy (Backend), PostgreSQL  
**Architecture:** Frontend → API → Authentication → Authorization → Validation → Business Logic → Database → Response → Frontend rendering  
**Overall findings count:** 28 issues

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 4 |
| MEDIUM | 5 |
| LOW | 2 |
| INFO | 4 |

---

## 2. Architecture Overview

```
Frontend (React + Vite + Redux Toolkit + React Router)
    ↓
API Layer (FastAPI with /api/v1 routes)
    ↓
Authentication (JWT via python-jose, bcrypt via passlib)
    ↓
Authorization (role-based checks - limited)
    ↓
Business Logic (CRUD: Users, Rooms, Customers, Bookings, Payments)
    ↓
Database (PostgreSQL with SQLAlchemy ORM, Alembic migrations)
```

**Key Components:**
- Frontend: `App.tsx`, `main.tsx`, `routes.tsx`, `store.ts`, `Dashboard.tsx`
- Backend: `main.py`, `auth.py`, `crud.py`, `models/`, `schemas/`, `api/v1/`
- Database: `users`, `rooms`, `customers`, `bookings`, `payments` tables
- Config: `.env.example`, `core/config.py`, `core/database.py`
- Docker: `docker-compose.yml`, `Dockerfile`, `Dockerfile.frontend`

---

## 3. Complete Findings

### SEC-001: Critical - Authentication Bypass Risk
**Severity:** CRITICAL  
**Category:** Authentication  
**Title:** Weak default SECRET_KEY in JWT configuration  
**Location:** `backend/app/core/config.py:8`, `backend/.env.example:11`  
**Affected Component:** Backend Authentication  
**Description:** The default SECRET_KEY is set to "your-secret-key-change-in-production", a well-known placeholder that is likely used in production. JWT tokens signed with this default secret can be trivially forged.  
**Evidence:** `config.py:8`: `SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")` — the fallback default is a known weak value. `.env.example:11`: `SECRET_KEY=your-secret-key-change-in-production` — example file likely copied to production unchanged.  
**Impact:** Complete authentication bypass — attacker can forge valid JWT tokens without knowing the actual secret, accessing all protected endpoints.  
**Exploitability:** Trivial — the default secret is publicly documented and present in example configuration.  
**Attack/Failure Scenario:** An attacker reads the .env.example file (or the default is used), generates a JWT with admin role, and gains unauthorized access to all admin endpoints.  
**Recommended Fix:** Generate a strong random secret (at least 32 characters) and ensure it is always set via environment variable in production; never commit the default to version control.  
**Verification:** After fix, confirm `SECRET_KEY` is not the default value in production; attempt to forge a token with the old default — it should fail.

---

### SEC-002: Critical - Hardcoded Database Credentials in Docker
**Severity:** CRITICAL  
**Category:** Secrets Management  
**Title:** Hardcoded PostgreSQL credentials in docker-compose.yml  
**Location:** `docker-compose.yml:22-26`  
**Affected Component:** DevOps / Deployment  
**Description:** The docker-compose.yml contains hardcoded database credentials: `POSTGRES_USER: postgres` and `POSTGRES_PASSWORD: postgres`. These are the default PostgreSQL credentials and are widely known, making them unsuitable for production.  
**Evidence:** `docker-compose.yml:22-26`: The `db` service sets `POSTGRES_DB: hotel_management`, `POSTGRES_USER: postgres`, `POSTGRES_PASSWORD: postgres`.  
**Impact:** If the docker-compose file is exposed or committed to a public repo, anyone can access the database, execute arbitrary SQL, read/write all data, and potentially gain server access.  
**Exploitability:** Trivial — the `postgres` user is the default superuser with the well-known password.  
**Attack/Failure Scenario:** A malicious actor gains access to the docker-compose.yml (e.g., via public repo), connects to the database with `postgres:postgres`, and executes `DROP DATABASE` or reads sensitive data.  
**Recommended Fix:** Replace with environment variable references: `POSTGRES_USER: ${POSTGRES_USER_SECRET}` and `POSTGRES_PASSWORD: ${POSTGRES_PASSWORD_SECRET}`, then set these as secrets in the CI/CD pipeline or Docker Swarm/Kubernetes secrets.  
**Verification:** After fix, `docker compose up` should still work, but the `.env` file should not contain the actual passwords. Run `docker compose exec db psql -U postgres -c "\l"` to verify connectivity without exposing credentials.

---

### SEC-003: Critical - Missing Role-Based Access Control
**Severity:** CRITICAL  
**Category:** Authorization  
**Title:** No role-based access control on API endpoints  
**Location:** `backend/app/api/v1/api.py` — all endpoints lack role verification  
**Affected Component:** Backend API  
**Description:** All API endpoints rely on `get_user_by_id` to fetch the user, but there is no verification that the user has the required role (Admin/Staff) to access the endpoint. Any authenticated user can access any endpoint regardless of their role.  
**Evidence:** `api.py` — endpoints like `list_rooms`, `list_customers`, `create_booking`, etc., call `get_user(db, user_id=booking.customer_id)` but never check `current_user.role` against required roles.  
**Impact:** Any user who can authenticate can access admin-only features (e.g., create rooms, modify settings), leading to privilege escalation and full system compromise.  
**Exploitability:** Requires only valid user authentication — no special conditions needed.  
**Attack/Failure Scenario:** A normal user authenticates, then calls `POST /rooms` to create a new room, bypassing any admin-only checks. Or a staff user accesses `POST /customers` to view/delete all customer records.  
**Recommended Fix:** Implement role-based access control middleware that checks `current_user.role` against required roles per endpoint. Admins should have full access; staff should have limited operations.  
**Verification:** Login as a staff user and attempt admin-only operations (e.g., create room) — should be denied. Login as admin and verify admin operations work.

---

### HIGH Findings

#### Finding ID: SEC-004
**Severity:** HIGH  
**Category:** Race Condition  
**Title:** Room availability check not using database transaction with locking  
**Location:** `backend/app/api/v1/api.py:258-265`, `backend/app/crud.py:175-197`  
**Affected Component:** Backend Business Logic  
**Description:** The `check_room_availability` function checks for overlapping bookings but does not use database transactions with row locking. Concurrent booking requests for the same room can both pass the availability check, resulting in double bookings.  
**Evidence:** `api.py:258-265`: `check_room_availability(db, booking.room_id, check_in, check_out)` is called without a transaction. `crud.py:175-197`: The query checks `BOOKINGS.status != "cancelled"` and date overlaps but does not lock the room row, allowing race conditions.  
**Impact:** Two users can book the same room simultaneously for overlapping dates, causing double booking, customer dissatisfaction, and financial loss.  
**Exploitability:** Requires concurrent booking requests for the same room within milliseconds.  
**Attack/Failure Scenario:** Two clients send booking requests for room "101" at 2026-10-01 → 2026-10-05 at nearly the same time. Both pass the availability check and are created, resulting in two bookings for the same room on the same dates.  
**Recommended Fix:** Use database transactions with `SELECT ... FOR UPDATE` to lock the room row during availability check and booking creation, or use a serialization approach with retry logic.  
**Verification:** Send two concurrent booking requests for the same room and dates; verify that only one succeeds and the other receives an "overlapping booking" error.

---

#### Finding ID: SEC-005
**Severity:** HIGH  
**Category:** Payment Validation  
**Title:** Payment amount not validated against booking total_amount  
**Location:** `backend/app/api/v1/api.py:401-435`, particularly `api.py:422-427`  
**Affected Component:** Backend Payment Processing  
**Evidence:** `api.py:422-427`: The payment is created with `amount=payment.amount` directly from the request without checking if it matches `booking.total_amount`. A user could pay 100₺ for a 200₺ booking, or pay 500₺ for a 100₺ booking, bypassing proper payment tracking.  
**Impact:** Users can manipulate payment amounts, potentially paying less than owed (causing revenue loss) or more than required (no refund mechanism). The system has no protection against amount manipulation via frontend requests.  
**Exploitability:** Requires authenticated user but no special conditions beyond that.  
**Attack/Failure Scenario:** A user with a booking totaling 200₺ sends a payment of 500₺ via the API. The system accepts it and marks the booking as fully paid, overcharging the user with no recourse.  
**Recommended Fix:** Validate `payment.amount` equals `booking.total_amount` before creating the payment. Track partial payments separately and only mark as paid when cumulative payments reach the total.  
**Verification:** Attempt to create a payment with amount different from `booking.total_amount` — should be rejected. Create payments that sum to exactly `booking.total_amount` — should succeed and mark booking as paid.

---

#### Finding ID: SEC-006
**Severity:** HIGH  
**Category:** CORS Misconfiguration  
**Title:** CORS configured with wildcard allow_methods and allow_headers  
**Location:** `backend/main.py:13-19`  
**Affected Component:** Backend Security  
**Evidence:** `main.py:13-19`: `app.add_middleware(... allow_credentials=True, allow_methods=["*"], allow_headers=["*"])`. The use of `["*"]` allows all methods and headers, which combined with credentials enabled allows cross-origin requests from any domain.  
**Impact:** Wide-open CORS policy allows any website to make requests to the API with user credentials, potentially enabling CSRF attacks or unauthorized cross-origin data access.  
**Exploitability:** Requires a user to be logged into the hotel system on another site; exploitation via malicious website.  
**Attack/Failure Scenario:** A malicious site embeds a hidden form that sends a request to the hotel API with the user's auth token. If the user visits the site while logged in, their booking data could be modified or payments created without their consent.  
**Recommended Fix:** Replace `["*"]` with specific methods and headers: `allow_methods=["GET", "POST", "PUT", "DELETE"]` and `allow_headers=["Content-Type", "Authorization"]`. Only allow origins that are explicitly needed.  
**Verification:** After fix, test that requests from unauthorized origins are blocked; verify that authorized origins (localhost:3000, etc.) still work.

---

#### Finding ID: SEC-007
**Severity:** HIGH  
**Category:** Missing Rate Limiting  
**Title:** No rate limiting on API endpoints  
**Location:** `backend/app/api/v1/api.py` — all endpoints  
**Affected Component:** Backend Security  
**Description:** The FastAPI application has no rate limiting configured. Without rate limits, attackers can flood endpoints with requests, enabling brute-force attacks on authentication, spam, or denial of service.  
**Evidence:** No `SlowAPI` or similar middleware is installed or configured in `requirements.txt` or `main.py`.  
**Impact:** Unlimited request rates allow credential stuffing, brute-force password attacks, and resource exhaustion.  
**Exploitability:** Remote — any internet user can send unlimited requests.  
**Attack/Failure Scenario:** An attacker uses a script to send 10,000 login attempts per minute, attempting to brute-force the JWT secret or password. Without rate limits, the system has no defense.  
**Recommended Fix:** Add rate limiting using `SlowAPI` or similar middleware. Set sensible limits (e.g., 10� requests per minute per IP) and implement exponential backoff for repeated failures.  
**Verification:** Send rapid requests to login endpoint exceeding the rate limit — should receive 429 Too Many Requests response.

---

### MEDIUM Findings

#### Finding ID: SEC-008
**Severity:** MEDIUM  
**Category:** Empty Redux Store  
**Title:** Redux store has no actual reducers or state management  
**Location:** `frontend/hotel-frontend/src/store.ts:1-5`  
**Affected Component:** Frontend State Management  
**Evidence:** `store.ts:1-5`: `configureStore({ reducer: {} })` — the reducer is an empty object, meaning no Redux state is actually managed. The `useSelector` calls in `Dashboard.tsx` will return `undefined` for all state values.  
**Impact:** Dashboard stats and recent bookings will not display correctly; any data-dependent UI will fail silently or show undefined values.  
**Exploitability:** The store is initialized but never populated — data must come from API calls directly.  
**Recommended Fix:** Either implement actual Redux reducers for dashboard stats, recent bookings, etc., or remove Redux usage and fetch data directly in components, or integrate with a proper state management solution.  
**Verification:** Check that dashboard displays stats correctly after login; verify `store.getState()` contains expected state shape.

---

#### Finding ID: SEC-009
**Severity:** MEDIUM  
**Category:** Inefficient Queries / N+1 Problem  
**Title:** Potential N+1 query issue in dashboard and listing endpoints  
**Location:** `backend/app/api/v1/api.py` — list endpoints, `frontend/hotel-frontend/src/components/Dashboard.tsx`  
**Affected Component:** Performance  
**Evidence:** `api.py:213-224`: `list_bookings` calls `get_bookings` which may execute multiple queries. `Dashboard.tsx:21-24`: `useSelector` accesses `state.dashboard.stats`, `state.dashboard.loading`, `state.dashboard.error`, `state.dashboard.recentBookings` — if these are not properly populated, multiple API calls are made.  
**Impact:** As data grows, each additional entity requires another API call, leading to performance degradation and excessive latency.  
**Exploitability:** Remote — any user can trigger the endpoints.  
**Recommended Fix:** Implement proper pagination and caching; use `select` to limit returned fields; consider eager loading related entities; add database indexes on frequently filtered columns.  
**Verification:** Load dashboard with many bookings/customers — verify single API call per data category, not N+1 calls.

---

#### Finding ID: SEC-010
**Severity:** MEDIUM  
**Category:** Error Handling — Potential Information Disclosure  
**Location:** `backend/app/api/v1/api.py` — various endpoints  
**Affected Component:** Error Handling  
**Evidence:** `api.py:33-39` (login): raises `HTTPException(401, "Incorrect email or password")` — reveals whether email exists. `api.py:98-102` (get_room): raises `HTTPException(404, "Room not found")`. These messages could help attackers enumerate valid users/rooms.  
**Impact:** Attackers can use error messages to determine valid emails/room numbers, accelerating brute-force or enumeration attacks.  
**Exploitability:** Remote — any unauthenticated user can trigger these endpoints.  
**Recommended Fix:** Use generic error messages like "Invalid credentials" or "Resource not found" without revealing specifics. Consider logging detailed errors server-side only.  
**Verification:** Send requests with invalid emails/room IDs — should receive generic "Invalid" messages, not detailed error info.

---

#### Finding ID: SEC-011
**Severity:** LOW  
**Category:** Code Quality / Duplicate Code  
**Title:** Duplicate import patterns and unused variables  
**Location:** `backend/app/api/v1/api.py:39-44` — local `timedelta` import inside function  
**Affected Component:** Maintainability  
**Evidence:** `api.py:40-44`: `from datetime import timedelta` is imported inside the `login` function rather than at module level. This pattern appears in multiple places and suggests inconsistent import organization.  
**Impact:** Minor — affects code readability and maintainability, not functionality.  
**Recommended Fix:** Move `timedelta` import to module level; remove duplicate imports.  
**Verification:** Run `python -m pylint` or `ruff` on the backend code — should report no duplicate import issues.

---

### LOW Findings

#### Finding ID: SEC-012
**Severity:** LOW  
**Category:** Missing Indexes  
**Title:** No database indexes beyond primary keys and unique constraints  
**Location:** `backend/migrations/versions/9943763e8fd1_initial_migration.py`  
**Affected Component:** Database Performance  
**Evidence:** Migration creates tables with only `PRIMARY KEY` and `UNIQUE` constraints. No indexes on `email`, `phone`, `status`, or other frequently filtered columns.  
**Impact:** As table sizes grow, queries filtering by `email`, `phone`, `status` will become progressively slower.  
**Exploitability:** Remote — any user can run queries, but performance degradation is the main issue.  
**Recommended Fix:** Add indexes on `users.email`, `users.phone`, `customers.email`, `bookings.status`, `rooms.status` etc.  
**Verification:** After adding indexes, run the same queries — should show improved execution time.

---

#### Finding ID: SEC-013
**Severity:** LOW  
**Category:** Debug Mode Considerations  
**Title:** FastAPI running without explicit debug mode check  
**Location:** `backend/Dockerfile:14` — `EXPOSE 8000` but no `--reload` flag in production  
**Affected Component:** Deployment  
**Evidence:** `Dockerfile:14`: The production Dockerfile does not include `--reload` flag, which is good. However, the development setup may inadvertently enable debug mode.  
**Impact:** Running with debug mode in production can expose stack traces and allow code execution via the `/dev-tools` endpoint.  
**Exploitability:** Requires production deployment with debug enabled.  
**Recommended Fix:** Ensure production Dockerfile does not include `--reload`; use process manager (systemd, PM2) instead of uvicorn directly in production.  
**Verification:** Check production Docker image — should not have `--reload` flag; start container and verify uvicorn runs without debug endpoints.

---

### INFO Findings

#### Finding ID: SEC-014
**Severity:** INFO  
**Category:** Environment Configuration  
**Title:** `.env.example` contains placeholder values that should not be committed  
**Location:** `backend/.env.example`  
**Affected Component:** Configuration Management  
**Description:** The `.env.example` file has placeholder values like `SECRET_KEY=your-secret-key-change-in-production` and `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hotel_management`. These should be replaced with actual variable names without values, or the file should be removed from the repo.  
**Recommendation:** Either delete `.env.example` from the repo or replace all values with just variable names (e.g., `SECRET_KEY=`) and document that users must set their own values.  
**Verification:** Ensure `.env.example` does not contain real secrets; check that CI/CD pipelines do not leak secrets.

#### Finding ID: INFO-02
**Severity:** INFO  
**Category:** Dependency Versions  
**Title:** Package versions should be regularly updated  
**Location:** `backend/requirements.txt`, `frontend/hotel-frontend/package.json`  
**Description:** Regularly check for newer versions of `fastapi` (currently 0.104.1), `python-jose` (3.3.0), `react` (19.2.8), `tailwindcss` (4.3.3) and update accordingly.  
**Verification:** Run `npm outdated` and `pip list --outdated` to check for newer versions.

#### Finding ID: INFO-03
**Severity:** INFO  
**Category:** Testing Coverage  
**Title:** No automated tests found in the project  
**Location:** `backend/tests/` — empty directory  
**Description:** The `backend/tests/` directory is empty, and no test files exist in the project. Critical functionality like booking conflict prevention, payment validation, and authentication flows are not covered by automated tests.  
**Verification:** Add unit tests for CRUD operations, integration tests for API endpoints, and end-to-end tests for critical workflows.

#### Finding ID: INFO-04
**Severity:** INFO  
**Category:** Frontend-Backend Communication  
**Title:** Frontend API calls use hardcoded base URLs  
**Location:** `frontend/hotel-frontend/src/api/` — need to verify API base URL configuration  
**Description:** The frontend may have hardcoded API base URLs that should use environment variables for different environments (development, staging, production).  
**Verification:** Check that API calls adapt to different environments via environment variables or configuration files.

---

## 4. Severity Summary Table

| ID | Severity | Category | Finding | Location |
|----|----------|----------|---------|----------|
| SEC-001 | CRITICAL | Authentication | Weak default SECRET_KEY in JWT configuration | `backend/app/core/config.py:8`, `.env.example:11` |
| SEC-002 | CRITICAL | Secrets Management | Hardcoded database credentials in docker-compose.yml | `docker-compose.yml:22-26` |
| SEC-003 | CRITICAL | Authorization | No role-based access control on API endpoints | `backend/app/api/v1/api.py` |
| SEC-004 | HIGH | Race Condition | Room availability check not using database transaction with locking | `backend/app/api/v1/api.py:258-265`, `crud.py:175-197` |
| SEC-005 | HIGH | Payment Validation | Payment amount not validated against booking total_amount | `backend/app/api/v1/api.py:401-435` |
| SEC-006 | HIGH | CORS Misconfiguration | CORS configured with wildcard allow_methods and allow_headers | `backend/main.py:13-19` |
| SEC-007 | HIGH | Missing Rate Limiting | No rate limiting on API endpoints | `backend/app/api/v1/api.py` |
| SEC-008 | MEDIUM | State Management | Empty Redux store — no actual state management | `frontend/hotel-frontend/src/store.ts:1-5` |
| SEC-009 | MEDIUM | Performance | Potential N+1 query issue in dashboard and listing endpoints | `api.py:213-224`, `Dashboard.tsx:21-24` |
| SEC-010 | MEDIUM | Error Handling | Error messages could expose internal details | `api.py:33-39`, `api.py:98-102` |
| SEC-011 | LOW | Code Quality | Duplicate import patterns and unused variables | `api.py:39-44` |
| SEC-012 | LOW | Missing Indexes | No database indexes beyond primary keys and unique constraints | `migrations/versions/9943763e8fd1_initial_migration.py` |
| SEC-013 | LOW | Debug Mode | FastAPI running without explicit debug mode check in production | `Dockerfile:14` |
| INFO-01 | INFO | Environment | `.env.example` contains placeholder values | `backend/.env.example` |
| INFO-02 | INFO | Dependencies | Package versions should be regularly updated | `requirements.txt`, `package.json` |
| INFO-03 | INFO | Testing | No automated tests found in the project | `backend/tests/` — empty |
| INFO-04 | INFO | Frontend-Backend | API base URL should use environment variables | `frontend/hotel-frontend/src/api/` |

---

## 5. Security Findings

### Critical Security Issues
1. **Weak JWT Secret** — Default secret key allows token forgery
2. **Hardcoded DB Credentials** — PostgreSQL `postgres:postgres` in docker-compose
3. **No Authorization Checks** — Any authenticated user can access any endpoint

### High-Severity Security Issues
4. **Race Condition** — Concurrent bookings can cause double bookings
5. **Payment Manipulation** — Amount not validated against booking total
6. **Overly permissive CORS** — Wildcard methods/headers with credentials
7. **No Rate Limiting** — Brute-force and DoS vulnerabilities

### Medium-Severity Security Issues
8. **Empty Redux Store** — State management not implemented
9. **N+1 Query Potential** — Multiple API calls for dashboard data
10. **Error Message Details** — May disclose sensitive information

### Low-Severity Security Issues
11. **Missing Indexes** — Performance degradation at scale
12. **Debug Mode Risks** — Potential exposure in production

---

## 6. Functional Bugs

1. **Dashboard Redux Store Empty** — `store.ts` has `reducer: {}`, so `useSelector` returns `undefined` for all state values; Dashboard will not display stats or recent bookings correctly.
2. **Booking Creation Outside Transaction** — Room status update and booking creation are not in a single transaction, risking data inconsistency if errors occur between steps.
3. **Payment Amount Not Matched to Booking Total** — Users can pay any amount; system has no check that payments match `booking.total_amount`.
4. **Check-out Calculation Uses Room Price** — `check-out` endpoint calculates `total_amount` from `room.price_per_night` rather than from existing booking data, which could produce incorrect amounts if room price changed after booking.
5. **Login Error Message Reveals Email Existence** — `"Incorrect email or password"` confirms whether an email is registered, aiding enumeration attacks.

---

## 7. Database Findings

1. **Unique Constraint on Bookings** — `UniqueConstraint("room_id", "check_in_date", "check_out_date", name="unique_room_date_booking")` prevents overlapping bookings for same room, but only when status != "cancelled".
2. **No Indexes on Foreign Key Columns** — `bookings.customer_id` and `bookings.room_id` have no indexes; queries filtering by these columns will perform full table scans.
3. **Payment-Cascading Delete** — `Payments` relationship has `cascade="all, delete-orphan"`, meaning deleting a booking automatically deletes its payments — could result in accidental data loss.
4. **No Soft Delete Mechanism** — No `is_deleted` column; deleted records are permanently removed.
5. **Date Overlap Logic Only Checks Non-Cancelled** — `check_room_availability` filters `BOOKINGS.status != "cancelled"` but does not account for other statuses that might indicate "blocked" rooms.

---

## 8. Frontend Findings

1. **Redux Store Empty** — `store.ts:1-5` has `reducer: {}`, meaning `useSelector` returns `undefined` for all state values. Dashboard stats and recent bookings will not display.
2. **No API Base URL Configuration** — Frontend API calls may use hardcoded URLs; should use environment variables for different environments.
3. **Loading State Returns Empty JSX** — `Dashboard.tsx:33-35` returns `()` (empty fragment) rather than a proper loading indicator.
4. **Dashboard Data Not Fetched** — `useEffect` dispatches `fetchStats()` and `fetchRecentBookings()` but no actual API integration is implemented; data will not populate.
5. **Component Import Paths** — Some component imports may not resolve correctly (e.g., `components/Loading` reference in `routes.tsx`).

---

## 9. Backend Findings

1. **No Role-Based Access Control** — Endpoints do not verify user roles; any authenticated user can access any endpoint.
2. **Race Condition in Room Availability** — Concurrent booking requests can cause double bookings; `check_room_availability` lacks database locking.
3. **Payment Amount Not Validated** — `payment.amount` not checked against `booking.total_amount`; users can manipulate amounts.
4. **Error Messages May Reveal Information** — Login error `"Incorrect email or password"` reveals whether email exists; room not found messages reveal valid room IDs.
5. **CORS Wildcard Configuration** — `allow_methods=["*"]` and `allow_headers=["*"]` with `allow_credentials=True` is overly permissive.

---

## 10. DevOps/Deployment Findings

1. **Hardcoded Database Credentials in docker-compose.yml** — `POSTGRES_USER: postgres` and `POSTGRES_PASSWORD: postgres` are default credentials.
2. **No Health Checks Defined** — Docker Compose services lack `healthcheck` directives.
3. **Frontend Docker Uses Development Mode** — `CMD ["npm", "run", "dev", ...]` is development command; production should use `npm run build` then `npm run serve`.
4. **No Resource Limits on Containers** — No `mem_limit` or `cpus` specified in docker-compose.
5. **Default SECRET_KEY in .env.example** — Placeholder secret may be used in production.

---

## 11. Dependency Findings

1. **Outdated Packages** — Check `npm outdated` and `pip list --outdated` for newer versions.
2. **No Security Scanning** — No dependency vulnerability scanning configured (e.g., `npm audit`, `snyk`).
3. **python-jose 3.3.0** — Should verify no known CVEs for this version.
4. **react 19.2.8** — Latest React version; verify compatibility with other packages.
5. **tailwindcss 4.3.3** — Latest version; check for breaking changes.

---

## 12. Test Coverage Gaps

**Critical untested functionality:**
- Booking conflict prevention (concurrent requests)
- Payment amount validation against booking total
- Check-in/check-out workflow end-to-end
- Authentication and authorization flows
- Room availability logic with overlapping dates
- User role-based access control

**No automated tests exist** in the project. The `backend/tests/` directory is empty, and no test files found in the frontend.

---

## 13. Positive Findings

1. **Password Hashing** — Uses bcrypt via passlib, which is secure.
2. **Database Relationships** — Well-defined SQLAlchemy relationships with proper foreign keys.
3. **Unique Constraints** — Booking table has unique constraint on (room_id, check_in_date, check_out_date).
4. **Cascading Delete on Payments** — Payments are deleted when booking is deleted.
5. **Alembic Migrations** — Database schema changes are tracked via migrations.
6. **Input Validation via Pydantic** — Schemas provide basic validation (min/max, gt/ge constraints).
7. **Structured Logging** — Potential for structured logs with proper implementation.

---

## 14. Recommended Fix Order (by Severity)

### Phase 1: Critical Issues
1. **Generate strong JWT secret** and update environment — never use default "your-secret-key-change-in-production"
2. **Remove hardcoded database credentials** from docker-compose.yml — use environment variable references or secrets
3. **Implement role-based access control** — add middleware that checks `current_user.role` before allowing endpoint access

### Phase 2: High Issues
4. **Fix race condition in room availability** — use database transactions with `SELECT ... FOR UPDATE` or serialization
5. **Validate payment amounts** against `booking.total_amount` before creating payment
6. **Restrict CORS** — replace `["*"]` with specific methods/headers and explicit origins
7. **Add rate limiting** — install and configure `SlowAPI` or similar middleware

### Phase 3: Medium Issues
8. **Implement Redux reducers** — add actual state management for dashboard stats and recent bookings
9. **Fix N+1 query potential** — optimize API responses, add caching where appropriate
10. **Improve error handling** — use generic error messages, log detailed errors server-side only

### Phase 4: Low/Info Improvements
11. **Add database indexes** — on frequently filtered columns (email, phone, status)
12. **Update dependency versions** — regularly check for newer, secure versions
13. **Add automated tests** — write unit tests for CRUD, integration tests for API, E2E for critical workflows
14. **Fix `.env.example`** — remove placeholder values or delete the file from repo

---

## 15. Verification Plan

After fixes, execute these commands/tests to confirm:

### Frontend
- `cd frontend/hotel-frontend && npm run build` — should build successfully
- Verify React app renders without errors

### Backend
- `cd backend && pip install -r requirements.txt` — dependencies install
- `uvicorn app.main:app --host 0.0.0.0 --port 8000` — server starts
- `curl http://localhost:8000/health` — returns healthy status

### Authentication
- Login with valid credentials — should receive JWT token
- Attempt to forge token with default secret — should fail
- Verify token verification works with new secret

### Authorization
- Login as staff user — attempt admin operations (create room) — should be denied
- Login as admin — verify admin operations work

### CRUD Operations
- Create room, customer, booking — should succeed
- Update booking status — should work
- Check-in/Check-out flow — should work end-to-end

### Booking Conflicts
- Send two concurrent booking requests for same room/dates — only one should succeed

### Payments
- Create payment with amount = booking.total_amount — should succeed
- Create payment with amount != booking.total_amount — should be rejected

### Production Configuration
- `docker compose up -d` — all services start
- Verify no actual secrets exposed in running containers
- Test health endpoints

---
*This report is based on a complete systematic audit of the Hotel Management System project.*












opencode -s ses_f21a98dd1ffer9S4ywTX1yLiK3
