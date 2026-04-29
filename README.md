# Mumzworld Gift Finder 🎁

**Track A — AI Engineering Intern**

Natural-language gift recommendations for mothers and babies on Mumzworld. 
Type a request like "thoughtful gift for a friend with a 6-month-old, under 200 AED" 
and get a curated shortlist of 3–5 gifts with reasoning, confidence scores, and 
full copy in both English and Arabic. Out-of-scope requests are refused explicitly. 
Vague requests trigger a disclaimer rather than a confident wrong answer.

---

## Setup (under 5 minutes)

```bash
git clone https://github.com/YOUR_USERNAME/mumzworld-gift-finder
cd mumzworld-gift-finder
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:

OPENROUTER_API_KEY=sk-or-v1-your-key-here

Get a free key at openrouter.ai — no credit card required.

Run the app:
```bash
python -m streamlit run app.py
```

Run evals:
```bash
python evals.py
```

---

## Evals

See [EVALS.md](./EVALS.md) for full rubric, 12 test cases, and scores.

Quick summary: X/12 passing. Known failure modes: very low budgets, 
occasional missing disclaimer on vague input.

---

## Tradeoffs

See [TRADEOFFS.md](./TRADEOFFS.md) for full architecture reasoning.

---

## Tooling

- **OpenRouter + Llama 3.3 70B (free):** Main inference model. Used for all gift 
  generation. Called via OpenAI-compatible SDK.
- **Claude (claude.ai):** Used for prompt iteration, system message drafting, 
  eval case design, and README structure. Pair-coding style — I reviewed and 
  edited all outputs before committing.
- **Pydantic v2:** Schema validation. Every response is validated before being 
  shown to the user. Parse failures and schema mismatches are caught explicitly.
- **Streamlit:** UI framework. Chosen over Flask for speed — zero boilerplate.
- **python-dotenv:** Keeps API key out of source code.

---

## AI Usage Note

Used Claude (claude.ai) for system prompt drafting and iterating eval cases. 
Used Llama 3.3 70B via OpenRouter for all gift generation inference. 
No AI-generated code was committed without review and understanding. 
Pydantic schema and eval assertions were written and verified manually.

---

## Time Log

- Setup + OpenRouter account: 30 min
- Core gift_finder.py + prompt engineering: 90 min  
- Streamlit UI: 45 min
- Evals (writing + running + iterating): 60 min
- README + EVALS.md + TRADEOFFS.md: 45 min
- Total: ~5 hours
