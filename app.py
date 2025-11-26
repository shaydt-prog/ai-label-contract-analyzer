import streamlit as st

st.set_page_config(page_title="AI Label", page_icon="Contract", layout="wide")

st.markdown("""
<style>
    .main {background:#0a0a0a; color:white;}
    .stButton>button {background:#00ff99; color:black; font-weight:bold; border-radius:15px;}
    .warning {background:#330000; padding:20px; border-left:6px solid #ff3366; border-radius:10px;}
    .big {font-size:1.9rem; line-height:2.4rem;}
    h1 {color:#00ff99; text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>AI Label Contract Analyzer</h1>", unsafe_allow_html=True)
st.markdown("### See the real deal behind your label contract — instantly.", unsafe_allow_html=True)

st.markdown("""
<div class="warning">
<b>NOT LEGAL ADVICE</b><br>
This tool helps you understand your contract in plain English.<br>
<b>Always</b> have a music lawyer review before signing.
</div>
""", unsafe_allow_html=True)

if st.button("Analyze My Contract Now", type="primary", use_container_width=True):
    st.switch_page("pages/analyze.py")

st.caption("Free preview • Full report + comparison = $9.99/month")