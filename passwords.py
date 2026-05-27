# ============================================================
# CSE 111 - W02 Project: Password Strength Checker
# Author  : Anselm Munango
# Date    : 2026-05-15
#
# ENHANCEMENT (Exceeds Requirements):
#   1. Visual ASCII strength meter — after every check, a
#      colour-coded bar (via ANSI escape codes) renders the
#      strength score (0-5) directly in the terminal so
#      employees receive instant visual feedback.
#   2. Actionable improvement hints — when a password scores
#      below 5, the program lists the specific character
#      categories that are still missing (uppercase, lowercase,
#      digits, special symbols) so the user knows exactly what
#      to add to raise their score.
# ============================================================

import string
import os

# ------------------------------------------------------------------
# Character-type constant lists (provided by architect Sven Larson)
# ------------------------------------------------------------------
LOWER   = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
           "n","o","p","q","r","s","t","u","v","w","x","y","z"]
UPPER   = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
           "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
DIGITS  = ["0","1","2","3","4","5","6","7","8","9"]
SPECIAL = ["!","@","#","$","%","^","&","*","(",")","-","_","=",
           "+","[","]","{","}","|",";",":","'","\"",",",".",
           "<",">","?","/","\\","`","~"]

# File paths — resolved relative to the directory containing this script's location, so the
# program works regardless of the terminal's working directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_FILE = os.path.join(BASE_DIR, "wordlist.txt")
TOP_PASS_FILE = os.path.join(BASE_DIR, "toppasswords.txt")

# ANSI colour helpers for the visual strength meter (enhancement)
_ANSI = {
    "reset":  "\033[0m",
    "red":    "\033[91m",
    "yellow": "\033[93m",
    "green":  "\033[92m",
    "bold":   "\033[1m",
}


# ==================================================================
# Core utility functions
# ==================================================================

def word_in_file(word, filename, case_sensitive=False):
    """Return True if *word* is found in *filename* (one word per line).

    Parameters
    ----------
    word           : str  – the word to search for.
    filename       : str  – path to the word-list file.
    case_sensitive : bool – when False (default) comparison is
                            case-insensitive; when True it is exact.

    Returns
    -------
    bool – True if a match is found, False otherwise.
    """
    search_word = word if case_sensitive else word.lower()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                file_word = line.strip()
                compare_word = file_word if case_sensitive else file_word.lower()
                if search_word == compare_word:
                    return True
    except FileNotFoundError:
        print(f"  Warning: word-list file '{filename}' was not found.")
    return False


def word_has_character(word, character_list):
    """Return True if any character in *word* appears in *character_list*.

    Parameters
    ----------
    word           : str  – the string to inspect.
    character_list : list – list of characters to check against.

    Returns
    -------
    bool – True if at least one matching character is found.
    """
    for char in word:
        if char in character_list:
            return True
    return False


def word_complexity(word):
    """Calculate a complexity score (0–4) for *word*.

    One point is awarded for each of the four character categories
    (lowercase, uppercase, digits, special symbols) present in the word.

    Parameters
    ----------
    word : str – the password candidate to evaluate.

    Returns
    -------
    int – complexity score in the range [0, 4].
    """
    complexity = 0
    if word_has_character(word, LOWER):
        complexity += 1
    if word_has_character(word, UPPER):
        complexity += 1
    if word_has_character(word, DIGITS):
        complexity += 1
    if word_has_character(word, SPECIAL):
        complexity += 1
    return complexity


# ==================================================================
# Primary strength-evaluation function
# ==================================================================

def password_strength(password, min_length=10, strong_length=16):
    """Evaluate and return the strength of *password* on a 0–5 scale.

    Evaluation order (first matching rule wins):
      1. Dictionary word  → strength 0
      2. Known/top password → strength 0
      3. Too short (< min_length) → strength 1
      4. Long (>= strong_length) → strength 5
      5. Otherwise → strength = 1 + complexity score (1–5)

    Parameters
    ----------
    password      : str – the password to evaluate.
    min_length    : int – minimum acceptable length  (default 10).
    strong_length : int – length at which length alone is sufficient
                          (default 16).

    Returns
    -------
    int – strength score in the range [0, 5].
    """
    # Rule 1 – dictionary word (case-insensitive)
    if word_in_file(password, DICT_FILE, case_sensitive=False):
        print("  Password is a dictionary word and is not secure.")
        return 0

    # Rule 2 – known/top password (case-sensitive)
    if word_in_file(password, TOP_PASS_FILE, case_sensitive=True):
        print("  Password is a commonly used password and is not secure.")
        return 0

    # Rule 3 – too short
    if len(password) < min_length:
        print("  Password is too short and is not secure.")
        return 1

    # Rule 4 – length alone makes it strong
    if len(password) >= strong_length:
        print("  Password is long, length trumps complexity this is a good password.")
        return 5

    # Rule 5 – complexity-based score
    complexity = word_complexity(password)
    strength = 1 + complexity
    return strength


# ==================================================================
# ENHANCEMENT helpers
# ==================================================================

def _strength_label(score):
    """Return a human-readable label for a numeric strength score."""
    labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Moderate",
        4: "Strong",
        5: "Very Strong",
    }
    return labels.get(score, "Unknown")


def _strength_colour(score):
    """Return an ANSI colour code appropriate for the given score."""
    if score <= 1:
        return _ANSI["red"]
    if score <= 3:
        return _ANSI["yellow"]
    return _ANSI["green"]


def display_strength_meter(score):
    """Print a visual ASCII strength bar to the terminal.

    Example output (score = 3):
        Strength: [████████░░]  Moderate (3/5)

    This is an ENHANCEMENT beyond base requirements.
    """
    filled   = score
    empty    = 5 - score
    bar      = "█" * filled + "░" * empty
    colour   = _strength_colour(score)
    label    = _strength_label(score)
    print(f"\n  {_ANSI['bold']}Strength:{_ANSI['reset']} "
          f"{colour}[{bar}]{_ANSI['reset']}  "
          f"{colour}{label} ({score}/5){_ANSI['reset']}")


def display_improvement_hints(password, score):
    """Print actionable hints when the password scores below 5.

    This is an ENHANCEMENT beyond base requirements.
    """
    if score >= 5:
        return  # No hints needed for maximum strength

    hints = []
    if not word_has_character(password, LOWER):
        hints.append("• Add lowercase letters  (a–z)")
    if not word_has_character(password, UPPER):
        hints.append("• Add uppercase letters  (A–Z)")
    if not word_has_character(password, DIGITS):
        hints.append("• Add numeric digits     (0–9)")
    if not word_has_character(password, SPECIAL):
        hints.append("• Add special symbols    (!@#$%…)")
    if len(password) < 16:
        remaining = 16 - len(password)
        hints.append(f"• Add {remaining} more character(s) to reach the 'very strong' length threshold")

    if hints:
        print(f"\n  {_ANSI['bold']}Suggestions to improve your password:{_ANSI['reset']}")
        for hint in hints:
            print(f"    {hint}")


# ==================================================================
# Entry-point / user interaction loop
# ==================================================================

def main():
    """Run the interactive password strength checker.

    Continuously prompts the user to enter a password for evaluation.
    Entering 'q' or 'Q' terminates the program.
    """
    print("=" * 52)
    print("       Password Strength Checker")
    print("  Enter 'q' or 'Q' at any time to quit.")
    print("=" * 52)

    while True:
        password = input("\nEnter a password to check: ")

        if password in ("q", "Q"):
            print("\nThank you for using the Password Strength Checker. Goodbye!")
            break

        print()  # visual spacing before results
        score = password_strength(password)

        # --- ENHANCEMENT: visual meter + improvement hints ---
        display_strength_meter(score)
        display_improvement_hints(password, score)
        print()  # visual spacing after results


if __name__ == "__main__":
    main()
