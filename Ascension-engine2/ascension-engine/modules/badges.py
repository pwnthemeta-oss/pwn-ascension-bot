"""
modules/badges.py
Badge UI screens for PWN Ascension Engine.

Includes:
- Badge list screen
- Badge details screen
- Progress bars
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_user, load_db, save_db
from ui.components import render_text


# ---------------------------------------------------------
# MAIN BADGES MENU
# ---------------------------------------------------------
def handle_badges_callback(bot, update):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data == "badge_main":
        return _show_badge_list(bot, update)

    if data.startswith("badge_detail_"):
        badge_name = data.replace("badge_detail_", "")
        return _show_badge_detail(bot, update, badge_name)

    if data == "badge_back":
        return _show_badge_list(bot, update)


# ---------------------------------------------------------
# BADGE LIST SCREEN (GOLD MODE)
# ---------------------------------------------------------
def _show_badge_list(bot, update):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_user(user_id)

    badge_defs = get_badge_definitions()
    unlocked = user.get("badges", [])

    # EMOJI MAP
    emoji_map = {
        "Initiate": "🟦",
        "First Grind": "🔥",
        "Grind Master": "⚡",
        "Streak Keeper": "📅",
        "Streak Legend": "💀",
        "XP Hunter": "📈",
        "XP Champion": "🏆",
        "Dominator": "⚙️",
    }

    total_badges = len(badge_defs)
    unlocked_count = len(unlocked)

    text = (
        "👑✨👑  *GOLD BADGE VAULT*  👑✨👑\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏆 *Badges Unlocked:* {unlocked_count} / {total_badges}\n\n"
    )

    if not unlocked:
        text += "_You haven't unlocked any badges yet._\n\n"
    else:
        for b in unlocked:
            emoji = emoji_map.get(b, "🔸")
            text += f"{emoji} {b}\n"
        text += "\n"

    text += (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 *Badge Grid*\n"
    )

    all_badge_names = list(badge_defs.keys())
    grid_emojis = [emoji_map.get(name, "🔸") for name in all_badge_names]
    
    for i in range(0, len(grid_emojis), 4):
        row_emojis = grid_emojis[i:i+4]
        row_text = " ".join([f"[{e}]" for e in row_emojis])
        text += row_text + "\n"

    text += (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "\"Your legacy shines brighter today.\""
    )

    text = render_text(user, text)

    # Build button grid
    keyboard_rows = []
    for badge_name in badge_defs.keys():
        keyboard_rows.append([
            InlineKeyboardButton(
                f"{emoji_map.get(badge_name, '🔸')} {badge_name}",
                callback_data=f"badge_detail_{badge_name}"
            )
        ])

    keyboard_rows.append([InlineKeyboardButton("🏠 Menu", callback_data="menu_main")])
    keyboard_rows.append([InlineKeyboardButton("🧿 Profile", callback_data="prof_main")])

    keyboard = InlineKeyboardMarkup(keyboard_rows)

    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# ---------------------------------------------------------
# BADGE DETAIL SCREEN
# ---------------------------------------------------------
def _show_badge_detail(bot, update, badge_name):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_user(user_id)
    unlocked = user.get("badges", [])

    defs = get_badge_definitions()
    info = defs.get(badge_name, {})

    title = info.get("title", badge_name)
    desc = info.get("description", "")
    required_type = info.get("type")

    text = f"📜 *{badge_name}*\n\n{desc}\n\n"

    # If unlocked
    if badge_name in unlocked:
        text += "✅ *Unlocked*\n"
    else:
        # Progress display
        progress = get_badge_progress(user, badge_name)
        text += f"Progress: `{progress}`\n"

    text = render_text(user, text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("↩️ Back", callback_data="badge_main")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])

    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# ---------------------------------------------------------
# BADGE DEFINITIONS
# ---------------------------------------------------------
def get_badge_definitions():
    """Return all badge definitions."""
    return {
        "Initiate": {
            "title": "Initiate",
            "description": "Complete the onboarding process and begin your ascension.",
            "type": "onboarding_complete",
            "required_value": True
        },
        "First Grind": {
            "title": "First Grind",
            "description": "Complete your first grind session.",
            "type": "grinds",
            "required_value": 1
        },
        "Grind Master": {
            "title": "Grind Master",
            "description": "Complete 100 grind sessions.",
            "type": "grinds",
            "required_value": 100
        },
        "Streak Keeper": {
            "title": "Streak Keeper",
            "description": "Maintain a 7-day streak.",
            "type": "streak",
            "required_value": 7
        },
        "Streak Legend": {
            "title": "Streak Legend",
            "description": "Maintain a 30-day streak.",
            "type": "streak",
            "required_value": 30
        },
        "XP Hunter": {
            "title": "XP Hunter",
            "description": "Reach 1000 XP.",
            "type": "xp",
            "required_value": 1000
        },
        "XP Champion": {
            "title": "XP Champion",
            "description": "Reach 10000 XP.",
            "type": "xp",
            "required_value": 10000
        },
        "Dominator": {
            "title": "Dominator",
            "description": "Finish in the top 3 on the weekly leaderboard.",
            "type": "top3",
            "required_value": True
        }
    }


# ---------------------------------------------------------
# CHECK FOR NEW BADGES
# ---------------------------------------------------------
def check_for_new_badges(user_id: int):
    """
    Check if the user has earned any new badges.
    Returns the name of a new badge, or None.
    """
    db = load_db()
    uid = str(user_id)
    
    if uid not in db:
        return None
    
    user = db[uid]
    unlocked = user.get("badges", [])
    definitions = get_badge_definitions()
    
    for badge_name, badge_info in definitions.items():
        # Skip if already unlocked
        if badge_name in unlocked:
            continue
        
        badge_type = badge_info.get("type")
        required_value = badge_info.get("required_value")
        
        # Check if user meets requirements
        earned = False
        
        if badge_type == "onboarding_complete":
            earned = user.get("onboarding_complete", False)
        
        elif badge_type == "grinds":
            total_grinds = user.get("weekly", {}).get("grinds", 0)
            earned = total_grinds >= required_value
        
        elif badge_type == "streak":
            earned = user.get("streak", 0) >= required_value
        
        elif badge_type == "xp":
            earned = user.get("xp", 0) >= required_value
        
        elif badge_type == "top3":
            earned = user.get("weekly", {}).get("top3", False)
        
        if earned:
            # Award the badge
            user.setdefault("badges", []).append(badge_name)
            save_db(db)
            return badge_name
    
    return None


# ---------------------------------------------------------
# GET BADGE PROGRESS
# ---------------------------------------------------------
def get_badge_progress(user, badge_name):
    """
    Return a progress string for a badge.
    """
    definitions = get_badge_definitions()
    badge_info = definitions.get(badge_name, {})
    
    badge_type = badge_info.get("type")
    required_value = badge_info.get("required_value")
    
    if badge_type == "onboarding_complete":
        return "Complete onboarding" if not user.get("onboarding_complete", False) else "Completed"
    
    elif badge_type == "grinds":
        total_grinds = user.get("weekly", {}).get("grinds", 0)
        return f"{total_grinds}/{required_value} grinds"
    
    elif badge_type == "streak":
        current_streak = user.get("streak", 0)
        return f"{current_streak}/{required_value} days"
    
    elif badge_type == "xp":
        current_xp = user.get("xp", 0)
        return f"{current_xp}/{required_value} XP"
    
    elif badge_type == "top3":
        return "Finish top 3 on weekly leaderboard"
    
    return "Unknown"
