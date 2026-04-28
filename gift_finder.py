import os
import json
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# ---------- Pydantic Schema ----------

class GiftItem(BaseModel):
    name_en: str
    name_ar: str
    description_en: str
    description_ar: str
    estimated_price_aed: float
    reasoning_en: str
    reasoning_ar: str
    confidence: float  # 0.0 to 1.0

class GiftFinderResponse(BaseModel):
    understood_request_en: str
    understood_request_ar: str
    gifts: list[GiftItem]
    disclaimer_en: Optional[str] = None
    disclaimer_ar: Optional[str] = None
    refused: bool = False
    refusal_reason: Optional[str] = None

# ---------- System Prompt ----------

SYSTEM_PROMPT = """
You are a gift recommendation assistant for Mumzworld, the largest mother-and-baby
e-commerce platform in the Middle East.

Your job: suggest thoughtful, specific gift products for mothers and babies
based on a natural language request. All responses must be in BOTH English and Arabic.

STRICT RULES:
1. Return ONLY valid JSON. No preamble, no markdown fences, no extra text.
2. Suggest 3-5 specific, realistic products available in the GCC market.
3. ALL prices must be in AED and STRICTLY under the user's stated budget.
4. Arabic text must be native-quality Arabic, NOT a word-for-word translation from English.
   Write Arabic as a native speaker would — natural phrasing, correct grammar.
5. If input is vague (no budget or no age), still respond but set confidence below 0.6
   and add a helpful disclaimer in both languages asking for more detail.
6. If the request is completely off-topic (not about mothers, babies, or gifts),
   set refused=true and explain in refusal_reason. Return empty gifts array.
7. confidence: 0.9+ = very confident fit. Below 0.6 = uncertain.
8. Never fabricate prices wildly. Use realistic UAE/GCC market estimates.
9. If budget is impossibly low (under 20 AED for a physical gift), add a disclaimer
   saying budget may be too low and suggest alternatives.

Return this exact JSON structure:
{
  "understood_request_en": "string",
  "understood_request_ar": "string",
  "gifts": [
    {
      "name_en": "string",
      "name_ar": "string",
      "description_en": "string",
      "description_ar": "string",
      "estimated_price_aed": number,
      "reasoning_en": "string",
      "reasoning_ar": "string",
      "confidence": number
    }
  ],
  "disclaimer_en": "string or null",
  "disclaimer_ar": "string or null",
  "refused": false,
  "refusal_reason": null
}
"""

# ---------- Core Function ----------

def find_gifts(user_query: str) -> dict:
    """
    Takes a natural language gift request.
    Returns structured recommendations validated against Pydantic schema.
    Never silently fails — all errors are explicit in the return dict.
    """
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ],
            temperature=0.4,
            max_tokens=2000,
        )

        raw_text = response.choices[0].message.content.strip()

        # Strip markdown fences if model ignores instructions
        if raw_text.startswith("```"):
            parts = raw_text.split("```")
            raw_text = parts[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        parsed_json = json.loads(raw_text)
        validated = GiftFinderResponse(**parsed_json)  # Pydantic validates schema

        return {"success": True, "data": validated.model_dump()}

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Model returned invalid JSON: {str(e)}",
            "raw": raw_text if 'raw_text' in locals() else "no response"
        }

    except ValidationError as e:
        return {
            "success": False,
            "error": f"Schema validation failed: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


# ---------- Quick Test ----------

if __name__ == "__main__":
    test_query = "thoughtful gift for a friend with a 6-month-old, under 200 AED"
    print(f"Testing with: '{test_query}'\n")
    result = find_gifts(test_query)
    print(json.dumps(result, indent=2, ensure_ascii=False))