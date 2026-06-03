Automated AI Lead Responder (Micro-SaaS Starter)

This project is a starter Micro-SaaS: an Automated AI Lead Responder for local service businesses.

Quick features:
- FastAPI backend with a `/api/leads` webhook to accept incoming leads
- SQLAlchemy-based DB (`SQLite` by default) with easy switch to Postgres/Supabase
- Background AI responder placeholder (OpenAI integration)
- Minimal HTML dashboard to view leads

Getting started (local, quick):

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy environment variables:

```powershell
copy .env.example .env
# Edit .env to set OPENAI_API_KEY, DATABASE_URL, TWILIO_ACCOUNT_SID,
# TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, DASHBOARD_PASSWORD, and SECRET_KEY
```

3. Run the app:

```powershell
uvicorn app.main:app --reload
```

4. Open http://127.0.0.1:8000 in your browser.

The app now includes a secure owner login. Use the password from `DASHBOARD_PASSWORD` in your `.env` file to access `/dashboard`.

If you have not created a `.env` file yet, the local default password is `changeme`.

Switching to Postgres / Supabase:
- Set `DATABASE_URL` in `.env` to your Postgres connection (e.g. from Supabase).
- Install the `psycopg2-binary` package (already listed in requirements).

Next steps I can do for you:
- Deploy to a free host (Render, Fly, or Supabase Functions)
- Wire SMS sending (Twilio) or SMS via an SMS gateway
- Connect to your Supabase DB and create production secrets
- Help price, market, and reach local contractors

Deployment Notes:
- A `render.yaml` file is included in the project root to deploy this app to Render.
- Set `DATABASE_URL` to your Supabase Postgres connection string for the live database.
- Add `OPENAI_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `DASHBOARD_PASSWORD`, and `SECRET_KEY` in Render.
