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

## 🏁 Getting Started (Step-by-Step)

### 1. Create your Telegram Bot
1. Open Telegram and search for **@BotFather**.
2. Start a chat and send `/newbot`.
3. Give your bot a **Name** (e.g., *My OdoSight*) and a **Username** (e.g., *my_odosight_bot*).
4. **Copy the API Token** provided (it looks like `123456789:ABCdef...`).

### 2. Launch OdoSight
Deploy the whole stack on any Linux server (with Docker installed) with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/ashrf-in/odosight/master/install.sh | bash -s -- YOUR_TELEGRAM_BOT_TOKEN
```
*(Replace `YOUR_TELEGRAM_BOT_TOKEN` with the token you got from @BotFather)*

### 3. Setup Odoo & Gemini
1. Once the bot is running, find it on Telegram and type `/start`.
2. Run the `/setup` command.
3. Follow the prompts to enter your **Odoo URL**, **Database**, **Username**, **Password**, and **Gemini API Key**.

#### 🔑 How to get a Gemini API Key (Free)
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Log in with your Google account.
3. Click on **"Get API key"** in the left sidebar.
4. Click **"Create API key in new project"**.
5. Copy your key (it starts with `AIza...`).
6. Paste it into the bot when prompted during `/setup`.

## 🛡️ Security & Privacy
- **Standalone Onboarding**: Users run `/setup` to link their own Odoo and Gemini credentials.
- **Natural Language Querying**: Users can ask financial questions in plain English/Arabic.
- **Data Privacy**: Each user's data is isolated and queried only with their own credentials.
- **Forensic Audit**: Automated anomaly detection on recent transactions.
