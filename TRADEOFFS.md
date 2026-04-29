# TRADEOFFS.md — Design Decisions & Reasoning

## Problem Selection

### Why Gift Finder?

I evaluated four problems from the brief before picking:

| Problem | Pros | Cons | Verdict |
|---|---|---|---|
| Gift Finder | Multilingual, structured output, natural evals, demos well | No RAG/retrieval component | ✅ Picked |
| Review Synthesizer | Good RAG opportunity | Needs real review data | Rejected |
| CS Email Triage | Good classification task | Less visually impressive | Rejected |
| Operations Dashboard | Real data engineering | Needs order data pipeline | Rejected |

Gift Finder won because it naturally hits 3 of the required AI engineering dimensions 
(structured output + validation, multilingual output, uncertainty handling/refusals) 
without requiring external datasets I'd have to fabricate heavily.

---

## Architecture Decisions

### Single-turn vs. Multi-turn Agent

**Chose:** Single-turn prompt → structured JSON output

**Rejected:** Multi-turn agent with tool calls (e.g., search for products, validate prices)

**Why:** The task doesn't require external state. A single well-engineered prompt with 
strict schema validation gives deterministic, fast, low-cost results. Adding an agent 
loop would add latency and failure points without meaningful accuracy gain for this use case.

**What I'd do with more time:** Add a RAG layer over a Mumzworld product catalog 
(even a synthetic one) so recommendations cite real SKUs with real prices.

---

## Model Choice

**Used:** `meta-llama/llama-3.3-70b-instruct:free` via OpenRouter

**Why:**
- Free tier, no cost barrier for the evaluator to reproduce
- 70B parameters — sufficient for multilingual structured output
- Instruction-following is strong enough to return valid JSON consistently

**Tradeoff:** GPT-4o or Claude 3.5 Sonnet would produce better Arabic fluency and 
more reliable JSON on first try. Llama 3.3 70B requires the markdown-fence stripping 
fallback ~5% of the time.

**Temperature = 0.4:** Low enough for consistent JSON structure, high enough for varied 
gift recommendations across repeated queries.

---

## Uncertainty Handling

Three explicit uncertainty signals are built in:

1. **`refused: true`** — for completely out-of-scope requests (non-baby/mom topics)
2. **`confidence` per gift (0.0–1.0)** — shown as a progress bar in the UI
3. **`disclaimer_en/ar`** — triggered for vague inputs (no budget, no age specified)

This means the system never silently fails or invents confident answers for bad inputs.

---

## What I Cut

| Feature | Why cut | Would add if... |
|---|---|---|
| RAG over product catalog | No real catalog data; synthetic data would mislead | Had Mumzworld's product feed |
| Real price verification via web search | Adds latency + complexity | Production deployment |
| Voice input (Arabic/English) | Out of 5-hour scope | Had Whisper API access |
| Product image output | Multimodal generation overkill for this task | Multimodal was required |
| Saved history / user profiles | Needs a database | Building a real product |

---

## What I'd Build Next

1. **RAG over Mumzworld catalog** — embed real product data, retrieve by semantic 
   similarity to the gift request, ground recommendations in actual SKUs and prices
2. **Feedback loop** — thumbs up/down per gift, used to fine-tune the ranking prompt
3. **WhatsApp integration** — mothers in GCC use WhatsApp heavily; a bot interface 
   makes more sense than a web UI for this use case