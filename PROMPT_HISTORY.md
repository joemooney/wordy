# Prompt History

All development sessions with detailed actions, fixes, and git operations.

---

## Session: Continued from Context Summary (2025-10-18)

### Context
Continued session from previous conversation that ran out of context. Previous work included:
- Game history storage system with JSON tracking
- Score recalculation with proportional time scaling
- Game over modal keyboard shortcuts
- Recalculated scores UI in leaderboard

### Prompt: Complete Perfect vs Completed Word Bonus System

**User Request:**
"Increase Perfect Word default to 100 points. But if any letter is incorrectly entered it is no longer perfect but Completed which defaults to 50 points. So completed is the same as Perfect is now (no hint or reveals). And perfect requires no mistaken letters typed."

**Implementation Details:**

1. **Settings Updated** (`templates/spelling_quiz.html:773-787`):
   - Changed `perfectWordBonus` from 50 to 100
   - Added `completedWordBonus: 50`
   - Added `wrongLetterThisWord` tracking flag

2. **Word Tracking** (`templates/spelling_quiz.html:1530-1556`):
   - Reset both `usedHelpThisWord` and `wrongLetterThisWord` in `displayWord()`
   - Initialize `currentWordResult` with both `perfectWord` and `completedWord` flags

3. **Wrong Letter Detection** (`templates/spelling_quiz.html:1773-1779`):
   - Set `wrongLetterThisWord = true` when wrong letter typed
   - Mark `currentWordResult.perfectWord = false`

4. **Bonus Logic** (`templates/spelling_quiz.html:1968-1982`):
   - If no help and no wrong letters → Perfect Word (+100)
   - If no help but had wrong letters → Completed Word (+50)
   - Mark `completedWord = false` if help was used

5. **Visual Feedback** (`templates/spelling_quiz.html:1914-1926`):
   - Created `showCompletedWordBonus()` with blue background
   - Shows "✅ Completed Word! +50 bonus points!"

6. **Settings UI** (`templates/spelling_quiz.html:641-650`):
   - Added Perfect Word Bonus input (default 100)
   - Added Completed Word Bonus input (default 50)

7. **Settings Persistence** (`templates/spelling_quiz.html:1395`):
   - Updated `saveSettings()` to save `completedWordBonus`
   - Updated `updateSettingsUI()` to load `completedWordBonus`

8. **Score Display** (`templates/spelling_quiz.html:1454-1463, 1480-1489`):
   - Updated start screen to show both bonuses
   - Updated pause screen to show both bonuses
   - Changed Perfect Word description to "no hints/reveals/mistakes"
   - Added Completed Word description "no hints/reveals but had mistakes"

9. **Score Recalculation** (`templates/spelling_quiz.html:1033-1040`):
   - Updated `recalculateScore()` to apply `completedWordBonus`
   - Uses else-if logic: perfectWord takes precedence, then completedWord

**Git Operations:**
```bash
git add -A
git commit -m "Implement Perfect vs Completed word bonus distinction"
git push
```

**Commit:** `bfc8d74`

**Files Modified:**
- `/home/joe/ai/wordy/templates/spelling_quiz.html`

---

## Session: Leaderboard Dialog Enhancements (2025-10-18)

### Prompt: Enhance Leaderboard with Keyboard Shortcuts and Dynamic Scoring

**User Request:**
"On the Leaderboard dialog, SPACE ENTER or ESC is close dialog. Rename Recalulated button to 'Scores' and make that the first and default button and place 'Original Scores' button to right of that button. If you hover over 'Original Scores' review a tip that the scoring has changed from the original. Hide the 'Original Scores' if the scoring has not changed from the beginning of history. One the first game store the original history. So if we clear history we can change the scoring system and start with a clean slate with the current scoring system."

**Implementation Details:**

1. **Keyboard Shortcuts** (`templates/spelling_quiz.html:2051-2058`):
   - Added leaderboard modal keyboard handler
   - SPACE, ENTER, or ESC all close the leaderboard
   - Prevents event propagation to avoid conflicts

2. **Original Settings Management** (`templates/spelling_quiz.html:942-963`):
   - Created `getOriginalSettings()` - retrieves baseline settings from localStorage
   - Created `saveOriginalSettings()` - stores baseline settings
   - Created `settingsHaveChanged()` - compares current to original settings
   - Compares: letterTimeLimit, baseScore, bonusPerSecond, hintPenalty, perfectWordBonus, completedWordBonus

3. **Save Original Settings on First Game** (`templates/spelling_quiz.html:969-972`):
   - Modified `saveToLeaderboard()` to detect first game
   - Saves settings as baseline when leaderboard is empty
   - If history is cleared, next game becomes new baseline

4. **Button Reordering and Renaming** (`templates/spelling_quiz.html:1203-1210`):
   - "Scores" button now first (default view)
   - "Original Scores" button second (conditional)
   - Swapped parameter logic: `showOriginal = false` is now default

5. **Conditional Display** (`templates/spelling_quiz.html:1207-1209`):
   - Check `hasSettingsChanged` before showing "Original Scores" button
   - Only displays second button if scoring system has changed
   - Provides clean interface when settings are unchanged

6. **Hover Tooltip** (`templates/spelling_quiz.html:1208`):
   - Added `title="Scoring system has changed from original"` to Original Scores button
   - Explains why two views are available

7. **Default Behavior** (`templates/spelling_quiz.html:1173`):
   - Changed function signature to `displayLeaderboard(showOriginal = false)`
   - "Scores" view (recalculated with current settings) is now default
   - Cleaner user experience - see current scoring by default

**Git Operations:**
```bash
git add -A
git commit -m "Enhance leaderboard dialog with keyboard shortcuts and dynamic scoring display"
git push
```

**Commit:** `4118f92`

**Files Modified:**
- `/home/joe/ai/wordy/templates/spelling_quiz.html`

**Benefits:**
- Keyboard-driven workflow for power users
- Clean UI that only shows "Original Scores" when relevant
- Automatic baseline tracking allows score system evolution
- Clear history resets baseline for fresh start
- Tooltip provides context for users

---

## Previous Sessions (From Context Summary)

### Session 1: Game History Storage System

**Prompt:** Store game answers to enable score recalculation with different settings

**Implementation:**
- Created JSON structure for detailed game history tracking
- Track per-letter data: letter, correct, timeElapsed, revealed, noScore
- Track per-word data: word, definition, letters array, hintsUsed, perfectWord
- Track game-level data: settings snapshot, timestamps, wordResults array
- Implemented `recalculateScore()` with proportional time scaling
- Modified all game functions to track history data

**Git Operations:**
```bash
git commit -m "Implement detailed game history tracking with score recalculation"
```

**Commit:** `54e26e6`

---

### Session 2: Game Over Modal Keyboard Shortcuts

**Prompt:** Add keyboard shortcuts to end-of-game dialog

**Implementation:**
- SPACE/ENTER → Start new game
- L key → View leaderboard
- ESC → Return home
- Updated button text to show shortcuts
- Added keyboard event handler for game over modal

**Git Operations:**
```bash
git commit -m "Add keyboard shortcuts to game over modal"
```

**Commit:** `a94a0bf`

---

### Session 3: Recalculated Scores UI

**Prompt:** Add UI to view leaderboard with recalculated scores

**Implementation:**
- Added toggle buttons: "Original Scores" and "Recalculated"
- Modified `displayLeaderboard()` to accept useRecalculated parameter
- Recalculates all scores with current settings when toggled
- Shows "Score (was OriginalScore)" format
- Re-sorts leaderboard based on selected view

**Git Operations:**
```bash
git commit -m "Add UI for viewing recalculated scores in leaderboard"
```

**Commit:** `25b1e7c`

---
