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

### GRE Word Review
- Self-test mode showing word with hidden definition
- Click or press SPACE to reveal definition
- No scoring, just practice
- Favorite/remove word functionality

### GRE Definition Review
- Self-test mode showing definition with hidden word
- Click or press SPACE to reveal word
- No scoring, just practice
- Favorite/remove word functionality

### Spelling Quiz (Main Focus)
- Type word letter by letter from definition
- Time-based scoring with bonuses
- Game timer (configurable, default 120 seconds)
- Letter timer (configurable, default 20 seconds per letter)
- Leaderboard with rankings (all-time, month, week, today)
- Detailed game history tracking for score recalculation

### Trivia Quiz
- General knowledge quiz
- Multiple categories
- Score tracking

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
- Responsive design
- Mobile-friendly
- Clean, modern UI with gradients
- Real-time updates
- Modal dialogs
- Virtual keyboard support

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
