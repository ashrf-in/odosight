# OdoSight Standalone App

This is a standalone Telegram bot that provides financial intelligence for Odoo ERP using Gemini 3.

## Deployment Instructions

1. **Clone the project** to your server.
2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Set Environment Variables**:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token"
   ```
4. **Run the App**:
   ```bash
   python3 main.py
   ```

## Features
- **Standalone Onboarding**: Users run `/setup` to link their own Odoo and Gemini credentials.
- **Natural Language Querying**: Users can ask financial questions in plain English/Arabic.
- **Data Privacy**: Each user's data is isolated and queried only with their own credentials.
- **Forensic Audit**: Automated anomaly detection on recent transactions.
