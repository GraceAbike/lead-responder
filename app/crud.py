from sqlalchemy.orm import Session
from . import models, schemas
import os
import openai
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


def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(customer_name=lead.customer_name, customer_phone=lead.customer_phone)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def get_leads(db: Session):
    return db.query(models.Lead).order_by(models.Lead.timestamp.desc()).all()


def send_confirmation_sms(lead: models.Lead):
    message = f"Hi {lead.customer_name}, thank you for reaching out! We received your request and will contact you shortly."
    send_sms(lead.customer_phone, message)


def mark_lead_contacted(lead_id: int):
    db = SessionLocal()
    try:
        lead = db.get(models.Lead, lead_id)
        if not lead:
            return
        lead.status = "Contacted"
        db.add(lead)
        db.commit()
    finally:
        db.close()
