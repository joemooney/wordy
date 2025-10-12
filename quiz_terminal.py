#!/usr/bin/env python3
"""
Terminal-based GRE vocabulary quiz.
"""

import random
import os

class GREQuiz:
    def __init__(self, filename='manhattan_prep_gre_words_formatted.txt'):
        """Initialize quiz with words from file."""
        self.words = self.load_words(filename)
        self.word_list = list(self.words.keys())
        self.score = 0
        self.total = 0

    def load_words(self, filename):
        """Load words and definitions from file."""
        words_dict = {}
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '|' in line:
                    word, definition = line.split('|', 1)
                    words_dict[word] = definition
        return words_dict

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def generate_question(self):
        """Generate a multiple choice question."""
        # Pick a random word
        correct_word = random.choice(self.word_list)
        correct_definition = self.words[correct_word]

        # Pick 3 other random definitions
        other_words = random.sample([w for w in self.word_list if w != correct_word], 3)
        other_definitions = [self.words[w] for w in other_words]

        # Combine and shuffle
        all_choices = [correct_definition] + other_definitions
        random.shuffle(all_choices)

        # Find the correct answer index
        correct_index = all_choices.index(correct_definition) + 1  # 1-based for display

        return {
            'word': correct_word,
            'choices': all_choices,
            'correct_index': correct_index,
            'correct_definition': correct_definition
        }

    def display_question(self, question):
        """Display a question with choices."""
        print("\n" + "="*80)
        print(f"\n  📚 Word: {question['word'].upper()}")
        print("\n" + "="*80)
        print("\nWhat is the definition?\n")

        for i, choice in enumerate(question['choices'], 1):
            # Word wrap for long definitions
            print(f"{i}. {choice}")
            print()

    def get_user_choice(self):
        """Get user's choice with validation."""
        while True:
            try:
                choice = input("Enter your choice (1-4) or 'q' to quit: ").strip().lower()

                if choice == 'q':
                    return None

                choice = int(choice)
                if 1 <= choice <= 4:
                    return choice
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number or 'q' to quit.")

    def display_stats(self):
        """Display current statistics."""
        accuracy = (self.score / self.total * 100) if self.total > 0 else 0
        print("\n" + "-"*80)
        print(f"  Score: {self.score}/{self.total} ({accuracy:.1f}%)")
        print("-"*80)

    def run(self):
        """Run the quiz."""
        self.clear_screen()
        print("="*80)
        print(" "*25 + "GRE VOCABULARY QUIZ")
        print("="*80)
        print(f"\n  Loaded {len(self.words)} words from Manhattan Prep GRE list")
        print("\n  Instructions:")
        print("  - You will be shown a word and 4 possible definitions")
        print("  - Select the correct definition by entering 1, 2, 3, or 4")
        print("  - Enter 'q' at any time to quit")
        print("\n" + "="*80)
        input("\nPress Enter to start...")

        try:
            while True:
                self.clear_screen()

                # Generate and display question
                question = self.generate_question()
                self.display_question(question)

                # Get user's answer
                user_choice = self.get_user_choice()

                if user_choice is None:
                    # User wants to quit
                    break

                # Check answer
                self.total += 1
                if user_choice == question['correct_index']:
                    self.score += 1
                    print("\n✓ Correct! Well done!")
                else:
                    print(f"\n✗ Incorrect.")
                    print(f"\nThe correct answer was:")
                    print(f"{question['correct_index']}. {question['correct_definition']}")

                # Display stats
                self.display_stats()

                # Continue prompt
                cont = input("\nPress Enter for next question (or 'q' to quit): ").strip().lower()
                if cont == 'q':
                    break

        except KeyboardInterrupt:
            print("\n\nQuiz interrupted.")

        # Final results
        self.clear_screen()
        print("="*80)
        print(" "*30 + "FINAL RESULTS")
        print("="*80)
        print(f"\n  Total Questions: {self.total}")
        print(f"  Correct Answers: {self.score}")
        print(f"  Incorrect Answers: {self.total - self.score}")

        if self.total > 0:
            accuracy = (self.score / self.total * 100)
            print(f"  Accuracy: {accuracy:.1f}%")

            # Performance feedback
            print("\n  Performance:")
            if accuracy >= 90:
                print("  🌟 Outstanding! You have excellent GRE vocabulary knowledge!")
            elif accuracy >= 75:
                print("  ⭐ Great job! You're well-prepared!")
            elif accuracy >= 60:
                print("  👍 Good effort! Keep practicing!")
            else:
                print("  📖 Keep studying! Practice makes perfect!")

        print("\n" + "="*80)
        print("\nThank you for practicing!\n")


if __name__ == '__main__':
    quiz = GREQuiz()
    quiz.run()
