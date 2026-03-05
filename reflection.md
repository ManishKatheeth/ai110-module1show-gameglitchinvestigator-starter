# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The game looked fine at first glance — the UI loaded, I could type a number and hit submit. But it was pretty much unwinnable. The hints were completely backwards. I guessed 80 when the secret was around 30, and it told me to go higher. I thought I was misreading it, so I guessed even higher and kept getting the same message. Eventually I opened the debug panel and realized the hints were just inverted — too high said go higher, too low said go lower.

The second thing I caught was that the secret number seemed to be changing. I'd open the debug info, note the secret, submit a guess, and the secret would be different on the next turn. Turned out the code was converting the secret to a string on every even attempt, so the comparison was happening alphabetically instead of numerically. Like "9" > "50" comes out true alphabetically because "9" > "5", which is obviously wrong.

The third one was the difficulty settings. I switched to Hard expecting it to be harder, but the range was 1–50, which is actually easier than Normal's 1–100. That was clearly a copy-paste mistake in the original code.

---

## 2. How did you use AI as a teammate?

I used AI to help me trace through the bugs once I had a rough idea of where things were going wrong.

For the string coercion bug, I described the symptom — hints being correct on odd attempts but wrong on even ones — and the AI pointed me straight to the lines where the secret was getting cast to a string. It explained why that breaks numeric comparison, which confirmed what I suspected. That suggestion was spot on and saved me from digging through all the session state logic manually.

Where the AI wasn't helpful was when I asked whether the Hard difficulty range was intentional. It tried to argue that maybe 1–50 was a "trick" hard mode where the smaller range is deceptively easy. That made no sense given how the game is described, so I ignored it and just set Hard to 1–200, which is what it should've been all along. That was a good reminder that AI will sometimes defend broken code instead of just admitting it's wrong.

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
