import random
import asyncio
from datetime import datetime, timedelta
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

SPIN_COOLDOWN_HOURS = 24

REWARDS = [
    ("+300 XP", "xp", 300, 60),
    ("+600 XP", "xp", 600, 50),
    ("+900 XP", "xp", 900, 40),
    ("⚡ 1-Day XP Boost (x2)", "boost", 1, 20),
    ("📅 +1 Streak Day", "streak", 1, 15),
    ("🟦 Badge Fragment", "fragment", 1, 12),
    ("🂡 JACKPOT: +2,000 XP", "xp", 2000, 3),
    ("💠 Wheel Master Badge", "badge", 1, 1),
]


def spin_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Spin Now", callback_data="spin_start")],
        [InlineKeyboardButton("↩️ Back to Menu", callback_data="menu")]
    ])


def back_to_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("↩️ Back to Menu", callback_data="menu")]
    ])


def handle_spin_command(bot, update):
    """Command handler for /spin"""
    user_id = update.message.from_user.id
    open_spin_screen(bot, update, user_id)


def handle_spin_callback(bot, update):
    """Callback handler for spin actions"""
    data = update.callback_query.data
    user_id = update.callback_query.from_user.id
    
    if data == "open_spin":
        open_spin_screen(bot, update, user_id)
    elif data == "spin_start":
        start_spin(bot, update, user_id)


def open_spin_screen(bot, update, user_id):
    """Show spin screen or cooldown message"""
    from database import get_user
    
    user_data = get_user(user_id)
    last_spin = user_data.get("last_spin")
    
    if last_spin:
        last_spin_time = datetime.fromtimestamp(last_spin)
        next_time = last_spin_time + timedelta(hours=SPIN_COOLDOWN_HOURS)
        
        if datetime.now() < next_time:
            remaining = next_time - datetime.now()
            hours = int(remaining.total_seconds() // 3600)
            mins = int((remaining.total_seconds() % 3600) // 60)
            
            text = (
                f"⏳ **DAILY SPIN USED**\n\n"
                f"Next spin in **{hours}h {mins}m**."
            )
            
            if hasattr(update, 'callback_query'):
                update.callback_query.answer()
                update.callback_query.message.edit_text(
                    text,
                    reply_markup=back_to_menu(),
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=back_to_menu(),
                    parse_mode="Markdown"
                )
            return
    
    text = (
        "🎰 **DAILY SPIN**\n\n"
        "Spin the Ascension Wheel and claim your reward.\n"
        "You can play **once every 24 hours**.\n\n"
        "Ready?"
    )
    
    if hasattr(update, 'callback_query'):
        update.callback_query.answer()
        update.callback_query.message.edit_text(
            text,
            reply_markup=spin_button(),
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=spin_button(),
            parse_mode="Markdown"
        )


def start_spin(bot, update, user_id):
    """Perform the spin animation and award reward"""
    from database import load_db, save_db, log_activity
    import time
    
    db = load_db()
    uid = str(user_id)
    
    if uid not in db:
        return
    
    db[uid]["last_spin"] = int(time.time())
    save_db(db)
    
    update.callback_query.answer()
    msg = update.callback_query.message
    
    frames = ["⚡", "🔵", "🟣", "🟢", "🔴", "🟠", "🌀"]
    
    for i, frame in enumerate(frames):
        msg.edit_text(
            f"🎰 **Spinning...**\n{frame}",
            parse_mode="Markdown"
        )
        time.sleep(0.4)
    
    reward = random.choices(REWARDS, weights=[r[3] for r in REWARDS])[0]
    text, r_type, amount, _ = reward
    
    db = load_db()
    
    if r_type == "xp":
        db[uid]["xp"] = db[uid].get("xp", 0) + amount
        log_activity(user_id, f"🎰 Daily Spin: {text}")
        
    elif r_type == "boost":
        db[uid]["xp_boost_until"] = int(time.time()) + (24 * 3600)
        log_activity(user_id, f"🎰 Daily Spin: {text}")
        
    elif r_type == "streak":
        db[uid]["streak"] = db[uid].get("streak", 0) + 1
        log_activity(user_id, f"🎰 Daily Spin: {text}")
        
    elif r_type == "fragment":
        db[uid]["badge_fragments"] = db[uid].get("badge_fragments", 0) + 1
        log_activity(user_id, f"🎰 Daily Spin: {text}")
        
    elif r_type == "badge":
        if "Wheel Master" not in db[uid].get("badges", []):
            db[uid].setdefault("badges", []).append("Wheel Master")
        log_activity(user_id, f"🎰 Daily Spin: {text}")
    
    save_db(db)
    
    msg.edit_text(
        f"🎉 **YOU WON:**\n{text}\n\n"
        f"Come back tomorrow for another spin! 🌀",
        reply_markup=back_to_menu(),
        parse_mode="Markdown"
    )
