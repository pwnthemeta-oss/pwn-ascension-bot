"""
router.py
Unified router for ALL Telegram updates (messages + callbacks)
FULL VERSION WITH ALL COMMAND HANDLERS - Polling Version
"""

import logging
from telegram import Update
from telegram.error import TelegramError

# Core screens
from modules.start import handle_start_command
from modules.menu import handle_menu_command, handle_menu_callback
from modules.profile import handle_profile_callback, handle_profile_command
from modules.help_center import handle_help_command, handle_help_callback
from modules.error_screen import show_error

# Grind
from modules.grind_command import handle_grind_command
from modules.grinding import handle_grind_callback

# Badges
from modules.badges_command import handle_badges_command
from modules.badges import handle_badges_callback

# Leaderboards
from modules.leaderboards_command import handle_leaderboards_command
from modules.leaderboard import handle_leaderboard_callback

# Settings
from modules.settings_command import handle_settings_command
from modules.settings import handle_settings_callback

# Activity
from modules.activity_command import handle_activity_command
from modules.activity import handle_activity_callback

# Challenges
from modules.challenges_command import handle_challenges_command
from modules.challenges import handle_challenges_callback

# Onboarding
from modules.onboarding import handle_onboarding_callback, handle_join_community, handle_joined_yes

# Dice Battle
from modules.dice_battle import handle_dice_battle_callback

# Games Hub
from modules.games import handle_games_callback

# Tap Speed Test
from modules.tap_speed import handle_tap_speed_callback

# Bomb Defusal
from modules.bomb_defusal import handle_bomb_defusal_callback

# Mind Hack Puzzle
from modules.mind_hack import handle_mindhack_callback

# Ascension Rush
from modules.ascension_rush import handle_ascension_rush_callback

# Dark Corridor
from modules.dark_corridor import handle_dark_corridor_callback

# XP Typhoon
from modules.xp_typhoon import handle_typhoon_callback

# Quiz Game
from modules.quiz_game import handle_quiz_callback

# Corrupted Oracle
from modules.corrupted_oracle import handle_oracle_callback

# Quantum Flip
from modules.quantum_flip import handle_quantum_callback

# Daily Spin
from modules.spin import handle_spin_callback, handle_spin_command

# Verification
from modules.verify_reasoning import handle_reasoning_callback

# Database
from database import init_user

logger = logging.getLogger(__name__)


# ------------------------------------------------------
# POLLING-BASED HANDLERS
# ------------------------------------------------------
def handle_command(update: Update, context):
    """Handle all command messages."""
    try:
        bot = context.bot
        text = update.message.text or ""
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        init_user(user_id, username)

        # Route based on command
        if text == "/start":
            return handle_start_command(bot, update)
        elif text == "/menu":
            return handle_menu_command(bot, update)
        elif text == "/profile":
            return handle_profile_command(bot, update)
        elif text == "/help":
            return handle_help_command(bot, update)
        elif text == "/grind":
            return handle_grind_command(bot, update)
        elif text == "/badges":
            return handle_badges_command(bot, update)
        elif text == "/leaderboards":
            return handle_leaderboards_command(bot, update)
        elif text == "/settings":
            return handle_settings_command(bot, update)
        elif text == "/activity":
            return handle_activity_command(bot, update)
        elif text == "/challenges":
            return handle_challenges_command(bot, update)
        elif text == "/spin":
            return handle_spin_command(bot, update)
        else:
            # Default → open menu
            return handle_menu_command(bot, update)

    except TelegramError as te:
        logger.error(f"Telegram error: {te}")
    except Exception as e:
        logger.error(f"Command handler error: {e}")


def handle_callback(update: Update, context):
    """Handle all callback queries (button presses)."""
    try:
        bot = context.bot
        data = update.callback_query.data
        user_id = update.callback_query.from_user.id
        username = update.callback_query.from_user.username
        
        init_user(user_id, username)

        # Route based on callback data prefix
        if data.startswith("menu"):
            return handle_menu_callback(bot, update)
        elif data.startswith("prof"):
            return handle_profile_callback(bot, update)
        elif data.startswith("grind"):
            return handle_grind_callback(bot, update)
        elif data.startswith("games") or data.startswith("game_"):
            return handle_games_callback(bot, update)
        elif data.startswith("tapspeed"):
            return handle_tap_speed_callback(bot, update)
        elif data.startswith("bomb_"):
            return handle_bomb_defusal_callback(bot, update)
        elif data.startswith("mindhack"):
            return handle_mindhack_callback(bot, update)
        elif data.startswith("rush_"):
            return handle_ascension_rush_callback(bot, update)
        elif data.startswith("badge"):
            return handle_badges_callback(bot, update)
        elif data.startswith("lb_"):
            return handle_leaderboard_callback(bot, update)
        elif data.startswith("set_"):
            return handle_settings_callback(bot, update)
        elif data.startswith("act_"):
            return handle_activity_callback(bot, update)
        elif data.startswith("ch_"):
            return handle_challenges_callback(bot, update)
        elif data.startswith("onb_"):
            return handle_onboarding_callback(bot, update)
        elif data.startswith("dice_"):
            return handle_dice_battle_callback(bot, update)
        elif data.startswith("door_pick_"):
            return handle_dark_corridor_callback(bot, update)
        elif data.startswith("typhoon") or data == "game_typhoon":
            return handle_typhoon_callback(bot, update)
        elif data.startswith("quiz_") or data == "quiz_menu":
            return handle_quiz_callback(bot, update)
        elif data.startswith("oracle_") or data == "game_oracle":
            return handle_oracle_callback(bot, update)
        elif data.startswith("quantum_") or data == "game_quantum":
            return handle_quantum_callback(bot, update)
        elif data.startswith("verify_reason") or data == "verify_reason_start":
            return handle_reasoning_callback(bot, update)
        elif data == "join_community":
            return handle_join_community(bot, update)
        elif data == "joined_yes":
            return handle_joined_yes(bot, update)
        elif data.startswith("spin_") or data == "open_spin":
            return handle_spin_callback(bot, update)
        elif data.startswith("help"):
            return handle_help_callback(bot, update)
        else:
            return show_error(bot, update)

    except TelegramError as te:
        logger.error(f"Telegram error: {te}")
    except Exception as e:
        logger.error(f"Callback handler error: {e}")
