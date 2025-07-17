import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# SQLAlchemy base
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
mail = Mail()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "maven-secret-key-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///chatbot.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@mavenchatbot.com')

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Import routes
from routes import *

# App context setup
with app.app_context():
    import models
    db.create_all()

    # Create default settings if they don't exist
    from models import Settings
    if not Settings.query.first():
        default_settings = Settings(
            counselor_title="counselors",
            phone_number="(555) 123-4567",
            email_recipients="abbasjadoon915@gmail.com",
            dropdown_options="General Inquiry,Technical Support,Billing,Other",
            logo_position="top-left",
            logo_url_1="images/logo.png",
            primary_color="#0d1b2a",
            chatbot_color="#2e7d32",
            user_color="#e0e1dd",
            button_color="#4db6ac"
        )
        db.session.add(default_settings)
        db.session.commit()

# Run app only if executed directly (local testing)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
