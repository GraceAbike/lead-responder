from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import db, crud, schemas
from .auth import is_authenticated, login_response, logout_response, verify_password

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = str(BASE_DIR / "static")
TEMPLATE_DIR = BASE_DIR / "templates"
DASHBOARD_FILE = TEMPLATE_DIR / "index.html"
LOGIN_FILE = TEMPLATE_DIR / "login.html"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.on_event("startup")
def startup():
    db.init_db()


def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")

@app.get("/login", response_class=HTMLResponse)
def login_page():
    html = LOGIN_FILE.read_text(encoding="utf-8")
    return HTMLResponse(html.replace("{{error}}", ""))

@app.post("/login")
def login(password: str = Form(...)):
    html = LOGIN_FILE.read_text(encoding="utf-8")
    if verify_password(password):
        response = RedirectResponse(url="/dashboard", status_code=303)
        return login_response(response)
    return HTMLResponse(html.replace("{{error}}", "Invalid password."), status_code=401)

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    return logout_response(response)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")
    html = DASHBOARD_FILE.read_text(encoding="utf-8")
    return HTMLResponse(html)

@app.post("/api/leads")
def receive_lead(lead: schemas.LeadCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_lead = crud.create_lead(db, lead)
    crud.send_confirmation_sms(db_lead)
    background_tasks.add_task(crud.mark_lead_contacted, db_lead.id)
    return {"status":"ok","id":db_lead.id}

@app.get("/api/leads")
def list_leads(db: Session = Depends(get_db)):
    leads = crud.get_leads(db)
    return leads
