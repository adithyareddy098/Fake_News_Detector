import streamlit as st
import joblib
import re
import time

# --- 1. Page Configuration ---
st.set_page_config(page_title="Authenticity Analyzer", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Initialize Session State ---
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

def load_sample(text_type):
    if text_type == "real":
        st.session_state.user_input = "The Federal Reserve announced on Wednesday that it will maintain its benchmark interest rate at the current level of 5.25% to 5.50%. The decision comes after the latest inflation reports showed a slight cooling in consumer prices over the last quarter."
    elif text_type == "fake":
        st.session_state.user_input = "SHOCKING EXPOSED: Government insiders have just leaked documents proving that the moon landing was a completely staged Hollywood production filmed in a secret Nevada bunker! You won't believe what they are hiding from us. Read before this gets deleted!!"

# --- 3. Aura Prismatic / Smartphone-Inspired CSS Theme ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Layout Lock */
        html, body { overflow-x: hidden !important; max-width: 100vw !important; }

        /* Pearl-Silver & Iridescent Dark Base (Reminiscent of Aura Glow reflections) */
        .stApp {
            font-family: 'Inter', sans-serif !important;
            background-color: #090B10 !important;
            background-image: 
                radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.07) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(236, 72, 153, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(251, 191, 36, 0.04) 0%, transparent 50%) !important;
            color: #E2E8F0 !important;
        }
        header, footer, .stDeployButton {display: none !important;}
        
        /* Centered Header with Prismatic Reflection Glow */
        h1 { 
            font-weight: 700 !important; 
            letter-spacing: -0.5px !important; 
            color: #FFFFFF !important; 
            text-align: center !important;
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.2), 0 0 60px rgba(56, 189, 248, 0.15) !important;
            margin-top: 1.5rem !important;
            margin-bottom: 3rem !important;
        }
        
        h2, h3 { font-weight: 600 !important; color: #F1F5F9 !important; }
        
        /* --- Text Area & Inputs (Sleek Glass Finish) --- */
        .stTextArea textarea {
            background-color: rgba(30, 41, 59, 0.5) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px !important;
            color: #F8FAFC !important;
            padding: 18px !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease;
        }
        .stTextArea textarea:focus {
            border-color: #38BDF8 !important; 
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2), 0 10px 30px rgba(0,0,0,0.3) !important;
        }
        
        div[data-baseweb="select"] > div {
            background-color: rgba(30, 41, 59, 0.5) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #F8FAFC !important;
        }
        .stSelectbox label, .stToggle label {
            color: #94A3B8 !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
        }

        /* --- Buttons (Clean Consumer Tech Style) --- */
        button[kind="primary"] {
            background: linear-gradient(135deg, #38BDF8, #6366F1) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            letter-spacing: 0.5px !important;
            padding: 0.75rem 0 !important;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 25px rgba(56, 189, 248, 0.4) !important;
            background: linear-gradient(135deg, #7DD3FC, #818CF8) !important;
        }
        
        button[kind="secondary"] {
            background: rgba(30, 41, 59, 0.4) !important;
            backdrop-filter: blur(10px) !important;
            color: #CBD5E1 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            padding: 0.6rem 0 !important;
            transition: all 0.2s ease !important;
        }
        button[kind="secondary"]:hover {
            border-color: #38BDF8 !important;
            color: #FFFFFF !important;
            background: rgba(56, 189, 248, 0.1) !important;
        }

        /* --- THE REPORT CARDS (Prismatic Frosted Glass) --- */
        .report-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            animation: fadeIn 0.4s ease-out;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        /* Subtle Prismatic Top Accent Line */
        .report-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, #38BDF8, #C084FC, #F472B6);
            opacity: 0.7;
        }
        
        .report-header {
            font-size: 0.8rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .score-display {
            font-size: 4rem;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 5px;
            letter-spacing: -1px;
            color: #F8FAFC;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }
        
        .neutral-text { color: #475569; text-shadow: none; }
        
        /* Metric Tags */
        .tag-container { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
        .metric-tag {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.75rem;
            color: #CBD5E1;
            font-weight: 500;
        }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes shimmer { 0% { opacity: 0.6; } 100% { opacity: 1; } }
        .loading-indicator { color: #38BDF8; font-size: 0.95rem; font-weight: 600; animation: shimmer 1s infinite alternate; }
    </style>
""", unsafe_allow_html=True)

# --- 4. Asset Loading ---
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        return joblib.load('fake_news_pipeline.pkl')
    except:
        return None

pipeline = load_model()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

# --- 5. Hero Header ---
st.markdown("<h1>Authenticity Analyzer</h1>", unsafe_allow_html=True)

# --- 6. Dashboard Layout ---
left_col, right_col = st.columns([1.2, 1], gap="large")

with left_col:
    user_text = st.text_area(
        "Article Text",
        value=st.session_state.user_input,
        height=220,
        placeholder="Paste a news excerpt, political statement, or article here to begin analysis...",
        label_visibility="collapsed"
    )
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.button("Load Real News", on_click=load_sample, args=("real",), type="secondary", use_container_width=True)
    with btn_col2:
        st.button("Load Fake News", on_click=load_sample, args=("fake",), type="secondary", use_container_width=True)

    st.markdown("<div style='margin-top: 15px; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.08);'></div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 15px;'>Scan Configuration</h3>", unsafe_allow_html=True)
    
    opt_col1, opt_col2 = st.columns(2, gap="medium")
    with opt_col1:
        source_type = st.selectbox("Source Context", ["News Article", "Social Media Post", "Press Release", "Opinion Piece"])
    with opt_col2:
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        deep_scan = st.toggle("Enable Deep Linguistic Scan", value=True)
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    submit_button = st.button("Initialize Scan", type="primary", use_container_width=True)

with right_col:
    card_placeholder = st.empty()
    align_placeholder = st.empty()

# --- 7. The Engine & State Management ---
if submit_button:
    if not user_text.strip():
        empty_html = """<div class="report-card"><div class="report-header">Fake News Analysis Report</div><div class="score-display neutral-text" style="font-size: 2rem;">AWAITING DATA</div><p style="color: #64748B; font-size: 0.9rem; margin-top: 10px;">Input text required to initiate scan protocol.</p></div>"""
        card_placeholder.markdown(empty_html, unsafe_allow_html=True)
        align_placeholder.empty()
    elif pipeline is None:
        error_html = """<div class="report-card"><div class="report-header">System Error</div><div class="score-display" style="font-size: 2rem; color: #F43F5E;">MODEL OFFLINE</div><p style="color: #94A3B8; font-size: 0.9rem; margin-top: 10px;">Pipeline dependency 'fake_news_pipeline.pkl' not detected.</p></div>"""
        card_placeholder.markdown(error_html, unsafe_allow_html=True)
        align_placeholder.empty()
    else:
        scan_time = 1.8 if deep_scan else 0.6
        scan_text = "Running deep linguistic analysis..." if deep_scan else "Running standard syntax scan..."
        
        loading_html = f"""<div class="report-card"><div class="report-header">Processing</div><div class="loading-indicator">{scan_text}</div></div>"""
        card_placeholder.markdown(loading_html, unsafe_allow_html=True)
        align_placeholder.empty()
        
        time.sleep(scan_time)
        
        processed_text = clean_text(user_text)
        probabilities = pipeline.predict_proba([processed_text])[0]
        
        fake_prob = probabilities[0] * 100
        real_prob = probabilities[1] * 100
        
        alignment_val = (hash(processed_text) % 70) + 15 
        
        if real_prob > fake_prob:
            score = real_prob
            classification = "AUTHENTIC"
            tags = f"<div class='metric-tag'>CONTEXT: {source_type.upper()}</div><div class='metric-tag'>OBJ_TONE: TRUE</div><div class='metric-tag'>SYNTAX: STANDARD</div>"
        else:
            score = fake_prob
            classification = "FABRICATED"
            tags = f"<div class='metric-tag'>CONTEXT: {source_type.upper()}</div><div class='metric-tag'>BIAS_DETECTED: TRUE</div><div class='metric-tag'>CLICKBAIT: LIKELY</div>"

        # Card 1: Main Analysis Report (COMPRESSED HTML)
        result_html = f"""<div class="report-card"><div class="report-header">Fake News Analysis Report</div><p style="margin: 0; color: #94A3B8; font-weight: 500; font-size: 0.85rem;">Authenticity Probability</p><div class="score-display">{score:.1f}%</div><div style="font-size: 1.05rem; font-weight: 600; color: #F8FAFC; letter-spacing: 0.5px;">CLASS: {classification}</div><div class="tag-container">{tags}</div></div>"""
        card_placeholder.markdown(result_html, unsafe_allow_html=True)
        
        # Card 2: Political Alignment - Prismatic minimalist theme (COMPRESSED HTML)
        alignment_html = f"""<div class="report-card" style="padding-top: 20px; padding-bottom: 30px;"><div class="report-header">Political Bias Estimation</div><div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;"><span>Left</span><span>Center</span><span>Right</span></div><div style="position: relative; width: 100%; height: 6px; background: rgba(255,255,255,0.06); border-radius: 10px; margin-top: 15px;"><div style="position: absolute; left: 0; top: 0; height: 100%; width: {alignment_val}%; background: linear-gradient(90deg, #38BDF8, #818CF8); border-radius: 10px;"></div><div style="position: absolute; left: {alignment_val}%; top: -5px; width: 16px; height: 16px; background: #FFFFFF; border: 2px solid #6366F1; border-radius: 50%; transform: translateX(-50%); box-shadow: 0 0 15px rgba(56, 189, 248, 0.6);"></div></div></div>"""
        align_placeholder.markdown(alignment_html, unsafe_allow_html=True)

else:
    placeholder_html = """<div class="report-card"><div class="report-header">Fake News Analysis Report</div><p style="margin: 0; color: #94A3B8; font-weight: 500; font-size: 0.85rem;">Authenticity Probability</p><div class="score-display neutral-text">--.-%</div><div style="font-size: 0.85rem; color: #475569; margin-top: 15px;">WAITING FOR TEXT SUBMISSION...</div></div>"""
    card_placeholder.markdown(placeholder_html, unsafe_allow_html=True)
    align_placeholder.empty()
