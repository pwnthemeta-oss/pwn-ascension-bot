# PWN Ascension Engine - Telegram Bot

## Overview
PWN Ascension Engine is a Telegram bot that gamifies user engagement through XP, ranks, streaks, badges, and challenges. Users interact with the bot via inline buttons and commands to grind for XP, track progress, compete on leaderboards, and unlock achievements.

**Current State**: Fully operational bot running in polling mode with premium UI themes. Features Gold Mode badges, Crystal Elite leaderboards, and Dark Mode animated challenges.

## Project Architecture

### Backend (Python)
- **Telegram Bot**: python-telegram-bot 13.15 (Polling Mode)
- **Database**: JSON file-based storage (`storage/database.json`)
- **Entry Point**: `ascension-engine/main.py`
- **Mode**: Polling (no webhooks required)

### Core Components

1. **Main Application** (`main.py`)
   - Flask web server for webhook handling
   - Telegram bot initialization
   - Webhook endpoint at `/webhook`

2. **Router** (`router.py`)
   - Unified dispatcher for all Telegram updates
   - Handles both commands and callback queries
   - Routes to appropriate module handlers

3. **Database** (`database.py`)
   - JSON-based user data storage
   - User initialization and management
   - Activity logging

4. **Modules** (`modules/`)
   - `start.py` - Welcome screen and /start command
   - `menu.py` - Main navigation menu
   - `profile.py` - User profile display
   - `grinding.py` - XP grinding mechanics and cooldowns
   - `badges.py` - Badge system and tracking
   - `leaderboard.py` - XP rankings
   - `settings.py` - User preferences
   - `activity.py` - Activity feed
   - `challenges.py` - Challenge system
   - `onboarding.py` - New user onboarding flow

5. **UI Components** (`ui/components.py`)
   - Reusable UI rendering functions

6. **Utils** (`utils/`)
   - `animations.py` - Fire + Cosmic Glow animation system

### Game Mechanics
- **XP System**: Users earn 50 XP per grind with 30-second cooldown
- **Ranks**: Bronze → Silver → Gold → Diamond → Master → Ascended (based on XP)
- **Streaks**: Daily activity tracking with milestone rewards
- **Badges**: 8 achievement badges (Initiate, First Grind, Grind Master, etc.)
- **Leaderboards**: Weekly XP rankings with top 3 rewards
- **Mini-Games**: 10 games total (Dice Battle, Tap Speed, Bomb Defusal, Mind Hack, Ascension Rush, Dark Corridor, XP Typhoon, Quiz Game, Corrupted Oracle, Quantum Flip)

## Setup Requirements

### Environment Variables
- `TELEGRAM_TOKEN` (required) - Your Telegram bot token from @BotFather

### Dependencies
All Python dependencies are listed in `requirements.txt`:
- python-telegram-bot==13.15
- Flask==2.2.5

## Recent Changes
**Date**: November 24, 2025

### Latest Updates - Dark Mode Challenges (Nov 24, 2025)
1. **Dark Mode Challenges UI** 🌑
   - Animated moon phase header (🌑🌘🌗🌖)
   - Dynamic progress bars using █ and ░ characters
   - Clean section separators with ━━━━━━
   - Visual progress indicators (● and ○)
   - Daily missions: Grind 20x, Earn 500 XP, Maintain streak
   - Weekly missions: Earn 5,000 XP, Complete 100 grinds, Unlock 1 badge
   - Sparkle loading effect "✦✦✦"
   
2. **Fire + Cosmic Glow Loading Animation** 🔥💫
   - Hybrid animation combining fire growth and cosmic sparkles
   - Plays when opening Challenges screen
   - 10-frame sequence with alternating ✨ and 💫 effects
   - Custom animation utility at `utils/animations.py`
   - Animation frames: 🔥 → 🔥🔥💫 → 🔥🔥🔥✨ → full bar completion
   - 0.18s delay between frames for smooth visual effect

3. **Premium Welcome Screen** 💠✨
   - Short, punchy /start command with dark mode theme
   - "PWN ASCENSION" header with crystal diamond styling (💠✨)
   - "DARK MODE ACTIVE" badge for premium feel
   - Concise welcome: "You've activated the Ascension Engine"
   - Quick tagline: "Every action lifts you higher" 🌌⚡
   - Clean button layout with emoji upgrades (🚀 🌌 🏆 🧿)

4. **Full Slash Command Support** ⚡
   - All features now accessible via slash commands
   - `/challenges` command with Fire + Cosmic animation
   - Commands work identically to button navigation
   - BotFather command list ready for registration
   - 10 total commands: start, menu, profile, grind, badges, leaderboards, challenges, settings, activity, help

5. **XP Typhoon Mini-Game** 🌪️
   - Tap survival game: tap as fast as possible to resist the storm
   - 5-second time window for maximum tapping
   - XP reward: 4 XP per tap (earned after stopping)
   - Penalty system: -5 XP for fewer than 3 taps
   - Interactive tap counter with real-time feedback
   - "Play Again" option for continuous gameplay
   - Added to Games Hub menu as 7th mini-game

6. **Multi-Category Quiz Game** 🧠
   - 5 quiz categories: Gaming, Content Creating, Crypto, Stock Market, Meme Coins
   - 60 total questions (12 per category)
   - Multiple-choice format with 3 options per question
   - Randomized question selection from question bank
   - XP rewards: +120 XP for correct answers, -15 XP penalty for wrong answers
   - Category selection menu with emoji icons
   - "Next" button for continuous play within same category
   - Added to Games Hub menu as 8th mini-game

7. **Corrupted Oracle Prediction Game** 🔮
   - Mysterious number prediction game (range: 1-12)
   - Three prediction options: Higher 🔼, Lower 🔽, Same 🟰
   - XP rewards based on difficulty:
     - Same prediction (hardest): +200 XP
     - Higher/Lower prediction: +100 XP
     - Wrong guess penalty: -15 XP
   - Randomized number generation for each round
   - "Play Again" option for continuous gameplay
   - Added to Games Hub menu as 9th mini-game

8. **Quantum Flip Prediction Game** ⚛️
   - User picks Heads or Tails before the coin flip
   - Three possible outcomes:
     - Correct guess: +100 XP
     - Wrong guess: -20 XP
     - Edge (1% ultra-rare): +500 XP + Rare "Quantum Master" Badge
   - Interactive prediction mechanic (player choice before flip)
   - Rare badge unlock on edge landing
   - "Flip Again" option for continuous gameplay
   - Added to Games Hub menu as 10th mini-game

9. **Human Reasoning Verification** 🔐🧠
   - Anti-bot verification screen before onboarding
   - Logic-based questions to confirm human intelligence
   - 5 reasoning questions: flying animals, light objects, writing tools, fruits, hot items
   - Users must select correct answer from 3 emoji options
   - Options are randomized each time
   - Wrong answer → different question retry
   - Correct answer → proceeds to onboarding
   - Prevents bot accounts from accessing the system
   - Integrated with existing Dark Mode theme

10. **Join the Community Flow** 🌐
   - Special handler for "Join the community" button in onboarding Step 1
   - Shows confirmation screen: "Did you join the PWN Community HQ yet?"
   - Two options:
     - ✅ Yes, I joined → Continues to Step 2 (awards +100 XP)
     - ❌ Not yet — open link → Opens https://t.me/PwnCommunityHQ in Telegram
   - Tracks answer as option "B" for onboarding analytics
   - Seamless integration with existing onboarding flow

### Premium UI Features (Nov 23-24, 2025)
1. **Gold Mode Badge System** 👑
   - Premium badge unlock notifications with ✨👑✨ styling
   - "Golden light washes over you" unlock animation
   - Gold Mode Badge Vault with luxurious 8-badge grid layout
   - "Your legacy shines brighter today" tagline
   
2. **Crystal Elite Leaderboards** 💠
   - Three leaderboard types: Top XP, Top Grinders, Top Badge Collectors
   - Premium 💠✨💠 crystal theme
   - Top 10 rankings with medal indicators (🥇🥈🥉)
   - Animated XP bars and badge counters

3. **Fire Theme Profile** 🔥
   - Animated fire-themed profile display
   - Real-time XP progress bars
   - Badge grid integration
   - Streak tracking with flame indicators

### Bot Configuration (Nov 24, 2025)
- **Mode Changed**: Switched from webhooks to polling mode for Replit compatibility
- **Token Rotation**: Resolved bot conflict by rotating Telegram token via @BotFather
- **Current Token**: 8569816585:AAHNegu7-3NGtg_hLS7ZFtPCS8fW4aJ6l0M

### GitHub Import Setup (Nov 23, 2025)
1. Installed Python 3.11 module
2. Installed all Python dependencies
3. Added missing badge system functions
4. Created `.gitignore` for Python project
5. Configured workflow for Telegram bot
6. Fixed circular import in `modules/badges.py`

## How to Run

### Local Development
1. Get a Telegram bot token from @BotFather
2. Add the token as a secret named `TELEGRAM_TOKEN` in Replit Secrets
3. Run the workflow (the bot will start automatically in polling mode)
4. Bot is ready to use - no webhook setup required!

### Deployment
The bot uses polling mode and runs continuously on Replit:
1. Make sure `TELEGRAM_TOKEN` secret is set
2. Workflow auto-starts on Replit
3. No additional webhook configuration needed

## User Preferences
None set yet.

## Notes
- The bot uses a JSON file database stored in `storage/` directory
- All bot interactions happen via inline keyboards (no free-text parsing except commands)
- The webhook approach is more reliable than polling for production use
