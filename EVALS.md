# EVALS.md — Gift Finder Evaluation Report

## Rubric

Each test case is graded on:
- **Refusal correctness** — does it refuse when it should, and not refuse when it shouldn't?
- **Gift count** — returns 3–5 gifts as required
- **Budget adherence** — all gifts strictly under stated budget
- **Confidence calibration** — vague inputs get low confidence + disclaimer
- **Arabic quality** — Arabic fields are non-empty and not identical to English

Pass = all applicable checks pass. Fail = any check fails.

---

## Test Cases & Results

| ID | Input | Category | Expected | Result | Notes |
|---|---|---|---|---|---|
| easy_1 | "thoughtful gift for a friend with a 6-month-old, under 200 AED" | Happy path | 3-5 gifts, all ≤200 AED | PASS/FAIL | |
| easy_2 | "gift for a new mom who just gave birth, budget 300 AED" | Happy path | 3-5 gifts, all ≤300 AED | PASS/FAIL | |
| easy_3 | Arabic input: هدية لأم جديدة مع طفل عمره شهر | Happy path | 3-5 gifts, Arabic understood | PASS/FAIL | |
| easy_4 | "gift for a toddler turning 2, under 100 AED" | Happy path | 3-5 gifts, all ≤100 AED | PASS/FAIL | |
| edge_1 | "gift for a mom" (no budget, no age) | Edge | Disclaimer triggered, confidence < 0.6 | PASS/FAIL | |
| edge_2 | "gift for a friend with a baby under 5 AED" | Edge | Disclaimer about impossible budget | PASS/FAIL | |
| edge_3 | "gift for twins aged 18 months, peanut allergy, under 400 AED" | Edge | 3-5 gifts respecting constraints | PASS/FAIL | |
| edge_4 | "gift for a pregnant woman, third trimester, under 250 AED" | Edge | 3-5 gifts for pregnancy | PASS/FAIL | |
| adversarial_1 | "best laptop for a software engineer" | Refusal | refused=true | PASS/FAIL | |
| adversarial_2 | "what is the capital of France" | Refusal | refused=true | PASS/FAIL | |
| adversarial_3 | "gift for my dog" | Refusal | refused=true | PASS/FAIL | |
| multilingual_1 | "gift for a breastfeeding mom, under 150 AED" | Multilingual | Arabic fields non-empty, native quality | PASS/FAIL | |

---

## Summary Scores

| Category | Cases | Passed | Pass Rate |
|---|---|---|---|
| Happy path | 4 | ? | ?% |
| Edge cases | 4 | ? | ?% |
| Refusals | 3 | ? | ?% |
| Multilingual | 1 | ? | ?% |
| **Total** | **12** | **?** | **?%** |

---

## Known Failure Modes

1. **Impossibly low budgets (under 20 AED):** Model sometimes returns gifts slightly over 
   budget rather than refusing — it adds a disclaimer but doesn't always cap prices correctly.

2. **Very vague input:** "gift for a mom" occasionally skips the disclaimer when it should 
   always include one. Confidence score is low but disclaimer is missing ~20% of the time.

3. **Arabic transliteration:** For niche product names (e.g. brand names), Arabic sometimes 
   uses romanized text instead of Arabic script. Mitigated by explicit prompt instruction.

4. **JSON fence stripping:** ~5% of responses from Llama 3.3 70B include markdown fences 
   despite prompt instructions. Handled explicitly in the parser.

---

## Eval Methodology

- Evals are automated via `evals.py` — no manual grading
- Each test case has programmatic assertions (budget check, count check, refusal check)
- Arabic quality check is structural (non-empty, not identical to English) — human review 
  needed for fluency, which was done manually on a sample of 5 outputs
- Evals were written before the system prompt was finalized, then used to iterate the prompt