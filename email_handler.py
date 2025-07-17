from flask_mail import Message
from app import mail, app
from models import Settings

def send_lead_notification(lead):
    """Send email notification when a new lead is submitted"""
    try:
        settings = Settings.query.first()
        if not settings:
            return
        
        # Get email recipients
        recipients = [email.strip() for email in settings.email_recipients.split(',')]
        
        # Create email subject
        subject = f"New Lead from {lead.name} - Maven Chatbot"
        
        # Create email body
        body = f"""
New lead received from the Maven Chatbot:

Name: {lead.name}
Email: {lead.email}
Phone: {lead.phone}
Category: {lead.dropdown_selection}
Language: {'Spanish' if lead.language == 'es' else 'English'}
Message: {lead.message}

Submitted on: {lead.created_at.strftime('%Y-%m-%d %H:%M:%S')}

---
This is an automated message from the Maven Chatbot system.
        """
        
        # Create HTML version
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0d1b2a; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .lead-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .lead-info h3 {{ color: #0d1b2a; margin-top: 0; }}
                .field {{ margin: 10px 0; }}
                .field strong {{ color: #2e7d32; }}
                .footer {{ text-align: center; color: #666; font-size: 0.9em; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>New Lead Notification</h1>
                <p>Maven Chatbot System</p>
            </div>
            
            <div class="content">
                <div class="lead-info">
                    <h3>Lead Details</h3>
                    <div class="field"><strong>Name:</strong> {lead.name}</div>
                    <div class="field"><strong>Email:</strong> {lead.email}</div>
                    <div class="field"><strong>Phone:</strong> {lead.phone}</div>
                    <div class="field"><strong>Category:</strong> {lead.dropdown_selection}</div>
                    <div class="field"><strong>Language:</strong> {'Spanish' if lead.language == 'es' else 'English'}</div>
                    <div class="field"><strong>Submitted:</strong> {lead.created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                
                <div class="lead-info">
                    <h3>Message</h3>
                    <p>{lead.message}</p>
                </div>
            </div>
            
            <div class="footer">
                <p>This is an automated message from the Maven Chatbot system.</p>
            </div>
        </body>
        </html>
        """
        
        # Create and send message
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html_body
        )
        
        mail.send(msg)
        app.logger.info(f"Email notification sent for lead {lead.id}")
        
    except Exception as e:
        app.logger.error(f"Failed to send email notification: {str(e)}")
        raise

def send_welcome_email(lead):
    """Send welcome email to the lead"""
    try:
        settings = Settings.query.first()
        if not settings:
            return
        
        # Create welcome email
        subject = "Thank you for contacting Maven - We'll be in touch soon!"
        
        body = f"""
Hi {lead.name},

Thank you for reaching out to us through our website. We've received your inquiry and one of our {settings.counselor_title} will be in touch with you soon.

Here's a summary of your submission:
- Category: {lead.dropdown_selection}
- Phone: {lead.phone}
- Email: {lead.email}

If you need immediate assistance, please call us at {settings.phone_number}.

Best regards,
Maven Team
        """
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #0d1b2a; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 0.9em; margin-top: 30px; }}
                .contact-info {{ background-color: #2e7d32; color: white; padding: 15px; border-radius: 8px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Thank You for Contacting Maven!</h1>
            </div>
            
            <div class="content">
                <p>Hi {lead.name},</p>
                
                <p>Thank you for reaching out to us through our website. We've received your inquiry and one of our {settings.counselor_title} will be in touch with you soon.</p>
                
                <div class="summary">
                    <h3>Your Submission Summary:</h3>
                    <p><strong>Category:</strong> {lead.dropdown_selection}</p>
                    <p><strong>Phone:</strong> {lead.phone}</p>
                    <p><strong>Email:</strong> {lead.email}</p>
                </div>
                
                <div class="contact-info">
                    <h3>Need Immediate Assistance?</h3>
                    <p>Call us at: <strong>{settings.phone_number}</strong></p>
                </div>
                
                <p>Best regards,<br>Maven Team</p>
            </div>
            
            <div class="footer">
                <p>This is an automated message. Please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[lead.email],
            body=body,
            html=html_body
        )
        
        mail.send(msg)
        app.logger.info(f"Welcome email sent to {lead.email}")
        
    except Exception as e:
        app.logger.error(f"Failed to send welcome email: {str(e)}")
        # Don't raise here as this is secondary to the main notification
