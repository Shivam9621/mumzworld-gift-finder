"""
Evaluation suite for the Gift Finder.
Run with: python evals.py
"""
import time
from gift_finder import find_gifts

TEST_CASES = [
    {
        "id": "easy_1",
        "input": "thoughtful gift for a friend with a 6-month-old, under 200 AED",
        "expect_refused": False,
        "expect_gifts_count": (3, 5),
        "expect_all_under_budget": 200,
        "notes": "Standard happy path"
    },
    {
        "id": "easy_2",
        "input": "gift for a new mom who just gave birth, budget 300 AED",
        "expect_refused": False,
        "expect_gifts_count": (3, 5),
        "expect_all_under_budget": 300,
        "notes": "New mom, postpartum gifts"
    },
    {
        "id": "easy_3",
        "input": "هدية لأم جديدة مع طفل عمره شهر، الميزانية 150 درهم",
        "expect_refused": False,
        "expect_gifts_count": (3, 5),
        "notes": "Arabic language input"
    },
    {
        "id": "easy_4",
        "input": "gift for a toddler turning 2, under 100 AED",
        "expect_refused": False,
        "expect_gifts_count": (3, 5),
        "expect_all_under_budget": 100,
        "notes": "Toddler gift, tight budget"
    },
    {
        "id": "edge_1",
        "input": "gift for a mom",
        "expect_refused": False,
        "expect_low_confidence": True,
        "notes": "Very vague — should trigger disclaimer"
    },
    {
        "id": "edge_2",
        "input": "gift for a friend with a baby under 5 AED",
        "expect_refused": False,
        "expect_low_confidence": True,
        "notes": "Impossibly low budget"
    },
    {
        "id": "edge_3",
        "input": "best gift for twins aged 18 months, one has a peanut allergy, under 400 AED",
        "expect_refused": False,
        "expect_gifts_count": (3, 5),
        "notes": "Complex multi-constraint input"
    },
    {
        "id": "edge_4",
        "input": "gift for a pregnant woman in her third trimester, under 250 AED",
        "expect_refused": False,
        "expect_gifts_count": (3, 5),
        "notes": "Pregnant woman gifts"
    },
    {
        "id": "adversarial_1",
        "input": "best laptop for a software engineer",
        "expect_refused": True,
        "notes": "Completely off-topic — should refuse"
    },
    {
        "id": "adversarial_2",
        "input": "what is the capital of France",
        "expect_refused": True,
        "notes": "Random question — should refuse"
    },
    {
        "id": "adversarial_3",
        "input": "gift for my dog",
        "expect_refused": True,
        "notes": "Not a mom/baby request — should refuse"
    },
    {
        "id": "multilingual_1",
        "input": "gift for a breastfeeding mom, under 150 AED",
        "expect_refused": False,
        "expect_arabic_present": True,
        "notes": "Check Arabic fields are non-empty"
    },
]


def run_evals():
    passed = 0
    failed = 0

    print("=" * 60)
    print("GIFT FINDER EVAL SUITE — 12 TEST CASES")
    print("=" * 60)

    for tc in TEST_CASES:
        time.sleep(10)
        print(f"\n[{tc['id']}] {tc['notes']}")
        print(f"  Input: {tc['input'][:70]}")


        time.sleep(10)  # wait 10 seconds between calls to avoid rate limit
        result = find_gifts(tc["input"])
        issues = []

        if not result["success"]:
            issues.append(f"API/parse failure: {result['error']}")
        else:
            data = result["data"]

            if tc.get("expect_refused") and not data["refused"]:
                issues.append("Expected refusal but got gifts")

            if tc.get("expect_refused") == False and data["refused"]:
                issues.append(f"Unexpected refusal: {data['refusal_reason']}")

            if not data["refused"]:
                gifts = data["gifts"]

                if "expect_gifts_count" in tc:
                    lo, hi = tc["expect_gifts_count"]
                    if not (lo <= len(gifts) <= hi):
                        issues.append(f"Expected {lo}-{hi} gifts, got {len(gifts)}")

                if "expect_all_under_budget" in tc:
                    budget = tc["expect_all_under_budget"]
                    over = [g for g in gifts if g["estimated_price_aed"] > budget]
                    if over:
                        issues.append(f"{len(over)} gift(s) exceeded {budget} AED budget")

                if tc.get("expect_low_confidence"):
                    avg_conf = sum(g["confidence"] for g in gifts) / len(gifts) if gifts else 1
                    has_disclaimer = bool(data.get("disclaimer_en"))
                    if avg_conf > 0.8 and not has_disclaimer:
                        issues.append(f"Expected disclaimer, avg confidence was {avg_conf:.2f}")

                if tc.get("expect_arabic_present"):
                    for g in gifts:
                        if not g["name_ar"] or g["name_ar"] == g["name_en"]:
                            issues.append(f"Arabic name missing/same as English: {g['name_en']}")
                            break
                        if not g["description_ar"]:
                            issues.append("Arabic description is empty")
                            break

        status = "✅ PASS" if not issues else "❌ FAIL"
        if not issues:
            passed += 1
        else:
            failed += 1

        print(f"  Status: {status}")
        for issue in issues:
            print(f"    ⚠️  {issue}")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{len(TEST_CASES)} passed ({100*passed//len(TEST_CASES)}%)")
    print("=" * 60)


if __name__ == "__main__":
    run_evals()