import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- check_guess ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# FIX verification: original code inverted the hints — these tests confirm the
# fix. guess=1 against secret=100 must be "Too Low" (not "Too High").
def test_hints_not_inverted_low():
    assert check_guess(1, 100) == "Too Low"

def test_hints_not_inverted_high():
    assert check_guess(100, 1) == "Too High"

# FIX verification: secret was coerced to str on even attempts, causing
# lexicographic comparison. "9" > "50" is True lexicographically but 9 < 50
# numerically. This test catches that regression.
def test_no_string_coercion():
    # 9 < 50 numerically, so result must be "Too Low"
    assert check_guess(9, 50) == "Too Low"
    # 51 > 50, so "Too High"
    assert check_guess(51, 50) == "Too High"

# --- parse_guess ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err.lower()

# Edge cases
def test_parse_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_parse_very_large_number():
    ok, value, err = parse_guess("999999")
    assert ok is True
    assert value == 999999

# --- update_score ---

def test_win_on_first_attempt():
    # attempt_number=1 → points = 100 - 10*(1+1) = 80
    score = update_score(0, "Win", 1)
    assert score == 80

def test_win_score_floored_at_10():
    # attempt_number=9 → 100 - 100 = 0 → clamped to 10
    score = update_score(0, "Win", 9)
    assert score == 10

def test_wrong_guess_deducts_score():
    score = update_score(50, "Too High", 1)
    assert score == 45
    score = update_score(50, "Too Low", 2)
    assert score == 45

# FIX verification: original code gave +5 points for "Too High" on even
# attempts. Wrong guesses should never award points.
def test_no_points_for_wrong_guess_on_even_attempt():
    score = update_score(50, "Too High", 2)
    assert score == 45  # must deduct, not add

# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

# FIX verification: Hard was 1-50 (easier than Normal). Must be harder.
def test_hard_range_is_harder_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high
