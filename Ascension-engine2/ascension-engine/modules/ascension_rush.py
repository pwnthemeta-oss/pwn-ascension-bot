"""
ASCENSION RUSH — CLEAN + STABLE VERSION

No base64, no freezing, no corrupted callbacks.
Simple, fast, reliable gameplay:

1) Flash sequence to user
2) Ask for final emoji
3) Ask for emoji count
"""

import time
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_user, load_db, save_db
from ui.components import render_text


EMOJIS = ["🔥", "⚡", "💀"]

XP_FINAL = 100
XP_COUNT = 200
PENALTY = 10

FLASH_SEQUENCES = [
    ["🔥", "⚡", "🔥"],
    ["⚡", "💀", "⚡"],
    ["💀", "🔥", "💀"],
    ["⚡", "⚡", "🔥"],
    ["🔥", "💀", "⚡"],

    ["🔥", "⚡", "⚡", "💀"],
    ["💀", "🔥", "🔥", "⚡"],
    ["⚡", "⚡", "💀", "🔥"],
    ["💀", "⚡", "💀", "🔥"],
    ["🔥", "🔥", "⚡", "💀"],

    ["🔥", "⚡", "🔥", "💀", "🔥"],
    ["⚡", "💀", "⚡", "🔥", "⚡"],
    ["💀", "🔥", "💀", "⚡", "💀"],
    ["🔥", "💀", "⚡", "⚡", "🔥"],
    ["⚡", "🔥", "💀", "🔥", "⚡"],

    ["🔥", "⚡", "🔥", "⚡", "💀", "🔥"],
    ["⚡", "💀", "⚡", "🔥", "💀", "⚡"],
    ["💀", "🔥", "💀", "🔥", "⚡", "💀"],
    ["🔥", "🔥", "⚡", "💀", "⚡", "🔥"],
    ["💀", "⚡", "🔥", "⚡", "💀", "🔥"],
]


def handle_ascension_rush_callback(bot, update):
    q = update.callback_query
    d = q.data

    if d == "game_rush":
        return intro(bot, update)

    if d == "rush_start":
        return start_round(bot, update)

    if d.startswith("rush_final_"):
        _, _, chosen, correct, seq_index = d.split("_")
        return process_final(bot, update, chosen, correct, int(seq_index))

    if d.startswith("rush_count_"):
        _, _, chosen, correct = d.split("_")
        return process_count(bot, update, chosen, correct)


def intro(bot, update):
    q = update.callback_query
    user = get_user(q.from_user.id)

    t = render_text(user,
        "⚡ *ASCENSION RUSH*\n\n"
        "You will see emojis flash FAST.\n"
        "Then answer:\n"
        "1) What was the FINAL emoji?\n"
        "2) How many of a chosen emoji appeared?\n\n"
        "*Simple. Fast. No freezes.*"
    )

    k = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Start Rush", callback_data="rush_start")],
        [InlineKeyboardButton("↩️ Back", callback_data="games_main")]
    ])

    q.edit_message_text(t, parse_mode="Markdown", reply_markup=k)


def start_round(bot, update):
    q = update.callback_query
    user_id = q.from_user.id
    user = get_user(user_id)

    seq_index = random.randint(0, len(FLASH_SEQUENCES) - 1)
    seq = FLASH_SEQUENCES[seq_index]

    for emo in seq:
        try:
            q.edit_message_text(render_text(user, emo), parse_mode="Markdown")
        except:
            pass
        time.sleep(0.25)

    final = seq[-1]

    k = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(e,
                callback_data=f"rush_final_{e}_{final}_{seq_index}"
            ) for e in EMOJIS
        ]
    ])

    q.edit_message_text(
        render_text(user, "⚡ *What was the FINAL emoji?*"),
        parse_mode="Markdown",
        reply_markup=k
    )


def process_final(bot, update, chosen, correct, seq_index):
    q = update.callback_query
    user_id = q.from_user.id
    user = get_user(user_id)

    seq = FLASH_SEQUENCES[seq_index]

    db = load_db()
    uid = str(user_id)

    if chosen == correct:
        db[uid]["xp"] += XP_FINAL
        db[uid]["weekly"]["xp"] = db[uid].get("weekly", {}).get("xp", 0) + XP_FINAL
        save_db(db)

        t = render_text(
            user,
            f"🔥 Correct!\nFinal emoji *was* {correct}.\n+{XP_FINAL} XP\n\n"
            "Now choose the correct count:"
        )

        counts = {e: seq.count(e) for e in EMOJIS}

        k = []
        for e in EMOJIS:
            num = counts[e]
            k.append([
                InlineKeyboardButton(
                    f"{e} = {num}",
                    callback_data=f"rush_count_{num}_{num}"
                )
            ])

        q.edit_message_text(t, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(k))

    else:
        db[uid]["xp"] = max(0, db[uid]["xp"] - PENALTY)
        save_db(db)

        t = render_text(user,
            f"💥 WRONG!\nFinal emoji was *{correct}*.\n−{PENALTY} XP"
        )

        q.edit_message_text(t, parse_mode="Markdown", reply_markup=after_menu())


def process_count(bot, update, chosen, correct):
    q = update.callback_query
    user_id = q.from_user.id
    user = get_user(user_id)

    db = load_db()
    uid = str(user_id)

    chosen = int(chosen)
    correct = int(correct)

    if chosen == correct:
        db[uid]["xp"] += XP_COUNT
        db[uid]["weekly"]["xp"] = db[uid].get("weekly", {}).get("xp", 0) + XP_COUNT
        save_db(db)

        t = render_text(user,
            f"⚡ *AMAZING MEMORY!*\n\n+{XP_COUNT} XP"
        )
    else:
        db[uid]["xp"] = max(0, db[uid]["xp"] - PENALTY)
        save_db(db)

        t = render_text(user,
            f"💥 WRONG COUNT!\n−{PENALTY} XP"
        )

    q.edit_message_text(t, parse_mode="Markdown", reply_markup=after_menu())


def after_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Play Again", callback_data="rush_start")],
        [InlineKeyboardButton("🎮 Games", callback_data="games_main")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])
