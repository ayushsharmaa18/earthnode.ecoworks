from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Campaign(db.Model):
    """A cause/campaign the NGO runs, e.g. tree plantation, mental health camps."""
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False)
    pillar = db.Column(db.String(50), nullable=False)  # Environment / Mental Health / Skill Development
    summary = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Campaign {self.title}>"


class ContactMessage(db.Model):
    """Messages submitted via the Contact page form."""
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class VolunteerApplication(db.Model):
    """Submissions from the Get Involved page (volunteer / partner / CSR)."""
    __tablename__ = "volunteer_applications"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    interest = db.Column(db.String(50), nullable=False)  # Volunteer / Partner / CSR Collaboration
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="new")  # new / contacted / onboarded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subscriber(db.Model):
    """Newsletter subscribers."""
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminUser(UserMixin, db.Model):
    """Admin panel login for managing campaigns and submissions."""
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False, default="Admin")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)