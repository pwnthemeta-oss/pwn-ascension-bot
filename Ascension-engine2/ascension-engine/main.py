#!/usr/bin/env python
"""
PWN Ascension Engine — Polling Version
Entry point for the entire Telegram bot.
"""

import os
import logging
import time
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.error import Conflict

# ROUTER
from router import handle_command, handle_callback

# Logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Telegram Bot token (NEVER hardcode)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise Exception("TELEGRAM_TOKEN environment variable not set!")


def main():
    """Start the bot with polling and automatic conflict recovery."""
    logger.info("Starting PWN Ascension Engine...")
    
    retry_delay = 10
    max_retry_delay = 120
    
    while True:
        try:
            # Create updater and dispatcher
            updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
            dispatcher = updater.dispatcher
            
            # Register command handler (catches all commands)
            dispatcher.add_handler(CommandHandler(
                ['start', 'menu', 'profile', 'help', 'grind', 'badges', 
                 'leaderboards', 'settings', 'activity'],
                handle_command
            ))
            
            # Register callback query handler (catches all button presses)
            dispatcher.add_handler(CallbackQueryHandler(handle_callback))
            
            # Start polling
            logger.info("Bot is running with polling...")
            updater.start_polling(drop_pending_updates=True)
            
            retry_delay = 10
            
            # Keep the bot running
            updater.idle()
            break
            
        except Conflict as e:
            logger.warning(
                f"⚠️ CONFLICT DETECTED: Another bot instance is running elsewhere. "
                f"Retrying in {retry_delay} seconds... "
                f"Close all other instances (phone/desktop/browser) to resolve this."
            )
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 1.5, max_retry_delay)
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()
