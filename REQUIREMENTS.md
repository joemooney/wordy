# Project Requirements

All system requirements organized by main categories.

---

## Quiz Types

### GRE Vocabulary Quiz
- Show GRE word with 4 multiple-choice definitions
- Track score and accuracy
- Save scores to JSON file
- Display leaderboard
- 994 words from Manhattan Prep GRE word list

### Inverse GRE Quiz
- Show definition with 4 word choices
- Reverse of standard GRE quiz
- Same scoring and tracking

### Word Review
- Self-test mode showing word with hidden definition
- Click/tap or press SPACE to reveal definition
- Click/tap on revealed definition to advance to next word
- No scoring, just practice
- Favorite/remove word functionality
- Familiarity levels (0-3) for word tracking
- **Session-based reviews:**
  - Time-based mode (1-60 minutes)
  - Word count mode (1-100 words)
  - Filter by familiarity levels
  - Favorites-only filter
  - No word repetition within session
  - Progress tracking (words reviewed, time elapsed)
  - Completion dialog when done
- **Two-stage ESC behavior:**
  - First ESC: End review (with confirmation)
  - Second ESC (in modal): Return home
- **Dynamic word sizing:** Adjusts for long words on small screens
- **Responsive modals:** Optimized for older iPads and small screens

### GRE Definition Review
- Self-test mode showing definition with hidden word
- Click/tap or press SPACE to reveal word
- Click/tap on revealed word to advance to next word
- No scoring, just practice
- Favorite/remove word functionality
- **Dynamic word sizing:** Adjusts for long words on small screens
- **Responsive design:** Optimized for all screen sizes

### Spelling Quiz (Main Focus)
- Type word letter by letter from definition
- Time-based scoring with bonuses
- Game timer (configurable, default 120 seconds)
- Letter timer (configurable, default 20 seconds per letter)
- Leaderboard with rankings (all-time, month, week, today)
- Detailed game history tracking for score recalculation

### Trivia Quiz
- General knowledge quiz
- 22 categories (Celebrities, Geography, Music, Movies, etc.)
- 48,472+ questions from CSV files
- Multiple choice format (2-4 choices per question)
- Category selection
- Score tracking

### Letter Grid
- **3×3 letter grid word-finding puzzle**
- **Grid generation:** Based on random 9-letter word (5,137 words available)
  - Guarantees at least one 9-letter word solution
  - Letters shuffled to hide the base word
  - Finds all valid words (3+ letters) from those letters
  - **Word limit:** Maximum 150 words per game (prevents overwhelming puzzles)
  - Tries up to 100 different 9-letter words to find suitable grid
- **Word discovery:**
  - Click/tap tiles to select letters
  - Build words from available letters
  - Submit to check validity
  - Track found words vs. total words
- **Progress tracking:**
  - Words found / Total words / Remaining
  - Percentage completion with progress bar
  - Found words displayed alphabetically
- **Hint mode (💡 button):**
  - Toggle to show match count as you type
  - Displays "X remaining word(s) with these letters"
  - Only counts words starting with typed letters that haven't been found yet
- **Resolve button:**
  - Appears when hint is ON and exactly 1 match exists
  - Auto-fills remaining letters to complete the word
  - Selects correct tiles in grid automatically
- **Show Nine button (🔍):**
  - Reveals the nine-letter base word
  - Visually selects tiles in grid to spell the word
  - Displays word in current word area (same as manual typing)
  - Helpful when stuck or curious about the puzzle solution
- **Word exclusion:**
  - Red X button on each found word (high visibility)
  - Click to immediately remove word from current game and exclude from future games
  - Updates found/remaining counts instantly
  - No confirmation required for faster workflow
  - Persists in words_deleted.txt file
  - Can exclude multiple words (not limited like a radio button)
- **Word dispute:**
  - Red ⚠️ Dispute button appears temporarily after word rejection
  - Shows for 1.5 seconds to left of Clear button
  - Click to add rejected word to disputed words list
  - No duplicates (tracks in Set)
  - Logs disputed words to console
- **Button Layout:**
  - Row 1: Dispute, Clear, Submit, Resolve (main game actions)
  - Row 2: Hint, Show Nine, New Game (helper functions)
  - Two-row layout prevents width shifting
  - All buttons use visibility (hidden/visible) to maintain fixed positions
  - Dispute only appears after rejected word submission
- **Controls:**
  - Click tiles or use keyboard (letter keys)
  - Enter to submit, Escape to clear
  - Backspace to undo last letter
- **Data storage:**
  - Word list: wordlist_50000.txt (49,301 words)
  - Deleted words: words_deleted.txt (user-excluded words)
- **Responsive design:**
  - Touch-friendly for iPad/iPhone
  - Viewport optimized to prevent zoom on iPhone

### Dictionary Browser
- Browse all 994 GRE words
- **Search functionality:**
  - Search by word or definition
  - Fuzzy matching algorithm
  - Ranking by relevance (exact, starts-with, contains)
- **Keyboard navigation:**
  - Arrow keys to navigate
  - Type to search
- **Display:**
  - Alphabetically sorted
  - Word + definition pairs
  - Total word count

---

## Spelling Quiz - Detailed Requirements

### Scoring System

#### Base Scoring
- **Correct Letter:** Base score (default 20 points) + time bonus
- **Time Bonus:** Points per second remaining (default 2 points/sec)
- **Letter Time Limit:** Default 20 seconds per letter

#### Word Completion Bonuses
- **Perfect Word:** +100 points (no hints/reveals/mistakes)
- **Completed Word:** +50 points (no hints/reveals but had wrong letter attempts)

#### Penalties
- **Hint Penalty:** -7 points per hint use
- **Reveal Penalty:** +20 seconds to game timer
- **Wrong Letter Penalty:** +5 seconds to game timer

### Game Mechanics

#### Letter Revealing
- **Initial Letters Revealed:** Configurable (0-10)
- **Reveal Mode:** Initial (sequential from start) or Random
- **Space Key Reveal Mode:** Sequential (next letter) or Random
- **Revealed letters:** Don't score points, add time penalty

#### Hint System
- **Hint Letters:** Show N letters (default 4) including correct one
- **Progressive Hints:** Press '/' again to eliminate wrong letters
- **Hint Penalty:** Points deducted per hint use
- **Final Letter:** Auto-filled when only correct letter remains

#### Game Timer
- **Total Game Time:** Configurable (30-600 seconds, default 120)
- **Timer Display:** Real-time countdown with color coding
  - Green: >30 seconds
  - Yellow: 10-30 seconds
  - Orange: <10 seconds
  - Red: 0 seconds (game over)

#### Pause System
- **Pause Key:** '?' key
- **Pause Screen:** Shows scoring info and remaining time
- **Resume:** SPACE or ENTER
- **Timer Adjustment:** Accounts for paused time

### Game History & Analytics

#### Detailed Tracking
- **Per-Letter Data:**
  - Letter character
  - Correct/incorrect
  - Time elapsed
  - Revealed flag
  - No-score flag
- **Per-Word Data:**
  - Word and definition
  - Array of letter data
  - Hints used count
  - Perfect word flag
  - Completed word flag
- **Per-Game Data:**
  - Settings snapshot (for recalculation)
  - Start/end timestamps
  - Final score
  - Words completed
  - Array of word results

#### Score Recalculation
- **Proportional Time Scaling:** Adjust letter times based on new time limits
- **Settings Override:** Recalculate with current settings
- **Leaderboard View:** Toggle between original and recalculated scores
- **Preserved History:** Original scores always preserved

#### Leaderboard
- **Rankings:**
  - All-time top 10
  - This month
  - This week
  - Today
- **Display Options:**
  - Original scores
  - Recalculated scores (with original shown)
- **Ranking Display:** Show rank out of total (e.g., "#3 of 45")

### Keyboard Controls

#### Game Controls
- **Letter Input:** A-Z keys
- **Reveal Letter:** SPACE
- **Hint:** / key (press multiple times to eliminate letters)
- **Pause:** ? key
- **Backspace:** Remove last typed letter
- **Escape:** Return to home

#### Modal Controls
- **Start Game:** SPACE or ENTER
- **Game Over Modal:**
  - SPACE/ENTER → New game
  - L → View leaderboard
  - ESC → Home
- **Settings Modal:** ESC to close

### Visual Feedback

#### Letter Boxes
- **Active:** Pulsing white glow
- **Filled:** Blue background
- **Revealed:** Yellow background
- **Wrong Letter:** Shake animation

#### Notifications
- **Score Feedback:** Green background, "+X points!"
- **Perfect Word:** Green background, "🎉 Perfect Word! +100 bonus!"
- **Completed Word:** Blue background, "✅ Completed Word! +50 bonus!"
- **Reveal Penalty:** Orange background, "+20s penalty! (Letter revealed)"
- **Wrong Letter:** Orange background, "+5s penalty! (Wrong letter)"
- **Hint Penalty:** Score deduction shown

### Settings (All Configurable)

#### Letter Revealing
- Initial Letters Revealed (0-10)
- Reveal Mode (initial/random)
- Space Reveal Mode (sequential/random)
- Reveal Penalty Seconds (0-60)
- Wrong Letter Penalty Seconds (0-60)

#### Scoring
- Letter Time Limit (1-60 seconds)
- Base Score Per Letter (0-100)
- Bonus Points Per Second (0-10)
- Perfect Word Bonus (0-200)
- Completed Word Bonus (0-200)

#### Hint System
- Number of Hint Letters (2-10)
- Hint Point Penalty (0-100)

#### Game Timer
- Game Time Limit (30-600 seconds)

### Data Persistence
- Settings stored in localStorage (key: 'spellingQuizSettings_v2')
- Leaderboard stored in localStorage (key: 'spellingQuizLeaderboard')
- Review favorites stored in localStorage (per mode)
- Review removed words stored in localStorage (per mode)

---

## Home Page Requirements

### Menu Cards
- Display all quiz types as clickable cards
- Hover effects and visual feedback
- Active/disabled states
- Icon representation for each quiz

### Progress Statistics
- GRE Score (overall correct/total)
- GRE Accuracy percentage
- Rounds played count

---

## Technical Requirements

### Backend (Flask)
- Python 3.x
- Flask web framework
- Routes for all quiz types
- Word randomization
- Session management (if needed)

### Frontend
- **Responsive design:**
  - Media queries for screen height (≤800px, ≤700px, ≤600px)
  - Media queries for screen width (≤600px, ≤400px)
  - Dynamic modal sizing for older iPads
  - Compact spacing and typography for small screens
- **Touch device support:**
  - Auto-detection of touch devices (iPad, iPhone, Android)
  - Virtual keyboard for Spelling Quiz
  - Touch-optimized button sizes (55px min-width, 20px padding)
  - Viewport fixes to prevent auto-zoom on iPhone
- **Dynamic content sizing:**
  - Words automatically resize based on length and screen size
  - Proportional scaling for long words (>10, >12, >15 letters)
  - Responsive on device rotation
- **Clean, modern UI:**
  - Purple gradient backgrounds (#667eea → #764ba2)
  - Glassmorphism effects (backdrop-filter blur)
  - Real-time updates and smooth transitions
  - Modal dialogs with responsive breakpoints
- **Keyboard navigation:**
  - Extensive keyboard shortcuts across all modes
  - Arrow keys, SPACE, ENTER, ESC support
  - Type-to-search in Dictionary
  - Letter keys for game input

### Data Format
- Word list: pipe-delimited format (word|definition)
- JSON for settings and leaderboards
- LocalStorage for client-side persistence

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- LocalStorage support required

---

## Future Enhancements (Not Yet Implemented)

### Potential Features
- User accounts and cloud sync
- Custom word lists
- Study progress tracking over time
- Spaced repetition algorithm
- Mobile app versions
- Export/import settings and progress
- Detailed analytics dashboard
- Practice mode for specific words

---
