# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it appeared to work visually — the Streamlit UI loaded, difficulty settings showed up, and I could type a guess. However, several bugs made the game unplayable.

- **Bug 1 — Inverted hints:** The hint logic was completely backwards. When my guess was too high (e.g., 80 against a secret of 30), the game told me "📈 Go HIGHER!" instead of "Go LOWER!" This made it impossible to navigate toward the secret number. I expected a guess of 80 against secret 30 to say "Go Lower," but instead it encouraged me to guess even higher.

- **Bug 2 — Secret number corrupted on even attempts:** On every even-numbered attempt, `app.py` silently converted the integer secret to a string (`secret = str(st.session_state.secret)`) before passing it to `check_guess`. This caused Python to fall into the `TypeError` branch and compare numbers as strings using lexicographic order — so `"9" > "50"` evaluated to `True` because `"9" > "5"`. I expected the comparison to always be numeric; instead the behavior changed unpredictably every other turn.

- **Bug 3 — Hard difficulty was easier than Normal:** The `get_range_for_difficulty` function returned `1–50` for Hard and `1–100` for Normal, meaning Hard mode was actually *less* difficult. I expected Hard to widen the range and make guessing harder; instead switching to Hard gave me a smaller target range.

- **Bonus Bug — logic_utils.py was all stubs:** Every function in `logic_utils.py` raised `NotImplementedError`. The real implementations were duplicated inside `app.py`, so all existing tests failed immediately when imported from `logic_utils`.

---

## 2. How did you use AI as a teammate?

I used Claude (via Claude Code) as my AI pair programmer throughout this project.

**Correct suggestion — identifying the string coercion bug:**
When I described the symptom ("the game gives wrong hints on every second guess but right hints on odd-numbered guesses"), Claude immediately identified lines 158–161 in `app.py` where the secret was being cast to `str` on even attempts. It explained that string comparison is lexicographic, which is why `check_guess(9, "50")` returned "Too High" (because `"9" > "5"` alphabetically). I verified this by reading those lines directly in the code and confirming the if/else on `attempt_number % 2 == 0`. The fix — always passing the integer secret — made the behavior consistent across all attempts.

**Incorrect/misleading suggestion — Hard difficulty range:**
When I asked the AI what the Hard difficulty range *should* be, it initially suggested `1–50` might be intentional as a "trick hard mode" where the smaller range could be argued as deceptively easy. This framing was misleading — the README clearly says Hard should make the game harder, and a range half the size of Normal contradicts that. I rejected this reasoning, checked the README's intent ("make the hints harder"), and set Hard to `1–200` instead, which genuinely increases difficulty.

---

## 3. Debugging and testing your fixes

I verified each fix in two ways: automated pytest tests and manual play in the Streamlit app.

For the inverted hints bug, I wrote `test_hints_not_inverted_low` and `test_hints_not_inverted_high` in `test_game_logic.py`. These confirmed that `check_guess(1, 100)` returns `"Too Low"` and `check_guess(100, 1)` returns `"Too High"` — the opposite of what the original code produced. Before the fix, these tests failed; after moving the corrected logic into `logic_utils.py`, both passed.

For the string coercion bug, I added `test_no_string_coercion` which specifically checks that `check_guess(9, 50)` returns `"Too Low"` — a case where lexicographic comparison would have returned the wrong answer. Running `pytest` confirmed this test passes with the fixed integer comparison.

I also ran `python -m streamlit run app.py` and played several full games on Easy difficulty. I could now win by following the hints, the attempts counter correctly started at 0, and switching to Hard mode showed the wider 1–200 range in the sidebar. All 20 tests passed: `20 passed in 0.03s`.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number appeared to change because Streamlit **reruns the entire script from top to bottom** every time a button is clicked or any input changes. Without `st.session_state`, `random.randint(low, high)` would be called again on every rerun, generating a fresh secret each time.

Streamlit "reruns" are like refreshing a web page — the script re-executes completely, so any variable assigned at module level gets reset to its initial value. `st.session_state` is a dictionary that persists across these reruns, letting you store values that should survive a page refresh (like the secret number, attempt counter, and score).

The fix that gave the game a stable secret was the `if "secret" not in st.session_state:` guard — it only assigns a new random number the very first time the script runs, and leaves it alone on every subsequent rerun. This is the standard Streamlit pattern for any value that must persist across interactions.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is **writing regression tests immediately after finding a bug**, before writing the fix. Describing the exact broken behavior as a failing test (e.g., `assert check_guess(9, 50) == "Too Low"`) gave me a clear, runnable definition of "fixed." It also caught when I accidentally re-introduced a bug during refactoring.

Next time I work with AI on a coding task, I would give it smaller, more targeted prompts rather than asking it to fix everything at once. When I described multiple bugs together, the AI's responses were harder to evaluate. Isolating one bug per conversation kept the context focused and the suggestions easier to verify against the code.

This project changed how I think about AI-generated code: I used to assume AI code either works or has obvious errors. Now I see that AI bugs are often subtle logic inversions or type-coercion issues that *look* correct at a glance but break in specific conditions — exactly the kind of bug that requires a human to read carefully and test systematically, not just run once and assume it's fine.
