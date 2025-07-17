# Maven Chatbot System

## Overview

This is a Flask-based web application that implements a multilingual chatbot system for lead generation. The system features a conversational interface that collects user information (name, email, phone, category, and message) and forwards leads to designated recipients via email notifications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (default) or PostgreSQL support
- **Email Service**: Flask-Mail for SMTP email delivery
- **Session Management**: Flask's built-in session handling
- **Configuration**: Environment variable-based configuration

### Frontend Architecture
- **Templates**: Jinja2 templating engine
- **CSS Framework**: Bootstrap 5 for responsive design
- **JavaScript**: Vanilla JavaScript with ES6 classes for chatbot state management
- **UI Components**: Custom CSS with CSS custom properties for theming
- **Animations**: Canvas Confetti library for success animations

### Database Schema
- **Lead Model**: Stores lead information with fields for name, email, phone, category selection, message, language preference, and timestamp
- **Settings Model**: Stores configurable application settings including UI colors, email recipients, dropdown options, and branding elements

## Key Components

### Core Application Files
- `app.py`: Main Flask application configuration and initialization
- `routes.py`: URL routing and request handling logic
- `models.py`: SQLAlchemy database models for Lead and Settings
- `email_handler.py`: Email notification system for new leads
- `main.py`: Application entry point

### Frontend Components
- `templates/index.html`: Main chatbot interface
- `templates/admin.html`: Administrative panel for settings management
- `templates/base.html`: Base template with common HTML structure
- `static/css/style.css`: Custom styling with CSS variables for theming
- `static/js/chatbot.js`: Chatbot conversation flow and state management
- `static/js/admin.js`: Admin panel functionality

### Configuration
- `config.py`: Configuration class with environment variable defaults
- `translations.json`: Multilingual text content for English and Spanish

## Data Flow

1. **User Interaction**: Users interact with the chatbot through a conversational interface
2. **State Management**: JavaScript manages conversation flow and form data collection
3. **Form Submission**: Lead data is submitted via POST request to `/submit_lead`
4. **Database Storage**: Lead information is stored in SQLite/PostgreSQL database
5. **Email Notification**: System sends email notifications to configured recipients
6. **Admin Management**: Administrators can view leads and modify settings through `/admin`

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Mail: Email functionality
- Werkzeug: WSGI utilities

### Frontend Libraries
- Bootstrap 5: CSS framework
- Font Awesome: Icon library
- Canvas Confetti: Animation library

### Email Service
- SMTP server configuration (Gmail by default)
- Environment variables for email credentials

## Deployment Strategy

### Environment Configuration
- Uses environment variables for sensitive configuration
- Supports both SQLite (development) and PostgreSQL (production)
- Configurable SMTP settings for email delivery

### Application Setup
- Database tables are created automatically on startup
- Default settings are initialized if none exist
- Proxy fix middleware for deployment behind reverse proxies

### Key Environment Variables
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Session encryption key
- `MAIL_USERNAME`, `MAIL_PASSWORD`: Email credentials
- `MAIL_SERVER`, `MAIL_PORT`: SMTP server configuration

### Features
- **Multilingual Support**: English and Spanish translations
- **Customizable Theming**: Admin-configurable colors and branding
- **Lead Management**: Administrative interface for viewing and managing leads
- **Email Notifications**: Automated email delivery to multiple recipients with dedicated management interface
- **Logo Management**: Upload and position custom logos with real-time preview
- **Responsive Design**: Mobile-friendly interface
- **Conversation Flow**: Structured chatbot conversation with interruption handling
- **Backend Dashboard**: Complete admin panel for managing all chatbot settings