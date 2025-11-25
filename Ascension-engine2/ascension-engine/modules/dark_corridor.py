"""
modules/dark_corridor.py
BALANCED DARK CORRIDOR RNG

Doors:
• Treasure  → small XP gain
• Trap      → small XP loss
• Teleport  → goes deeper
• Secret    → rare tiny bonus

Streak increases difficulty slightly but XP stays controlled.
"""

import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_user, load_db, save_db
from ui.components import render_text


TREASURE_MIN = 25
TREASURE_MAX = 75

TRAP_MIN = 5
TRAP_MAX = 20

SECRET_MIN = 10
SECRET_MAX = 35

DEPTH_FACTOR = 1.12
STREAK_FACTOR = 0.03


def handle_dark_corridor_callback(bot, update):
    q = update.callback_query
    q.answer()
    data = q.data

    if data == "game_corridor":
        return _intro(bot, update)

    if data.startswith("door_pick_"):
        _, _, door_index, depth = data.split("_")
        return _resolve_choice(bot, update, int(door_index), int(depth))


def _intro(bot, update):
    q = update.callback_query
    q.answer()
    user = get_user(q.from_user.id)

    text = render_text(user,
        "3️⃣ *DARK CORRIDOR*\n\n"
        "Three doors lie ahead...\n\n"
        "🚪  🚪  🚪\n\n"
        "Behind one: *TREASURE* 💰 (+small XP)\n"
        "Behind another: *TRAP* 💀 (small XP loss)\n"
        "The last: *TELEPORT* 🌀 (go deeper)\n\n"
        "Rare chance for a *SECRET ROOM* ✨\n"
        "Streak slightly increases difficulty and reward."
    )

    k = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚪", callback_data="door_pick_0_0"),
            InlineKeyboardButton("🚪", callback_data="door_pick_1_0"),
            InlineKeyboardButton("🚪", callback_data="door_pick_2_0")
        ],
        [InlineKeyboardButton("↩️ Back", callback_data="games_main")]
    ])

    q.edit_message_text(text=text, parse_mode="Markdown", reply_markup=k)


def _resolve_choice(bot, update, door, depth):
    q = update.callback_query
    q.answer()
    user_id = q.from_user.id
    user = get_user(user_id)

    db = load_db()
    uid = str(user_id)

    streak = user.get("streak", 0)

    multiplier = (1 + STREAK_FACTOR * streak) * (DEPTH_FACTOR ** depth)

    outcomes = ["treasure", "trap", "teleport"]
    
    if random.random() < 0.05:
        outcomes = ["secret"]
    else:
        random.shuffle(outcomes)

    outcome = outcomes[door] if len(outcomes) > 1 else "secret"

    if outcome == "treasure":
        amount = random.randint(TREASURE_MIN, TREASURE_MAX)
        amount = int(amount * multiplier)

        db[uid]["xp"] += amount
        db[uid]["weekly"]["xp"] = db[uid].get("weekly", {}).get("xp", 0) + amount
        save_db(db)

        text = render_text(user,
            f"💰 *TREASURE!*\n\n"
            f"You gained +{amount} XP.\n"
            f"Depth {depth} | Streak bonus applied."
        )

        return q.edit_message_text(
            text=text, parse_mode="Markdown", reply_markup=_next(depth)
        )

    if outcome == "trap":
        amount = random.randint(TRAP_MIN, TRAP_MAX)
        amount = int(amount * multiplier)

        db[uid]["xp"] = max(0, db[uid]["xp"] - amount)
        save_db(db)

        text = render_text(user,
            f"💀 *A TRAP!* You lost −{amount} XP.\n"
            f"Depth {depth} | Streak scaling."
        )

        return q.edit_message_text(text=text, parse_mode="Markdown", reply_markup=_after())

    if outcome == "secret":
        amount = random.randint(SECRET_MIN, SECRET_MAX)
        amount = int(amount * multiplier)

        db[uid]["xp"] += amount
        db[uid]["weekly"]["xp"] = db[uid].get("weekly", {}).get("xp", 0) + amount
        save_db(db)

        text = render_text(user,
            f"✨ *SECRET ROOM FOUND!*\n\n"
            f"Hidden treasure grants +{amount} XP."
        )

        return q.edit_message_text(text=text, parse_mode="Markdown", reply_markup=_next(depth))

    new_depth = depth + 1

    text = render_text(user,
        f"🌀 *TELEPORT!* You go deeper...\n"
        f"Depth is now {new_depth}."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚪", callback_data=f"door_pick_0_{new_depth}"),
            InlineKeyboardButton("🚪", callback_data=f"door_pick_1_{new_depth}"),
            InlineKeyboardButton("🚪", callback_data=f"door_pick_2_{new_depth}"),
        ],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")]
    ])

    return q.edit_message_text(text=text, parse_mode="Markdown", reply_markup=keyboard)


def _next(depth):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Continue", callback_data=f"door_pick_0_{depth+1}")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")]
    ])


def _after():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Try Again", callback_data="door_pick_0_0")],
        [InlineKeyboardButton("🎮 Games", callback_data="games_main")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])
