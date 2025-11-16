# CLAUDE.md - Development Guide

Essential project overview and architecture for new development sessions.

---

## Quick Project Summary

**Wordy** is a Flask-based GRE vocabulary quiz application with 6 different quiz modes. The **Spelling Quiz** is the most feature-rich mode, with sophisticated time-based scoring, game history tracking, and leaderboard rankings.

**Tech Stack:** Python 3 + Flask, vanilla JavaScript, HTML5/CSS3, LocalStorage
**Word List:** 994 GRE words from Manhattan Prep (pipe-delimited format)

---

## Architecture Overview

### Backend (Flask)
- **File:** `quiz_app.py`
- **Framework:** Flask with simple route handlers
- **Endpoints:**
  - `/` - Home page
  - `/gre-quiz` - Standard GRE quiz
  - `/inverse-gre-quiz` - Reverse quiz
  - `/word-review` - Word flashcards
  - `/definition-review` - Definition flashcards
  - `/spelling-quiz` - Main spelling quiz
  - `/trivia-quiz` - Trivia quiz
  - `/review/get_word` - API to fetch random word
  - Round management endpoints (if applicable)

### Frontend
- **Location:** `templates/*.html`
- **Style:** Self-contained with inline CSS (no external stylesheets)
- **Scripts:** Inline JavaScript (no build process)
- **Storage:** LocalStorage for settings, leaderboards, favorites

### Data Storage
- **Word List:** `manhattan_prep_gre_words_formatted.txt` (word|definition format)
- **Stats:** `quiz_stats.json` (for non-spelling quiz modes)
- **Client-Side:**
  - `localStorage['spellingQuizSettings_v2']` - Game settings
  - `localStorage['spellingQuizLeaderboard']` - All game scores
  - `localStorage['wordReviewFavoritedWords']` - Favorited words
  - `localStorage['definitionReviewRemovedWords']` - Removed words
  - etc.

---

## Key Design Principles

### 1. Self-Contained Templates
Each HTML template includes all CSS and JavaScript inline. This makes each mode fully self-contained and easy to modify without affecting others.

### 2. Client-Side State Management
Most game state is managed in JavaScript variables and persisted to LocalStorage. The backend primarily serves templates and random words.

### 3. Responsive Gradient Design
All pages use purple gradient backgrounds (`linear-gradient(135deg, #667eea 0%, #764ba2 100%)`) with glassmorphism effects (backdrop-filter blur).

### 4. Keyboard-First UX
All quiz modes support extensive keyboard shortcuts:
- SPACE, ENTER for primary actions
- ESC for navigation back/home
- Letter keys for input
- Special keys (/, ?) for hints/pause

---

## Critical Implementation Details

### Spelling Quiz Scoring System

#### Letter Scoring Formula
```javascript
const letterScore = baseScore + (bonusPerSecond * timeRemaining)
// Default: 20 + (2 * timeRemaining)
// Max: 20 + (2 * 20) = 60 points per letter
```

#### Word Completion Bonuses
```javascript
if (!usedHelpThisWord) {
    if (!wrongLetterThisWord) {
        // Perfect: +100 points
        currentScore += settings.perfectWordBonus;
    } else {
        // Completed: +50 points
        currentScore += settings.completedWordBonus;
    }
}
```

**Important:** `wrongLetterThisWord` tracks typing mistakes, separate from `usedHelpThisWord` which tracks hints/reveals.

### Game History Structure

```javascript
currentGameHistory = {
    wordResults: [
        {
            word: "aberration",
            definition: "deviation from what is normal",
            letters: [
                {
                    letter: "A",
                    correct: true,
                    timeElapsed: 1.234,
                    revealed: false,
                    noScore: false
                },
                // ... more letters
            ],
            hintsUsed: 0,
            perfectWord: true,
            completedWord: true,
            startTime: 1697123456789
        },
        // ... more words
    ],
    settings: { /* snapshot of all settings */ },
    startTime: 1697123456789,
    endTime: 1697123576789,
    finalScore: 2450,
    wordsCompleted: 15
}
```

### Score Recalculation Logic

**Proportional Time Scaling:**
```javascript
// If time limit changed, scale the elapsed time proportionally
const scalingFactor = newSettings.letterTimeLimit / oldSettings.letterTimeLimit;
const scaledTimeElapsed = letterData.timeElapsed * scalingFactor;
```

This assumes the player would have taken proportionally longer/shorter time with different time limits.

### Leaderboard Rankings

Rankings are calculated by counting how many scores are **strictly better** than the current score:
```javascript
const rank = scoresStrictlyBetter.length + 1;
```

Separate rankings for:
- All-time (all scores)
- This month (same month and year)
- This week (within 7 days)
- Today (same date)

---

## Common Commands

### Start Development Server
```bash
./start_quiz.sh
# or manually:
source venv/bin/activate
python3 quiz_app.py
```

### Access Application
```
http://localhost:5000
```

### Git Workflow
```bash
git add -A
git commit -m "Message with Co-Authored-By: Claude"
git push
```

---

## Recent Major Updates

### Perfect vs Completed Word Bonuses (2025-10-18)
- **Perfect Word:** +100 points (no hints, no reveals, no wrong letters)
- **Completed Word:** +50 points (no hints, no reveals, but had wrong letter attempts)
- Added `wrongLetterThisWord` tracking flag
- Updated `handleLetterInput()` to detect wrong letters
- Modified `handleWordComplete()` bonus logic
- Created `showCompletedWordBonus()` notification
- Updated settings UI with both bonus inputs
- Updated `recalculateScore()` to apply completed bonus

### Game History Tracking (Previous Session)
- Detailed per-letter tracking (letter, correct, timeElapsed, revealed, noScore)
- Per-word tracking (word, definition, letters[], hintsUsed, perfectWord, completedWord)
- Per-game tracking (settings snapshot, wordResults[], timestamps, finalScore)
- Score recalculation with proportional time scaling
- Settings snapshot preserved with each game

### Leaderboard Enhancements (Previous Session)
- Toggle between original and recalculated scores
- Multi-timeframe rankings (all-time, month, week, today)
- Display format: "Score (was OriginalScore)" for recalculated view
- Re-sorting based on recalculated scores

### Keyboard Shortcuts (Previous Session)
- Game over modal: SPACE/ENTER → new game, L → leaderboard, ESC → home
- Enhanced navigation across all modals

---

## Technical Limitations

### LocalStorage Size
Each origin typically has 5-10MB of LocalStorage. Game history can grow large with detailed per-letter tracking. Consider:
- Limiting number of stored games (e.g., keep only recent 100)
- Implementing export/clear functionality
- Warning users when storage is nearly full

### No User Accounts
Currently all data is stored locally in the browser. Clearing browser data loses all progress. Future enhancement could add:
- Cloud sync
- User authentication
- Cross-device access

### Single-Player Only
No multiplayer or social features yet. Leaderboards are local to each browser.

### No Server-Side Validation
Scores could theoretically be manipulated via browser console. Not a concern for personal study app, but would need server validation for competitive use.

---

## Development Workflow

### Making Changes

1. **Identify the file:**
   - Home page: `templates/home.html`
   - Spelling quiz: `templates/spelling_quiz.html`
   - Backend: `quiz_app.py`

2. **Modify inline CSS/JavaScript:**
   All styles and scripts are in the HTML templates for easy editing.

3. **Test locally:**
   Refresh browser, test thoroughly.

4. **Commit and push:**
   ```bash
   git add -A
   git commit -m "Description"
   git push
   ```

5. **Update documentation:**
   - Add to `PROMPT_HISTORY.md`
   - Update `REQUIREMENTS.md` if needed
   - Update this file (`CLAUDE.md`) for major changes
   - Update `OVERVIEW.md` for architectural changes

### Adding New Features

**For Spelling Quiz features:**
- Add settings to `settings` object
- Update `updateSettingsUI()` to load new settings
- Update `saveSettings()` to persist new settings
- Add UI controls to settings modal
- Implement feature logic
- Update scoring/tracking if needed
- Update documentation

**For New Quiz Mode:**
- Create new template in `templates/`
- Add route in `quiz_app.py`
- Add card to `templates/home.html`
- Style consistently with other modes
- Test thoroughly

---

## Environment Variables

Currently none. All configuration is in code or LocalStorage.

Potential future env vars:
- `FLASK_ENV=development`
- `SECRET_KEY=...` (if adding sessions)
- `DATABASE_URL=...` (if adding database)

## Port Configuration

The application uses **Port Manager** for centralized port management and web-based launcher functionality.

### Port Manager Integration
- **Location:** `/home/joe/ai/port_manager`
- **Registry File:** `$HOME/.ports`
- **Web Dashboard:** `http://localhost:5050`
- **Wordy Assignment:** Port 5000

### How It Works
1. At startup, `quiz_app.py` registers with Port Manager using `pm.register_port()`
2. Registration includes:
   - App name: `wordy`
   - Port: `5000`
   - Description: `Wordy GRE Vocabulary Quiz Application`
   - Start command: `/home/joe/ai/wordy/venv/bin/python quiz_app.py`
   - Working directory: `/home/joe/ai/wordy`
   - Stop command: `pkill -f 'wordy/venv/bin/python quiz_app.py'`
   - Restart command: (empty - uses stop + start)
3. The app gets its port from Port Manager via `pm.get_port('wordy')`
4. Falls back to port 5000 if Port Manager is unavailable

### Launcher Functionality
The Port Manager web dashboard provides:
- **Start button** - Launch the app in background with process tracking
- **Stop button** - Gracefully stop the app using the configured stop command
- **Restart button** - Stop then start the app (or use custom restart command)
- **Status indicator** - Green when running, gray when stopped
- **Open button** - Quick link to `http://localhost:5000`
- **Process monitoring** - Shows PID and resource usage
- **Log viewer** - View application logs in real-time

### Process Management Commands
```bash
# Start command (runs in background)
/home/joe/ai/wordy/venv/bin/python quiz_app.py

# Stop command (graceful shutdown)
pkill -f 'wordy/venv/bin/python quiz_app.py'

# Restart (automatic: stop + start)
# No custom restart command configured
```

### Usage
```bash
# View Port Manager dashboard
cd /home/joe/ai/port_manager && ./run_web.sh
# Open http://localhost:5050

# Command line
port-manager list               # List all apps
port-manager get wordy          # Get wordy port

# Manual process management
pkill -f 'wordy/venv/bin/python quiz_app.py'  # Stop
/home/joe/ai/wordy/venv/bin/python quiz_app.py &  # Start
```

### Example .ports File Entry
```
wordy:5000:{"description": "Wordy GRE Vocabulary Quiz Application", "start_command": "/home/joe/ai/wordy/venv/bin/python quiz_app.py", "working_dir": "/home/joe/ai/wordy", "stop_command": "pkill -f 'wordy/venv/bin/python quiz_app.py'", "restart_command": ""}
```

---

## Debugging Tips

### JavaScript Console
- All game state is in global variables (easy to inspect)
- Check LocalStorage in DevTools > Application tab
- Console.log statements in event handlers

### Common Issues
- **Settings not saving:** Check `saveSettings()` includes new field
- **Score calculation wrong:** Verify `calculateLetterScore()` logic
- **Timer issues:** Check `startLetterTimer()` and `stopLetterTimer()` calls
- **Leaderboard not updating:** Verify `saveToLeaderboard()` called with correct data

### Testing Score Recalculation
1. Play a game with default settings
2. Save the game (it will be in localStorage)
3. Change settings (e.g., increase perfectWordBonus to 200)
4. View leaderboard
5. Toggle to "Recalculated" view
6. Verify scores update correctly

---

## File Reference

### Key Files to Know

**templates/spelling_quiz.html** (2266 lines)
- Most complex template
- Main game logic: lines 757-2255
- Settings: lines 773-787
- Game state variables: lines 759-819
- Scoring functions: lines 861-870, 1968-1982
- Display functions: lines 1531-1644
- History tracking: Throughout game functions

**quiz_app.py**
- Flask routes
- Word fetching logic
- Simple, minimal backend

**templates/home.html**
- Menu navigation
- Progress stats
- Link to all quiz modes

### Settings Object Reference

```javascript
settings = {
    initialLettersRevealed: 0,       // 0-10
    revealMode: 'initial',           // 'initial' or 'random'
    spaceRevealMode: 'sequential',   // 'sequential' or 'random'
    revealPenaltySeconds: 20,        // 0-60
    wrongLetterPenaltySeconds: 5,    // 0-60
    letterTimeLimit: 20,             // 1-60 seconds
    baseScore: 20,                   // 0-100
    bonusPerSecond: 2,               // 0-10
    hintLetterCount: 4,              // 2-10
    hintPenalty: 7,                  // 0-100
    perfectWordBonus: 100,           // 0-200
    completedWordBonus: 50,          // 0-200
    gameTimeLimit: 120               // 30-600 seconds
};
```

---

## Next Development Session Checklist

When starting a new session:

1. Read this file (CLAUDE.md) for context
2. Check PROMPT_HISTORY.md for recent changes
3. Review REQUIREMENTS.md for feature specifications
4. Test the current state by running the app
5. Make changes
6. Test thoroughly
7. Commit and push
8. Update documentation (especially PROMPT_HISTORY.md)

---

## Contact & Resources

- **Repository:** (Add GitHub URL here)
- **Word List Source:** Manhattan Prep GRE Words
- **Target GRE Score:** 160+ Verbal

---

*Last Updated: 2025-10-18*
*Session: Perfect vs Completed Word Bonus Implementation*
