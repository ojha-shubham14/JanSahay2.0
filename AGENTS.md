# JanSahay: rules for AI agents

## What this is
A need-first platform that helps people find government financial assistance (later: recycling help and civic-issue routing). Eligibility is rule-based. It never approves anything or guarantees benefits.

## Stack (do not change)
Frontend: React + TypeScript + Tailwind (Vite). Backend: Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic. Database: PostgreSQL 16. Tests: pytest, Vitest.
Environment: Windows, VS Code, PowerShell. Give commands that work in PowerShell.

## Hard rules
1. Eligibility is decided only by the rule engine in backend/app/matching. It is pure Python and imports no web or database code. Never use an LLM to decide eligibility.
2. A missing answer is NEEDS_VERIFICATION, never eligible.
3. Never invent scheme data, URLs, amounts, dates or document lists. Unknown is null.
4. Matching answers are not stored or logged. (From v1.1, profiles are stored only with user consent.)
5. All SQL goes through SQLAlchemy. Validate input on the server. Secrets only in .env, never in code.
6. Do not add libraries, rename field_keys or change the database schema without asking. Every schema change needs an Alembic migration.
7. Build only the v1.0 core. Do not build anything from PROJECT-IDEAS.md (alerts, recycling, civic router) unless I say so. See DECISIONS.md for past decisions.

## How to work with me
Plan first and wait for my approval. Do one small step at a time, on one feature only. Add or update tests with each change. After coding, explain in simple words what changed and why. Do not refactor files I did not mention. Never edit a test just to make it pass. If unsure, ask me (at most 3 questions).

## Conventions
API prefix /api/v1. Error body {error: {code, message, fields}}. Python type hints everywhere. TypeScript strict mode, no any. Folders: backend/app/{routers,schemas,services,matching,models,core}, frontend/src/{pages,components,api,types,hooks}.