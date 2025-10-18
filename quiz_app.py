#!/usr/bin/env python3
"""
Web-based GRE vocabulary quiz application using Flask.
"""

from flask import Flask, render_template, request, jsonify, session
import random
import os
import json
import csv
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Stats database file
STATS_FILE = Path('quiz_stats.json')

# Load words from file
def load_words(filename='manhattan_prep_gre_words_formatted.txt'):
    """Load words and definitions from file."""
    words_dict = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '|' in line:
                word, definition = line.split('|', 1)
                words_dict[word] = definition
    return words_dict

# Global word dictionary
WORDS = load_words()
WORD_LIST = list(WORDS.keys())

# Load trivia questions from CSV files
def load_trivia_questions():
    """Load trivia questions from CSV files in the trivia directory."""
    trivia_dir = Path('trivia')
    categories = {}

    if not trivia_dir.exists():
        print("Warning: trivia directory not found")
        return categories

    for csv_file in trivia_dir.glob('category_*.csv'):
        category_name = csv_file.stem.replace('category_', '').replace('-', ' ').title()
        questions = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Skip rows with empty questions or correct answers
                    if not row.get('Questions') or not row.get('Correct'):
                        continue

                    question_text = row['Questions'].strip()
                    correct_answer = row['Correct'].strip()

                    # Get all choices
                    choices = []
                    for choice_key in ['A', 'B', 'C', 'D']:
                        choice = row.get(choice_key, '').strip()
                        if choice:
                            choices.append(choice)

                    # Skip if we don't have at least 2 choices
                    if len(choices) < 2 or not correct_answer:
                        continue

                    # Ensure correct answer is in choices
                    if correct_answer not in choices:
                        continue

                    questions.append({
                        'question': question_text,
                        'correct': correct_answer,
                        'choices': choices
                    })

        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
            continue

        if questions:
            categories[category_name] = questions
            print(f"Loaded {len(questions)} questions for category: {category_name}")

    return categories

# Load trivia questions
TRIVIA_CATEGORIES = load_trivia_questions()

# Stats database functions
def load_stats():
    """Load statistics from JSON file."""
    if STATS_FILE.exists():
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return init_stats()
    return init_stats()

def init_stats():
    """Initialize empty stats structure."""
    return {
        'overall': {
            'score': 0,
            'total': 0
        },
        'round_history': []
    }

def save_stats(stats):
    """Save statistics to JSON file."""
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
    except IOError as e:
        print(f"Error saving stats: {e}")

def get_user_id():
    """Get or create a user ID for this session."""
    if 'user_id' not in session:
        session['user_id'] = os.urandom(16).hex()
    return session['user_id']

# Load stats on startup
STATS = load_stats()

def generate_question(removed_words=None, round_words=None):
    """Generate a multiple choice question (word → definition).

    Args:
        removed_words: List of words to exclude from questions (permanently removed)
        round_words: List of words already used in current round (temporary exclusion)
    """
    if removed_words is None:
        removed_words = []
    if round_words is None:
        round_words = []

    # Combine excluded words (removed + already used in round)
    excluded_words = set(removed_words) | set(round_words)

    # Filter out excluded words
    available_words = [w for w in WORD_LIST if w not in excluded_words]

    # If too few words remaining, use full list (minus permanently removed)
    if len(available_words) < 4:
        available_words = [w for w in WORD_LIST if w not in removed_words]

    # Pick a random word
    correct_word = random.choice(available_words)
    correct_definition = WORDS[correct_word]

    # Pick 3 other random definitions (also excluding removed words when possible)
    other_candidates = [w for w in available_words if w != correct_word]
    if len(other_candidates) < 3:
        other_candidates = [w for w in WORD_LIST if w not in removed_words and w != correct_word]

    other_words = random.sample(other_candidates, 3)
    other_definitions = [WORDS[w] for w in other_words]

    # Combine and shuffle
    all_choices = [correct_definition] + other_definitions
    random.shuffle(all_choices)

    # Find the correct answer index
    correct_index = all_choices.index(correct_definition)

    return {
        'word': correct_word,
        'choices': all_choices,
        'correct_index': correct_index,
        'correct_definition': correct_definition
    }

def generate_inverse_question(removed_words=None, round_words=None):
    """Generate an inverse multiple choice question (definition → word).

    Args:
        removed_words: List of words to exclude from questions (permanently removed)
        round_words: List of words already used in current round (temporary exclusion)
    """
    if removed_words is None:
        removed_words = []
    if round_words is None:
        round_words = []

    # Combine excluded words (removed + already used in round)
    excluded_words = set(removed_words) | set(round_words)

    # Filter out excluded words
    available_words = [w for w in WORD_LIST if w not in excluded_words]

    # If too few words remaining, use full list (minus permanently removed)
    if len(available_words) < 4:
        available_words = [w for w in WORD_LIST if w not in removed_words]

    # Pick a random word
    correct_word = random.choice(available_words)
    correct_definition = WORDS[correct_word]

    # Pick 3 other random words (also excluding removed words when possible)
    other_candidates = [w for w in available_words if w != correct_word]
    if len(other_candidates) < 3:
        other_candidates = [w for w in WORD_LIST if w not in removed_words and w != correct_word]

    other_words = random.sample(other_candidates, 3)

    # Combine and shuffle (words instead of definitions)
    all_choices = [correct_word] + other_words
    random.shuffle(all_choices)

    # Find the correct answer index
    correct_index = all_choices.index(correct_word)

    return {
        'definition': correct_definition,
        'choices': all_choices,
        'correct_index': correct_index,
        'correct_word': correct_word
    }

@app.route('/')
def home():
    """Home page with menu."""
    # Calculate stats for display
    score = STATS['overall']['score']
    total = STATS['overall']['total']
    accuracy = round((score / total * 100)) if total > 0 else 0
    rounds_played = len(STATS['round_history'])

    return render_template('home.html',
                         stats=STATS['overall'],
                         accuracy=accuracy,
                         rounds_played=rounds_played)

@app.route('/gre-quiz')
def gre_quiz():
    """GRE vocabulary quiz page."""
    # Initialize session if needed
    if 'score' not in session:
        session['score'] = STATS['overall']['score']
        session['total'] = STATS['overall']['total']
    if 'round_score' not in session:
        session['round_score'] = 0
        session['round_total'] = 0
        session['round_active'] = False
        session['round_start_time'] = None

    return render_template('quiz.html')

@app.route('/get_question', methods=['GET', 'POST'])
def get_question():
    """API endpoint to get a new question."""
    # Get removed words and round words from request if provided
    removed_words = []
    round_words = []
    if request.method == 'POST':
        data = request.json or {}
        removed_words = data.get('removed_words', [])
        round_words = data.get('round_words', [])

    question = generate_question(removed_words, round_words)
    # Don't send the correct answer to the client
    return jsonify({
        'word': question['word'],
        'choices': question['choices']
    })

@app.route('/check_answer', methods=['POST'])
def check_answer():
    """Check if the answer is correct."""
    data = request.json
    word = data.get('word')
    selected_choice = data.get('choice')

    correct_definition = WORDS.get(word)
    is_correct = selected_choice == correct_definition

    # Initialize session if needed
    if 'score' not in session:
        session['score'] = STATS['overall']['score']
    if 'total' not in session:
        session['total'] = STATS['overall']['total']

    # Update session stats
    session['total'] = session.get('total', 0) + 1
    if is_correct:
        session['score'] = session.get('score', 0) + 1

    # Update persistent stats
    STATS['overall']['total'] = session['total']
    STATS['overall']['score'] = session['score']
    save_stats(STATS)

    # Update round stats if round is active
    if session.get('round_active', False):
        session['round_total'] = session.get('round_total', 0) + 1
        if is_correct:
            session['round_score'] = session.get('round_score', 0) + 1

    return jsonify({
        'correct': is_correct,
        'correct_definition': correct_definition,
        'score': session['score'],
        'total': session['total'],
        'round_score': session.get('round_score', 0),
        'round_total': session.get('round_total', 0),
        'round_complete': session.get('round_active', False) and
                         session.get('round_total', 0) >= session.get('round_size', 20)
    })

@app.route('/reset_stats')
def reset_stats():
    """Reset score statistics."""
    session['score'] = 0
    session['total'] = 0

    # Reset persistent stats
    STATS['overall']['score'] = 0
    STATS['overall']['total'] = 0
    save_stats(STATS)

    return jsonify({'status': 'ok'})

@app.route('/stats')
def get_stats():
    """Get current statistics."""
    return jsonify({
        'score': session.get('score', 0),
        'total': session.get('total', 0)
    })

@app.route('/round/start', methods=['POST'])
def start_round():
    """Start a new round."""
    data = request.json or {}
    round_size = data.get('round_size', 20)

    session['round_active'] = True
    session['round_score'] = 0
    session['round_total'] = 0
    session['round_size'] = round_size
    session['round_start_time'] = None  # Will be set on first question

    return jsonify({'status': 'ok', 'round_size': round_size})

@app.route('/round/status')
def round_status():
    """Get current round status."""
    return jsonify({
        'active': session.get('round_active', False),
        'score': session.get('round_score', 0),
        'total': session.get('round_total', 0),
        'size': session.get('round_size', 20),
        'start_time': session.get('round_start_time')
    })

@app.route('/round/complete', methods=['POST'])
def complete_round():
    """Mark round as complete."""
    data = request.json or {}
    save_to_history = data.get('save_to_history', False)

    # Save to history if requested
    if save_to_history and session.get('round_active', False):
        round_data = {
            'score': session.get('round_score', 0),
            'total': session.get('round_total', 0),
            'time': data.get('time', 0),
            'date': datetime.now().isoformat()
        }
        STATS['round_history'].append(round_data)
        save_stats(STATS)

    session['round_active'] = False

    return jsonify({
        'status': 'ok',
        'score': session.get('round_score', 0),
        'total': session.get('round_total', 0)
    })

@app.route('/round/history')
def get_round_history():
    """Get round history."""
    return jsonify({
        'history': STATS['round_history']
    })

# Inverse GRE quiz routes (definition → word)
@app.route('/inverse-gre-quiz')
def inverse_gre_quiz():
    """Inverse GRE vocabulary quiz page (definition → word)."""
    # Initialize session if needed
    if 'score' not in session:
        session['score'] = STATS['overall']['score']
        session['total'] = STATS['overall']['total']
    if 'round_score' not in session:
        session['round_score'] = 0
        session['round_total'] = 0
        session['round_active'] = False
        session['round_start_time'] = None

    return render_template('inverse_quiz.html')

@app.route('/word-review')
def word_review():
    """GRE Word Review page - shows word, definition blurred until revealed."""
    return render_template('word_review.html')

@app.route('/definition-review')
def definition_review():
    """GRE Definition Review page - shows definition, word blurred until revealed."""
    return render_template('definition_review.html')

@app.route('/spelling-quiz')
def spelling_quiz():
    """GRE Spelling Quiz page - type the word letter by letter from definition."""
    # Initialize session if needed
    if 'score' not in session:
        session['score'] = STATS['overall']['score']
        session['total'] = STATS['overall']['total']
    if 'round_score' not in session:
        session['round_score'] = 0
        session['round_total'] = 0
        session['round_active'] = False
        session['round_start_time'] = None
    return render_template('spelling_quiz.html')

@app.route('/review/get_word', methods=['GET'])
def get_review_word():
    """API endpoint to get a random word with its definition for review modes."""
    # Pick a random word
    word = random.choice(WORD_LIST)
    definition = WORDS[word]

    return jsonify({
        'word': word,
        'definition': definition
    })

@app.route('/inverse/get_question', methods=['GET', 'POST'])
def get_inverse_question():
    """API endpoint to get a new inverse question."""
    # Get removed words and round words from request if provided
    removed_words = []
    round_words = []
    if request.method == 'POST':
        data = request.json or {}
        removed_words = data.get('removed_words', [])
        round_words = data.get('round_words', [])

    question = generate_inverse_question(removed_words, round_words)
    # Don't send the correct answer to the client
    return jsonify({
        'definition': question['definition'],
        'choices': question['choices']
    })

@app.route('/inverse/check_answer', methods=['POST'])
def check_inverse_answer():
    """Check if the inverse answer is correct."""
    data = request.json
    definition = data.get('definition')
    selected_choice = data.get('choice')

    # Find the word with this definition
    correct_word = None
    for word, defn in WORDS.items():
        if defn == definition:
            correct_word = word
            break

    is_correct = selected_choice == correct_word

    # Initialize session if needed
    if 'score' not in session:
        session['score'] = STATS['overall']['score']
    if 'total' not in session:
        session['total'] = STATS['overall']['total']

    # Update session stats
    session['total'] = session.get('total', 0) + 1
    if is_correct:
        session['score'] = session.get('score', 0) + 1

    # Update persistent stats
    STATS['overall']['total'] = session['total']
    STATS['overall']['score'] = session['score']
    save_stats(STATS)

    # Update round stats if round is active
    if session.get('round_active', False):
        session['round_total'] = session.get('round_total', 0) + 1
        if is_correct:
            session['round_score'] = session.get('round_score', 0) + 1

    return jsonify({
        'correct': is_correct,
        'correct_word': correct_word,
        'score': session['score'],
        'total': session['total'],
        'round_score': session.get('round_score', 0),
        'round_total': session.get('round_total', 0),
        'round_complete': session.get('round_active', False) and
                         session.get('round_total', 0) >= session.get('round_size', 20)
    })

# Trivia quiz routes
@app.route('/trivia-quiz')
def trivia_quiz():
    """Trivia quiz page."""
    # Get list of available categories
    categories = list(TRIVIA_CATEGORIES.keys())
    return render_template('trivia.html', categories=categories)

@app.route('/trivia/categories')
def get_trivia_categories():
    """Get list of trivia categories."""
    categories = [{
        'name': name,
        'count': len(questions)
    } for name, questions in TRIVIA_CATEGORIES.items()]
    return jsonify({'categories': categories})

@app.route('/trivia/question', methods=['POST'])
def get_trivia_question():
    """Get a random trivia question from specified category."""
    data = request.json or {}
    category = data.get('category')

    if not category or category not in TRIVIA_CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400

    questions = TRIVIA_CATEGORIES[category]
    if not questions:
        return jsonify({'error': 'No questions available'}), 404

    # Get random question
    question_data = random.choice(questions)

    # Shuffle choices
    choices = question_data['choices'].copy()
    random.shuffle(choices)

    return jsonify({
        'question': question_data['question'],
        'choices': choices
    })

@app.route('/trivia/check', methods=['POST'])
def check_trivia_answer():
    """Check if the trivia answer is correct."""
    data = request.json
    category = data.get('category')
    question_text = data.get('question')
    selected_choice = data.get('choice')

    if not category or category not in TRIVIA_CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400

    # Find the question
    questions = TRIVIA_CATEGORIES[category]
    question_data = None
    for q in questions:
        if q['question'] == question_text:
            question_data = q
            break

    if not question_data:
        return jsonify({'error': 'Question not found'}), 404

    is_correct = selected_choice == question_data['correct']

    return jsonify({
        'correct': is_correct,
        'correct_answer': question_data['correct']
    })

# Dictionary browser routes
@app.route('/dictionary')
def dictionary():
    """Dictionary browser page."""
    return render_template('dictionary.html', total_words=len(WORDS))

@app.route('/dictionary/all')
def get_all_words():
    """Get all words in the dictionary."""
    words_list = [{'word': word, 'definition': defn} for word, defn in WORDS.items()]
    # Sort alphabetically
    words_list.sort(key=lambda x: x['word'].lower())
    return jsonify({'words': words_list, 'total': len(words_list)})

@app.route('/dictionary/search', methods=['POST'])
def search_dictionary():
    """Search the dictionary with fuzzy matching.

    Searches both word names and definitions.
    Returns results ranked by relevance.
    """
    data = request.json or {}
    query = data.get('query', '').strip().lower()

    if not query:
        # Return all words if no query
        words_list = [{'word': word, 'definition': defn} for word, defn in WORDS.items()]
        words_list.sort(key=lambda x: x['word'].lower())
        return jsonify({'words': words_list, 'total': len(words_list)})

    results = []

    for word, definition in WORDS.items():
        word_lower = word.lower()
        definition_lower = definition.lower()
        score = 0

        # Exact word match (highest priority)
        if word_lower == query:
            score = 1000
        # Word starts with query
        elif word_lower.startswith(query):
            score = 500
        # Word contains query
        elif query in word_lower:
            score = 250
        # Definition contains query (meaning-based search)
        elif query in definition_lower:
            score = 100
            # Boost if query appears at start of definition
            if definition_lower.startswith(query):
                score = 150
        else:
            # Fuzzy matching - check if most characters match
            matching_chars = sum(1 for c in query if c in word_lower)
            if matching_chars >= len(query) * 0.7:  # 70% of characters match
                score = matching_chars * 10

        if score > 0:
            results.append({
                'word': word,
                'definition': definition,
                'score': score
            })

    # Sort by score (descending) then alphabetically
    results.sort(key=lambda x: (-x['score'], x['word'].lower()))

    # Remove score from results before sending
    for result in results:
        del result['score']

    return jsonify({'words': results, 'total': len(results), 'query': query})

if __name__ == '__main__':
    print("Starting Wordy Quiz Application...")
    print(f"Loaded {len(WORDS)} GRE vocabulary words")
    print(f"Loaded {len(TRIVIA_CATEGORIES)} trivia categories with {sum(len(q) for q in TRIVIA_CATEGORIES.values())} questions")
    print("Open your browser to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
