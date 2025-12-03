# FastAPI RBAC Project (Postgres + JWT Access & Refresh)

Instructions:

1. Create a Python virtualenv and activate it.
2. Install requirements: `pip install -r requirements.txt`
3. Create a Postgres database and update `.env` file.
4. Run `python -m app.commands.create_admin` to seed admin user.
5. Start server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8080`

This project uses JWT access tokens and refresh tokens (no OAuth2 flows).