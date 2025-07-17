from app import db
from datetime import datetime
from sqlalchemy import Text

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dropdown_selection = db.Column(db.String(100), nullable=False)
    message = db.Column(Text, nullable=False)
    language = db.Column(db.String(2), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lead {self.name} - {self.email}>'

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    counselor_title = db.Column(db.String(100), default="counselors")
    phone_number = db.Column(db.String(20), default="(866)9284248")
    email_recipients = db.Column(Text, default="abbasjadoon915@gmail.com")
    dropdown_options = db.Column(Text, default="General Inquiry,Technical Support,Billing,Other")
    logo_position = db.Column(db.String(20), default="top-left")
    # Support for 3 logos
    logo_url_1 = db.Column(db.String(255), default="")
    logo_url_2 = db.Column(db.String(255), default="")
    logo_url_3 = db.Column(db.String(255), default="")
    logo_1_enabled = db.Column(db.Boolean, default=True)
    logo_2_enabled = db.Column(db.Boolean, default=False)
    logo_3_enabled = db.Column(db.Boolean, default=False)
    primary_color = db.Column(db.String(7), default="#0d1b2a")
    chatbot_color = db.Column(db.String(7), default="#2e7d32")
    user_color = db.Column(db.String(7), default="#e0e1dd")
    button_color = db.Column(db.String(7), default="#4db6ac")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Settings {self.id}>'
