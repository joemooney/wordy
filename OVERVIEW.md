# Wordy - GRE Vocabulary Quiz Application

## Vision

Wordy is a comprehensive web-based vocabulary training application designed to help students prepare for the GRE exam. It provides multiple quiz modes and study methods to master 994 essential GRE words from Manhattan Prep's word list.

The application emphasizes active recall, spaced repetition principles, and gamification to make vocabulary learning engaging and effective.

## Project Purpose

- **Primary Goal:** Help students master GRE vocabulary through various quiz formats
- **Target Audience:** GRE test takers, vocabulary enthusiasts
- **Learning Approach:** Multiple quiz modes to reinforce learning from different angles
- **Gamification:** Leaderboards, scoring, and time challenges to maintain motivation

## Application Modes

### 1. GRE Vocabulary Quiz
Traditional multiple-choice format where students see a word and select the correct definition from 4 options. Perfect for initial learning and quick assessment.

### 2. Inverse GRE Quiz
Reverse format showing definitions with word choices. Helps reinforce the word-definition connection from the opposite direction.

### 3. GRE Word Review
Self-paced flashcard mode showing words with hidden definitions. Students can click or press SPACE to reveal. No pressure, just practice. Includes favorite/remove functionality for personalized study.

### 4. GRE Definition Review
Reverse flashcard mode showing definitions with hidden words. Helps with word recall from definition clues.

### 5. Spelling Quiz (Featured Mode)
The most comprehensive and challenging mode. Students must type words letter-by-letter from their definitions under time pressure. Features:
- Sophisticated scoring system with time bonuses
- Game timer creating urgency (default 2 minutes)
- Letter timer for each character
- Hint system with progressive elimination
- Perfect vs Completed word bonuses
- Comprehensive leaderboard with time-based rankings
- Detailed game history for score recalculation

### 6. Trivia Quiz
General knowledge quiz for variety and mental breaks from vocabulary study.

## Key Features

### Comprehensive Scoring
The spelling quiz features a sophisticated scoring system:
- Base points for correct letters
- Time bonuses for quick responses
- Perfect word bonuses (no mistakes, no help)
- Completed word bonuses (no help but had mistakes)
- Penalties for hints and reveals

### Game History & Analytics
Every game is fully tracked with detailed history:
- Per-letter timing data
- Correct/incorrect letter tracking
- Hint and reveal usage
- Settings snapshot for each game
- Score recalculation with new settings
- Proportional time scaling

### Leaderboard System
Multi-timeframe rankings:
- All-time top scores
- Monthly rankings
- Weekly rankings
- Daily rankings

### Customization
Extensive settings for personalized learning:
- Adjustable time limits
- Configurable scoring parameters
- Hint system customization
- Reveal mode options
- Penalty adjustments

## Technology Stack

### Backend
- **Python 3.x:** Core language
- **Flask:** Web framework
- **Standard Library:** File I/O, JSON handling

### Frontend
- **HTML5:** Structure
- **CSS3:** Modern styling with gradients and animations
- **Vanilla JavaScript:** Interactive functionality, no frameworks
- **LocalStorage:** Client-side data persistence

### Data Storage
- **Text Files:** Word lists (pipe-delimited format)
- **JSON:** Settings and leaderboards
- **LocalStorage:** Browser-based persistence

## Design Philosophy

### User Experience
- **Clean, Modern UI:** Gradient backgrounds, smooth animations
- **Responsive Design:** Works on desktop and mobile
- **Immediate Feedback:** Visual and textual confirmation of actions
- **Keyboard-Centric:** Full keyboard navigation for power users

### Learning Principles
- **Active Recall:** Students must retrieve information from memory
- **Multiple Exposures:** Different quiz formats reinforce learning
- **Time Pressure:** Simulates test conditions for the GRE
- **Progressive Difficulty:** Students can adjust settings as they improve

### Gamification
- **Scoring System:** Motivates achievement
- **Leaderboards:** Social comparison and competition
- **Visual Feedback:** Celebrations for perfect words
- **Rankings:** Track improvement over time

## File Structure

```
wordy/
├── quiz_app.py                          # Flask web application
├── quiz_terminal.py                     # Terminal-based quiz
├── manhattan_prep_gre_words_formatted.txt  # Word list (994 words)
├── quiz_stats.json                      # Score tracking
├── templates/
│   ├── home.html                        # Home page with mode selection
│   ├── quiz.html                        # GRE vocabulary quiz
│   ├── inverse_quiz.html                # Inverse GRE quiz
│   ├── word_review.html                 # Word review mode
│   ├── definition_review.html           # Definition review mode
│   ├── spelling_quiz.html               # Spelling quiz (main feature)
│   └── trivia_quiz.html                 # Trivia quiz
├── CLAUDE.md                            # Development documentation
├── OVERVIEW.md                          # This file
├── REQUIREMENTS.md                      # Detailed requirements
├── PROMPT_HISTORY.md                    # Development session history
└── README.md                            # Quick start guide
```

## Getting Started

### Quick Start
1. Run the startup script: `./start_quiz.sh`
2. Open browser to `http://localhost:5000`
3. Choose a quiz mode from the home page
4. Start learning!

### Development
- Backend: Flask app in `quiz_app.py`
- Frontend: HTML templates in `templates/`
- Styling: Inline CSS in templates (self-contained)
- Scripts: Inline JavaScript (no build process needed)

## Project Status

### Current State (October 2025)
- All quiz modes fully functional
- Spelling quiz is the most advanced feature
- Game history and recalculation working
- Leaderboards with multi-timeframe rankings
- Perfect vs Completed word bonuses implemented
- Extensive customization options

### Recent Additions
- Perfect word bonus (100 points) vs Completed word bonus (50 points)
- Wrong letter tracking separate from hint/reveal usage
- Recalculated score viewing in leaderboards
- Keyboard shortcuts for game over modal

## Study Recommendations

### For Best Results
1. **Start with GRE Vocabulary Quiz:** Get familiar with words
2. **Use Review Modes:** Reinforce with flashcard-style review
3. **Practice Spelling:** Master words with the spelling quiz
4. **Try Inverse Quiz:** Test definition recall
5. **Adjust Settings:** Increase difficulty as you improve
6. **Track Progress:** Use leaderboards to monitor improvement

### Study Tips
- Aim for 90%+ accuracy before the actual GRE
- Review incorrect answers carefully
- Use the favorite feature to mark challenging words
- Practice with time pressure to simulate test conditions
- Study in short, focused sessions for better retention

## Future Vision

### Potential Enhancements
- User accounts with cloud synchronization
- Custom word list uploads
- Detailed analytics and progress charts
- Spaced repetition algorithm
- Mobile native apps
- Word categorization (difficulty, topic, frequency)
- Study streak tracking
- Multiplayer competitive modes

---

**Good luck with your GRE preparation!**
