def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Hard was returning 1-50 which is *easier* than Normal (1-100).
    # Hard should have a larger range to make guessing harder.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    Returns: "Win", "Too High", or "Too Low"
    """
    # FIX: Removed the string-coercion path that was in app.py. Always compare
    # as integers so "9 vs 50" is numeric, not lexicographic ("9" > "5" = True).
    if guess == secret:
        return "Win"

    # FIX: Original hints were inverted — guess > secret means the guess is too
    # high, so the player should go LOWER, not higher.
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Original code gave +5 points on even attempts for a wrong "Too High"
    # guess, rewarding incorrect answers. Wrong guesses always deduct 5.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
