import os
import logging
from typing import Tuple

import requests
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ================== CONFIG ==================

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RISK_THRESHOLD = 80.0

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ================== HELPERS ==================

def build_risk_message(score: float, high_risk: bool) -> str:
    if high_risk:
        return (
            "🚨 *High Scam Risk Detected*\n\n"
            f"Risk Score: *{score:.2f}%*\n\n"
            "This media shows strong signs of manipulation and may be part of a financial scam.\n"
            "Do *NOT* proceed with any payment, and do not share OTPs, PINs or banking details.\n"
        )
    else:
        return (
            "✅ *Low Scam Risk Detected*\n\n"
            f"Risk Score: *{score:.2f}%*\n\n"
            "No strong deepfake patterns were detected, but scams can still occur.\n"
            "Stay cautious and verify using official channels before paying."
        )


def build_action_keyboard(event_id: int, high_risk: bool, media_type: str, score: float) -> InlineKeyboardMarkup:
    buttons = []

    if high_risk:
        buttons.append(
            InlineKeyboardButton(
                "🛑 Block Payment (Simulated)",
                callback_data=f"block:{event_id}",
            )
        )

    buttons.append(
        InlineKeyboardButton(
            "📄 Generate Report (Coming Soon)",
            callback_data=f"report:{event_id}:{media_type}:{score}",
        )
    )

    buttons.append(
        InlineKeyboardButton(
            "✅ Mark as Safe (Feedback)",
            callback_data=f"safe:{event_id}",
        )
    )

    keyboard = [buttons[:2], buttons[2:3]]
    return InlineKeyboardMarkup(keyboard)


def extract_file_from_message(msg: Message) -> Tuple[bytes, str] | Tuple[None, None]:
    """
    Get raw file bytes and inferred media type from a Telegram message.
    Supports: photo, voice, audio.
    """
    file = None
    media_type = None

    if msg.photo:
        file = msg.photo[-1]  # highest resolution
        media_type = "image"
    elif msg.voice:
        file = msg.voice
        media_type = "audio"
    elif msg.audio:
        file = msg.audio
        media_type = "audio"

    if file is None:
        return None, None

    file_obj = file.get_file()
    file_bytes = file_obj.download_as_bytearray()

    return file_bytes, media_type


# ================== HANDLERS ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.effective_chat.type

    if chat_type in ("group", "supergroup"):
        text = (
            "🛡️ *Scamp Chat Shield Activated*\n\n"
            "I will automatically scan images and voice notes sent in this group for deepfake patterns "
            "and potential scam content.\n\n"
            "If I detect something suspicious, I will immediately raise an alert here."
        )
    else:
        text = (
            "🛡️ *Welcome to Scamp — Your Scam Bodyguard*\n\n"
            "Send me a *suspicious image* or *voice note* and I will analyze it for deepfake patterns and scam risk.\n\n"
            "You can also add me to a Telegram group to automatically scan media posted there."
        )

    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ *How to use Scamp*\n\n"
        "1. *DM Mode* — Send me any suspicious image or voice note.\n"
        "2. *Group Mode* — Add me to a group; I will auto-scan media messages.\n\n"
        "When I detect high scam risk, I will:\n"
        "• Show a clear warning\n"
        "• Offer mock payment block\n"
        "• Allow report generation (coming soon)\n"
        "• Let you mark my decision as safe/false alarm\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user

    file_bytes, media_type = extract_file_from_message(message)
    if file_bytes is None:
        await message.reply_text("Please send a photo or voice note to analyze.")
        return

    user_id = str(user.id)
    platform = "telegram"

    await message.reply_text(
        "🔍 Analyzing this media for deepfake and scam risk. Please wait...",
        quote=True,
    )

    try:
        files = {"file": ("media", file_bytes)}
        data = {
            "media_type": media_type,
            "user_id": user_id,
            "platform": platform,
        }
        resp = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data, timeout=60)
    except Exception as e:
        logger.exception("Error calling backend /analyze: %s", e)
        await message.reply_text(
            "⚠️ Unable to analyze right now. Please try again in a moment."
        )
        return

    if resp.status_code != 200:
        await message.reply_text(
            f"⚠️ Analysis failed with status {resp.status_code}. Backend error."
        )
        return

    result = resp.json()
    score = float(result.get("score", 0.0))
    threshold = float(result.get("threshold", RISK_THRESHOLD))
    event_id = int(result.get("event_id", -1))
    high_risk = score >= threshold

    text = build_risk_message(score, high_risk)
    keyboard = build_action_keyboard(event_id, high_risk, media_type, score)

    await message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ""

    parts = data.split(":")
    action = parts[0] if parts else ""

    if action == "block":
        await query.edit_message_text(
            "🛑 *Payment Blocked (Simulation)*\n\n"
            "In a real integration, this would notify your bank or payment provider to freeze the suspicious transaction.",
            parse_mode="Markdown",
        )

    elif action == "safe":
        # TODO: call backend.save_feedback(event_id, user_id, "safe")
        await query.edit_message_text(
            "✅ Marked as safe.\n"
            "Your feedback helps Scamp reduce false positives over time."
        )

    elif action == "report":
        await query.edit_message_text(
            "📄 Report generation feature is coming soon.\n"
            "For now, treat this media as flagged and avoid engaging with the sender."
        )

    else:
        await query.edit_message_text("Unknown action.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I didn't understand that command.\n"
        "Send me an image or voice note, or use /help for instructions."
    )


# ================== MAIN ==================

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set. Please set it as an environment variable."
        )

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    media_filter = filters.PHOTO | filters.VOICE | filters.AUDIO
    app.add_handler(MessageHandler(media_filter, handle_media))

    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Scamp Telegram bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
