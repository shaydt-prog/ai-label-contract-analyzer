import streamlit as st
import requests
import json
import re
import os
from PyPDF2 import PdfReader
from docx import Document

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Missing API key – contact admin")
    st.stop()

st.markdown("<h1 style='color:#00ff88; text-align:center;'>Analyze Your Contract</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.3rem; color:#ccc;'>Upload your label deal and get instant clarity</p>", unsafe_allow_html=True)

file = st.file_uploader("Upload contract (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

if not file:
    st.stop()

# Extract text
with st.spinner("Reading..."):
    if file.type == "application/pdf":
        text = "".join(p.extract_text() or "" for p in PdfReader(file).pages)
    else:
        text = "\n".join(p.text for p in Document(file).paragraphs)

if st.button("Generate Report", type="primary", use_container_width=True):
    with st.spinner("Analyzing with Llama 3.3..."):
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"""
Analyze this music contract and return ONLY valid JSON with 'free_preview' (array of 4-6 bullets) and 'premium_report' (object with 'summary' and 'clauses' array). ALWAYS include all fields.

{{
  "free_preview": [
    "Royalties: 50% of net revenue",
    "Term: 10 years exclusive",
    "Exclusivity: Worldwide",
    "Advance: $10,000 recoupable",
    "Masters: Label owns forever"
  ],
  "premium_report": {{
    "summary": "3-5 sentence plain English summary",
    "clauses": [
      {{
        "name": "Royalties",
        "explanation": "Artist gets 50% after costs",
        "risk_score": 6,
        "red_flags": ["Recoupable advance", "Vague cost deductions"],
        "suggestions": ["Ask for 70/30 split", "Cap recoupable costs"]
      }}
    ]
  }}
}}

Contract:
{text}
""" }]],
            "temperature": 0.2
        }

        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        raw = r.json()["choices"][0]["message"]["content"]
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        data = json.loads(match.group(0))

        # FIXED: Fallback for missing keys
        if "free_preview" not in data:
            data["free_preview"] = ["Royalties: Not specified", "Term: Not specified", "Exclusivity: Not specified", "Advance: Not specified", "Masters: Not specified"]
        if "premium_report" not in data:
            data["premium_report"] = {"summary": "Analysis incomplete – try again.", "clauses": []}
        if "summary" not in data["premium_report"]:
            data["premium_report"]["summary"] = "Summary not generated – full report available in premium."

        st.session_state.result = data
        st.rerun()

if "result" in st.session_state:
    d = st.session_state.result
    st.markdown("### Free Preview – Key Deal Points")
    for b in d["free_preview"]:
        st.markdown(f"<h3 style='color:#00ff88; font-size:1.8rem;'>• {b}</h3>", unsafe_allow_html=True)

    st.success("Free preview complete!")

    if st.button("Unlock Full Report ($9.99/mo)", type="primary", use_container_width=True):
        st.markdown("### Full Professional Report")
        st.info(d["premium_report"]["summary"])

        st.markdown("### Detailed Clauses")
        for c in d["premium_report"]["clauses"]:
            risk = c["risk_score"]
            color = "🟢" if risk <= 4 else "🟡" if risk <= 7 else "🔴"
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

st.info("Free preview • Full report + comparison = $9.99/month")