"""
modules/challenges_command.py
Handles /challenges command - displays Dark Mode challenges with Fire+Cosmic animation
"""

from database import get_user
from ui.components import render_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.animations import animated_fire_cosmic_bar
from modules.challenges import get_challenge_definitions


def handle_challenges_command(bot, update):
    """Handle /challenges command - show challenges with animation."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user = get_user(user_id)

    # Send loading message
    msg = bot.send_message(
        chat_id=chat_id,
        text="🔥 Loading your challenges…",
        parse_mode="Markdown"
    )

    # Run Fire + Cosmic Glow animation
    animated_fire_cosmic_bar(
        bot=bot,
        chat_id=chat_id,
        message_id=msg.message_id,
        total_steps=10,
        delay=0.18
    )

    # Get challenge data
    from database import load_db
    db = load_db()
    uid = str(user_id)
    challenges = db[uid].setdefault("challenges", {"daily": {}, "weekly": {}})
    defs = get_challenge_definitions()

    # Initialize current challenge progress if missing
    for section in ["daily", "weekly"]:
        for cname, c in defs[section].items():
            challenges[section].setdefault(cname, {
                "current": 0,
                "completed": False
            })

    from database import save_db
    save_db(db)

    # Helper: draw progress bars
    def bar(current, total, length=10):
        filled = int((current / total) * length) if total > 0 else 0
        empty = length - filled
        return "█" * filled + "░" * empty

    # Get challenge progress
    daily_grinds = challenges["daily"]["grinds_today"]["current"]
    daily_xp = challenges["daily"]["xp_today"]["current"]
    streak_done = 1 if challenges["daily"]["streak_day"]["current"] >= 1 else 0

    weekly_xp = challenges["weekly"]["xp_week"]["current"]
    weekly_grinds = challenges["weekly"]["grinds_week"]["current"]
    weekly_badges = challenges["weekly"]["badge_collector"]["current"]

    text = render_text(user, f"""
🌑🌘🌗🌖  *DAILY + WEEKLY CHALLENGES*  🌖🌗🌘🌑
*Loading your assignments…* ✦✦✦


🔥 *DAILY MISSIONS*
━━━━━━━━━━━━━━━━━━

⚡ *Grind 20 times*
Progress: `{bar(daily_grinds, 20)}` {daily_grinds}/20

💠 *Earn 500 XP*
Progress: `{bar(daily_xp, 500)}` {daily_xp}/500

🌙 *Maintain your streak*
Progress: `{"●" if streak_done else "○"}{"○" if not streak_done else ""}`  {streak_done}/1


━━━━━━━━━━━━━━━━━━
🏆 *WEEKLY MISSIONS*
━━━━━━━━━━━━━━━━━━

💥 *Earn 5,000 XP*
Progress: `{bar(weekly_xp, 5000)}` {weekly_xp}/5000

⚙️ *Complete 100 grinds*
Progress: `{bar(weekly_grinds, 100)}` {weekly_grinds}/100

✨ *Unlock 1 New Badge*
Progress: `{"●" if weekly_badges > 0 else "○"}{"○" if weekly_badges == 0 else ""}` {weekly_badges}/1


━━━━━━━━━━━━━━━━━━
*"Choose your path… rise higher."*
""")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
        [InlineKeyboardButton("🧿 Profile", callback_data="prof_main")],
    ])

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg.message_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
