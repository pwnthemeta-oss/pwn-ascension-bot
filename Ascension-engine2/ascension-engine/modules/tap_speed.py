"""
modules/tap_speed.py
Tap Speed Test mini-game for PWN Ascension Engine.

User must tap within 1 second after receiving a "⚡ TAP NOW!" signal.
"""

import time
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_user, load_db, save_db
from ui.components import render_text


XP_FAST = 200
XP_MEDIUM = 120
XP_SLOW = 60
XP_FAIL = 0


def handle_tap_speed_callback(bot, update):
    query = update.callback_query
    data = query.data

    if data == "game_tapspeed":
        return _show_intro(bot, update)

    if data == "tapspeed_start":
        return _start_test(bot, update)

    if data.startswith("tapspeed_tap_"):
        timestamp = float(data.replace("tapspeed_tap_", ""))
        return _process_tap(bot, update, timestamp)


def _show_intro(bot, update):
    query = update.callback_query
    user = get_user(query.from_user.id)

    text = render_text(user,
        "⚡ *TAP SPEED TEST*\n\n"
        "Tap as fast as possible when the signal appears.\n\n"
        "Rewards:\n"
        "• <300ms → +200 XP\n"
        "• <600ms → +120 XP\n"
        "• <1000ms → +60 XP\n"
        "• Too slow → 0 XP\n"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Start Test", callback_data="tapspeed_start")],
        [InlineKeyboardButton("↩️ Back", callback_data="games_main")],
    ])

    query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=keyboard)


def _start_test(bot, update):
    query = update.callback_query
    user = get_user(query.from_user.id)
    chat_id = query.message.chat.id

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text=render_text(user, "⏳ Get ready...\n"),
        parse_mode="Markdown",
    )

    wait = random.uniform(1.5, 3.0)
    time.sleep(wait)

    signal_ts = time.time()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ TAP NOW!", callback_data=f"tapspeed_tap_{signal_ts}")]
    ])

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text=render_text(user, "⚡ *TAP NOW!*"),
        parse_mode="Markdown",
        reply_markup=keyboard
    )


def _process_tap(bot, update, signal_ts):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_user(user_id)

    now = time.time()
    reaction = now - signal_ts

    db = load_db()
    uid = str(user_id)

    if reaction < 0:
        xp = XP_FAIL
        msg = "⛔ You tapped too early!"
    elif reaction < 0.3:
        xp = XP_FAST
        msg = f"⚡ *INSANE SPEED!* {int(reaction*1000)}ms (+200 XP)"
    elif reaction < 0.6:
        xp = XP_MEDIUM
        msg = f"🔥 Great reaction! {int(reaction*1000)}ms (+120 XP)"
    elif reaction < 1.0:
        xp = XP_SLOW
        msg = f"👍 Good! {int(reaction*1000)}ms (+60 XP)"
    else:
        xp = XP_FAIL
        msg = f"🐌 Too slow... {int(reaction*1000)}ms (+0 XP)"

    db[uid]["xp"] += xp
    db[uid]["weekly"]["xp"] = db[uid].get("weekly", {}).get("xp", 0) + xp
    save_db(db)
    user = get_user(user_id)

    text = render_text(user, msg)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Play Again", callback_data="tapspeed_start")],
        [InlineKeyboardButton("🎮 Games", callback_data="games_main")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])

    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
