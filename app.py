import streamlit as st
from gift_finder import find_gifts

st.set_page_config(
    page_title="Mumzworld Gift Finder 🎁",
    page_icon="🎁",
    layout="wide"
)

# Header
st.title("🎁 Mumzworld Gift Finder")
st.caption("Find the perfect gift for any mom or baby — recommendations in English & Arabic")
st.divider()

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    user_query = st.text_input(
        "Describe what you're looking for:",
        placeholder="e.g. thoughtful gift for a friend with a 6-month-old, under 200 AED",
    )
with col2:
    st.write("")  # spacing
    st.write("")
    search_btn = st.button("Find Gifts 🎀", use_container_width=True)

# Example queries
st.caption("Try: &nbsp; `gift for a new mom, 300 AED` &nbsp;|&nbsp; `هدية لطفل عمره شهر، 150 درهم` &nbsp;|&nbsp; `twins turning 2, under 400 AED`")

# Results
if search_btn and user_query:
    with st.spinner("Finding perfect gifts..."):
        result = find_gifts(user_query)

    if not result["success"]:
        st.error(f"⚠️ Something went wrong: {result['error']}")
        if "raw" in result:
            with st.expander("Raw model output (for debugging)"):
                st.code(result["raw"])

    else:
        data = result["data"]

        # Handle refusals
        if data["refused"]:
            st.warning(f"⚠️ This request is outside my scope.\n\n**Reason:** {data['refusal_reason']}")
            st.info("I can only help with gift recommendations for mothers and babies.")

        else:
            # What the model understood
            st.success(f"🔍 **Understood:** {data['understood_request_en']}")
            st.caption(f"الطلب المفهوم: {data['understood_request_ar']}")

            # Disclaimer for vague/edge inputs
            if data.get("disclaimer_en"):
                st.warning(f"💡 {data['disclaimer_en']}")
                st.caption(f"ملاحظة: {data['disclaimer_ar']}")

            st.divider()
            st.subheader(f"🎁 Gift Recommendations ({len(data['gifts'])} found) / توصيات الهدايا")

            for i, gift in enumerate(data["gifts"], 1):
                confidence_pct = int(gift["confidence"] * 100)
                confidence_color = "🟢" if confidence_pct >= 80 else "🟡" if confidence_pct >= 60 else "🔴"

                with st.expander(
                    f"{confidence_color} {i}. {gift['name_en']}  —  {gift['estimated_price_aed']:.0f} AED  |  {gift['name_ar']}",
                    expanded=(i == 1)  # first one open by default
                ):
                    col_en, col_ar = st.columns(2)

                    with col_en:
                        st.markdown("**🇬🇧 English**")
                        st.write(gift["description_en"])
                        st.caption(f"💬 Why this? {gift['reasoning_en']}")

                    with col_ar:
                        st.markdown("**🇦🇪 العربية**")
                        st.write(gift["description_ar"])
                        st.caption(f"💬 لماذا هذا؟ {gift['reasoning_ar']}")

                    st.progress(gift["confidence"], text=f"Confidence: {confidence_pct}%")

elif search_btn and not user_query:
    st.warning("Please enter a gift request first.")