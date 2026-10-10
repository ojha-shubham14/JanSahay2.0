# JanSahay: Decision Log

A short record of the important choices made in this project, why they were made, and what they cost.
Add a new entry whenever a design choice changes.

**Status values:** `Accepted` (frozen) | `Proposed` (confirm before relying on it) | `Superseded` | `Deferred`

---

## Index

| ID | Decision | Status |
|----|----------|--------|
| D-001 | Dedicated repository and project structure | Accepted |
| D-002 | Product is a navigation tool, not an approval authority | Accepted |
| D-003 | Frontend: React + TypeScript + Tailwind (Vite) | Accepted |
| D-004 | Backend: Python + FastAPI + Pydantic | Accepted |
| D-005 | Database: PostgreSQL 16 with SQLAlchemy + Alembic | Accepted (confirm) |
| D-006 | Eligibility is rule-based; AI never decides | Accepted |
| D-007 | Rules are stored as data, not code | Accepted |
| D-008 | Rule engine is a pure, isolated module | Accepted |
| D-009 | Three-state rule result; missing answer is never "eligible" | Accepted |
| D-010 | Program outcome logic and ranking | Accepted |
| D-011 | Region handled as a filter before rule evaluation | Accepted |
| D-012 | Assistance type is a first-class field | Accepted |
| D-013 | Every program carries source and freshness metadata | Accepted |
| D-014 | Program lifecycle: draft, published, archived | Accepted |
| D-015 | No public accounts; user answers are not stored | Accepted |
| D-016 | Admin-only authentication with JWT and role check | Proposed |
| D-017 | Audit log for program changes | Accepted |
| D-018 | MVP scope and what is deferred | Accepted |
| D-019 | EMI calculator is a stretch task | Proposed |
| D-020 | Small curated dataset (target 20-25 programs) | Accepted |
| D-021 | API conventions: versioning, error format, status codes | Proposed |
| D-022 | Testing strategy and minimum targets | Accepted |
| D-023 | Git workflow and secrets handling | Accepted |
| D-024 | Staleness window for verification dates | Proposed |
| D-025 | Build workflow: one feature at a time, explain before moving on | Accepted |

---

## D-001: Dedicated repository and project structure
- **Date:** 2026-10-10 | **Status:** Accepted
- **Context:** JanSahay is a new project built from scratch, to be submitted as a college mini project and extended afterwards.
- **Decision:** Create one repository `jansahay` with `backend/`, `frontend/` and `docs/` folders, plus `README.md`, `DECISIONS.md` and `PROJECT-IDEAS.md` at the root.
- **Why:** A single clean repository makes setup, review and evaluation simple, and keeps the project easy to explain and grow.
- **Consequences:** All code, documentation and data live in this repository. Every dependency and design choice is recorded here.

## D-002: Navigation and decision-support tool, not an authority
- **Date:** 2026-10-10 | **Status:** Accepted
- **Context:** Users may mistake a match for approval.
- **Decision:** JanSahay never claims to approve, guarantee, submit or track an application. Results are labelled "preliminary suitability". Final eligibility rests with the implementing authority.
- **Why:** Honesty and trust are the product (see Product Boundaries, NFR-19, NFR-34, NFR-55).
- **Consequences:** Disclaimer on results and detail pages; copy reviewed so no screen says "eligible", "approved" or "submitted".

## D-003: Frontend stack, React + TypeScript + Tailwind (Vite)
- **Date:** 2026-10-10 | **Status:** Accepted
- **Why:** Matches the product spec; TypeScript catches API-shape mistakes early; Tailwind speeds up responsive layout from 360 px.
- **Alternatives considered:** Plain JavaScript (fewer guard rails), Next.js (extra concepts not needed for MVP).
- **Consequences:** Learning curve for TypeScript. Keep types simple and mirror backend schemas in `src/types/`.

## D-004: Backend stack, Python + FastAPI + Pydantic v2
- **Date:** 2026-10-10 | **Status:** Accepted
- **Why:** Automatic Swagger docs, strong request validation, fits the Python learning path and later AI integration.
- **Consequences:** Routers stay thin; business logic lives in `services/` and `matching/`.

## D-005: Database, MySQL 8 with SQLAlchemy 2.x and Alembic
- **Date:** 2026-10-10 | **Status:** Accepted (confirm)
- **Context:** The product spec specifies MySQL. Earlier planning notes may mention a different database.
- **Decision:** Use MySQL 8 as the single source of structured data. All schema changes go through Alembic migrations.
- **Why:** Relational integrity for programs, rules, documents, steps and channels; follows the spec.
- **Alternatives considered:** PostgreSQL (very close fit, easy to switch later because of the ORM).
- **Consequences:** Do not mix two databases. **Action:** confirm this matches the 12-week plan and update whichever document disagrees.

## D-006: Eligibility is rule-based; AI never decides
- **Date:** 2026-10-10 | **Status:** Accepted
- **Why:** Eligibility has financial consequences, so it must be explainable, testable and deterministic. AI interpretation can be wrong.
- **Decision:** The matching engine uses structured program data and defined rules only. AI, if added later, only helps turn free text into structured answers and explain results grounded in the data.
- **Consequences:** No AI in the MVP. A future AI layer sits in front of the engine and cannot override it.

## D-007: Rules are stored as data, not code
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** Each criterion is a row in `eligibility_rules` as `(field_key, operator, value_json, is_mandatory, description, source_note)`.
- **Why:** Admins can add or change programs without a code change or redeploy (spec section 11).
- **Consequences:** `field_key` values must exist in the `questions` table. The admin UI uses dropdowns to prevent typos. Supported operators start small: `eq, neq, in, not_in, gt, gte, lt, lte, between, is_true, is_false`. Add an operator only when a real program needs it.

## D-008: Rule engine is a pure, isolated module
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** `backend/app/matching/` takes programs with rules plus a dictionary of answers and returns structured results. It imports no web framework and no database code.
- **Why:** Easy to unit-test; identical input, data and rule version always give identical output.
- **Consequences:** The service layer loads data and calls the engine; the engine never queries the database.

## D-009: Three-state result; a missing answer is never "eligible"
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** Each rule evaluates to `SATISFIED`, `NOT_SATISFIED` or `NEEDS_VERIFICATION`. If the user did not provide the needed value, the result is `NEEDS_VERIFICATION`.
- **Why:** Treating silence as a pass would produce false hope. This is the core honesty rule of the product (FR-15, FR-17, FR-19).
- **Consequences:** A program with zero recorded rules is shown as needs verification ("criteria not recorded"), never as suitable.

## D-010: Program outcome logic and ranking
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:**
  - Any mandatory rule `NOT_SATISFIED` gives `NOT_MATCHED` (shown separately with reasons).
  - No mandatory failure but at least one mandatory `NEEDS_VERIFICATION` gives `NEEDS_VERIFICATION`.
  - All mandatory rules `SATISFIED` gives `LIKELY_SUITABLE` (always labelled preliminary).
  - Non-mandatory rules never exclude a program; they affect ranking only.
  - Ranking is deterministic: outcome order, then more satisfied rules, then fewer unverified rules, then program id.
- **Why:** Predictable, explainable and testable (FR-18, FR-24).

## D-011: Region handled as a filter before rule evaluation
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** Central programs apply everywhere. State programs apply only when `state_code` matches the user's state. Non-applicable programs are excluded before evaluation.
- **Why:** Keeps rules about the user, and region about the program. Simpler schema and queries (FR-09).

## D-012: Assistance type is a first-class field
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** `assistance_type` is one of `loan, subsidy, grant, scholarship, other` and drives UI labels and (later) comparison.
- **Why:** A scholarship and a loan must never be compared as the same product (FR-11, FR-22 note).

## D-013: Every program carries source and freshness metadata
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** A published program must have `source_url`, `source_authority` and `last_verified_on`, or be explicitly marked "unverified source". Unknown values stay null and show as "Not available". Values are never guessed. `last_verified_on` is the date the maintainer read the source.
- **Why:** Trust over coverage (FR-12, FR-13, FR-44, NFR-16, NFR-17).
- **Consequences:** A database check must return zero published programs without a source or an unverified flag.

## D-014: Program lifecycle, draft, published, archived
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** New programs start as `draft`. Publishing runs required-field validation. Archiving hides a program from the public without deleting it. The public API returns only `published`.
- **Why:** Prevents half-entered or outdated data reaching users (FR-54, FR-55).

## D-015: No public accounts; answers are not stored
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** Questionnaire answers travel in the request, are used for matching and are discarded. They are not saved or logged. Progress may live in browser `sessionStorage` and is cleared at the end of the journey.
- **Why:** Data minimisation and privacy (NFR-29 to NFR-34); less to secure and explain.
- **Consequences:** No saved journeys in the MVP (Future scope). Logs must not contain answer values.

## D-016: Admin-only authentication, JWT with role check
- **Date:** 2026-10-10 | **Status:** Proposed
- **Decision:** Admin accounts are created by a CLI script, not public registration. Passwords are hashed (bcrypt or argon2). Login returns a short-lived JWT; every admin route requires a valid token and role.
- **Why:** Only the admin area needs identity (NFR-22, NFR-23). JWT secret comes from the environment.
- **Open question:** Token storage on the frontend (memory vs httpOnly cookie). Decide in Week 8 and record it here.

## D-017: Audit log for program changes
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** Every create, edit, publish, archive and verify action writes a row to `audit_log` with who, when and a diff.
- **Why:** Traceability of changes to official information (NFR-20, FR-47).

## D-018: MVP scope and deferrals
- **Date:** 2026-10-10 | **Status:** Accepted
- **MVP:** Need selection, questionnaire, MySQL program database, rule-based matching with explanations, program details, official links, admin CRUD, validation and no-match handling, tests, responsive UI.
- **Phase 2:** Program comparison, document checklist page, provider discovery and map, multilingual interface, advanced verification workflow.
- **Future:** AI-assisted input, notifications, official data integrations, saved journeys, application submission or tracking.
- **Rule:** New ideas go to `PROJECT-IDEAS.md`. They are reviewed only after MVP v1.0.

## D-019: EMI calculator is a stretch task
- **Date:** 2026-10-10 | **Status:** Proposed
- **Context:** The spec's MVP Scope section lists EMI as "later", while Functional Requirements section 13 includes it in the MVP.
- **Decision:** Build EMI in Week 9 only if the core journey, exception states and tests are done. It is a pure function with known-value tests and clearly stated assumptions. Drop it without penalty if behind schedule.
- **Test anchors:** Rs. 2,00,000 at 12% for 24 months gives EMI 9,414.69; Rs. 5,00,000 at 9% for 60 months gives EMI 10,379.18.

## D-020: Small curated dataset
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** Target 20-25 programs across business, education, agriculture, housing and skills, including some Karnataka state programs. Each is researched from an official source, never from memory or AI.
- **Why:** A small, trustworthy dataset beats broad, doubtful coverage. The product must not claim to list every scheme.
- **Consequences:** Add 2-3 programs per week from Week 3. Seed script must be idempotent. Keep `docs/data-sources.md` up to date.

## D-021: API conventions
- **Date:** 2026-10-10 | **Status:** Proposed
- **Decision:** Prefix `/api/v1`. Consistent error body `{"error": {"code", "message", "fields"}}`. Correct HTTP codes (200, 201, 401, 403, 404, 422, 500). Public schemas never expose internal fields. The match response includes a `rules_version` string.
- **Why:** Predictable client code and demonstrable determinism.

## D-022: Testing strategy and minimum targets
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** pytest for the engine (30+ tests), EMI (8+, if built) and the API (20+, including admin 401/403). Vitest for key UI parts (5-8). Manual checklist for 360 px, desktop and keyboard-only runs.
- **Why:** NFR-44 requires automated tests for matching, eligibility and calculations. Tests are written with each feature, not at the end.

## D-023: Git workflow and secrets handling
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** `main` always runs. Work on `feature/...` and `fix/...` branches and merge through pull requests, even solo. Commit messages use `feat:`, `fix:`, `test:`, `docs:`. `.gitignore` is added before the first commit. Real `.env` files are never committed; only `.env.example`.
- **Why:** Habit that teams expect, and protection against leaked credentials (NFR-24).

## D-024: Staleness window for verification dates
- **Date:** 2026-10-10 | **Status:** Proposed
- **Decision:** Treat `last_verified_on` older than **180 days** as stale. The UI shows a re-verification warning and the admin list highlights it. The window is a config value, not hard-coded.
- **Why:** Gives FR-13 and FR-48 a concrete, testable meaning. Revisit the number once real programs show how often they change.

## D-025: Build workflow, one feature at a time
- **Date:** 2026-10-10 | **Status:** Accepted
- **Decision:** For every feature: spec it, design it on paper, build one small piece (with AI assistance only for reviewable pieces), read every line, test it, explain it aloud without AI, then commit. A feature is done only when it can be run, explained, modified and debugged without AI.
- **Why:** The project must be defensible in a viva and useful as a portfolio piece.

---

## Template for new entries

```
## D-0XX: Short title
- **Date:** YYYY-MM-DD | **Status:** Proposed / Accepted
- **Context:** What problem or question triggered this?
- **Decision:** What exactly was chosen?
- **Why:** Reasons, and what was rejected.
- **Consequences:** What this makes easier, harder or forbidden.
```