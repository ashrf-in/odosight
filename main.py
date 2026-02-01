import os
import sys
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.connectors.odoo_client import OdooClient
from src.logic.intelligence_engine import IntelligenceEngine
from src.bots.database import Session, UserConfig

# Ensure internal imports work for standalone structure
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Conversation states
SETTING_ODOO_URL, SETTING_ODOO_DB, SETTING_ODOO_USER, SETTING_ODOO_PWD, SETTING_GEMINI_KEY = range(5)

class StandaloneCFOBot:
    def __init__(self, token):
        self.app = ApplicationBuilder().token(token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('setup', self.start_setup)],
            states={
                SETTING_ODOO_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.save_url)],
                SETTING_ODOO_DB: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.save_db)],
                SETTING_ODOO_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.save_user)],
                SETTING_ODOO_PWD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.save_pwd)],
                SETTING_GEMINI_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.save_gemini)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        self.app.add_handler(CommandHandler('start', self.start))
        self.app.add_handler(CommandHandler('summary', self.get_summary))
        self.app.add_handler(conv_handler)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_query))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Welcome to *OdoSight*! 🦾\n"
            "I connect your Odoo ERP to Gemini 3 AI for high-level financial intelligence.\n\n"
            "1️⃣ Use /setup to link your account.\n"
            "2️⃣ Ask me questions like: 'What are my top expenses?'\n"
            "3️⃣ Type /summary for a quick 30-day snapshot.",
            parse_mode='Markdown'
        )

    async def start_setup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Step 1/5: What is your Odoo URL? (e.g., https://company.odoo.com)")
        return SETTING_ODOO_URL

    async def save_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['odoo_url'] = update.message.text
        await update.message.reply_text("Step 2/5: Database Name?")
        return SETTING_ODOO_DB

    async def save_db(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['odoo_db'] = update.message.text
        await update.message.reply_text("Step 3/5: Odoo Username/Email?")
        return SETTING_ODOO_USER

    async def save_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['odoo_user'] = update.message.text
        await update.message.reply_text("Step 4/5: Odoo API Password?")
        return SETTING_ODOO_PWD

    async def save_pwd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['odoo_pwd'] = update.message.text
        await update.message.reply_text("Step 5/5: Gemini API Key?")
        return SETTING_GEMINI_KEY

    async def save_gemini(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = str(update.effective_user.id)
        data = context.user_data
        
        session = Session()
        user = session.query(UserConfig).filter_by(telegram_id=tid).first()
        if not user:
            user = UserConfig(telegram_id=tid)
            session.add(user)
        
        user.odoo_url = data['odoo_url']
        user.odoo_db = data['odoo_db']
        user.odoo_user = data['odoo_user']
        user.odoo_password = data['odoo_pwd']
        user.gemini_key = update.message.text
        
        session.commit()
        session.close()
        
        await update.message.reply_text("✅ Setup Complete! Your OdoSight is now live. Try asking a question!")
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Setup cancelled.")
        return ConversationHandler.END

    async def get_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = self._get_user_config(update.effective_user.id)
        if not user:
            await update.message.reply_text("Please run /setup first!")
            return
        
        await update.message.reply_text("Fetching 30-day summary... 📊")
        # Logic to call finance_engine and format response
        await update.message.reply_text("Summary logic connected! (Coming in next patch)")

    async def handle_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = self._get_user_config(update.effective_user.id)
        if not user:
            await update.message.reply_text("Please run /setup first!")
            return

        query = update.message.text
        await update.message.reply_text("Thinking... 🧠")
        
        client = OdooClient(user.odoo_url, user.odoo_db, user.odoo_user, user.odoo_password)
        # Pass the user's specific Gemini key to the engine
        os.environ["GOOGLE_API_KEY"] = user.gemini_key 
        intelligence = IntelligenceEngine(client)
        
        try:
            answer = intelligence.ask(query)
            await update.message.reply_text(answer)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

    def _get_user_config(self, telegram_id):
        session = Session()
        user = session.query(UserConfig).filter_by(telegram_id=str(telegram_id)).first()
        session.close()
        return user

    def run(self):
        print("Bot is running...")
        self.app.run_polling()

if __name__ == "__main__":
    # In a real scenario, the token would come from an ENV var
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Missing TELEGRAM_BOT_TOKEN")
        sys.exit(1)
    bot = StandaloneCFOBot(token)
    bot.run()
