import streamlit as st
import requests
import json
import re
from PyPDF2 import PdfReader
from docx import Document

# YOUR WORKING GROQ KEY
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "fallback_key_for_local_test")
st.title("Your Contract Analysis")
st.warning("**NOT LEGAL ADVICE** – Always consult a qualified lawyer before signing.")

file = st.file_uploader("Upload your contract (PDF/DOCX)", type=["pdf", "docx"])
if not file:
    st.info("Upload a contract to see the free preview")
    st.stop()

# Read file once
with st.spinner("Reading contract..."):
    if file.type == "application/pdf":
        text = "".join(p.extract_text() or "" for p in PdfReader(file).pages)
    else:
        from docx import Document
        text = "\n".join(p.text for p in Document(file).paragraphs)
    st.success(f"Extracted {len(text):,} characters")

# Only analyze when user clicks the button
if st.button("Generate Report", type="primary", use_container_width=True):
    with st.spinner("Analyzing with Llama 3.3 70B..."):
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{
                "role": "user",
                "content": f"""
Analyze this music contract and return ONLY valid JSON with this exact structure:

{{
  "free_preview": [
    "Royalties: 50% of net revenue",
    "Term: 10 years exclusive",
    "Exclusivity: Worldwide exclusive",
    "Advance: $10,000 recoupable",
    "Masters: Label owns forever"
  ],
  "premium_report": {{
    "summary": "3-5 sentence plain English summary",
    "clauses": [
      {{
        "name": "Royalties",
        "explanation": "Artist gets 50% after label recoups costs",
        "risk_score": 6,
        "red_flags": ["Recoupable advance", "Vague cost deductions"],
        "suggestions": ["Ask for 70/30 split", "Cap recoupable costs"]
      }}
    ]
  }}
}}

Contract:
{text}
"""
            }],
            "temperature": 0.2
        }

        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            raw = r.json()["choices"][0]["message"]["content"]

            # Extract JSON
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            data = json.loads(match.group(0))

            # Store in session state so it survives button clicks
            st.session_state.analysis_result = data
            st.rerun()

        except Exception as e:
            st.error("Analysis failed. Please try again.")
            st.code(str(e))

# If we have results → show free + premium
if "analysis_result" in st.session_state:
    data = st.session_state.analysis_result

    st.markdown("### Free Preview – Key Deal Points")
    for bullet in data["free_preview"]:
        st.markdown(f"**• {bullet}**", unsafe_allow_html=True)

    st.markdown("###")
    st.success("Free preview complete!")

    # PREMIUM UNLOCK BUTTON – NOW WORKS!
    if st.button("Unlock Full Report + Save & Compare ($9.99/month)", type="primary", use_container_width=True):
        st.markdown("### Full Professional Report")
        st.info(data["premium_report"]["summary"])

        st.markdown("### Detailed Clauses")
        for c in data["premium_report"]["clauses"]:
            risk = c["risk_score"]
            color = "Green" if risk <= 4 else "Yellow" if risk <= 7 else "Red"
            with st.expander(f"{color} {c['name']} – Risk {risk}/10"):
                st.write("**Explanation:**", c["explanation"])
                if c.get("red_flags"):
                    st.error("Red Flags: " + " • ".join(c["red_flags"]))
                if c.get("suggestions"):
                    st.success("Suggestions: " + " • ".join(c["suggestions"]))

        st.balloons()
        st.success("Full report unlocked!")

else:
    st.info("Click 'Generate Report' to see your free preview")

st.markdown("---")
st.caption("Free preview • Full report + comparison = $9.99/month")