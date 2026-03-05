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
1. **Inverted hints** — `check_guess` in `app.py` returned "Go HIGHER!" when the guess was too high and "Go LOWER!" when too low. The emoji and text both pointed the wrong direction.
2. **String coercion of secret on even attempts** — `app.py` converted the integer secret to a string on every even attempt (`secret = str(st.session_state.secret)`), causing lexicographic comparison. `"9" > "50"` is `True` alphabetically but `False` numerically, so hints were wrong every other turn.
3. **Hard difficulty easier than Normal** — `get_range_for_difficulty("Hard")` returned `(1, 50)` — a smaller range than Normal's `(1, 100)` — making Hard the easiest mode.
4. **Attempts counter started at 1** — `st.session_state.attempts` initialized to `1` instead of `0`, so the first guess was counted as attempt 2, incorrectly reducing the displayed remaining attempts and skewing scoring.
5. **Score rewarded wrong guesses on even attempts** — `update_score` gave `+5` points for "Too High" on even attempt numbers, rewarding incorrect answers.
6. **`logic_utils.py` was all stubs** — Every function raised `NotImplementedError`; all logic lived in `app.py` with no separation of concerns.
7. **New Game ignored difficulty range** — The New Game button always called `random.randint(1, 100)` regardless of the selected difficulty.
8. **Info box hardcoded range** — The hint text always said "Guess a number between 1 and 100" even on Easy (1–20) or Hard (1–200).

**Fixes applied:**
- Moved all game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) into `logic_utils.py` with correct implementations.
- Fixed `check_guess` to always compare integers and return the correct "Too High" / "Too Low" outcome.
- Fixed Hard difficulty range to `1–200`.
- Fixed attempts to start at `0`.
- Fixed `update_score` to always deduct points for wrong guesses regardless of attempt parity.
- Fixed New Game and info box to use the difficulty-based `low`/`high` range.

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
