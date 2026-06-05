from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import db, crud, schemas, auth
from .auth import is_admin_authenticated, is_client_authenticated, admin_login_response, admin_logout_response, client_login_response, client_logout_response, get_client_id_from_session

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = str(BASE_DIR / "static")
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.on_event("startup")
def startup():
    try:
        db.init_db()
    except Exception as exc:
        print("Application startup failed during database initialization:", exc)
        raise


def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# ========== ROOT & STATUS ==========

@app.get("/")
def root(request: Request):
    if is_admin_authenticated(request):
        return RedirectResponse(url="/admin/dashboard")
    elif is_client_authenticated(request):
        return RedirectResponse(url="/client/dashboard")
    else:
        return RedirectResponse(url="/client/login")

@app.get("/status")
def status():
    return {"status": "ok", "message": "AI Lead Responder is running"}

# ========== ADMIN ROUTES ==========

@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page():
    return HTMLResponse("""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="/static/styles.css" />
        <title>Admin Login</title>
      </head>
      <body class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-slate-100">
        <div class="flex min-h-screen items-center justify-center px-4 py-10 sm:px-6 lg:px-8">
          <div class="w-full max-w-2xl space-y-8 rounded-[2.5rem] border border-white/10 bg-slate-950/95 p-10 shadow-2xl shadow-slate-950/60 backdrop-blur-xl">
            <div class="text-center">
              <p class="text-xs uppercase tracking-[0.4em] text-sky-300/80">Master Admin</p>
              <h1 class="mt-4 text-5xl font-semibold tracking-tight text-white sm:text-6xl">Admin Login</h1>
              <p class="mx-auto mt-4 max-w-xl text-sm leading-7 text-slate-400 sm:text-base">
                Manage all clients, generate access credentials, and monitor platform usage.
              </p>
            </div>

            <div class="rounded-[2rem] border border-slate-800 bg-slate-900/90 p-8 shadow-inner shadow-slate-950/20">
              <form class="space-y-6" method="post" action="/admin/login">
                <div>
                  <label for="password" class="block text-sm font-medium text-slate-300">Admin password</label>
                  <div class="mt-3">
                    <input id="password" name="password" type="password" required class="w-full rounded-3xl border border-slate-700 bg-slate-950/90 px-5 py-4 text-base text-slate-100 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30" placeholder="Enter admin password" />
                  </div>
                </div>
                <button type="submit" class="inline-flex w-full items-center justify-center rounded-3xl bg-gradient-to-r from-sky-500 to-cyan-400 px-6 py-4 text-base font-semibold text-slate-950 shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-cyan-300">
                  Sign in
                </button>
              </form>
              <p class="mt-4 text-sm text-rose-400">{{error}}</p>
            </div>
          </div>
        </div>
      </body>
    </html>
    """.replace("{{error}}", ""))

@app.post("/admin/login")
def admin_login(password: str = Form(...)):
    if auth.verify_admin_password(password):
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        return admin_login_response(response)
    return RedirectResponse(url="/admin/login", status_code=303)

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    if not is_admin_authenticated(request):
        return RedirectResponse(url="/admin/login")
    
    clients = crud.get_all_clients(db)
    clients_html = ""
    for client in clients:
        leads_count = len(client.leads) if client.leads else 0
        clients_html += f"""
        <tr class="hover:bg-slate-900/80">
          <td class="px-6 py-4 font-semibold text-slate-100">{client.client_id}</td>
          <td class="px-6 py-4 text-slate-200">{client.name}</td>
          <td class="px-6 py-4 text-slate-400">{leads_count}</td>
          <td class="px-6 py-4 text-slate-400">{client.created_at.strftime('%Y-%m-%d %H:%M') if client.created_at else 'N/A'}</td>
        </tr>
        """
    
    if not clients_html:
        clients_html = '<tr><td colspan="4" class="px-6 py-8 text-center text-sm text-slate-500">No clients yet. Create one below.</td></tr>'
    
    return HTMLResponse(f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="/static/styles.css" />
        <title>Admin Dashboard</title>
      </head>
      <body class="bg-slate-950 text-slate-100">
        <div class="min-h-screen">
          <header class="bg-slate-950/95 border-b border-slate-800/80 backdrop-blur-xl shadow-lg shadow-slate-950/20">
            <div class="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-5 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
              <div>
                <p class="text-sm uppercase tracking-[0.28em] text-sky-300/70">Master Admin</p>
                <h1 class="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">Client Management</h1>
                <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">Manage all clients and generate secure access credentials.</p>
              </div>
              <a href="/admin/logout" class="inline-flex items-center rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800">Logout</a>
            </div>
          </header>

          <main class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
            <section class="mb-8">
              <div class="rounded-[2rem] bg-slate-900/95 p-6 shadow-2xl shadow-slate-950/20 ring-1 ring-white/5">
                <h2 class="text-2xl font-semibold text-white mb-6">Create New Client</h2>
                <form id="createClientForm" class="grid gap-4 sm:grid-cols-[1fr_0.8fr]">
                  <input id="clientName" name="client_name" type="text" placeholder="Client business name" required class="rounded-3xl border border-slate-700 bg-slate-950/90 px-5 py-4 text-sm text-slate-100 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-500/20" />
                  <button type="submit" class="rounded-3xl bg-gradient-to-r from-emerald-500 to-teal-400 px-5 py-4 text-sm font-semibold text-slate-950 transition hover:from-emerald-400 hover:to-teal-300">Create Client</button>
                </form>
                <div id="clientResult" class="mt-4 hidden rounded-3xl bg-slate-950/90 p-4 text-sm text-emerald-300 border border-emerald-500/30"></div>
              </div>
            </section>

            <section>
              <div class="rounded-[2rem] bg-slate-900/95 p-6 shadow-2xl shadow-slate-950/20 ring-1 ring-white/5">
                <h2 class="text-2xl font-semibold text-white mb-6">All Clients</h2>
                <div class="overflow-hidden rounded-[1.75rem] border border-slate-800 bg-slate-950/90">
                  <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-800 text-left text-sm text-slate-300">
                      <thead class="bg-slate-900 text-slate-400">
                        <tr>
                          <th class="px-6 py-4 font-semibold uppercase tracking-[0.2em]">Client ID</th>
                          <th class="px-6 py-4 font-semibold uppercase tracking-[0.2em]">Name</th>
                          <th class="px-6 py-4 font-semibold uppercase tracking-[0.2em]">Leads</th>
                          <th class="px-6 py-4 font-semibold uppercase tracking-[0.2em]">Created</th>
                        </tr>
                      </thead>
                      <tbody id="clientTable" class="bg-slate-950 divide-y divide-slate-800">
                        {clients_html}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </section>
          </main>
        </div>

        <script>
          document.getElementById('createClientForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const name = document.getElementById('clientName').value;
            const res = await fetch('/api/admin/clients', {{
              method: 'POST',
              headers: {{'Content-Type': 'application/json'}},
              body: JSON.stringify({{name: name}})
            }});
            const data = await res.json();
            const resultDiv = document.getElementById('clientResult');
            if (res.ok) {{
              resultDiv.innerHTML = `<strong>✓ Client created!</strong><br/>Client ID: <code>${{data.client_id}}</code><br/>Password: <code>${{data.password}}</code><br/><small>Share these securely with the client.</small>`;
              resultDiv.classList.remove('hidden');
              document.getElementById('clientName').value = '';
              location.reload();
            }} else {{
              resultDiv.innerHTML = 'Error creating client.';
              resultDiv.classList.remove('hidden');
            }}
          }});
        </script>
      </body>
    </html>
    """)

@app.get("/admin/logout")
def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    return admin_logout_response(response)

# ========== CLIENT ROUTES ==========

@app.get("/client/login", response_class=HTMLResponse)
def client_login_page():
    login_file = TEMPLATE_DIR / "login.html"
    return HTMLResponse(login_file.read_text(encoding="utf-8").replace("{{error}}", ""))

@app.post("/client/login")
def client_login(client_id: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    login_file = TEMPLATE_DIR / "login.html"
    html = login_file.read_text(encoding="utf-8")
    
    db_client = crud.verify_client_password(db, client_id, password)
    if db_client:
        response = RedirectResponse(url="/client/dashboard", status_code=303)
        return client_login_response(response, db_client.id)
    
    return HTMLResponse(html.replace("{{error}}", "Invalid client ID or password."), status_code=401)

@app.get("/client/dashboard", response_class=HTMLResponse)
def client_dashboard(request: Request, db: Session = Depends(get_db)):
    if not is_client_authenticated(request):
        return RedirectResponse(url="/client/login")
    
    client_db_id = get_client_id_from_session(request, db)
    client = crud.get_client_by_id(db, client_db_id)
    if not client:
        return RedirectResponse(url="/client/login")
    
    dashboard_file = TEMPLATE_DIR / "index.html"
    html = dashboard_file.read_text(encoding="utf-8")
    return HTMLResponse(html)

@app.get("/client/logout")
def client_logout():
    response = RedirectResponse(url="/client/login", status_code=303)
    return client_logout_response(response)

# ========== API ROUTES (Client-specific) ==========

@app.post("/api/leads")
def receive_lead(lead: schemas.LeadCreate, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    if not is_client_authenticated(request):
        return {"status": "error", "message": "Not authenticated"}
    
    client_db_id = get_client_id_from_session(request, db)
    db_lead = crud.create_lead(db, lead, client_db_id)
    crud.send_confirmation_sms(db_lead)
    background_tasks.add_task(crud.mark_lead_contacted, db_lead.id)
    return {"status": "ok", "id": db_lead.id}

@app.get("/api/leads")
def list_leads(request: Request, db: Session = Depends(get_db)):
    if not is_client_authenticated(request):
        return []
    
    client_db_id = get_client_id_from_session(request, db)
    leads = crud.get_leads(db, client_db_id)
    return leads

# ========== ADMIN API ROUTES ==========

@app.post("/api/admin/clients")
async def create_admin_client(request: Request, db: Session = Depends(get_db)):
    if not is_admin_authenticated(request):
        return {"status": "error", "message": "Unauthorized"}
    
    try:
        body = await request.json()
    except:
        return {"status": "error", "message": "Invalid JSON"}
    
    name = body.get("name")
    if not name:
        return {"status": "error", "message": "Missing name"}
    
    db_client, plain_password = crud.create_client(db, name)
    return {
        "status": "ok",
        "client_id": db_client.client_id,
        "password": plain_password,
        "name": db_client.name
    }

