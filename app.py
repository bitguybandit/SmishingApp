import streamlit as st
import joblib
import re
import time

# ==========================================
# 1. LOAD MODEL
# ==========================================


@st.cache_resource
def load_model():
    return joblib.load('smishing_nb_model.pkl')


model = load_model()

# ==========================================
# 2. RED FLAG PATTERNS
# ==========================================
RED_FLAGS = {
    "URL": r'http[s]?://\S+|www\.\S+',
    "PHONE": r'\b09\d{9}\b|\b\+639\d{9}\b',
    "EMAIL": r'\S+@\S+',
    "URGENCY": r'\b(urgent|immediately|now|today|suspend|deactivate|final warning|limited|blocked)\b',
    "OTP_REQUEST": r'\b(otp|one-time password|pin|code)\b',
    "REWARD": r'\b(won|congratulations|prize|reward|claim|winner)\b',
    "THREAT": r'\b(suspend|deactivate|locked|freeze|blocked|unauthorized)\b'
}

# ==========================================
# 3. PREPROCESS TEXT
# ==========================================


def preprocess_text(text):
    text = re.sub(r'http[s]?://\S+', '[URL]', text)
    text = re.sub(r'www\.\S+', '[URL]', text)
    text = re.sub(r'\b09\d{9}\b', '[PHONE]', text)
    text = re.sub(r'\b\+639\d{9}\b', '[PHONE]', text)
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    text = re.sub(r'\b\d{10,16}\b', '[ACCOUNT]', text)
    text = re.sub(r'\b\d{4,6}\b', '[OTP]', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ==========================================
# 4. HIGHLIGHT RED FLAGS
# ==========================================


def highlight_red_flags(text):
    highlighted = text
    for flag, pattern in RED_FLAGS.items():
        highlighted = re.sub(
            pattern,
            lambda m: f"<span style='background: rgba(255,0,80,0.25); color: #ff2e63; font-weight: bold; padding: 2px 6px; border-radius: 4px; border: 1px solid #ff2e63;'>{m.group(0)}</span>",
            highlighted,
            flags=re.IGNORECASE
        )
    return highlighted


# ==========================================
# 5. CYBER THEME CSS
# ==========================================
st.set_page_config(page_title="PH Smishing Detector",
                   page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    /* Import cyber font */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');

    /* Main background - dark cyber grid */
    .stApp {
        background: 
            linear-gradient(rgba(0, 255, 170, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.03) 1px, transparent 1px),
            radial-gradient(ellipse at top, #0a1929 0%, #000000 80%);
        background-size: 40px 40px, 40px 40px, 100% 100%;
        font-family: 'Share Tech Mono', monospace;
        color: #00ffaa;
    }

    /* Animated scan line */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ffaa, transparent);
        animation: scan 6s linear infinite;
        z-index: 999;
        pointer-events: none;
    }
    @keyframes scan {
        0% { top: 0; opacity: 0.8; }
        100% { top: 100vh; opacity: 0.2; }
    }

    /* Title */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00ffaa !important;
        text-align: center;
        font-size: 2.5rem !important;
        text-shadow: 0 0 10px #00ffaa, 0 0 20px #00ffaa, 0 0 40px #00ffaa;
        animation: pulseGlow 2.5s ease-in-out infinite;
        letter-spacing: 3px;
    }
    @keyframes pulseGlow {
        0%, 100% { text-shadow: 0 0 10px #00ffaa, 0 0 20px #00ffaa, 0 0 40px #00ffaa; }
        50% { text-shadow: 0 0 20px #00ffaa, 0 0 40px #00ffaa, 0 0 80px #00ffaa; }
    }

    /* Subtitle and text */
    .stMarkdown, p, label {
        color: #7fffd4 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* Text area */
    .stTextArea textarea {
        background: rgba(0, 20, 30, 0.9) !important;
        color: #00ffaa !important;
        border: 2px solid #00ffaa !important;
        border-radius: 8px !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 15px !important;
        box-shadow: 0 0 10px rgba(0, 255, 170, 0.3), inset 0 0 10px rgba(0, 255, 170, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.6), inset 0 0 15px rgba(0, 255, 255, 0.2) !important;
    }

    /* Button */
    .stButton button {
        background: linear-gradient(135deg, #003322, #005544) !important;
        color: #00ffaa !important;
        border: 2px solid #00ffaa !important;
        border-radius: 8px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        padding: 12px 30px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.4) !important;
        text-transform: uppercase;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #005544, #00aa66) !important;
        color: #000 !important;
        box-shadow: 0 0 30px rgba(0, 255, 170, 0.9), 0 0 60px rgba(0, 255, 170, 0.5) !important;
        transform: translateY(-2px) scale(1.02);
    }

    /* Alert boxes (Streamlit native) */
    .stAlert {
        background: rgba(0, 20, 30, 0.9) !important;
        border-radius: 10px !important;
        border-left: 6px solid #00ffaa !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ffaa !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 10px #00ffaa !important;
    }
    [data-testid="stMetricLabel"] {
        color: #7fffd4 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* Divider */
    hr {
        border-color: rgba(0, 255, 170, 0.3) !important;
    }

    /* Custom result cards */
    .result-card {
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        font-family: 'Share Tech Mono', monospace;
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-smishing {
        background: linear-gradient(135deg, rgba(255, 0, 80, 0.15), rgba(255, 0, 80, 0.05));
        border: 2px solid #ff2e63;
        box-shadow: 0 0 20px rgba(255, 46, 99, 0.5), inset 0 0 20px rgba(255, 46, 99, 0.1);
        animation: fadeIn 0.5s ease-in, dangerPulse 2s ease-in-out infinite;
    }
    @keyframes dangerPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 46, 99, 0.5), inset 0 0 20px rgba(255, 46, 99, 0.1); }
        50% { box-shadow: 0 0 40px rgba(255, 46, 99, 0.9), inset 0 0 30px rgba(255, 46, 99, 0.2); }
    }
    .result-legitimate {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.15), rgba(0, 255, 170, 0.05));
        border: 2px solid #00ffaa;
        box-shadow: 0 0 20px rgba(0, 255, 170, 0.5), inset 0 0 20px rgba(0, 255, 170, 0.1);
    }

    /* Custom progress bar */
    .cyber-progress {
        background: rgba(0, 20, 30, 0.9);
        border: 1px solid #00ffaa;
        border-radius: 8px;
        height: 24px;
        overflow: hidden;
        margin: 8px 0;
        position: relative;
    }
    .cyber-progress-fill {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 10px;
        font-weight: bold;
        font-size: 12px;
        color: #000;
        transition: width 1s ease;
    }
    .fill-ham { background: linear-gradient(90deg, #00aa66, #00ffaa); }
    .fill-smishing { background: linear-gradient(90deg, #aa0033, #ff2e63); }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. HEADER
# ==========================================
st.markdown("<h1>🛡️ SMISHING DETECTOR</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#7fffd4; font-size:14px; letter-spacing:2px;'>"
    "&gt;&gt; EXPLAINABLE AI SECURITY SYSTEM v1.0 &lt;&lt;</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#00ffaa; font-size:13px;'>"
    "Paste an SMS message below to scan for phishing threats.</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ==========================================
# 7. INPUT
# ==========================================
user_input = st.text_area(
    "📱 ▸ INPUT SMS MESSAGE:",
    height=150,
    placeholder="e.g., BDO Alert: Your account will be suspended. Verify at http://bdo-secure.xyz"
)

# ==========================================
# 8. ANALYZE
# ==========================================
if st.button("⚡ SCAN MESSAGE"):
    if user_input.strip() == "":
        st.warning("⚠ Please enter a message to scan.")
    else:
        # Animated analyzing state
        with st.spinner("🔍 Analyzing message patterns..."):
            time.sleep(0.8)  # Small delay for effect

        # Preprocess
        clean_input = preprocess_text(user_input)

        # Predict
        prediction = model.predict([clean_input])[0]
        probabilities = model.predict_proba([clean_input])[0]

        # Dynamic probability mapping
        class_labels = model.classes_
        prob_dict = dict(zip(class_labels, probabilities))
        ham_prob = prob_dict.get('ham', 0.0) * 100
        smishing_prob = prob_dict.get('Smishing', 0.0) * 100
        confidence = max(ham_prob, smishing_prob)

        st.markdown("---")

        # Result card
        if prediction == 'Smishing':
            st.markdown(f"""
            <div class='result-card result-smishing'>
                <h2 style='color:#ff2e63; margin:0; font-family:Orbitron,sans-serif; letter-spacing:2px;'>
                    🚨 THREAT DETECTED
                </h2>
                <p style='color:#ff2e63; margin:8px 0 0 0; font-size:18px;'>
                    SMISHING IDENTIFIED — Confidence: <b>{confidence:.2f}%</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 🚩 RED FLAGS IDENTIFIED:")
            st.markdown(highlight_red_flags(
                user_input), unsafe_allow_html=True)
            st.markdown(
                "<p style='color:#ff2e63; font-weight:bold;'>⚠️ DO NOT click any links or share personal information.</p>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"""
            <div class='result-card result-legitimate'>
                <h2 style='color:#00ffaa; margin:0; font-family:Orbitron,sans-serif; letter-spacing:2px;'>
                    ✅ MESSAGE CLEARED
                </h2>
                <p style='color:#00ffaa; margin:8px 0 0 0; font-size:18px;'>
                    LEGITIMATE MESSAGE — Confidence: <b>{confidence:.2f}%</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📝 ANALYSIS:")
            st.markdown(
                "<p style='color:#7fffd4;'>No suspicious patterns detected. This message appears safe based on our model.</p>",
                unsafe_allow_html=True
            )

        # Custom progress bars
        st.markdown("### 📊 CONFIDENCE BREAKDOWN")
        st.markdown(f"""
        <div>
            <p style='color:#7fffd4; margin-bottom:4px;'>LEGITIMATE (HAM)</p>
            <div class='cyber-progress'>
                <div class='cyber-progress-fill fill-ham' style='width:{ham_prob:.2f}%;'>{ham_prob:.2f}%</div>
            </div>
        </div>
        <div style='margin-top:12px;'>
            <p style='color:#ff2e63; margin-bottom:4px;'>SMISHING</p>
            <div class='cyber-progress'>
                <div class='cyber-progress-fill fill-smishing' style='width:{smishing_prob:.2f}%;'>{smishing_prob:.2f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#7fffd4; font-size:11px; letter-spacing:1px;'>"
    "⚠ STUDENT RESEARCH PROTOTYPE — Always verify with your official bank app or hotline.</p>",
    unsafe_allow_html=True
)
