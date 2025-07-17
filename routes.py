from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app, db
from models import Lead, Settings
from email_handler import send_lead_notification
import json
import os
from werkzeug.utils import secure_filename
import time

@app.route('/')
def index():
    try:
        settings = Settings.query.first()
        return render_template('index.html', settings=settings)
    except Exception as e:
        app.logger.error(f"Error loading index page: {str(e)}")
        return "Service unavailable. Please try again later.", 503

@app.route('/admin')
def admin():
    try:
        settings = Settings.query.first()
        leads = Lead.query.order_by(Lead.created_at.desc()).all()
        return render_template('admin.html', settings=settings, leads=leads)
    except Exception as e:
        app.logger.error(f"Error loading admin page: {str(e)}")
        flash('Database connection error. Please try again.', 'error')
        return render_template('error.html'), 500

@app.route('/admin/save', methods=['POST'])
def save_settings():
    try:
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
        
        # Add delay to simulate connection issues
        time.sleep(0.5)
        
        settings.counselor_title = request.form.get('counselor_title', 'counselors')
        settings.phone_number = request.form.get('phone_number', '(866)9284248')
        settings.email_recipients = request.form.get('email_recipients', 'abbasjadoon915@gmail.com')
        settings.dropdown_options = request.form.get('dropdown_options', 'General Inquiry,Technical Support,Billing,Other')
        settings.logo_position = request.form.get('logo_position', 'top-left')
        
        # Logo settings
        settings.logo_url_1 = request.form.get('logo_url_1', '')
        settings.logo_url_2 = request.form.get('logo_url_2', '')
        settings.logo_url_3 = request.form.get('logo_url_3', '')
        settings.logo_1_enabled = 'logo_1_enabled' in request.form
        settings.logo_2_enabled = 'logo_2_enabled' in request.form
        settings.logo_3_enabled = 'logo_3_enabled' in request.form
        
        # Color settings
        settings.primary_color = request.form.get('primary_color', '#0d1b2a')
        settings.chatbot_color = request.form.get('chatbot_color', '#2e7d32')
        settings.user_color = request.form.get('user_color', '#e0e1dd')
        settings.button_color = request.form.get('button_color', '#4db6ac')
        
        db.session.commit()
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f"Error saving settings: {str(e)}")
        flash('Failed to save settings. Please try again.', 'error')
        return redirect(url_for('admin')), 500

@app.route('/submit_lead', methods=['POST'])
def submit_lead():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dropdown_selection = request.form.get('dropdown_selection')
        message = request.form.get('message')
        language = request.form.get('language', 'en')
        
        # Validate required fields
        if not all([name, email, phone, dropdown_selection, message]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        # Create new lead
        lead = Lead(
            name=name,
            email=email,
            phone=phone,
            dropdown_selection=dropdown_selection,
            message=message,
            language=language
        )
        
        db.session.add(lead)
        db.session.commit()
        
        # Send email notification to admin
        try:
            send_lead_notification(lead)
            app.logger.info(f"Email notification sent for lead {lead.id}")
        except Exception as e:
            app.logger.error(f"Failed to send email notification: {str(e)}")
        
        # Send welcome email to customer
        try:
            from email_handler import send_welcome_email
            send_welcome_email(lead)
            app.logger.info(f"Welcome email sent to {lead.email}")
        except Exception as e:
            app.logger.error(f"Failed to send welcome email: {str(e)}")
        
        return jsonify({'success': True, 'message': 'Lead submitted successfully'}), 200
        
    except Exception as e:
        app.logger.error(f"Error submitting lead: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/get_translations/<language>')
def get_translations(language):
    try:
        # Add cache buster to prevent stale translations
        cache_buster = request.args.get('cb', int(time.time()))
        
        with open('translations.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
        return jsonify(translations.get(language, translations['en']))
    except Exception as e:
        app.logger.error(f"Error loading translations: {str(e)}")
        return jsonify({"error": "Translations unavailable"}), 500

@app.route('/get_settings')
def get_settings():
    try:
        settings = Settings.query.first()
        if settings:
            return jsonify({
                'counselor_title': settings.counselor_title,
                'phone_number': settings.phone_number,
                'dropdown_options': settings.dropdown_options.split(','),
                'logo_position': settings.logo_position,
                'logo_url_1': settings.logo_url_1 or '',
                'logo_url_2': settings.logo_url_2 or '',
                'logo_url_3': settings.logo_url_3 or '',
                'logo_1_enabled': settings.logo_1_enabled,
                'logo_2_enabled': settings.logo_2_enabled,
                'logo_3_enabled': settings.logo_3_enabled,
                'primary_color': settings.primary_color,
                'chatbot_color': settings.chatbot_color,
                'user_color': settings.user_color,
                'button_color': settings.button_color
            })
        return jsonify({})
    except Exception as e:
        app.logger.error(f"Error retrieving settings: {str(e)}")
        return jsonify({"error": "Settings unavailable"}), 500

@app.route('/delete_lead/<int:lead_id>', methods=['POST'])
def delete_lead(lead_id):
    try:
        lead = Lead.query.get_or_404(lead_id)
        db.session.delete(lead)
        db.session.commit()
        flash('Lead deleted successfully!', 'success')
    except Exception as e:
        app.logger.error(f"Error deleting lead: {str(e)}")
        flash('Error deleting lead!', 'error')
    return redirect(url_for('admin'))

@app.route('/admin/save_email_settings', methods=['POST'])
def save_email_settings():
    try:
        email_recipients = request.form.get('email_recipients', '')
        
        # Validate email recipients
        if not email_recipients.strip():
            return jsonify({'success': False, 'error': 'At least one email address is required'}), 400
        
        # Get or create settings
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
        
        settings.email_recipients = email_recipients
        db.session.commit()
        
        app.logger.info(f"Email settings updated: {email_recipients}")
        return jsonify({'success': True, 'message': 'Email settings saved successfully'}), 200
        
    except Exception as e:
        app.logger.error(f"Error saving email settings: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Add favicon route to prevent 404 errors
@app.route('/favicon.ico')
def favicon():
    return '', 204
