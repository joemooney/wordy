# Wordy - GRE Vocabulary Quiz Application

A comprehensive web-based quiz application to help you master 994 essential GRE words from Manhattan Prep. Features 6 different quiz modes, time-based scoring, leaderboards, and detailed game history tracking.

## 🚀 Quick Start

### Starting the Server

**Method 1: Using the startup script (Recommended)**
```bash
./start_quiz.sh
```

**Method 2: Manual start**
```bash
source venv/bin/activate
python3 quiz_app.py
```

Once the server is running, open your browser to:
**http://localhost:5000**

The server runs on port 5000 by default and includes:
- Flask development server with auto-reload
- Debug mode enabled for development
- Access from any device on your local network

To stop the server, press `Ctrl+C` in the terminal.

---

## 📚 Quiz Modes

### 1. **GRE Quiz** (Standard Multiple Choice)
- Traditional multiple-choice quiz
- 4 answer options per question
- Score tracking and accuracy percentage
- Perfect for quick vocabulary drills

### 2. **Inverse GRE Quiz**
- Reversed format: definition → word
- Test your recall from the opposite direction
- Same tracking features as standard quiz

### 3. **Spelling Quiz** ⭐ (Featured)
The most advanced mode with sophisticated time-based scoring:

**Features:**
- Type words letter-by-letter from their definitions
- 2-minute timed game sessions
- Time-based scoring (faster = more points)
- Perfect word bonuses (+100 pts: no hints/reveals/mistakes)
- Completed word bonuses (+50 pts: no hints/reveals but had mistakes)
- Hint system (/ key) with point penalties
- Letter reveal (SPACE key) with time penalties
- Detailed game history tracking
- Multi-timeframe leaderboards (all-time, monthly, weekly, daily)
- Score recalculation with new settings
- No word repetition within a game session
- Customizable settings for difficulty

**Keyboard Shortcuts:**
- Letter keys: Type the word
- SPACE: Reveal next letter (+time penalty)
- /: Show hint (-points, press again to eliminate wrong letters)
- ?: Pause game and show instructions
- ESC: Pause (first press) or Home (when paused)
- Backspace: Remove last letter

### 4. **Word Review** (Flashcards)
- Flashcard-style word review
- See the word, then reveal its definition
- Favorite words for later review
- Navigate with keyboard or click
- Keyboard shortcuts: SPACE/ENTER (next), F (favorite), ESC (home)

### 5. **Definition Review** (Reverse Flashcards)
- See the definition first, then reveal the word
- Tests recall in reverse direction
- Remove words you've mastered
- Same navigation as Word Review

### 6. **Trivia Quiz**
- General knowledge trivia across 22 categories
- 48,472 questions covering celebrities, geography, science, history, and more
- Break from GRE studying with fun trivia

---

## 🎮 Features

### Spelling Quiz Advanced Features

**Time-Based Scoring:**
- Base points per letter (default: 20)
- Time bonus: +2 points per second remaining (20s limit per letter)
- Maximum 60 points per letter (20 base + 40 bonus)

**Word Completion Bonuses:**
- Perfect Word: +100 points (no hints, no reveals, no wrong letters)
- Completed Word: +50 points (no hints/reveals, but had typing mistakes)

**Help Systems:**
- Hint system: Shows N random letters including the correct one (-7 points)
- Letter reveal: Automatically fills next/random letter (+20s penalty)
- Wrong letter penalty: +5s added to game time

**Game History:**
- Detailed per-letter tracking (time, correctness, revealed status)
- Per-word statistics (hints used, perfect/completed status)
- Complete game sessions with settings snapshots
- Score recalculation when settings change

**Leaderboards:**
- All-time rankings
- Monthly rankings
- Weekly rankings (last 7 days)
- Daily rankings
- View original scores vs. recalculated scores

**Customizable Settings:**
- Initial letters revealed (0-10)
- Reveal mode (initial or random)
- Space reveal mode (sequential or random)
- Letter time limit (1-60 seconds)
- Game time limit (30-600 seconds)
- All point values and penalties
- Settings preserved with each game for fair comparison

### General Features
- Beautiful, responsive gradient design
- Glassmorphism UI effects
- Keyboard-first navigation
- Real-time score tracking
- LocalStorage for persistence
- No user accounts needed (all data stored locally)
- Mobile-friendly interface

---

## 📁 Project Structure

```
wordy/
├── quiz_app.py                 # Flask application (main server)
├── start_quiz.sh               # Startup script
├── manhattan_prep_gre_words_formatted.txt  # 994 GRE words
├── quiz_stats.json             # Quiz statistics
├── templates/
│   ├── home.html               # Main menu
│   ├── quiz.html               # GRE Quiz
│   ├── inverse_quiz.html       # Inverse GRE Quiz
│   ├── spelling_quiz.html      # Spelling Quiz (most complex)
│   ├── word_review.html        # Word Review flashcards
│   ├── definition_review.html  # Definition Review flashcards
│   └── trivia_quiz.html        # Trivia Quiz
├── CLAUDE.md                   # Development guide
├── OVERVIEW.md                 # Project overview
├── REQUIREMENTS.md             # Feature requirements
└── PROMPT_HISTORY.md           # Development history
```

---

## 🎯 Tips for GRE Preparation

### Using the Spelling Quiz Effectively
1. Start with default settings to establish your baseline
2. Use hints sparingly to maintain perfect word bonuses
3. Aim for consistent improvement in weekly rankings
4. Review game history to identify patterns in mistakes
5. Gradually reduce time limits as you improve

### General Study Tips
- Rotate between quiz modes to prevent monotony
- Use Word Review to familiarize yourself with new words
- Test yourself with Inverse Quiz to strengthen recall
- Practice Spelling Quiz to master spelling and typing speed
- Aim for 90%+ accuracy before the actual GRE
- Track your progress with the leaderboard system

### Keyboard Shortcuts
Most quiz modes support extensive keyboard shortcuts for efficient studying without touching the mouse. Check each mode's help screen (usually ? key) for specific shortcuts.

---

## 🔧 Technical Details

**Backend:**
- Python 3 + Flask
- Simple route handlers for each quiz mode
- Random word selection from formatted text file
- JSON-based statistics tracking

**Frontend:**
- Vanilla JavaScript (no frameworks)
- Self-contained HTML templates with inline CSS/JS
- LocalStorage for client-side persistence
- Responsive design with CSS Grid and Flexbox

**Data Storage:**
- Word list: Pipe-delimited text file (`word|definition`)
- Quiz stats: JSON file (server-side)
- Game history: LocalStorage (client-side)
- Leaderboards: LocalStorage (client-side)

**Browser Compatibility:**
- Modern browsers with LocalStorage support
- ES6 JavaScript features
- CSS3 animations and gradients

---

## 📊 Word List

994 essential GRE words from Manhattan Prep's 1000 GRE Words list.

Format: `word|definition`

Example:
```
aberration|deviation from what is normal
abscond|to depart suddenly and secretively
abstemious|characterized by self-denial or abstinence, as in the use of drink or food
```

---

## 🛠️ Development

To make changes to the application:

1. Modify the appropriate template in `templates/`
2. Refresh your browser (Flask auto-reloads in debug mode)
3. For server-side changes, the server will auto-restart

For major features or architectural changes, update:
- `CLAUDE.md` - Development guide and architecture
- `REQUIREMENTS.md` - Feature specifications
- `PROMPT_HISTORY.md` - Development session log

---

## 📝 License

For educational and personal use. Word list courtesy of Manhattan Prep.

---

Good luck with your GRE preparation! 🎓
