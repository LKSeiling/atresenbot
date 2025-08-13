import datetime as dt
from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_json, save_json
from config import TOPS_FILE

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message or not update.effective_message.text:
        return
    text = update.effective_message.text.strip()
    if text.startswith("TOP: "):
        today = dt.date.today().isoformat()
        month = today[:7]
        tops = load_json(TOPS_FILE, {})
        tops.setdefault(month, []).append({
            "date": today,
            "text": text[5:].strip(),
            "user": update.effective_user.full_name,
            "user_id": update.effective_user.id,
            "message_id": update.effective_message.message_id,
            "chat_id": update.effective_chat.id,
        })
        save_json(TOPS_FILE, tops)
        await update.effective_message.reply_text("✅ TOP gespeichert!")