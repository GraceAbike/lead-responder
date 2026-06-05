from sqlalchemy.orm import Session
from . import models, schemas, auth
import os
import openai
import uuid
from .db import SessionLocal
from .notifications import send_sms


def _openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY must be set in .env before calling generate_ai_response()")
    return openai.OpenAI(api_key=api_key)


def _build_customer_prompt(customer_message: str) -> str:
    return (
        "You are a professional and courteous service assistant. Reply politely to the customer request, "
        "confirm that help can be arranged quickly, and ask for the customer's preferred appointment time. "
        "The response should be clear, empathetic, and businesslike.\n\n"
        f"Customer request: {customer_message}\n\n"
        "AI response:"
    )


def generate_ai_response(customer_message: str) -> str:
    client = _openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a highly professional customer support assistant."},
            {"role": "user", "content": _build_customer_prompt(customer_message)},
        ],
        temperature=0.2,
        max_tokens=250,
    )
    message = response.choices[0].message
    if hasattr(message, "content"):
        content = message.content
    else:
        content = message["content"]
    return content.strip()


# ========== CLIENT MANAGEMENT ==========

def create_client(db: Session, name: str) -> tuple:
    """Create a new client with a unique client_id and plain-text password. Returns (client, plain_password)"""
    client_id = str(uuid.uuid4())[:8].upper()
    plain_password = str(uuid.uuid4())[:16]
    password_hash = auth.hash_password(plain_password)
    
    db_client = models.Client(
        client_id=client_id,
        name=name,
        password_hash=password_hash
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client, plain_password


def get_client_by_id(db: Session, client_id: int) -> models.Client:
    """Get a client by database ID."""
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_client_id(db: Session, client_id: str) -> models.Client:
    """Get a client by public client_id."""
    return db.query(models.Client).filter(models.Client.client_id == client_id).first()


def get_all_clients(db: Session):
    """Get all clients (admin only)."""
    return db.query(models.Client).order_by(models.Client.created_at.desc()).all()


def verify_client_password(db: Session, client_id: str, password: str) -> models.Client:
    """Verify client password and return client if valid, else None."""
    db_client = get_client_by_client_id(db, client_id)
    if not db_client:
        return None
    if auth.verify_password(password, db_client.password_hash):
        return db_client
    return None


# ========== LEAD MANAGEMENT ==========

def create_lead(db: Session, lead: schemas.LeadCreate, client_id: int):
    """Create a lead for a specific client."""
    db_lead = models.Lead(
        client_id=client_id,
        customer_name=lead.customer_name,
        customer_phone=lead.customer_phone
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def get_leads(db: Session, client_id: int):
    """Get all leads for a specific client."""
    return db.query(models.Lead).filter(models.Lead.client_id == client_id).order_by(models.Lead.timestamp.desc()).all()


def get_all_leads(db: Session):
    """Get all leads across all clients (admin only)."""
    return db.query(models.Lead).order_by(models.Lead.timestamp.desc()).all()


def send_confirmation_sms(lead: models.Lead):
    message = (
        f"Hello {lead.customer_name}, thank you for reaching out to our team. "
        "We have received your request and will contact you shortly to confirm your preferred appointment time. "
        "If you have any urgent details, feel free to reply to this message."
    )
    send_sms(lead.customer_phone, message)


def mark_lead_contacted(lead_id: int):
    """Mark a lead as contacted."""
    db = SessionLocal()
    try:
        lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
        if not lead:
            return
        lead.status = "Contacted"
        db.add(lead)
        db.commit()
    finally:
        db.close()

