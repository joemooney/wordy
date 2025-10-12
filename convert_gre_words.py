#!/usr/bin/env python3
"""
Convert Manhattan Prep GRE words file to word|definition format.
"""

import re

def parse_gre_file(input_file, output_file):
    """Parse GRE words file and output in word|definition format."""

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    word_definitions = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Pattern 1: Just a number (entries 1-9)
        # Pattern 2: Number followed by word on same line (entries 10+)

        # Check for "number. word" pattern (entries 10+)
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match:
            number = match.group(1)
            word = match.group(2).strip()
            i += 1

            # Collect definition lines until next numbered entry
            definition_lines = []
            while i < len(lines):
                next_line = lines[i].strip()
                # Stop if we hit another numbered entry
                if re.match(r'^\d+\.', next_line):
                    break
                if next_line:  # Skip blank lines but collect content
                    definition_lines.append(next_line)
                i += 1

            definition = ' '.join(definition_lines)
            if word and definition:
                word_definitions.append((word, definition))
            continue

        # Check for "just number" pattern (entries 1-9)
        elif re.match(r'^\d+\.$', line):
            i += 1
            # Skip blank lines
            while i < len(lines) and not lines[i].strip():
                i += 1

            # Get the word
            if i < len(lines):
                word = lines[i].strip()
                i += 1

                # Skip blank lines
                while i < len(lines) and not lines[i].strip():
                    i += 1

                # Collect definition lines
                definition_lines = []
                while i < len(lines):
                    next_line = lines[i].strip()
                    # Stop if we hit another numbered entry
                    if re.match(r'^\d+\.', next_line):
                        break
                    if next_line:
                        definition_lines.append(next_line)
                    i += 1

                definition = ' '.join(definition_lines)
                if word and definition:
                    word_definitions.append((word, definition))
                continue

        i += 1

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, definition in word_definitions:
            f.write(f"{word}|{definition}\n")

    print(f"Converted {len(word_definitions)} entries")
    print(f"Output written to: {output_file}")

    # Show a few examples
    if word_definitions:
        print("\nFirst 5 entries:")
        for word, definition in word_definitions[:5]:
            print(f"  {word}: {definition[:60]}...")
        print("\nSample from middle:")
        mid = len(word_definitions) // 2
        for word, definition in word_definitions[mid:mid+3]:
            print(f"  {word}: {definition[:60]}...")

if __name__ == "__main__":
    input_file = "manhattan_prep_1000_gre_words_.txt"
    output_file = "manhattan_prep_gre_words_formatted.txt"

    parse_gre_file(input_file, output_file)
