import streamlit as st
import joblib
import re
import time

# 1. Page Configuration (Wide layout so we can control the center column)
st.set_page_config(page_title="Authenticity Analyzer", layout="wide")

# 2. True Premium CSS Overhaul
st.markdown("""
    <style>
/* Base Theme - Apple Ambient Glow */
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(41, 98, 255, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(41, 98, 255, 0.1) 0px, transparent 50%) !important;
            background-attachment: fixed !important;
        }
        
        /* Constrain width and center everything like ChatGPT */
        .block-container {
            max-width: 750px !important; 
            padding-top: 5rem !important;
        }
        
        header, footer {visibility: hidden;}

        /* Clean Typography for Headers */
        h1 {
            color: #FFFFFF !important;
            text-align: center;
            font-weight: 600;
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        p {
            color: #888888 !important;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2rem;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        
        /* The Text Area - Smooth, rounded, Apple-like */
        .stTextArea textarea {
            background-color: #111111 !important;
            border: 1px solid #333333 !important;
            border-radius: 20px !important;
            color: #FFFFFF !important;
            padding: 20px !important;
            font-size: 16px !important;
            line-height: 1.6 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
            transition: all 0.3s ease;
        }
        .stTextArea textarea:focus {
            border-color: #666666 !important;
            box-shadow: 0 0 0 1px #666666 !important;
        }

        /* Pill-shaped Button (White on Black) */
        .stButton {
            display: flex;
            justify-content: center;
            margin-top: 1.5rem;
            margin-bottom: 2rem;
        }
        .stButton > button {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 30px !important;
            padding: 0.6rem 2.5rem !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            border: none !important;
            transition: transform 0.2s ease, opacity 0.2s ease !important;
        }
        .stButton > button:hover {
            transform: scale(1.03);
            opacity: 0.9;
        }

        /* Custom iOS-Style Result Widget */
        .result-card {
            background-color: #111111;
            border: 1px solid #333333;
            border-radius: 24px;
            padding: 40px 30px;
            text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            animation: fadeIn 0.5s ease;
        }
        .result-title {
            color: #888888;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 15px;
        }
        .result-score {
            font-size: 64px;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
            line-height: 1;
        }
        .result-label {
            font-size: 20px;
            font-weight: 500;
            margin-top: 10px;
            margin-bottom: 30px;
        }
        .authentic { color: #34C759; } /* Apple Green */
        .misleading { color: #FF3B30; } /* Apple Red */
        
        /* Custom Animated Progress Bar */
        .progress-bg {
            background-color: #222222;
            border-radius: 20px;
            height: 6px;
            width: 100%;
            overflow: hidden;
            margin: 0 auto;
            max-width: 80%;
        }
        .progress-fill {
            height: 100%;
            border-radius: 20px;
            transition: width 1.5s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .fill-authentic { background-color: #34C759; }
        .fill-misleading { background-color: #FF3B30; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# 3. Model Caching
@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load('fake_news_pipeline.pkl')

pipeline = load_model()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

# 4. Minimalist UI Layout
st.markdown("<h1>Authenticity Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p>Paste an article excerpt below to detect synthetic or misleading linguistic patterns.</p>", unsafe_allow_html=True)

user_text = st.text_area(
    "Article Text",
    height=200,
    placeholder="Enter the news text here...",
    label_visibility="collapsed"
)

# 5. Analysis Logic with Custom Widget Output
if st.button("Analyze"):
    if not user_text.strip():
        st.warning("Please enter an article excerpt to analyze.")
    else:
        with st.spinner("Analyzing text patterns..."):
            time.sleep(0.5)
            
            processed_text = clean_text(user_text)
            probabilities = pipeline.predict_proba([processed_text])[0]
            
            fake_prob = probabilities[0] * 100
            real_prob = probabilities[1] * 100
            
            # Determine dominant trait and styling
            if real_prob > fake_prob:
                score = real_prob
                label = "Authentic"
                color_class = "authentic"
                fill_class = "fill-authentic"
            else:
                score = fake_prob
                label = "Misleading"
                color_class = "misleading"
                fill_class = "fill-misleading"
            
            # Inject Custom iOS-Style Widget
            widget_html = f"""
            <div class="result-card">
                <div class="result-title">Confidence Score</div>
                <div class="result-score">{score:.1f}%</div>
                <div class="result-label {color_class}">{label}</div>
                <div class="progress-bg">
                    <div class="progress-fill {fill_class}" style="width: {score}%;"></div>
                </div>
            </div>
            """
            st.markdown(widget_html, unsafe_allow_html=True)