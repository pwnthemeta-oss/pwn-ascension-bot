"""
utils/animations.py
Fire + Cosmic Glow animation for PWN Ascension Engine
"""

import time


def animated_fire_cosmic_bar(bot, chat_id, message_id, total_steps=10, delay=0.18):
    """
    Hybrid Fire + Cosmic Glow animation.

    total_steps: length of the animation
    delay: speed between frames (lower = faster)
    """
    bar = ""
    fire = "🔥"
    cosmic = ["✨", "💫"]

    for i in range(total_steps):
        bar = fire * (i + 1)

        cosmic_char = cosmic[i % len(cosmic)]
        bar_with_cosmic = bar + cosmic_char + "░" * (total_steps - i - 1)

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Progress:\n`{bar_with_cosmic}`",
            parse_mode="Markdown"
        )

        time.sleep(delay)
