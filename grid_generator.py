#!/usr/bin/env python3
"""
Background task for pre-generating and validating Letter Grid games.

This script:
1. Generates new word grids
2. Validates all words via Wordnik API
3. Respects API quota limits (waits if exceeded)
4. Stores completed games for instant play

Run hourly via cron or systemd timer.
"""

import json
import time
import requests
import random
from pathlib import Path
from datetime import datetime
from collections import Counter

# File paths
WORDLIST_FILE = Path('wordlist_50000.txt')
DELETED_WORDS_FILE = Path('words_deleted.txt')
VALIDATION_CACHE_FILE = Path('wordnik_validation_cache.json')
QUOTA_FILE = Path('wordnik_quota.json')
PRE_GENERATED_GAMES_FILE = Path('pre_generated_games.json')
WORDNIK_API_KEY_FILE = Path('wordnik_api_key.txt')

# Configuration
MAX_WORDS_PER_GAME = 150
WORDNIK_API_BASE = 'https://api.wordnik.com/v4'

def log(message):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def load_wordnik_api_key():
    """Load Wordnik API key from file."""
    if not WORDNIK_API_KEY_FILE.exists():
        log("ERROR: wordnik_api_key.txt not found!")
        return None

    with open(WORDNIK_API_KEY_FILE, 'r') as f:
        return f.read().strip()

def load_grid_words():
    """Load valid words for grid generation."""
    if not WORDLIST_FILE.exists():
        log(f"ERROR: {WORDLIST_FILE} not found!")
        return []

    with open(WORDLIST_FILE, 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip()]

    # Filter: only 3+ letter words
    words = [w for w in words if len(w) >= 3]
    log(f"Loaded {len(words)} words for grid generation")
    return words

def load_deleted_words():
    """Load user-deleted words."""
    if not DELETED_WORDS_FILE.exists():
        return set()

    with open(DELETED_WORDS_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())

def load_validation_cache():
    """Load Wordnik validation cache."""
    if VALIDATION_CACHE_FILE.exists():
        try:
            with open(VALIDATION_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log(f"Error loading validation cache: {e}")
    return {}

def save_validation_cache(cache):
    """Save Wordnik validation cache."""
    try:
        with open(VALIDATION_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        log(f"Error saving validation cache: {e}")
        return False

def load_quota():
    """Load Wordnik API quota tracking."""
    if QUOTA_FILE.exists():
        try:
            with open(QUOTA_FILE, 'r', encoding='utf-8') as f:
                quota = json.load(f)
                # Clean up old calls (older than 1 hour)
                one_hour_ago = int(time.time() * 1000) - (60 * 60 * 1000)
                quota['callsThisHour'] = [t for t in quota.get('callsThisHour', []) if t > one_hour_ago]
                quota['remaining'] = quota['limit'] - len(quota['callsThisHour'])

                # Reset if past reset time
                if quota.get('resetTime') and time.time() * 1000 > quota['resetTime']:
                    quota['callsThisHour'] = []
                    quota['remaining'] = quota['limit']
                    quota['resetTime'] = None

                return quota
        except Exception as e:
            log(f"Error loading quota: {e}")

    return {'limit': 50, 'remaining': 50, 'resetTime': None, 'callsThisHour': []}

def save_quota(quota):
    """Save Wordnik API quota tracking."""
    try:
        with open(QUOTA_FILE, 'w', encoding='utf-8') as f:
            json.dump(quota, f, indent=2)
        return True
    except Exception as e:
        log(f"Error saving quota: {e}")
        return False

def has_valid_definitions(word, validation_cache):
    """Check if a word has actual definitions in the validation cache."""
    word_lower = word.lower()
    if word_lower not in validation_cache:
        return True  # Not validated yet, allow it

    word_data = validation_cache[word_lower]

    # Check if validated as invalid
    if not word_data.get('validated', False):
        return False

    # Check if definitions exist and have actual text
    definitions = word_data.get('definitions', [])
    if not definitions:
        return False

    # Check if at least one definition has a 'text' field with content
    for defn in definitions:
        if isinstance(defn, dict) and defn.get('text'):
            return True

    # No real definitions found
    return False

def find_words_from_letters(letters, grid_words, deleted_words, validation_cache):
    """Find all valid words that can be formed from the given letters."""
    letters_lower = [l.lower() for l in letters]
    letter_counts = Counter(letters_lower)
    valid_words = []

    for word in grid_words:
        # Skip deleted words
        if word in deleted_words:
            continue

        # Check if word can be formed from available letters
        word_counts = Counter(word)
        if all(word_counts[char] <= letter_counts[char] for char in word_counts):
            # Also check if word has valid definitions (if it's been validated)
            if has_valid_definitions(word, validation_cache):
                valid_words.append(word)

    return valid_words

def generate_letter_grid(grid_words, deleted_words, validation_cache, max_words=150, max_attempts=100):
    """Generate a 3x3 grid of letters from a random 9-letter word."""
    nine_letter_words = [w for w in grid_words if len(w) == 9]

    if not nine_letter_words:
        log("ERROR: No 9-letter words available!")
        return None, None, None

    log(f"Trying to find suitable grid from {len(nine_letter_words)} nine-letter words...")

    for attempt in range(max_attempts):
        # Pick a random 9-letter word
        base_word = random.choice(nine_letter_words)

        # Use the letters from this word for the grid
        letters = [letter.upper() for letter in base_word]

        # Shuffle the letters
        random.shuffle(letters)

        # Find all valid words from these letters
        valid_words = find_words_from_letters(letters, grid_words, deleted_words, validation_cache)

        # Check if this word meets our criteria
        if len(valid_words) <= max_words:
            log(f"Found suitable grid with {len(valid_words)} words (attempt {attempt + 1}/{max_attempts})")
            return letters, valid_words, base_word

    log(f"WARNING: Could not find grid with <= {max_words} words after {max_attempts} attempts")
    return letters, valid_words, base_word

def validate_word_with_wordnik(word, api_key, quota):
    """Validate a word with Wordnik API and return definitions and examples."""
    word_lower = word.lower()

    # Check quota
    if quota['remaining'] <= 0:
        log(f"Quota exhausted ({quota['remaining']}/{quota['limit']})")
        return None

    log(f"Validating '{word}' via Wordnik API...")

    try:
        # Fetch definitions
        def_url = f"{WORDNIK_API_BASE}/word.json/{word_lower}/definitions"
        def_params = {
            'api_key': api_key,
            'limit': 3,
            'includeRelated': 'false',
            'useCanonical': 'false',
            'includeTags': 'false'
        }
        def_response = requests.get(def_url, params=def_params, timeout=10)

        # Update quota
        quota['callsThisHour'].append(int(time.time() * 1000))
        quota['remaining'] -= 1
        if not quota['resetTime']:
            quota['resetTime'] = int(time.time() * 1000) + (60 * 60 * 1000)  # 1 hour from now
        save_quota(quota)

        definitions = []
        if def_response.status_code == 200:
            definitions = def_response.json() or []

        # Fetch examples
        ex_url = f"{WORDNIK_API_BASE}/word.json/{word_lower}/examples"
        ex_params = {
            'api_key': api_key,
            'limit': 3
        }
        ex_response = requests.get(ex_url, params=ex_params, timeout=10)

        # Update quota
        quota['callsThisHour'].append(int(time.time() * 1000))
        quota['remaining'] -= 1
        save_quota(quota)

        examples = []
        if ex_response.status_code == 200:
            ex_data = ex_response.json()
            examples = ex_data.get('examples', []) if ex_data else []

        # Create validation data
        validation_data = {
            'validated': True,
            'timestamp': datetime.now().isoformat(),
            'definitions': definitions,
            'examples': examples
        }

        has_valid_def = any(d.get('text') for d in definitions)
        log(f"  '{word}': {len(definitions)} definitions, {len(examples)} examples, valid={has_valid_def}")

        return validation_data

    except Exception as e:
        log(f"ERROR validating '{word}': {e}")
        return None

def load_pre_generated_games():
    """Load pre-generated games."""
    if PRE_GENERATED_GAMES_FILE.exists():
        try:
            with open(PRE_GENERATED_GAMES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log(f"Error loading pre-generated games: {e}")
    return {'games': [], 'played_games': []}

def save_pre_generated_games(games_data):
    """Save pre-generated games."""
    try:
        with open(PRE_GENERATED_GAMES_FILE, 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        log(f"Error saving pre-generated games: {e}")
        return False

def generate_and_validate_game():
    """Generate one complete validated game."""
    log("=" * 60)
    log("Starting new game generation...")

    # Load API key
    api_key = load_wordnik_api_key()
    if not api_key:
        return None

    # Load data
    grid_words = load_grid_words()
    if not grid_words:
        return None

    deleted_words = load_deleted_words()
    validation_cache = load_validation_cache()
    quota = load_quota()

    log(f"Quota status: {quota['remaining']}/{quota['limit']} remaining")

    # Generate grid
    letters, valid_words, base_word = generate_letter_grid(
        grid_words, deleted_words, validation_cache, MAX_WORDS_PER_GAME
    )

    if not letters or not valid_words:
        log("ERROR: Failed to generate grid")
        return None

    log(f"Generated grid from base word '{base_word}' with {len(valid_words)} words")
    log(f"Words to validate: {len([w for w in valid_words if not has_valid_definitions(w, validation_cache)])}")

    # Validate all words
    words_validated = 0
    words_skipped = 0
    quota_exhausted = False

    for word in valid_words:
        # Check if already validated with valid definitions
        if has_valid_definitions(word, validation_cache) and word.lower() in validation_cache:
            words_skipped += 1
            continue

        # Check quota
        if quota['remaining'] <= 0:
            log(f"Quota exhausted after validating {words_validated} words")
            quota_exhausted = True
            break

        # Validate word
        validation_data = validate_word_with_wordnik(word, api_key, quota)
        if validation_data:
            validation_cache[word.lower()] = validation_data
            save_validation_cache(validation_cache)
            words_validated += 1

            # Small delay to avoid rate limiting
            time.sleep(0.3)

    log(f"Validation complete: {words_validated} new, {words_skipped} cached")

    # Filter out words without valid definitions
    final_words = [w for w in valid_words if has_valid_definitions(w, validation_cache)]
    log(f"Final word count after filtering: {len(final_words)}")

    # If quota was exhausted, we can't complete this game yet
    if quota_exhausted:
        log("Game incomplete due to quota - will retry next hour")
        return None

    # Create game data
    game = {
        'id': f"game_{int(time.time())}",
        'letters': letters,
        'words': sorted(final_words, key=lambda x: (len(x), x)),
        'base_word': base_word,
        'total_words': len(final_words),
        'generated_at': datetime.now().isoformat(),
        'played': False
    }

    log(f"Game complete: {game['id']} with {len(final_words)} validated words")
    return game

def main():
    """Main function - generate one game per run."""
    log("Letter Grid Generator Started")

    # Load existing games
    games_data = load_pre_generated_games()

    # Count unplayed games
    unplayed = [g for g in games_data['games'] if not g.get('played', False)]
    log(f"Current status: {len(unplayed)} unplayed, {len(games_data['played_games'])} played")

    # Generate one new game
    game = generate_and_validate_game()

    if game:
        # Add to games list
        games_data['games'].append(game)
        save_pre_generated_games(games_data)
        log(f"SUCCESS: Added game {game['id']}")
        log(f"New status: {len(unplayed) + 1} unplayed games available")
    else:
        log("No game generated this run (quota exhausted or error)")

    log("Letter Grid Generator Finished")
    log("=" * 60)

if __name__ == '__main__':
    main()
