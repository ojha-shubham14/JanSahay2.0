# F3: Database tables

Goal: Make all 8 v1.0 tables in PostgreSQL using Python.

Use: SQLAlchemy 2, Alembic, pytest. Database: jansahay_dev.
Put code in: backend/ (models in backend/app/models).

Do these:
1. Make one SQLAlchemy model for each table below.
2. Read DATABASE_URL from .env. Put only a fake example in .env.example.
3. Make the first Alembic migration that creates all 8 tables.
4. Write 2 pytest tests.

Tables (use exactly these names and columns):
- categories: id, name
- admin_users: id, email, password_hash
- programs: id, category_id, created_by, name, benefit_summary, status, last_verified_on
- questions: id, key, text, answer_type
- eligibility_rules: id, program_id, question_id, operator, value
- documents: id, program_id, name
- application_steps: id, program_id, step_no, description
- program_sources: id, program_id, title, url

Rules:
- id is the primary key in every table.
- program_id, category_id, created_by, question_id are foreign keys.
- Do not add any extra table or column.
- Do not make a table for user answers.
- Never put a real password in any file that goes to git.

Do NOT do now (out of scope):
- Real scheme data
- Admin login and "add a program" API
- Eligibility engine and frontend pages
- User accounts and saved profiles (v1.1)
- Alerts and notifications (v1.1)
- Recycling and civic router tables (v1.2 and v2)
- add anyother thing which are not mentioned in this for now. 

Tests:
- Save a program with a category, then read it back.
- Save a rule that links one program and one question.

Done when: the migration runs, all 8 tables exist, 2 tests pass.
If anything is unclear, ask me. Do not guess.
