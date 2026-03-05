# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The game loaded fine and I could type a number and click submit, so at first it seemed okay. But it was basically unwinnable.

**Bug 1 — Inverted hints:** I expected that if my guess was too high, the game would tell me to go lower. Instead it said "Go HIGHER!" every time I guessed above the secret. I guessed 80 when the secret was around 30, and it kept pushing me higher. I thought I was misreading it at first, but after a few rounds it was clear the hints were just completely backwards — too high said go higher, too low said go lower.

**Bug 2 — Secret number changing mid-game:** I expected the secret to stay the same for the whole game. But every time I submitted a guess, the secret in the debug panel was different. Turned out the code was converting the secret to a string on every even attempt, so the comparison was happening alphabetically instead of numerically. "9" > "50" is true alphabetically because "9" > "5", which made the hints wrong on every other turn.

**Bug 3 — Hard mode was easier than Normal:** I expected Hard to be harder than Normal — bigger range, harder to guess. Instead Hard had a range of 1–50 while Normal was 1–100, so switching to Hard actually made the game easier. That was clearly just a wrong value in the original code.

---

## 2. How did you use AI as a teammate?

I used AI to help me trace through the bugs once I had a rough idea of where things were going wrong.

For the string coercion bug, I described the symptom — hints being correct on odd attempts but wrong on even ones — and the AI pointed me straight to the lines where the secret was getting cast to a string. It explained why that breaks numeric comparison, which confirmed what I suspected. That suggestion was spot on and saved me from digging through all the session state logic manually.

Where the AI wasn't helpful was when I asked whether the Hard difficulty range was intentional. It suggested that 1–50 could be a "trick" hard mode where a smaller range is deceptively simple. That suggestion was misleading — the game description clearly states that Hard should make guessing harder, not easier. I verified by checking the sidebar: after setting Hard to 1–200 the range displayed correctly, and the pytest test `test_hard_range_is_harder_than_normal` confirmed the returned range was wider than Normal's. The AI was rationalizing the bug rather than flagging it as one.

---

## 3. Debugging and testing your fixes

After fixing the inverted hints, I wrote two tests specifically to catch that — one checking that a guess of 1 against a secret of 100 returns "Too Low", and one checking that 100 against 1 returns "Too High". Before the fix those would've returned the opposite. Running pytest confirmed they passed after the fix.

For the string coercion issue, I wrote a test using `check_guess(9, 50)` — because 9 < 50 numerically but "9" > "5" alphabetically. That specific case would have returned "Too High" in the broken code. After moving the logic into `logic_utils.py` with proper integer comparison, it correctly returned "Too Low".

I also just played the game a bunch after each fix to make sure it felt right. The hints now actually lead you to the answer, the score goes down when you guess wrong, and switching to Hard gives you a much bigger range to work with.

---

## 4. What did you learn about Streamlit and state?

The secret number changing every turn threw me off at first. I didn't realize Streamlit reruns the entire script from scratch every time you interact with anything — click a button, type in a box, doesn't matter. So any variable you define at the top of the file just gets reset on every interaction.

`st.session_state` is what keeps values alive across those reruns. The fix was wrapping the secret assignment in an `if "secret" not in st.session_state:` check so it only generates a new number the very first time, and leaves it alone after that. Same thing for attempts, score, and history. Once I understood that reruns were the root cause, everything else made more sense.

---

## 5. Looking ahead: your developer habits

The most useful thing I did was write the tests before fully fixing the bugs — or at least right after confirming the broken behavior. Having a failing test that described exactly what was wrong made it easy to know when the fix actually worked, and it caught a couple of cases where I thought I'd fixed something but hadn't quite.

I'd also be more careful about accepting AI suggestions on logic-heavy code. For straightforward stuff like "find where this variable is assigned," it's great. But when I asked it to evaluate whether a design decision was intentional, it just kind of rationalized the broken behavior instead of questioning it. Going forward I'd ask it to explain code rather than judge whether it's correct — that seems to be where it's actually reliable.
