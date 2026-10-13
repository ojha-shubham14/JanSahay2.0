# JanSahay

### Tell us what you need. We'll show you your options.

JanSahay is a need-first platform that helps people discover government
financial assistance without knowing a scheme's name. Choose a need such as
education, business, agriculture or housing, answer a few simple questions,
and see programs that may fit, why they match, what still needs checking,
and what to do next.

> **Status:** MVP in development (started October 2026).

> **Disclaimer:** JanSahay is an information and decision-support tool. It does
> not approve applications or guarantee eligibility, funding or benefits.
> Final decisions rest with the implementing authority.

---

## Why JanSahay?

Finding the right assistance is a navigation problem. Information is scattered,
eligibility rules are hard to read, and it is unclear where to apply. JanSahay
guides users from a financial need to clear next steps.

## Features (MVP)

- **Need-first discovery:** start from what you need, not a scheme name
- **Simple questionnaire:** only the information relevant to your need
- **Rule-based matching:** deterministic and testable, with no AI deciding eligibility
- **Explainable results:** each rule shown as satisfied, not satisfied, or needs verification
- **Source-backed data:** every program shows its official source and last-verified date
- **Next steps:** documents, application steps and the official application link
- **Admin panel:** authorized admins add, edit, publish and archive programs
- **Privacy-minded:** your answers are not stored

## Roadmap

- [ ] EMI / repayment calculator
- [ ] Program comparison and document checklists
- [ ] Multilingual interface (Kannada, Hindi)
- [ ] Provider and office locator
- [ ] Natural-language input (AI used only to read user text, never to decide eligibility)

## How it works

```
Need -> Questions -> Rule engine -> Results with explanations -> Source and next steps
```

1. The user picks a need and answers a few questions.
2. The backend loads published programs and their eligibility rules from PostgreSQL.
3. A pure rule engine checks each rule and returns satisfied, not satisfied or needs verification. A missing answer is never treated as eligible.
4. The user sees grouped, explained results with sources and verification dates.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Tailwind CSS (Vite) |
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| Testing | pytest, Vitest |

## Project Structure

```
jansahay/
  backend/    FastAPI app, rule engine, migrations, seed data, tests
  frontend/   React + TypeScript app
  docs/       requirements, ER diagram, API docs, data sources, test plan
  DECISIONS.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16

### 1. Clone

```bash
git clone https://github.com/<your-username>/jansahay.git
cd jansahay
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then fill in your values
```

Create the database (for example `jansahay_dev`), then:

```bash
alembic upgrade head              # create tables
python seed/seed.py               # load curated programs
uvicorn app.main:app --reload     # http://localhost:8000/docs
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev                       # http://localhost:5173
```

### Environment variables

| Variable | Where | Example |
|---|---|---|
| `DATABASE_URL` | backend | `postgresql+psycopg://user:password@localhost:5432/jansahay_dev` |
| `JWT_SECRET` | backend | a long random string |
| `CORS_ORIGINS` | backend | `http://localhost:5173` |
| `VITE_API_BASE_URL` | frontend | `http://localhost:8000/api/v1` |

Never commit your real `.env` file.

## Running Tests

```bash
cd backend && pytest
cd frontend && npm test
```

## Data and Sources

Program records are curated by hand from official sources. Each record stores
its source URL, issuing authority and last-verified date. The dataset is small
on purpose and does not claim to list every scheme. See
[`docs/data-sources.md`](docs/data-sources.md).

## Documentation

- [Requirements](docs/requirements.md)
- [Decision log](DECISIONS.md)
- [API reference](docs/api.md) (also at `/docs` when the backend is running)
- [Test plan](docs/test-plan.md)

## Limitations

- Covers only the programs in its curated database
- No live government integrations
- Cannot submit applications or track their status
- A match is preliminary and informational, not an official decision

## Screenshots

_Add 3-4 screenshots here once the UI works: home, questionnaire, results, program detail._

## Contributing

This is a college project, but feedback and suggestions are welcome through
issues. Follow the commit and branch conventions in `DECISIONS.md`.

## License

MIT (add a `LICENSE` file), or state another license.
