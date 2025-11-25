"""
modules/start.py
Handles /start command + first-time welcome screen.
Short, punchy welcome with dark mode theme.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import init_user, get_user
from ui.components import render_text


# ---------------------------------------------------------
# /start COMMAND - SHORT WELCOME SCREEN
# ---------------------------------------------------------
def handle_start_command(bot, update):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username

    # Initialize user in database
    init_user(user_id, username)
    user = get_user(user_id)

    # Check if user is verified
    if not user.get("verified", False):
        return send_verification_screen(bot, update)

    text = (
        "💠✨ *PWN ASCENSION* ✨💠\n"
        "🌑 *DARK MODE ACTIVE* 🌑\n\n"
        "🔥 *WELCOME, ASCENDER* 🔥\n"
        "You've activated the *Ascension Engine* — your XP reactor, rank booster, and evolution core.\n\n"
        "Every action lifts you higher. 🌌⚡\n\n"
        "*Ready to rise?* 🚀"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Begin Ascension", callback_data="onb_next")],
        [InlineKeyboardButton("🌌 What is PWN?", callback_data="help_main")],
        [InlineKeyboardButton("🏆 Leaderboards", callback_data="lb_xp")],
        [InlineKeyboardButton("🧿 My Profile", callback_data="prof_main")],
    ])

    bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


def send_verification_screen(bot, update):
    chat_id = update.effective_chat.id
    
    text = (
        "🔐 *VERIFICATION REQUIRED*\n\n"
        "Before you begin, confirm you're human."
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 Begin Verification", callback_data="verify_reason_start")]
    ])
    
    bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
