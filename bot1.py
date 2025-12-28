import os
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from database import (
    save_promo,
    list_promos,
    get_promo
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
# ADMIN_IDS = {123456789}  # 🔴 replace with your Telegram ID


# ================= UTIL =================

async def auto_delete(bot, chat_id, message_id, delay=120):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass


def schedule_delete(context, message, delay=120):
    asyncio.create_task(
        auto_delete(
            context.bot,
            message.chat_id,
            message.message_id,
            delay
        )
    )


def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            msg = await update.message.reply_text("❌ Admin only command.")
            schedule_delete(context, msg)
            return
        await func(update, context)
    return wrapper


# ================= COMMANDS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Commands:\n"
        "/promos <name> – Get a promotion\n"
        "/help – Help"
    )
    schedule_delete(context, msg)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(
        "📖 Help\n\n"
        "/promos <name> – Get promo\n"
        "/promos – Show suggestions\n"
        "/help – This help"
    )
    schedule_delete(context, msg)


# ================= PROMOS =================

async def promos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_promos = list_promos()

    if not all_promos:
        msg = await update.message.reply_text("No promos available.")
        schedule_delete(context, msg)
        return

    if context.args:
        query = context.args[0].lower()
        matched = [p for p in all_promos if query in p.lower()]
    else:
        matched = all_promos[:5]

    if not matched:
        msg = await update.message.reply_text("No matching promos found.")
        schedule_delete(context, msg)
        return

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"promo:{name}")]
        for name in matched
    ]

    msg = await update.message.reply_text(
        "📦 Choose a promo:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    schedule_delete(context, msg)


async def promo_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    name = query.data.split(":", 1)[1]
    promo = get_promo(name)

    if not promo:
        await query.message.reply_text("❌ Promo not found.")
        return

    file_id, media_type = promo
    user_id = query.from_user.id
    

    if media_type == "photo":
        await query.message.reply_photo(user_id, file_id)
    elif media_type == "video":
        await query.message.reply_video(user_id, file_id)
    else:
        await query.message.reply_document(user_id, file_id)


# ================= ADMIN SAVE =================

@admin_only
async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        msg = await update.message.reply_text("Usage: /save promo_name")
        schedule_delete(context, msg)
        return

    promo_name = context.args[0]
    context.user_data["pending_promo"] = promo_name

    msg = await update.message.reply_text(
        "📤 Send the promo media now."
    )
    schedule_delete(context, msg)


@admin_only
async def capture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    promo_name = context.user_data.get("pending_promo")
    if not promo_name:
        return

    msg = update.message

    if msg.photo:
        file_id = msg.photo[-1].file_id
        media = "photo"
    elif msg.video:
        file_id = msg.video.file_id
        media = "video"
    elif msg.document:
        file_id = msg.document.file_id
        media = "document"
    else:
        return

    save_promo(promo_name, file_id, media)
    context.user_data.pop("pending_promo", None)

    confirm = await msg.reply_text(f"✅ Promo '{promo_name}' saved.")
    schedule_delete(context, confirm)


# ================= FALLBACK =================

async def invalid_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(
        "ℹ️ Invalid message.\n\n"
        "Use:\n"
        "/promos <name>\n"
        "/help"
    )
    schedule_delete(context, msg)


# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("promos", promos))
    app.add_handler(CommandHandler("save", save))

    app.add_handler(CallbackQueryHandler(promo_click, pattern="^promo:"))
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, capture))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_message)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
