from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_json, save_json
from config import ADMINS_FILE

def is_admin(user_id: int) -> bool:
    admins = load_json(ADMINS_FILE, [])
    return user_id in admins

async def admin_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.effective_message.reply_text("🚫 Keine Berechtigung.")
    if not context.args:
        return await update.effective_message.reply_text("Bitte ID angeben: /admin_add <user_id>")
    try:
        new_id = int(context.args[0])
    except ValueError:
        return await update.effective_message.reply_text("Ungültige ID.")
    admins = load_json(ADMINS_FILE, [])
    if new_id not in admins:
        admins.append(new_id)
        save_json(ADMINS_FILE, admins)
    await update.effective_message.reply_text(f"✅ Admin {new_id} hinzugefügt.")

async def admin_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.effective_message.reply_text("🚫 Keine Berechtigung.")
    if not context.args:
        return await update.effective_message.reply_text("Bitte ID angeben: /admin_remove <user_id>")
    try:
        rem_id = int(context.args[0])
    except ValueError:
        return await update.effective_message.reply_text("Ungültige ID.")
    admins = load_json(ADMINS_FILE, [])
    if rem_id in admins:
        admins.remove(rem_id)
        save_json(ADMINS_FILE, admins)
    await update.effective_message.reply_text(f"❌ Admin {rem_id} entfernt.")

# Optional: Bot ein-/ausschalten Flag in admins.json
# Struktur: {"enabled": true, "admins": [123, 456]}

async def bot_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.effective_message.reply_text("🚫 Keine Berechtigung.")
    data = load_json(ADMINS_FILE, {"enabled": True, "admins": []})
    data["enabled"] = True
    save_json(ADMINS_FILE, data)
    await update.effective_message.reply_text("🔛 Bot aktiviert.")

async def bot_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.effective_message.reply_text("🚫 Keine Berechtigung.")
    data = load_json(ADMINS_FILE, {"enabled": True, "admins": []})
    data["enabled"] = False
    save_json(ADMINS_FILE, data)
    await update.effective_message.reply_text("🔌 Bot deaktiviert. (Nachrichten werden ignoriert)")


def bot_enabled() -> bool:
    data = load_json(ADMINS_FILE, {"enabled": True, "admins": []})
    # Falls Datei eine einfache Liste ist (älteres Format), als aktiviert behandeln
    if isinstance(data, list):
        return True
    return bool(data.get("enabled", True))