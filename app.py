import streamlit as st
import pandas as pd
import numpy as np

# Page Config (Responsive, No Sidebar)
st.set_page_config(
    page_title="AI Label – Contract Analyzer for Musicians 2025 | Save $47k on Bad Deals",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS (Responsive, Mobile-First, Neon Theme)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
.main {background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%); font-family: 'Inter', sans-serif; color: white;}
.stApp {background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);}
.stButton > button {background: linear-gradient(45deg, #00ff88, #00ccff); color: black; border-radius: 25px; font-weight: 700; padding: 15px 30px; box-shadow: 0 8px 25px rgba(0,255,136,0.3);}
.stButton > button:hover {transform: scale(1.05);}
.warning {background: linear-gradient(90deg, #330000, #660033); padding: 25px; border-left: 5px solid #ff0066; border-radius: 15px; margin: 30px 0;}
h1 {color: #00ff88; text-align: center; font-size: 3.5rem; text-shadow: 0 0 20px rgba(0,255,136,0.5);}
.sidebar {display: none !important;}  # Hide sidebar completely
.metric {color: #00ff88 !important;}
.feature-card {background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(0,255,136,0.2); border-radius: 20px; padding: 30px; margin: 20px 0; transition: all 0.3s;}
.feature-card:hover {transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,255,136,0.2);}
.testimonial {font-style: italic; color: #00ff88; font-size: 1.4rem; text-align: center; margin: 40px; background: rgba(0,255,136,0.1); padding: 25px; border-radius: 15px; border-left: 5px solid #00ff88;}
.price {font-size: 4rem; font-weight: 800; color: #00ff88;}
.popular {border: 3px solid #00ff88 !important; transform: scale(1.05);}
@media (max-width: 768px) {h1 {font-size: 2.5rem;} .stButton > button {width: 100%; margin: 10px 0;}}
</style>
""", unsafe_allow_html=True)

# Floating Top Navigation (No Sidebar)
st.markdown("""
<div style='position:fixed; top:0; left:0; right:0; height:80px; background:rgba(10,10,26,0.95); backdrop-filter:blur(12px); border-bottom:1px solid #00ff8830; z-index:9999; display:flex; align-items:center; justify-content:space-between; padding:0 5%; box-shadow:0 4px 20px rgba(0,0,0,0.5);'>
    <div style='font-size:2rem; font-weight:800; color:#00ff88;'>AI Label</div>
    <div style='display:flex; gap:30px;'>
        <a href='/' style='color:white; text-decoration:none; font-weight:600; padding:10px 20px; border-radius:12px; transition:all 0.3s;'>Home</a>
        <a href='/Analyze' style='color:white; text-decoration:none; font-weight:600; padding:10px 20px; border-radius:12px; transition:all 0.3s;'>Analyze</a>
        <a href='/Compare' style='color:white; text-decoration:none; font-weight:600; padding:10px 20px; border-radius:12px; transition:all 0.3s;'>Compare</a>
        <a href='#pricing' style='color:white; text-decoration:none; font-weight:600; padding:10px 20px; border-radius:12px; transition:all 0.3s;'>Pricing</a>
    </div>
</div>
<div style='height:100px;'></div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div style='text-align:center; padding:100px 20px;'>
    <h1>Stop Signing Bad Deals</h1>
    <p style='font-size:1.8rem; color:#ccc; max-width:900px; margin:30px auto;'>The #1 AI tool that reads your label contract and tells you — in plain English — what you're really giving away.</p>
    <h2 style='color:#00ff88; font-size:2.5rem; margin:40px 0;'>3 Free Analyses • No Card Required</h2>
</div>
""", unsafe_allow_html=True)

if st.button("Start Free Analysis Now →", type="primary", use_container_width=True):
    st.switch_page("pages/analyze.py")

# Stats Chart (Real Data Visualization)
st.markdown("<h2 style='text-align:center; color:#00ff88; margin:80px 0;'>Trusted by Thousands of Artists</h2>", unsafe_allow_html=True)
chart_data = pd.DataFrame({
    'Artists Protected': [4821],
    'Money Saved': [2.8],
    'Bad Deals Stopped': [1247],
    'Risk Reduced': [71]
})
st.bar_chart(chart_data, use_container_width=True)

# Features
st.markdown("<h2 style='text-align:center; color:#00ff88; margin:80px 0;'>Why Musicians Choose AI Label</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='feature-card'><h3>Free Preview</h3><p>Key bullets in seconds</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='feature-card'><h3>Full Risk Report</h3><p>Risk scores, red flags, negotiation tips</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='feature-card'><h3>Compare Deals</h3><p>See which label offer is better</p></div>", unsafe_allow_html=True)

# Testimonials
st.markdown("<h2 style='text-align:center; color:#00ff88; margin:100px 0;'>Real Artists. Real Results.</h2>", unsafe_allow_html=True)
t1, t2 = st.columns(2)
with t1:
    st.markdown("""
    <div class="testimonial">
        <p>"Found a perpetual masters clause I almost missed. Got it changed to 7 years and kept my catalog."</p>
        <p><strong>— Lena M., R&B Artist</strong></p>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown("""
    <div class="testimonial">
        <p>"Caught a hidden 360 deal. Renegotiated and kept $85k."</p>
        <p><strong>— DJ RICO, Producer</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Pricing
st.markdown("<h2 style='text-align:center; color:#00ff88; margin:100px 0 60px;'>Simple, Transparent Pricing</h2>", unsafe_allow_html=True)
p1, p2, p3 = st.columns([1.2, 1.6, 1.2])
with p1:
    st.markdown("""
    <div class='price-card'>
        <h3>Free</h3>
        <p style='font-size:1.2rem; color:#888;'>3 analyses/month</p>
        <p>Bullet summary only</p>
    </div>
    """, unsafe_allow_html=True)
with p2:
    st.markdown("""
    <div class='price-card popular'>
        <div style='background:#00ff8820; color:#00ff88; padding:10px; border-radius:50px; font-weight:bold; margin-bottom:20px;'>BEST VALUE</div>
        <h2 class='price'>$9.99<span style='font-size:1.5rem'>/month</span></h2>
        <p style='font-size:1.3rem;'>
            Unlimited analyses<br>
            Full reports<br>
            Save & compare<br>
            Priority support
        </p>
    </div>
    """, unsafe_allow_html=True)
with p3:
    st.markdown("""
    <div class='price-card'>
        <h3>One-Time</h3>
        <p style='font-size:1.8rem; color:#00ff88; font-weight:800;'><strong>$3.99</strong></p>
        <p>Full report for one contract</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close main-content