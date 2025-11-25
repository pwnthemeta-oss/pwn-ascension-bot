"""
modules/quantum_flip.py
QUANTUM FLIP — User Picks Heads or Tails

Outcomes:
• User guesses HEADS or TAILS
• Coin result is random: Heads / Tails / Edge (1%)
• Correct guess = +100 XP
• Wrong guess = –20 XP
• Edge = +500 XP + Rare Badge
"""

import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_user, load_db, save_db
from ui.components import render_text

XP_CORRECT = 100
XP_WRONG = 20
XP_EDGE = 500

RARE_BADGE_NAME = "Quantum Master"


# ---------------------------------------------------------
# Callback Handler
# ---------------------------------------------------------
def handle_quantum_callback(bot, update):
    q = update.callback_query
    data = q.data

    if data == "game_quantum":
        return intro(bot, update)

    if data.startswith("quantum_pick_"):
        _, _, user_pick = data.split("_")
        return flip(bot, update, user_pick)


# ---------------------------------------------------------
# Intro screen
# ---------------------------------------------------------
def intro(bot, update):
    q = update.callback_query
    user = get_user(q.from_user.id)

    text = render_text(
        user,
        "⚛️ *QUANTUM FLIP — PREDICTION MODE* ⚛️\n\n"
        "Pick your fate:\n"
        "• ⚛️ Heads → +100 XP if correct\n"
        "• ⚛️ Tails → +100 XP if correct\n"
        "• ⚛️ Edge (1%) → +500 XP + Rare Badge\n\n"
        "Choose wisely…"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚛️ Heads", callback_data="quantum_pick_heads"),
            InlineKeyboardButton("⚛️ Tails", callback_data="quantum_pick_tails"),
        ],
        [InlineKeyboardButton("↩️ Back", callback_data="games_main")]
    ])

    q.edit_message_text(text=text, parse_mode="Markdown", reply_markup=keyboard)


# ---------------------------------------------------------
# Execute the Flip
# ---------------------------------------------------------
def flip(bot, update, user_pick):
    q = update.callback_query
    user_id = q.from_user.id
    user = get_user(user_id)

    db = load_db()
    uid = str(user_id)

    # Determine actual coin outcome
    # 1% Edge
    if random.random() < 0.01:
        outcome = "edge"
    else:
        outcome = random.choice(["heads", "tails"])

    # -------------------------------
    # EDGE EVENT
    # -------------------------------
    if outcome == "edge":
        db[uid]["xp"] += XP_EDGE

        # Award badge if not unlocked
        if RARE_BADGE_NAME not in db[uid]["badges"]:
            db[uid]["badges"].append(RARE_BADGE_NAME)

        save_db(db)

        text = render_text(
            user,
            f"⚛️✨ *INCREDIBLE — COIN LANDED ON ITS EDGE!* ✨⚛️\n\n"
            f"You picked: *{user_pick.title()}*\n"
            f"Coin result: **EDGE**\n\n"
            f"+{XP_EDGE} XP\n"
            f"🎖️ Badge unlocked: *{RARE_BADGE_NAME}*"
        )

        return q.edit_message_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=_again_menu()
        )

    # -------------------------------
    # HEADS / TAILS LOGIC
    # -------------------------------
    correct = (user_pick == outcome)

    if correct:
        db[uid]["xp"] += XP_CORRECT
        save_db(db)

        text = render_text(
            user,
            f"⚛️ *YOU GUESSED CORRECT!* ⚛️\n\n"
            f"You picked: *{user_pick.title()}*\n"
            f"Coin result: *{outcome.title()}*\n\n"
            f"+{XP_CORRECT} XP"
        )
    else:
        db[uid]["xp"] = max(0, db[uid]["xp"] - XP_WRONG)
        save_db(db)

        text = render_text(
            user,
            f"💀 *WRONG GUESS!* 💀\n\n"
            f"You picked: *{user_pick.title()}*\n"
            f"Coin result: *{outcome.title()}*\n\n"
            f"−{XP_WRONG} XP"
        )

    return q.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=_again_menu()
    )


# ---------------------------------------------------------
# Replay menu
# ---------------------------------------------------------
def _again_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚛️ Flip Again", callback_data="game_quantum")],
        [InlineKeyboardButton("🎮 Games", callback_data="games_main")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])
