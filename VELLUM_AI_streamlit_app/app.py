import urllib.parse
import streamlit as st

from src.questions import SECTIONS
from src.ai import analyze

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="VELLUM AI — Student & International Education Advisor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# PREMIUM VELLUM AI DESIGN SYSTEM
# ============================================================
st.markdown(
    """
    <style>
    /* GLOBAL */
    .stApp {
        background: radial-gradient(circle at 8% 0%, rgba(99, 102, 241, 0.08), transparent 28%),
                    radial-gradient(circle at 92% 8%, rgba(14, 165, 233, 0.07), transparent 25%),
                    linear-gradient(180deg, #f7faff 0%, #ffffff 45%, #f8fafc 100%);
    }
    .block-container {
        max-width: 1180px;
        padding-top: 2.25rem;
        padding-bottom: 4rem;
    }

    /* HERO */
    .vellum-hero {
        position: relative;
        overflow: hidden;
        padding: 44px 46px;
        margin-bottom: 16px;
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(239, 246, 255, 0.96));
        box-shadow: 0 25px 70px rgba(15, 23, 42, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    .vellum-hero::after {
        content: "";
        position: absolute;
        width: 320px; height: 320px;
        right: -130px; top: -145px;
        border-radius: 50%;
        background: rgba(99, 102, 241, 0.065);
        filter: blur(4px);
    }

    /* BRAND BADGE */
    .vellum-badge {
        display: inline-block;
        position: relative; z-index: 2;
        padding: 8px 15px; border-radius: 999px;
        background: #172033; color: #ffffff;
        font-size: 11px; font-weight: 750;
        letter-spacing: 0.11em; text-transform: uppercase;
    }

    /* TYPOGRAPHY */
    .vellum-hero h1 {
        position: relative; z-index: 2;
        margin: 20px 0 10px; color: #111827;
        font-size: clamp(2.15rem, 4vw, 3.45rem);
        line-height: 1.04; letter-spacing: -0.045em; font-weight: 800;
    }
    .vellum-hero p {
        position: relative; z-index: 2;
        max-width: 850px; margin: 0;
        color: #64748b; font-size: 1rem; line-height: 1.7;
    }
    .vellum-attribution {
        margin: 7px 0 24px; color: #64748b; font-size: 0.82rem; letter-spacing: 0.01em;
    }
    .vellum-section-label {
        margin-top: 12px; margin-bottom: -7px;
        color: #64748b; font-size: 0.72rem; font-weight: 800;
        letter-spacing: 0.13em; text-transform: uppercase;
    }

    /* CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border: 1px solid #e5e7eb !important;
        background: rgba(255, 255, 255, 0.84) !important;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.045) !important;
    }

    /* INPUTS & DARK MODE OVERRIDE */
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] {
        border-radius: 11px;
    }
    input, textarea, div[data-baseweb="select"] > div, ul[data-baseweb="menu"] {
        border-radius: 10px !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* BUTTONS */
    .stButton > button {
        min-height: 48px; border-radius: 13px; font-weight: 700;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.10);
    }

    /* HEADERS & FOOTERS */
    .vellum-assessment {
        padding: 22px 25px; margin-top: 24px; margin-bottom: 20px;
        border-radius: 19px; background: linear-gradient(135deg, #172033, #263449);
        color: #ffffff; box-shadow: 0 18px 42px rgba(15, 23, 42, 0.14);
    }
    .vellum-assessment h2 {
        margin: 0; color: #ffffff; font-size: 1.5rem;
    }
    .vellum-assessment p {
        margin: 5px 0 0; color: #cbd5e1; font-size: 0.88rem;
    }
    .vellum-footer {
        margin-top: 50px; padding-top: 22px; border-top: 1px solid #e5e7eb;
        color: #94a3b8; text-align: center; font-size: 0.76rem; line-height: 1.7;
    }

    @media (max-width: 700px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .vellum-hero { padding: 30px 24px; border-radius: 22px; }
        .vellum-hero h1 { font-size: 2.05rem; }
        .vellum-hero p { font-size: 0.92rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# VELLUM AI HERO
# ============================================================
st.markdown(
    """
    <div class="vellum-hero">
        <span class="vellum-badge">VELLUM AI · STRICT ADVISORY ENGINE</span>
        <h1>Student & International Education Advisor</h1>
        <p>Career fit • degrees • scholarships • countries • university strategy • reality checks</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="vellum-attribution">
        A Project by Avenor · Made by Muhammad Talal Irfan
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE & HELPERS
# ============================================================
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "report" not in st.session_state:
    st.session_state.report = None

def normalize_section(section):
    if not isinstance(section, (tuple, list)):
        raise ValueError("Invalid section definition.")
    if len(section) == 3:
        return str(section[0]), str(section[1]), section[2]
    if len(section) == 2:
        return "", str(section[0]), section[1]
    raise ValueError("Invalid section definition.")

def normalize_question(question):
    if not isinstance(question, (tuple, list)):
        raise ValueError("Invalid question definition.")
    if len(question) == 3:
        key, label, spec = question
        key, label = str(key), str(label)
        if not isinstance(spec, str): return key, label, "text", None
        parts = [item.strip() for item in spec.split("|")]
        kind = parts[0].lower()
        options = parts[1:]
        if kind == "slider":
            try: return key, label, "slider", (int(options[0]), int(options[1])) if len(options) >= 2 else (0, 10)
            except ValueError: return key, label, "slider", (0, 10)
        return key, label, kind, options
    if len(question) == 4:
        return str(question[0]), str(question[1]), str(question[2]).lower(), question[3]
    raise ValueError("Invalid question definition.")

# ============================================================
# QUESTIONNAIRE LOGIC
# ============================================================
total_questions = sum(len(normalize_section(sec)[2]) for sec in SECTIONS)
answered = len([k for k, v in st.session_state.profile.items() if v not in ("", None, [])])

if total_questions > 0:
    progress = min(answered / total_questions, 1.0)
    st.progress(progress, text=f"Profile completion: {int(progress * 100)}%")

for raw_section in SECTIONS:
    section_id, title, questions = normalize_section(raw_section)
    if section_id:
        st.markdown(f'<div class="vellum-section-label">Section {section_id}</div>', unsafe_allow_html=True)
    
    st.header(title)
    with st.container(border=True):
        for raw_question in questions:
            key, label, kind, options = normalize_question(raw_question)
            old_value = st.session_state.profile.get(key)
            widget_key = f"vellum_{key}"

            if kind == "text":
                value = st.text_input(label, value=old_value or "", key=widget_key)
            elif kind == "textarea":
                value = st.text_area(label, value=old_value or "", height=120, key=widget_key)
            elif kind == "select":
                choices = list(options or ["Not specified"])
                idx = choices.index(old_value) if old_value in choices else 0
                value = st.selectbox(label, choices, index=idx, key=widget_key)
            elif kind == "multiselect":
                choices = list(options or [])
                prev = old_value if isinstance(old_value, list) else []
                defs = [i for i in prev if i in choices]
                value = st.multiselect(label, choices, default=defs, key=widget_key)
            elif kind == "slider":
                low, high = options if isinstance(options, tuple) and len(options) == 2 else (0, 10)
                try: default_val = int(old_value) if old_value is not None else (low + high) // 2
                except: default_val = (low + high) // 2
                value = st.slider(label, min_value=low, max_value=high, value=default_val, key=widget_key)
            else:
                value = st.text_input(label, value=old_value or "", key=widget_key)

            st.session_state.profile[key] = value

# ============================================================
# ASSESSMENT AREA
# ============================================================
st.divider()
st.markdown(
    """
    <div class="vellum-assessment">
        <h2>Ready for your VELLUM AI assessment?</h2>
        <p>Your answers will be evaluated to produce a structured education, career and international study advisory report.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([4, 1])
with col1:
    run_assessment = st.button("Run VELLUM AI Assessment", type="primary", use_container_width=True)
with col2:
    if st.button("Reset", use_container_width=True):
        st.session_state.profile = {}
        st.session_state.report = None
        st.rerun()

# ============================================================
# RUN AI & DISPLAY REPORT
# ============================================================
if run_assessment:
    if not st.session_state.profile:
        st.warning("Please complete your profile before running the assessment.")
    else:
        with st.spinner("VELLUM AI is analysing your profile and generating your advisory report..."):
            try:
                result = analyze(st.session_state.profile)
                if not result: raise ValueError("The AI returned an empty assessment.")
                st.session_state.report = result
            except Exception as exc:
                st.session_state.report = None
                st.error("VELLUM AI could not complete the assessment.")
                st.exception(exc)

if st.session_state.get("report"):
    st.markdown(
        """
        <div class="vellum-assessment">
            <h2>VELLUM AI Assessment</h2>
            <p>Your personalized advisory analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(st.session_state.report)
    
    # Format the email content
    profile_summary = "\n".join([f"{k}: {v}" for k, v in st.session_state.profile.items()])
    email_body = f"Student Profile:\n{profile_summary}\n\n---\n\nVELLUM AI Report:\n{st.session_state.report}"
    
    body_encoded = urllib.parse.quote(email_body)
    subject_encoded = urllib.parse.quote("New VELLUM AI Assessment Result")
    mailto_url = f"mailto:talal.irfan@outlook.com?subject={subject_encoded}&body={body_encoded}"

    col_dl, col_mail = st.columns(2)
    with col_dl:
        st.download_button(
            label="Download VELLUM AI Report",
            data=st.session_state.report,
            file_name="vellum_ai_assessment.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_mail:
        st.markdown(
            f'<a href="{mailto_url}" target="_blank" style="text-decoration:none;">'
            f'<button style="background-color:#172033; color:white; border:none; '
            f'border-radius:13px; padding:12px 24px; cursor:pointer; font-weight:bold; width:100%;">'
            f'✉️ Email Assessment to Admin</button></a>',
            unsafe_allow_html=True
        )

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="vellum-footer">
        <strong>VELLUM AI</strong> · Student & International Education Advisor<br>
        A Project by Avenor · Made by Muhammad Talal Irfan
    </div>
    """,
    unsafe_allow_html=True,
)
