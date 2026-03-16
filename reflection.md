# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The game loaded fine and I could type a number and click submit, so at first it seemed okay. But it was basically unwinnable.

**Bug 1 — Inverted hints:** I expected that if my guess was too high, the game would tell me to go lower. Instead it said "Go HIGHER!" every time I guessed above the secret. I guessed 80 when the secret was around 30, and it kept pushing me higher. I thought I was misreading it at first, but after a few rounds it was clear the hints were just completely backwards — too high said go higher, too low said go lower.

**Bug 2 — Secret number changing mid-game:** I expected the secret to stay the same for the whole game. But when I opened the debug panel, the number kept being different after each guess. At first I thought I was imagining it. After a few more attempts it was clearly changing on me — which made the hints even more confusing since they were already backwards. I had to dig into the code with Copilot's help to figure out what was actually happening.

**Bug 3 — Hard mode was easier than Normal:** I expected Hard to be harder than Normal — bigger range, harder to guess. Instead Hard had a range of 1–50 while Normal was 1–100, so switching to Hard actually made the game easier. That was clearly just a wrong value in the original code.

---

## 2. How did you use AI as a teammate?

I mostly used Copilot once I had a hunch about where something was going wrong, to help me confirm it or understand why.

For the changing secret bug, I described what I was seeing — the debug panel showing different numbers after each guess — and asked it to explain what was happening in the session state logic. It walked me through how the secret was being cast to a string on certain attempts, which is why the comparisons were off. That was genuinely useful. I wouldn't have spotted that on my own nearly as fast.

One place where it wasn't helpful: I asked whether the Hard difficulty range being smaller than Normal was maybe intentional (like a design choice). It actually tried to justify it — said something like a tighter range could be a different kind of challenge. I almost went with that, but it didn't make sense with how the game described Hard mode. So I just changed it to 1–200 and wrote a test to make sure Hard's range is actually wider than Normal's. The AI was kind of making excuses for the bug instead of calling it one, which was a good reminder to trust the spec over the explanation.

---

## 3. Debugging and testing your fixes

For the inverted hints, I wrote a couple of tests — one where the guess is way below the secret and one where it's way above — to make sure the right outcome came back. Honestly I wasn't sure if the tests were going to be enough at first, so I also just played through a few rounds manually after fixing it to double-check it felt right.

For the secret-changing bug, Copilot helped me write a test for the specific case where the guess is 9 and the secret is 50. That case would return the wrong answer in the broken code because of how string comparison works. Once the logic was moved into `logic_utils.py` and using regular integer comparison, it passed.

I ran pytest after each fix and also just played the game. The hints now actually point you in the right direction, which sounds obvious but was clearly not the case before.

---

## 4. What did you learn about Streamlit and state?

The changing secret thing really confused me because I didn't know how Streamlit worked. I had used it a little before but not enough to know that it re-runs the whole script every single time you click anything. So every time I clicked Submit, the secret was getting regenerated at the top of the file.

Once I looked it up and understood that, the fix made sense — you have to store anything you want to keep in `st.session_state` and check if it already exists before setting it. That way it only gets created once. It's a pretty different mental model from regular Python scripts, which caught me off guard.

---

## 5. Looking ahead: your developer habits

I want to get better about writing tests earlier in the process. I usually wrote them after I was pretty sure the fix worked, which meant a couple times I thought something was fixed and then the test showed it wasn't quite right. Writing the test first and watching it fail before fixing would have made that cleaner.

The AI thing I'll carry forward is being more skeptical when it explains a decision rather than questioning it. It was helpful for "show me where this variable gets set" but less helpful for "is this behavior intentional" — it tends to come up with a reason why the broken thing might make sense, which isn't what you need when debugging.
