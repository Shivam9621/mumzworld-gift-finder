# Mumzworld Gift Finder 🎁

Natural-language gift recommendations for mothers and babies — curated 
shortlist with reasoning in English and Arabic.

## Setup (under 5 minutes)

1. Clone the repo
2. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. Create `.env` with `OPENROUTER_API_KEY=your_key`
5. `streamlit run app.py`

## Evals

Run `python evals.py` — 12 test cases covering happy path, edge cases, 
adversarial/refusals, and multilingual quality.

| Category | Cases | Pass Rate |
|---|---|---|
| Happy path | 4 | X/4 |
| Edge cases | 4 | X/4 |
| Refusals | 3 | X/3 |
| Multilingual | 1 | X/1 |

Known failure modes:
- Very low budgets (under 20 AED) sometimes produce gifts slightly over budget
- Extremely vague input occasionally skips the disclaimer

## Tradeoffs

**Why this problem:** High customer value, showcases multilingual structured 
output, evals are natural to write, demos well.

**Model choice:** Llama 3.3 70B via OpenRouter (free). Capable enough for 
structured JSON + Arabic. GPT-4o would improve Arabic quality further.

**Architecture:** Single-turn prompt with strict JSON schema enforced by 
Pydantic. Chose this over multi-turn agent because the task fits in one 
inference step — no need to add latency.

**What I cut:** Product image generation, real catalog search via RAG, 
price verification via web search. Would add RAG over real Mumzworld 
catalog data next.

**Uncertainty handling:** Low-confidence inputs trigger a disclaimer. 
Out-of-scope inputs are refused with a reason. JSON parse failures 
surface explicitly, never silently.

## Tooling

- **OpenRouter + Llama 3.3 70B (free):** Main model for gift generation
- **Claude (claude.ai):** Used for prompt iteration and README drafting
- **Pydantic:** Schema validation — catches silent failures
- **Streamlit:** UI — chose over Flask for speed
