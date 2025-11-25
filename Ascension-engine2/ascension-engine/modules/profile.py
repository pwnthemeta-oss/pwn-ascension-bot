"""
modules/profile.py
Profile screen, grind initiator, and power stats panel.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_user, save_db
from ui.components import render_text

# Grinding engine
from modules.grinding import perform_grind


# ----------------------------------------------------
# Profile main screen
# ----------------------------------------------------
def handle_profile_command(bot, update):
    """Handles /profile typed command."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    user = get_user(user_id)
    _send_profile(bot, chat_id, user)


# ----------------------------------------------------
# INTERNAL: Send new profile message
# ----------------------------------------------------
def _send_profile(bot, chat_id, user):
    rank = user.get("rank", "Bronze")
    xp = user.get("xp", 0)
    streak = user.get("streak", 0)
    grinds = user.get("grinds_today", 0)
    badges = user.get("badges", [])
    
    badge_count = len(badges)
    
    # Badge emoji mapping
    badge_emojis = {
        "Initiate": "🎖",
        "First Grind": "⚡",
        "XP Hunter": "🏹",
        "Streak Master": "🔥",
        "Grind Lord": "👑",
        "Diamond Rank": "💎",
        "Challenge Complete": "🏆",
        "Week Warrior": "⚔️"
    }
    
    # Badge grid (2 rows x 4 columns)
    icons = []
    for badge in badges[:8]:
        if isinstance(badge, dict):
            icons.append(badge.get("emoji", "⬛"))
        else:
            icons.append(badge_emojis.get(badge, "⬛"))
    
    while len(icons) < 8:
        icons.append("⬛")
    
    grid = (
        f"{icons[0]} {icons[1]} {icons[2]} {icons[3]}\n"
        f"{icons[4]} {icons[5]} {icons[6]} {icons[7]}"
    )
    
    # XP progress bar
    progress = min(100, int((xp % 1000) / 10))
    filled = progress // 10
    empty = 10 - filled
    bar = "🔥" * filled + "░" * empty
    
    text = (
        "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥\n"
        "      ⚡ *YOUR PROFILE* ⚡\n"
        "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥\n\n"
        f"🏅 *Rank:* {rank}\n"
        f"⚡ *XP:* {xp}\n"
        f"🔥 *Streak:* {streak} days\n"
        f"🛠 *Grinds Today:* {grinds}\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"⭐ *BADGES UNLOCKED:* {badge_count}\n"
        f"{grid}\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🚀 *ASCENSION STATUS*\n"
        f"{bar}  {progress}%\n\n"
        "✨ \"A new flame flickers within you…\""
    )

    text = render_text(user, text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Grind", callback_data="prof_grind")],
        [InlineKeyboardButton("🏅 Badges", callback_data="badge_main")],
        [InlineKeyboardButton("📜 Activity Log", callback_data="act_0")],
        [InlineKeyboardButton("💠 Power Stats", callback_data="prof_stats")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])

    bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# ----------------------------------------------------
# INTERNAL: Edit existing profile message
# ----------------------------------------------------
def _edit_profile(bot, query, user):
    rank = user.get("rank", "Bronze")
    xp = user.get("xp", 0)
    streak = user.get("streak", 0)
    grinds = user.get("grinds_today", 0)
    badges = user.get("badges", [])
    
    badge_count = len(badges)
    
    # Badge emoji mapping
    badge_emojis = {
        "Initiate": "🎖",
        "First Grind": "⚡",
        "XP Hunter": "🏹",
        "Streak Master": "🔥",
        "Grind Lord": "👑",
        "Diamond Rank": "💎",
        "Challenge Complete": "🏆",
        "Week Warrior": "⚔️"
    }
    
    # Badge grid (2 rows x 4 columns)
    icons = []
    for badge in badges[:8]:
        if isinstance(badge, dict):
            icons.append(badge.get("emoji", "⬛"))
        else:
            icons.append(badge_emojis.get(badge, "⬛"))
    
    while len(icons) < 8:
        icons.append("⬛")
    
    grid = (
        f"{icons[0]} {icons[1]} {icons[2]} {icons[3]}\n"
        f"{icons[4]} {icons[5]} {icons[6]} {icons[7]}"
    )
    
    # XP progress bar
    progress = min(100, int((xp % 1000) / 10))
    filled = progress // 10
    empty = 10 - filled
    bar = "🔥" * filled + "░" * empty
    
    text = (
        "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥\n"
        "      ⚡ *YOUR PROFILE* ⚡\n"
        "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥\n\n"
        f"🏅 *Rank:* {rank}\n"
        f"⚡ *XP:* {xp}\n"
        f"🔥 *Streak:* {streak} days\n"
        f"🛠 *Grinds Today:* {grinds}\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"⭐ *BADGES UNLOCKED:* {badge_count}\n"
        f"{grid}\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🚀 *ASCENSION STATUS*\n"
        f"{bar}  {progress}%\n\n"
        "✨ \"A new flame flickers within you…\""
    )

    text = render_text(user, text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Grind", callback_data="prof_grind")],
        [InlineKeyboardButton("🏅 Badges", callback_data="badge_main")],
        [InlineKeyboardButton("📜 Activity Log", callback_data="act_0")],
        [InlineKeyboardButton("💠 Power Stats", callback_data="prof_stats")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])

    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# ----------------------------------------------------
# Grind callback handler
# ----------------------------------------------------
def handle_profile_callback(bot, update):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data == "prof_main":
        user = get_user(user_id)
        _edit_profile(bot, query, user)

    elif data == "prof_grind":
        return _handle_grind(bot, update)

    elif data == "prof_stats":
        return _show_power_stats(bot, update)


# ----------------------------------------------------
# GRIND LOGIC UI WRAPPER
# ----------------------------------------------------
def _handle_grind(bot, update):
    query = update.callback_query
    user_id = query.from_user.id

    result_type, value = perform_grind(user_id)
    user = get_user(user_id)

    # COOL DOWN
    if result_type == "cooldown":
        text = render_text(user, f"⏳ *Cooldown Active*\nWait *{value} seconds*.")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("↩️ Back", callback_data="prof_main")]
        ])
        return query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    # BADGE UNLOCK
    if result_type == "badge":
        text = render_text(user, f"🎖 *BADGE UNLOCKED!*\nYou earned: *{value}*")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("View Badges", callback_data="badge_main")],
            [InlineKeyboardButton("Continue", callback_data="prof_main")],
        ])
        return query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    # RANK UP
    if result_type == "rankup":
        text = render_text(user, f"🏅 *RANK UP!*\nYou are now *{value}*.")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Continue", callback_data="prof_main")]
        ])
        return query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    # STREAK MILESTONE
    if result_type == "streak_milestone":
        text = render_text(user, f"🔥 *STREAK MILESTONE*\nYou've reached *{value} days*!")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Continue", callback_data="prof_main")]
        ])
        return query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

    # SUCCESS
    return handle_profile_callback(bot, update)


# ----------------------------------------------------
# POWER STATS PANEL
# ----------------------------------------------------
def _show_power_stats(bot, update):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_user(user_id)

    streak = user.get("streak", 0)
    multiplier = 1 + (streak // 10) * 0.1

    text = (
        "💠 *POWER STATS*\n\n"
        f"⚡ XP: {user.get('xp', 0)}\n"
        f"🔥 Streak: {streak} days\n"
        f"🏅 Rank: {user.get('rank')}\n"
        f"🔋 Grind Multiplier: x{multiplier}\n\n"
        "Your stats influence your entire Ascension journey."
    )

    text = render_text(user, text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="prof_main")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")]
    ])

    query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)
