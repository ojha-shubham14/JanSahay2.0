# JanSahay: DECISIONS.md

One entry per decision. To change a decision, add a NEW entry that replaces the old one. Never delete history.
Plan version: Implementation Workflow v2 (12 Oct 2026). Core deadline: v1.0 on Fri 25 Dec 2026.

## Product in one line
Tell us what you need. We'll show you your options, and the right place to go next.

## Releases and goals
| Release | Scope | Target | Priority | Starts only when |
|---|---|---|---|---|
| v1.0 | Need-first financial help: questionnaire, rule engine, explanations, program pages, admin panel, tests, 20+ verified schemes | Fri 25 Dec 2026 | Must | Now |
| v1.1 | User accounts, saved profile (with consent), alerts when eligible, delete my data | Jan 2027 (Weeks 9-10 only if G1 passes) | Should | Gate G1 passed |
| v1.2 | Recycling guide: item to category to where it goes; nearby recyclers | Feb 2027 | Could | v1.1 stable |
| v2 | Civic issue router: right authority, draft complaint, official link | Spring 2027 | Could | v1.2 done |
| v3 | Mediation with municipal bodies | Later | Later | Official agreement or API exists |

## Gate G1 (Fri 27 Nov 2026, end of Week 8)
Go to extras only if ALL are true:
1. A person can finish Need, Questions, Results, Detail without help.
2. I added a program from the admin panel and saw it matched.
3. Rule-engine tests pass.
If not: Weeks 9-12 go to fixing, data and tests. Cut EMI, browse and deployment first. Never cut tests or honest states.

## Golden rules (unchanged)
1. Never let AI move faster than my understanding. A feature is done only when I can run, test, explain, modify and debug it without AI.
2. Rules decide eligibility, never AI. A missing answer is never eligible.
3. Trust over coverage. Never invent scheme data. Unknown stays blank (null).
4. One feature at a time: design on paper, plan with AI, build small, read, test, explain, commit.
5. Do not claim what is not built: no fake Apply button, no fake "submitted", no fake mediation.

## Decisions

### D-005 | Database is PostgreSQL | Active
- Reason: relational integrity, transactions, JSONB for rule values, PostGIS later.
- Action: fix the product spec. Replace MySQL with PostgreSQL in the technology table and the MVP scope text.

### D-015 | Answers storage | Changed 12 Oct 2026
- Old: answers are never stored.
- New: matching answers are still NOT stored or logged. From v1.1, a profile is stored only after the user creates an account and gives consent.

### D-016 | Authentication | Changed 12 Oct 2026
- Old: admin-only authentication.
- New: admin accounts stay as they are. From v1.1 there is a separate `user` role, with email verification.

### D-018 | MVP scope and deferrals | Changed 12 Oct 2026
- Added the release plan above.
- Alerts, recycling and civic router are roadmap items, NOT v1.0.

### D-026 | Module pattern | New 12 Oct 2026
- Every module (schemes, recyclers, civic channels) stores: authority, channel, source URL, last_verified_on, status.
- New modules get their own tables. Do NOT build a generic engine now.

### D-027 | Route, do not mediate | New 12 Oct 2026
- Civic features guide the user to the right official channel and link out.
- Mediation (v3) needs a formal agreement or official API.

### D-028 | Recycling uses PostGIS | New 12 Oct 2026
- Nearby search uses PostgreSQL's PostGIS extension. Navigation opens Google Maps or OpenStreetMap. No turn-by-turn.

### D-029 | EMI calculator is a stretch task | New 12 Oct 2026
- Product spec conflict: MVP Scope says "later", Functional Requirements says MVP.
- Decision: small stretch task in Week 9. Pure function, 8+ tests. Drop it without guilt if behind.

### D-030 | Frozen tech stack | New 12 Oct 2026
- Frontend: React + TypeScript + Tailwind (Vite). Backend: Python 3.11+, FastAPI, Pydantic v2.
- Database: PostgreSQL 16, SQLAlchemy 2.x + Alembic. Auth: JWT + bcrypt or argon2.
- Tests: pytest + httpx, Vitest + React Testing Library.
- Tools: Git/GitHub, VS Code or Antigravity, Swagger, pgAdmin, .env files.
- Changing any item needs a written reason here.

### D-031 | AI usage | New 12 Oct 2026
- AI is a build helper only. It never decides eligibility, never supplies scheme facts.
- Scheme data is read by humans from official pages only.
- One agent per repo at a time. Commit before every agent run. One feature per branch.

### D-032 | Rule engine is isolated | New 12 Oct 2026
- `backend/app/matching` is pure Python. No web or database imports.
- Three states: SATISFIED, NOT_SATISFIED, NEEDS_VERIFICATION.
- Zero-rule program = NEEDS_VERIFICATION. Ranking is deterministic.

### D-033 | Data quality rules | New 12 Oct 2026
- Every published program has: official source URL, section, last_verified_on (date I read it), status.
- Unclear or discontinued schemes stay draft or archived. Never published as active.
- Staleness window: 180 days, then is_stale = true.
- A channel is "verified" only if I reached the official page for that program.

### D-034 | Git rules | New 12 Oct 2026
- `main` always runs. Branches: feature/..., fix/..., docs/...
- Pull request for every feature, squash and merge after reading the diff.
- Commit format: type(scope): summary (feat, fix, test, docs, refactor, chore).
- .gitignore before the first commit: .env, venv, node_modules, __pycache__, dist, *.dump.

## What JanSahay will never do
- Approve applications or promise money.
- Claim to list every scheme.
- Submit applications or track status without a real integration.
- Let AI decide eligibility.
- Claim to mediate without an official agreement.

## Parked ideas
New ideas go in PROJECT-IDEAS.md. Do not build them before Gate G1.

## Note
Decisions D-001 to D-004, D-006 to D-014 and D-017, D-019 to D-025 come from my earlier file. Copy them below this line before committing.