"""
modules/games.py
Games hub menu — lists all available mini-games.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_user
from ui.components import render_text


def handle_games_callback(bot, update):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    user = get_user(user_id)

    # Games home screen
    if data == "games_main":
        return _show_games_menu(bot, update)

    # Forward into specific games
    if data.startswith("game_"):
        game = data.replace("game_", "")
        if game == "dice":
            from modules.dice_battle import _start_battle
            return _start_battle(bot, update)
        elif game == "tapspeed":
            from modules.tap_speed import _show_intro
            return _show_intro(bot, update)
        elif game == "bomb":
            from modules.bomb_defusal import _show_intro
            return _show_intro(bot, update)
        elif game == "mindhack":
            from modules.mind_hack import _intro
            return _intro(bot, update)
        elif game == "rush":
            from modules.ascension_rush import intro
            return intro(bot, update)
        elif game == "corridor":
            from modules.dark_corridor import _intro
            return _intro(bot, update)
        elif game == "oracle":
            from modules.corrupted_oracle import intro_screen
            return intro_screen(bot, update)
        elif game == "quantum":
            from modules.quantum_flip import intro
            return intro(bot, update)
        elif game == "typhoon":
            from modules.xp_typhoon import intro_screen
            return intro_screen(bot, update)

    return query.answer("Unknown game.")


def _show_games_menu(bot, update):
    query = update.callback_query
    user = get_user(query.from_user.id)

    text = render_text(user,
        "🎮 *GAMES*\n\n"
        "Choose a game to play and earn XP!\n"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Dice Battle", callback_data="game_dice")],
        [InlineKeyboardButton("⚡ Tap Speed Test", callback_data="game_tapspeed")],
        [InlineKeyboardButton("💣 Bomb Defusal", callback_data="game_bomb")],
        [InlineKeyboardButton("🧠 Mind Hack Puzzle", callback_data="game_mindhack")],
        [InlineKeyboardButton("⚡ Ascension Rush", callback_data="game_rush")],
        [InlineKeyboardButton("🚪 Dark Corridor", callback_data="game_corridor")],
        [InlineKeyboardButton("🌪️ XP Typhoon", callback_data="game_typhoon")],
        [InlineKeyboardButton("🧠 Quiz Game", callback_data="quiz_menu")],
        [InlineKeyboardButton("🔮 Corrupted Oracle", callback_data="game_oracle")],
        [InlineKeyboardButton("⚛️ Quantum Flip", callback_data="game_quantum")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu_main")],
    ])

    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
