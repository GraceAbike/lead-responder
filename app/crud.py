from sqlalchemy.orm import Session
from . import models, schemas
import os
from .db import SessionLocal
from .notifications import send_sms


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
