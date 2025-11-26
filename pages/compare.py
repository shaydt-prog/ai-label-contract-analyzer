import streamlit as st
import json
import re
import requests
from PyPDF2 import PdfReader
from docx import Document

# YOUR GROQ KEY (same as before)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "fallback_key_for_local_test")
st.set_page_config(page_title="Compare", page_icon="Balance Scale")

st.markdown("<h1 style='color:#00ff99; text-align:center;'>Compare Two Contracts</h1>", unsafe_allow_html=True)
st.warning("**NOT LEGAL ADVICE** – Always consult a qualified lawyer.")

st.markdown("### Upload two contracts to see which one is better for you")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Contract A")
    file_a = st.file_uploader("Upload first contract", type=["pdf", "docx"], key="a")

with col2:
    st.markdown("#### Contract B")
    file_b = st.file_uploader("Upload second contract", type=["pdf", "docx"], key="b")

if not file_a or not file_b:
    st.info("Upload both contracts to compare them")
    st.stop()

def extract_text(file):
    if file.type == "application/pdf":
        return "".join(p.extract_text() or "" for p in PdfReader(file).pages)
    else:
        from docx import Document
        return "\n".join(p.text for p in Document(file).paragraphs)

text_a = extract_text(file_a)
text_b = extract_text(file_b)

if st.button("Compare Both Contracts Now", type="primary", use_container_width=True):
    with st.spinner("Analyzing both contracts with Llama 3.3 70B..."):
        def analyze(text):
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{
                    "role": "user",
                    "content": f"""
Analyze this music contract and return ONLY valid JSON:

{{
  "summary": "2-3 sentence plain English summary",
  "royalties": "Royalties: XX% of XXX",
  "term": "Term: XX years or perpetual",
  "exclusivity": "Exclusivity: Yes/No + territory",
  "advance": "Advance: $XX (recoupable?)",
  "masters": "Masters ownership: Label/Artist",
  "risk_score": 1-10,
  "red_flags": ["list of problems"],
  "suggestions": ["negotiation tips"]
}}

Contract:
{text}
"""
                }],
                "temperature": 0.2
            }
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=60)
            raw = r.json()["choices"][0]["message"]["content"]
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            return json.loads(match.group(0))

        result_a = analyze(text_a)
        result_b = analyze(text_b)

        st.session_state.comp_a = result_a
        result_a["name"] = file_a.name
        result_b["name"] = file_b.name
        st.session_state.comp_b = result_b
        st.rerun()

# Show comparison if we have results
if "comp_a" in st.session_state and "comp_b" in st.session_state:
    a = st.session_state.comp_a
    b = st.session_state.comp_b

    st.markdown(f"### {a['name']} vs {b['name']}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Contract A")
        st.metric("Overall Risk", f"{a['risk_score']}/10", delta=None)
        st.info(a["summary"])
        st.write("**Key Terms:**")
        st.write(a["royalties"])
        st.write(a["term"])
        st.write(a["exclusivity"])
        st.write(a["advance"])
        st.write(a["masters"])

    with col2:
        st.markdown("#### Contract B")
        st.metric("Overall Risk", f"{b['risk_score']}/10", delta=None)
        st.info(b["summary"])
        st.write("**Key Terms:**")
        st.write(b["royalties"])
        st.write(b["term"])
        st.write(b["exclusivity"])
        st.write(b["advance"])
        st.write(b["masters"])

    st.markdown("### Which Deal Is Better?")
    if a["risk_score"] < b["risk_score"]:
        st.success(f"**Contract A is safer** (Risk {a['risk_score']} vs {b['risk_score']})")
    elif b["risk_score"] < a["risk_score"]:
        st.success(f"**Contract B is safer** (Risk {b['risk_score']} vs {a['risk_score']})")
    else:
        st.warning("Both contracts have similar risk levels")

    st.markdown("### Red Flags Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Contract A Red Flags**")
        for flag in a["red_flags"]:
            st.error(flag)
    with col2:
        st.markdown("**Contract B Red Flags**")
        for flag in b["red_flags"]:
            st.error(flag)

    st.balloons()
    st.success("Premium comparison complete!")

else:
    st.info("Click 'Compare Both Contracts Now' to see the full premium comparison")

st.caption("Premium feature • Included in $9.99/month plan")