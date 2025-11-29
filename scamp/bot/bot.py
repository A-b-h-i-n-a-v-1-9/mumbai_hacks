# scamp/bot/bot.py

import os
import logging
from io import BytesIO
from typing import Tuple

import requests
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from telegram.error import TimedOut
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest

# ================== CONFIG ==================

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Risk buckets (mirror backend)
RISK_LOW_THRESHOLD = 40.0
RISK_HIGH_THRESHOLD = 75.0

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ================== RISK HELPERS ==================


def bucketize_risk(score: float) -> str:
    """Return 'low', 'medium', or 'high' based on score."""
    try:
        score = float(score)
    except Exception:
        score = 0.0

    if score >= RISK_HIGH_THRESHOLD:
        return "high"
    elif score >= RISK_LOW_THRESHOLD:
        return "medium"
    return "low"


def build_risk_message(score: float, risk_level: str) -> str:
    """
    Render user-facing copy for 3 risk bands:
    - low:    0–40
    - medium: 40–75
    - high:   75–100
    """
    risk_level = (risk_level or "low").lower()

    if risk_level == "high":
        return (
            "🚨 *High Scam / Deepfake Risk*\n\n"
            f"Risk Score: *{score:.2f}%* _(75–100)_\n\n"
            "This content shows strong signs of manipulation and may be part of a financial scam.\n"
            "Do *NOT* proceed with any payment, and do not share OTPs, PINs or banking details.\n"
        )
    elif risk_level == "medium":
        return (
            "⚠️ *Medium Scam Risk*\n\n"
            f"Risk Score: *{score:.2f}%* _(40–75)_\n\n"
            "Some suspicious patterns were detected. Double‑check the sender, links, and payment details "
            "using official channels before you trust this.\n"
        )
    else:  # low
        return (
            "✅ *Lower Scam Risk*\n\n"
            f"Risk Score: *{score:.2f}%* _(0–40)_\n\n"
            "We didn’t cross our internal alert thresholds, but scams can still occur.\n"
            "Stay cautious and verify through official apps/websites before paying."
        )


def build_action_keyboard(
    event_id: int,
    risk_level: str,
    media_type: str,
    score: float,
) -> InlineKeyboardMarkup:
    """
    Show:
    - Block payment only for HIGH risk
    - Generate Report + Mark safe always
    """
    buttons = []

    is_high = (risk_level == "high")

    if is_high:
        buttons.append(
            InlineKeyboardButton(
                "🛑 Block Payment (Simulated)",
                callback_data=f"block:{event_id}",
            )
        )

    buttons.append(
        InlineKeyboardButton(
            "📄 Generate Report",
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


# ================== MEDIA EXTRACTION ==================


async def extract_file_from_message(msg: Message) -> Tuple[bytes, str] | Tuple[None, None]:
    """
    Get raw file bytes and inferred media type from a Telegram message.
    Supports: photo, image-document, voice, audio.
    Uses async get_file + download_as_bytearray for PTB v21+.
    """
    file = None
    media_type = None

    if msg.photo:
        file = msg.photo[-1]
        media_type = "image"
    elif msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"):
        file = msg.document
        media_type = "image"
    elif msg.voice:
        file = msg.voice
        media_type = "audio"
    elif msg.audio:
        file = msg.audio
        media_type = "audio"

    if file is None:
        return None, None

    try:
        file_obj = await file.get_file()
        file_bytes = await file_obj.download_as_bytearray()
        return bytes(file_bytes), media_type
    except TimedOut:
        logger.warning("Timed out while calling get_file/download for media.")
        return None, None


# ================== HELPERS FOR EXPLAINABILITY ==================


def format_explainability(highlights: list) -> str | None:
    """
    Turn backend highlights into a nice bullet list.
    Used for both text and media.
    """
    if not highlights:
        return None

    lines = []
    for h in highlights[:6]:
        span = h.get("span")
        htype = h.get("type", "signal")
        if not span:
            continue
        lines.append(f"- `{span}` _(signal: {htype})_")

    if not lines:
        return None

    return "🔎 *Why this looks risky*\n\n" + "\n".join(lines)


# ================== COMMAND HANDLERS ==================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.effective_chat.type

    if chat_type in ("group", "supergroup"):
        text = (
            "🛡️ *Scamp Chat Shield Activated*\n\n"
            "I will automatically scan images, voice notes, and suspicious text in this group "
            "for deepfake patterns and scam indicators.\n\n"
            "If I detect something suspicious, I will immediately raise an alert here."
        )
    else:
        text = (
            "🛡️ *Welcome to Scamp — Your Scam Bodyguard*\n\n"
            "Send me a *suspicious image*, *voice note*, or *message* and I will analyze it "
            "for deepfake patterns and scam risk.\n\n"
            "You can also add me to a Telegram group to automatically scan media posted there."
        )

    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ *How to use Scamp*\n\n"
        "1. *DM Mode* — Send me any suspicious image, voice note, or text.\n"
        "2. *Group Mode* — Add me to a group; I will auto-scan media and messages.\n\n"
        "When I detect risk, I will:\n"
        "• Show a clear risk level (low / medium / high)\n"
        "• Offer mock payment block for high risk\n"
        "• Generate a short report when you tap *Generate Report*\n"
        "• Let you mark my decision as safe/false alarm\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


# ================== CORE HANDLER ==================


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle ANY non-command message:
    - If it's text only: send to /analyze_text.
    - If it has media: send to /analyze.
    """
    message = update.effective_message
    user = update.effective_user

    logger.info("handle_media called. Chat=%s, User=%s", update.effective_chat.id, user.id)

    try:
        # First try to extract media
        file_bytes, media_type = await extract_file_from_message(message)

        # ---------- TEXT-ONLY CASE ----------
        if file_bytes is None:
            if not message.text:
                await message.reply_text(
                    "I see a message, but no media or text I can analyze.",
                )
                return

            text_content = message.text
            user_id = str(user.id)
            platform = "telegram"

            try:
                resp = requests.post(
                    f"{BACKEND_URL}/analyze_text",
                    data={
                        "text": text_content,
                        "user_id": user_id,
                        "platform": platform,
                    },
                    timeout=30,
                )
            except Exception as e:
                logger.exception("Error calling backend /analyze_text: %s", e)
                await message.reply_text(f"⚠️ Unable to analyze text right now: {e}")
                return

            if resp.status_code != 200:
                await message.reply_text(
                    f"⚠️ Text analysis failed (status {resp.status_code}): {resp.text[:200]}"
                )
                return

            result = resp.json()
            logger.info("backend_text: %s", result)

            score = float(result.get("score", 0.0))
            risk = (result.get("risk") or "low").lower()
            event_id = int(result.get("event_id", -1))
            highlights = result.get("highlights") or []

            risk_msg = build_risk_message(score, risk)
            keyboard = build_action_keyboard(event_id, risk, "text", score)

            try:
                await message.reply_text(
                    risk_msg,
                    parse_mode="Markdown",
                    reply_markup=keyboard,
                )
            except TimedOut:
                logger.warning("Timed out while sending text risk message.")
            except Exception as e:
                logger.exception("Error sending text risk message: %s", e)

            # Explanability block
            explain = format_explainability(highlights)
            if explain:
                try:
                    await message.reply_text(explain, parse_mode="Markdown")
                except Exception:
                    pass

            return

        # ---------- MEDIA CASE (image/audio) ----------
        user_id = str(user.id)
        platform = "telegram"

        try:
            await message.reply_text(
                "🔍 Analyzing this media for deepfake and scam risk. Please wait...",
                quote=True,
            )
        except TimedOut:
            logger.warning("Timed out while sending 'analyzing' message. Continuing anyway.")
        except Exception as e:
            logger.exception("Error sending 'analyzing' message: %s", e)

        # Call backend /analyze
        try:
            files = {"file": ("media", file_bytes)}
            data = {
                "media_type": media_type,
                "user_id": user_id,
                "platform": platform,
            }
            resp = requests.post(
                f"{BACKEND_URL}/analyze",
                files=files,
                data=data,
                timeout=90,
            )
        except Exception as e:
            logger.exception("Error calling backend /analyze: %s", e)
            await message.reply_text(f"⚠️ Unable to analyze media right now: {e}")
            return

        if resp.status_code != 200:
            await message.reply_text(
                f"⚠️ Media analysis failed (status {resp.status_code}): {resp.text[:200]}"
            )
            return

        result = resp.json()
        logger.info("backend_media: %s", result)

        score = float(result.get("score", 0.0))
        risk = (result.get("risk") or "low").lower()
        event_id = int(result.get("event_id", -1))
        highlights = result.get("highlights") or []

        text_msg = build_risk_message(score, risk)
        keyboard = build_action_keyboard(event_id, risk, media_type, score)

        try:
            await message.reply_text(
                text_msg,
                parse_mode="Markdown",
                reply_markup=keyboard,
            )
        except TimedOut:
            logger.warning("Timed out while sending media risk message.")
        except Exception as e:
            logger.exception("Error sending media risk message: %s", e)

        # Explanability for media (e.g., lighting / texture inconsistencies)
        explain = format_explainability(highlights)
        if explain:
            try:
                await message.reply_text(explain, parse_mode="Markdown")
            except Exception:
                pass

    except Exception as e:
        logger.exception("handle_media error: %s", e)
        try:
            await message.reply_text(f"⚠️ Internal bot error: {e}")
        except Exception:
            pass


# ================== BUTTON HANDLER ==================


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ""

    parts = data.split(":")
    action = parts[0] if parts else ""

    # ---- BLOCK PAYMENT ----
    if action == "block":
        await query.edit_message_text(
            "🛑 *Payment Blocked (Simulation)*\n\n"
            "In a real integration, this would notify your bank or payment "
            "provider to freeze the suspicious transaction.",
            parse_mode="Markdown",
        )
        return

    # ---- MARK SAFE ----
    if action == "safe":
        await query.edit_message_text(
            "✅ Marked as safe.\n"
            "Your feedback helps Scamp reduce false positives over time."
        )
        return

    # ---- GENERATE REPORT (text summary + PDF) ----
    if action == "report":
        # callback_data = f"report:{event_id}:{media_type}:{score}"
        try:
            event_id = int(parts[1])
        except (IndexError, ValueError):
            event_id = -1

        media_type = parts[2] if len(parts) > 2 else "unknown"

        try:
            score = float(parts[3]) if len(parts) > 3 else 0.0
        except ValueError:
            score = 0.0

        risk = bucketize_risk(score)

        risk_label = {
            "low": "Lower",
            "medium": "Medium",
            "high": "High",
        }.get(risk, "Unknown")

        range_note = {
            "low": "(0–40)",
            "medium": "(40–75)",
            "high": "(75–100)",
        }.get(risk, "")

        media_human = {
            "text": "Text message",
            "image": "Image / screenshot",
            "audio": "Voice / audio note",
        }.get(media_type, media_type or "Unknown")

        # Give quick feedback in the same message
        try:
            await query.edit_message_text(
                "📄 Generating detailed report...",
                parse_mode="Markdown",
            )
        except Exception:
            pass

        # ---- Call backend /report/{event_id} to get the PDF ----
        pdf_bytes = None
        try:
            if event_id > 0:
                resp = requests.get(
                    f"{BACKEND_URL}/report/{event_id}",
                    timeout=60,
                )
                if resp.status_code == 200:
                    pdf_bytes = resp.content
                else:
                    logger.warning(
                        "Backend /report/%s returned status %s: %s",
                        event_id,
                        resp.status_code,
                        resp.text[:200],
                    )
        except Exception as e:
            logger.exception("Error calling backend /report: %s", e)

        # ---- Build inline text report ----
        report_text = (
            "📄 *Scam Analysis Report*\n\n"
            f"*Event ID:* `{event_id}`\n"
            f"*Channel:* Telegram\n"
            f"*Content type:* {media_human}\n\n"
            f"*Risk level:* *{risk_label}* {range_note}\n"
            f"*Score:* *{score:.2f}%*\n\n"
        )

        if risk == "high":
            report_text += (
                "✅ *Recommendation:*\n"
                "- Do *NOT* proceed with any payment.\n"
                "- Do *NOT* share OTP, PIN, or card details.\n"
                "- Verify directly from your bank’s official app/website.\n\n"
            )
        elif risk == "medium":
            report_text += (
                "⚠️ *Recommendation:*\n"
                "- Treat this as suspicious.\n"
                "- Double‑check links, phone numbers, and payment requests.\n"
                "- Use only official apps/websites to verify.\n\n"
            )
        else:  # low
            report_text += (
                "ℹ️ *Recommendation:*\n"
                "- No strong scam patterns detected, but scams can still occur.\n"
                "- Avoid clicking unknown links or sharing sensitive info.\n\n"
            )

        report_text += (
            "*How to report this scam:*\n"
            "- Do not reply to the suspicious sender.\n"
            "- Forward this message and report to your bank’s official support or local cybercrime helpline.\n"
            "- If you already shared money or sensitive info, contact your bank immediately to block cards/UPI.\n\n"
            "_You can also review the 'Why this looks risky' message in the chat for the exact trigger signals I detected._"
        )

        # Send the text summary as a new message
        await query.message.reply_text(report_text, parse_mode="Markdown")

        # Attach PDF if we got it from backend
        if pdf_bytes:
            try:
                await query.message.reply_document(
                    document=BytesIO(pdf_bytes),
                    filename=f"scamp_report_{event_id}.pdf",
                    caption="📎 Detailed PDF report attached.",
                )
            except Exception as e:
                logger.exception("Failed to send PDF document: %s", e)
        else:
            # If PDF failed, at least tell the user
            try:
                await query.message.reply_text(
                    "⚠️ I couldn't attach the PDF report this time, but the summary above is still valid."
                )
            except Exception:
                pass

        return

    # ---- FALLBACK ----
    await query.edit_message_text("Unknown action.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I didn't understand that command.\n"
        "Send me an image, voice note, or suspicious message, or use /help for instructions."
    )


# ================== MAIN ==================


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set. Please set it as an environment variable."
        )

    # Increase Telegram HTTP timeouts a bit
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0,
    )

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Send ALL non-command messages into handle_media
    app.add_handler(MessageHandler(~filters.COMMAND, handle_media))

    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Scamp Telegram bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
