# GRE Vocabulary Quiz

Two quiz applications to help you study 994 essential GRE words from Manhattan Prep.

## Quick Start

### Option 1: Web-based Quiz (Recommended)

**Easiest way - use the startup script:**
```bash
./start_quiz.sh
```

Then open your browser to: **http://localhost:5000**

**Or manually:**
```bash
source venv/bin/activate
python3 quiz_app.py
```

**Features of the web interface:**
   - Beautiful, responsive design
   - Real-time score tracking
   - Visual feedback for correct/incorrect answers
   - Accuracy percentage display
   - Instant answer checking

### Option 2: Terminal-based Quiz

For a simpler, terminal-only experience:

```bash
python3 quiz_terminal.py
```

Features:
- No installation needed (uses only Python standard library)
- Clean terminal interface
- Score tracking
- Performance feedback
- Can be used over SSH

## How It Works

Both quiz applications:
- Show you a GRE word
- Present 4 possible definitions (multiple choice)
- Track your score and accuracy
- Use the same word list (994 words from Manhattan Prep)

## Files

- `quiz_app.py` - Flask web application
- `quiz_terminal.py` - Terminal-based quiz
- `templates/quiz.html` - Web interface template
- `manhattan_prep_gre_words_formatted.txt` - Word list (994 words)
- `convert_gre_words.py` - Script used to convert original word list

## Tips for Studying

- Start with the web version for the best experience
- Use the terminal version when you're away from a GUI
- Reset stats periodically to track improvement
- Aim for 90%+ accuracy before the actual GRE
- Review incorrect answers carefully

## Word List Source

Words are from Manhattan Prep's 1000 GRE Words list, formatted as:
```
word|definition
```

Good luck with your GRE preparation!
