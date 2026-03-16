# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`
3. Run the test suite: `pytest tests/ -v`

## 🕵️‍♂️ Your Mission (completed)

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** Move the logic into `logic_utils.py`. Run `pytest` in your terminal. Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number-guessing game where the player tries to identify a secret number within a limited number of attempts. Difficulty controls the range and attempt limit. The score decreases with each wrong guess and rewards winning quickly.

**Bugs found:**
1. **Inverted hints** — the game told you to go higher when your guess was already too high, and lower when it was too low. Completely backwards.
2. **Secret number changing mid-game** — the debug panel showed a different secret after each guess. Turned out the code was converting the secret to a string on certain attempts, so comparisons were happening alphabetically instead of numerically.
3. **Hard mode was easier than Normal** — Hard had a range of 1–50, which is smaller than Normal's 1–100. Switching to Hard made the game easier.
4. **Score math was off** — wrong guesses were sometimes rewarding points instead of deducting them, depending on which attempt number it was.

**Fixes applied:**
- Moved core logic into `logic_utils.py` and fixed the implementations there.
- Fixed `check_guess` to compare integers correctly and return the right hint direction.
- Fixed Hard difficulty range to `1–200`.
- Fixed `update_score` to always deduct points for wrong guesses.

## 📸 Demo

_(Run the app locally with `python -m streamlit run app.py` — the game is now fully functional. All 20 pytest tests pass.)_

**Test results:**
```
============================= test session starts ==============================
collected 20 items

tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_hints_not_inverted_low PASSED
tests/test_game_logic.py::test_hints_not_inverted_high PASSED
tests/test_game_logic.py::test_no_string_coercion PASSED
tests/test_game_logic.py::test_parse_valid_integer PASSED
tests/test_game_logic.py::test_parse_float_truncates PASSED
tests/test_game_logic.py::test_parse_empty_string PASSED
tests/test_game_logic.py::test_parse_none PASSED
tests/test_game_logic.py::test_parse_non_numeric PASSED
tests/test_game_logic.py::test_parse_negative_number PASSED
tests/test_game_logic.py::test_parse_very_large_number PASSED
tests/test_game_logic.py::test_win_on_first_attempt PASSED
tests/test_game_logic.py::test_win_score_floored_at_10 PASSED
tests/test_game_logic.py::test_wrong_guess_deducts_score PASSED
tests/test_game_logic.py::test_no_points_for_wrong_guess_on_even_attempt PASSED
tests/test_game_logic.py::test_easy_range PASSED
tests/test_game_logic.py::test_normal_range PASSED
tests/test_game_logic.py::test_hard_range_is_harder_than_normal PASSED

============================== 20 passed in 0.03s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
