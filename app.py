import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import langid
import string
import os

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------
# Custom CSS
# ---------------------------------
st.markdown("""
<style>

:root {
    --accent: #0EA5A5;
    --accent-hover: #0B8888;
    --accent-soft: #0EA5A522;
    --bg-card: #F0FBFB;
    --text-dim: #6B7280;
}

/* ---------- App background ---------- */
.stApp {
    background: radial-gradient(circle at 15% 0%, #ECFEFF 0%, #FFFFFF 45%);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B2E33 0%, #103B42 100%);
}
section[data-testid="stSidebar"] * {
    color: #E0FCFC !important;
}
section[data-testid="stSidebar"] h1 {
    font-size: 1.4rem;
    font-weight: 800;
}
section[data-testid="stSidebar"] hr {
    border-color: #ffffff22;
}
.sidebar-card {
    background: #ffffff0f;
    border: 1px solid #ffffff1f;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 14px;
}
.sidebar-card b { color: #67E8E8 !important; }
.tech-pill {
    display: inline-block;
    background: #0EA5A533;
    border: 1px solid #0EA5A555;
    color: #E0FCFC !important;
    border-radius: 999px;
    padding: 3px 12px;
    margin: 3px 4px 3px 0;
    font-size: 0.78rem;
}

/* ---------- Header ---------- */
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.1rem;
}
.hero-title .gradient-text {
    background: linear-gradient(90deg, #0EA5A5, #6366F1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: var(--text-dim);
    font-size: 1rem;
    text-align: center;
    margin-bottom: 1.6rem;
}

/* ---------- Text area ---------- */
textarea {
    border-radius: 14px !important;
    border: 1px solid #D5EEEE !important;
    box-shadow: 0 2px 10px rgba(14, 165, 165, 0.06);
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 2px 14px rgba(14, 165, 165, 0.18) !important;
}

/* ---------- Selectboxes ---------- */
div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border: 1px solid #D5EEEE !important;
}

/* ---------- Translate button ---------- */
div.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 46px;
    font-size: 17px;
    font-weight: 600;
    background: linear-gradient(90deg, var(--accent), #6366F1);
    color: white;
    border: none;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
}
div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 16px rgba(14, 165, 165, 0.3);
}
div.stButton > button:focus,
div.stButton > button:focus-visible,
div.stButton > button:active {
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 165, 0.35) !important;
}

/* ---------- Result card ---------- */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.result-card {
    background: #ffffff;
    border: 1px solid #D5EEEE;
    border-radius: 16px;
    padding: 18px 20px;
    margin-top: 10px;
    box-shadow: 0 4px 14px rgba(14, 165, 165, 0.08);
    animation: fadeInUp 0.4s ease-out;
}
.result-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
}
.result-text {
    font-size: 1.15rem;
    color: #111827;
    line-height: 1.6;
}
.detected-badge {
    display: inline-block;
    background: var(--accent-soft);
    color: var(--accent-hover);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.85rem;
    margin-bottom: 10px;
}

/* ---------- Character count ---------- */
.char-count {
    text-align: right;
    color: var(--text-dim);
    font-size: 0.78rem;
    margin-top: -6px;
}

/* ---------- Sidebar Clear button (overrides the gradient Translate-button rule) ---------- */
section[data-testid="stSidebar"] div.stButton > button {
    background: #EF4444 !important;
    color: #ffffff !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] div.stButton > button:hover {
    background: #DC2626 !important;
    transform: scale(1.03);
}

h1 { text-align: center; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Handle "Clear" reset (must run BEFORE any widget with these keys is created)
# ---------------------------------
DEFAULT_SOURCE_LANG = "Auto Detect"
DEFAULT_TARGET_LANG = "Urdu"

if st.session_state.get("clear_requested"):
    st.session_state["user_text"] = ""
    st.session_state["source_select"] = DEFAULT_SOURCE_LANG
    st.session_state["target_select"] = DEFAULT_TARGET_LANG
    st.session_state["clear_requested"] = False

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:
    st.markdown("# 🌍 AI Translator")
    st.markdown(
        "Translate text between multiple languages using AI-powered translation."
    )
    st.markdown("---")

    st.markdown("""
    <div class="sidebar-card">
    <b>✨ Features</b><br>
    🌐 Auto Detect Language<br>
    🔊 Text-to-Speech<br>
    🌍 Multiple Languages<br>
    ⚡ Fast Translation
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 22px;"></div>', unsafe_allow_html=True)
    st.markdown("**⚙️ Built with**")
    st.markdown("""
    <span class="tech-pill">Streamlit</span>
    <span class="tech-pill">Deep Translator</span>
    <span class="tech-pill">gTTS</span>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🗑️  Clear", use_container_width=True):
        st.session_state["clear_requested"] = True
        st.rerun()

# ---------------------------------
# Header
# ---------------------------------
st.markdown(
    '<div class="hero-title">🌍 <span class="gradient-text">AI Language Translator</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">Translate text from one language to another.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------
# Text Input
# ---------------------------------
user_text = st.text_area(
    "Enter Text",
    height=150,
    placeholder="Type something here...",
    max_chars=2000,
    key="user_text",
)
st.markdown(
    f'<div class="char-count">{len(user_text)}/2000</div>',
    unsafe_allow_html=True,
)

# ---------------------------------
# Language Dictionaries
# ---------------------------------
languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Arabic": "ar",
    "Hindi": "hi",
}

language_names = {
    "en": "English",
    "ur": "Urdu",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "zh": "Chinese",
    "ja": "Japanese",
    "ar": "Arabic",
    "hi": "Hindi",
}

tts_languages = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh",
    "Japanese": "ja",
    "Arabic": "ar",
    "Hindi": "hi",
}

# ---------------------------------
# Language Selection
# ---------------------------------
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "From",
        list(languages.keys()),
        index=0,
        key="source_select",
    )

with col2:
    target_options = [l for l in languages.keys() if l != "Auto Detect"]
    target_lang = st.selectbox(
        "To",
        target_options,
        index=1,
        key="target_select",
    )

# ---------------------------------
# Translate Button
# ---------------------------------
if st.button("🔄 Translate"):

    if not user_text.strip():
        st.warning("Please enter some text to translate.")

    else:
        try:
            with st.spinner("Translating..."):

                # Detect language only for Auto Detect and 3+ words
                detected_language = None

                if source_lang == "Auto Detect":
                    if len(user_text.split()) >= 3:
                        punct_to_space = str.maketrans(
                            string.punctuation, " " * len(string.punctuation)
                        )
                        detection_text = " ".join(
                            user_text.translate(punct_to_space).split()
                        )
                        detected_code, confidence = langid.classify(detection_text)
                        detected_language = language_names.get(
                            detected_code.lower(), detected_code
                        )

                # Translate
                translated_text = GoogleTranslator(
                    source=languages[source_lang],
                    target=languages[target_lang],
                ).translate(user_text)

            if detected_language:
                badge_html = f'<span class="detected-badge">🌐 Detected Language: {detected_language}</span>'
            elif source_lang == "Auto Detect":
                badge_html = '<span class="detected-badge">🌐 Detected Language: needs 3+ words to detect</span>'
            else:
                badge_html = ""
            result_html = f"""
            <div class="result-card">
                {badge_html}
                <div class="result-label">Translated Text</div>
                <div class="result-text">{translated_text}</div>
            </div>
            """
            st.markdown(result_html, unsafe_allow_html=True)

            # Text-to-Speech
            if target_lang in tts_languages:
                tts = gTTS(text=translated_text, lang=tts_languages[target_lang])
                audio_file = "translated.mp3"
                tts.save(audio_file)

                with open(audio_file, "rb") as file:
                    st.audio(file.read())

                if os.path.exists(audio_file):
                    os.remove(audio_file)

        except Exception as e:
            st.error(f"Translation failed: {e}")