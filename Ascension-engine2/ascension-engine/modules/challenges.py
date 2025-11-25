"""
modules/challenges.py
Dark Mode Ascension Challenges — Animated UI
Daily + Weekly challenge system for PWN Ascension.

Handles:
- Challenge definitions
- Progress tracking
- Completion bonuses
- Dark Mode animated UI rendering
"""

from datetime import datetime
from database import load_db, save_db, get_user
from ui.components import render_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.animations import animated_fire_cosmic_bar


# ---------------------------------------------------------
# CHALLENGE DEFINITIONS
# ---------------------------------------------------------
def get_challenge_definitions():
    return {
        "daily": {
            "grinds_today": {
                "title": "Grind 20 times today",
                "required": 20,
                "description": "You gain speed, momentum, and discipline.",
                "reward_xp": 200
            },
            "xp_today": {
                "title": "Earn 500 XP today",
                "required": 500,
                "description": "Push yourself past your daily limit.",
                "reward_xp": 300
            },
            "streak_day": {
                "title": "Maintain your streak today",
                "required": 1,
                "description": "Log in and grind at least once today.",
                "reward_xp": 150
            }
        },
        "weekly": {
            "xp_week": {
                "title": "Earn 5,000 XP this week",
                "required": 5000,
                "description": "Only the consistent rise.",
                "reward_xp": 500
            },
            "grinds_week": {
                "title": "Perform 100 grinds this week",
                "required": 100,
                "description": "Prove your dedication.",
                "reward_xp": 600
            },
            "badge_collector": {
                "title": "Unlock a new badge this week",
                "required": 1,
                "description": "Badge collectors dominate the hall of honor.",
                "reward_xp": 300
            }
        }
    }


# ---------------------------------------------------------
# UPDATE CHALLENGE PROGRESS
# (Called by grinding.py)
# ---------------------------------------------------------
def update_challenge_progress(user_id, field, value):
    db = load_db()
    uid = str(user_id)

    if uid not in db:
        return

    user = db[uid]
    challenges = user.setdefault("challenges", {
        "daily": {},
        "weekly": {}
    })

    # Update both daily & weekly if field matches
    if field in challenges["daily"]:
        challenges["daily"][field]["current"] = value

    if field in challenges["weekly"]:
        challenges["weekly"][field]["current"] = value

    save_db(db)


# ---------------------------------------------------------
# UI HANDLER
# ---------------------------------------------------------
def handle_challenges_callback(bot, update):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    user = get_user(user_id)

    if data == "ch_main" or data == "challenges_main":
        return _show_challenges_dark_mode(bot, update)

    return query.answer()


# ---------------------------------------------------------
# INTERNAL: RENDER DARK MODE CHALLENGE SCREEN
# ---------------------------------------------------------
def _show_challenges_dark_mode(bot, update):
    """Main Dark Mode Challenges UI with Fire + Cosmic animation."""
    query = update.callback_query
    user = get_user(query.from_user.id)
    db = load_db()

    uid = str(query.from_user.id)
    challenges = db[uid].setdefault("challenges", {"daily": {}, "weekly": {}})
    defs = get_challenge_definitions()

    # Initialize current challenge progress if missing
    for section in ["daily", "weekly"]:
        for cname, c in defs[section].items():
            challenges[section].setdefault(cname, {
                "current": 0,
                "completed": False
            })

    save_db(db)

    # Show loading message and run fire+cosmic animation
    query.edit_message_text(
        text="🔥 Loading progress…",
        parse_mode="Markdown"
    )

    # Run the Fire + Cosmic Glow animation
    animated_fire_cosmic_bar(
        bot=bot,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        total_steps=10,
        delay=0.18
    )

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

    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
