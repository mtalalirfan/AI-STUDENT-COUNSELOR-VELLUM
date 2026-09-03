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

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 0%,
                rgba(99, 102, 241, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 92% 8%,
                rgba(14, 165, 233, 0.07),
                transparent 25%
            ),
            linear-gradient(
                180deg,
                #f7faff 0%,
                #ffffff 45%,
                #f8fafc 100%
            );
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.25rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .vellum-hero {
        position: relative;
        overflow: hidden;

        padding: 44px 46px;
        margin-bottom: 16px;

        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 28px;

        background:
            linear-gradient(
                135deg,
                rgba(255, 255, 255, 0.98),
                rgba(239, 246, 255, 0.96)
            );

        box-shadow:
            0 25px 70px rgba(15, 23, 42, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }

    .vellum-hero::after {
        content: "";

        position: absolute;

        width: 320px;
        height: 320px;

        right: -130px;
        top: -145px;

        border-radius: 50%;

        background: rgba(99, 102, 241, 0.065);

        filter: blur(4px);
    }


    /* ========================================================
       BRAND BADGE
       ======================================================== */

    .vellum-badge {
        display: inline-block;

        position: relative;
        z-index: 2;

        padding: 8px 15px;

        border-radius: 999px;

        background: #172033;

        color: #ffffff;

        font-size: 11px;
        font-weight: 750;

        letter-spacing: 0.11em;
        text-transform: uppercase;
    }


    /* ========================================================
       HERO TYPOGRAPHY
       ======================================================== */

    .vellum-hero h1 {
        position: relative;
        z-index: 2;

        margin: 20px 0 10px;

        color: #111827;

        font-size: clamp(
            2.15rem,
            4vw,
            3.45rem
        );

        line-height: 1.04;

        letter-spacing: -0.045em;

        font-weight: 800;
    }

    .vellum-hero p {
        position: relative;
        z-index: 2;

        max-width: 850px;

        margin: 0;

        color: #64748b;

        font-size: 1rem;

        line-height: 1.7;
    }


    /* ========================================================
       ATTRIBUTION
       ======================================================== */

    .vellum-attribution {
        margin: 7px 0 24px;

        color: #64748b;

        font-size: 0.82rem;

        letter-spacing: 0.01em;
    }


    /* ========================================================
       SECTION LABEL
       ======================================================== */

    .vellum-section-label {
        margin-top: 12px;
        margin-bottom: -7px;

        color: #64748b;

        font-size: 0.72rem;

        font-weight: 800;

        letter-spacing: 0.13em;

        text-transform: uppercase;
    }


    /* ========================================================
       SECTION CARDS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;

        border: 1px solid #e5e7eb !important;

        background:
            rgba(255, 255, 255, 0.84) !important;

        box-shadow:
            0 12px 35px rgba(15, 23, 42, 0.045) !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] {
        border-radius: 11px;
    }

    input,
    textarea {
        border-radius: 10px !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        min-height: 48px;

        border-radius: 13px;

        font-weight: 700;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 10px 25px rgba(15, 23, 42, 0.10);
    }


    /* ========================================================
       ASSESSMENT HEADER
       ======================================================== */

    .vellum-assessment {
        padding: 22px 25px;

        margin-top: 24px;
        margin-bottom: 20px;

        border-radius: 19px;

        background:
            linear-gradient(
                135deg,
                #172033,
                #263449
            );

        color: #ffffff;

        box-shadow:
            0 18px 42px rgba(15, 23, 42, 0.14);
    }

    .vellum-assessment h2 {
        margin: 0;

        color: #ffffff;

        font-size: 1.5rem;
    }

    .vellum-assessment p {
        margin: 5px 0 0;

        color: #cbd5e1;

        font-size: 0.88rem;
    }


    /* ========================================================
       INFO CARD
       ======================================================== */

    .vellum-info {
        padding: 17px 20px;

        margin: 18px 0;

        border: 1px solid #e2e8f0;

        border-radius: 15px;

        background: rgba(248, 250, 252, 0.85);

        color: #475569;

        font-size: 0.88rem;

        line-height: 1.6;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .vellum-footer {
        margin-top: 50px;

        padding-top: 22px;

        border-top: 1px solid #e5e7eb;

        color: #94a3b8;

        text-align: center;

        font-size: 0.76rem;

        line-height: 1.7;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .vellum-hero {
            padding: 30px 24px;
            border-radius: 22px;
        }

        .vellum-hero h1 {
            font-size: 2.05rem;
        }

        .vellum-hero p {
            font-size: 0.92rem;
        }
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

        <span class="vellum-badge">
            VELLUM AI · STRICT ADVISORY ENGINE
        </span>

        <h1>
            Student & International Education Advisor
        </h1>

        <p>
            Career fit • degrees • scholarships • countries •
            university strategy • reality checks
        </p>

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
# SESSION STATE
# ============================================================

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "report" not in st.session_state:
    st.session_state.report = None


# ============================================================
# FLEXIBLE SECTION NORMALIZER
# ============================================================

def normalize_section(section):
    """
    Supports both section formats:

        (title, questions)

    and:

        (section_id, title, questions)
    """

    if not isinstance(section, (tuple, list)):
        raise ValueError(
            "Invalid section definition. "
            "Each section must be a tuple/list."
        )

    if len(section) == 3:
        section_id, title, questions = section

        return (
            str(section_id),
            str(title),
            questions,
        )

    if len(section) == 2:
        title, questions = section

        return (
            "",
            str(title),
            questions,
        )

    raise ValueError(
        "Invalid section definition. "
        f"Expected 2 or 3 values, received {len(section)}."
    )


# ============================================================
# FLEXIBLE QUESTION NORMALIZER
# ============================================================

def normalize_question(question):
    """
    Supports:

        (key, label, spec)

    and:

        (key, label, kind, options)

    Example specification:

        text

        textarea

        select|Option A|Option B|Option C

        multiselect|Option A|Option B|Option C

        slider|1|10
    """

    if not isinstance(question, (tuple, list)):
        raise ValueError(
            "Invalid question definition. "
            "Each question must be a tuple/list."
        )

    # --------------------------------------------------------
    # Modern compact format
    # --------------------------------------------------------

    if len(question) == 3:

        key, label, specification = question

        key = str(key)
        label = str(label)

        if not isinstance(specification, str):
            return (
                key,
                label,
                "text",
                None,
            )

        parts = [
            item.strip()
            for item in specification.split("|")
        ]

        kind = parts[0].lower()

        options = parts[1:]

        # Slider
        if kind == "slider":

            if len(options) >= 2:

                try:
                    low = int(options[0])
                    high = int(options[1])

                    return (
                        key,
                        label,
                        "slider",
                        (low, high),
                    )

                except ValueError:
                    return (
                        key,
                        label,
                        "slider",
                        (0, 10),
                    )

            return (
                key,
                label,
                "slider",
                (0, 10),
            )

        return (
            key,
            label,
            kind,
            options,
        )

    # --------------------------------------------------------
    # Legacy explicit format
    # --------------------------------------------------------

    if len(question) == 4:

        key, label, kind, options = question

        return (
            str(key),
            str(label),
            str(kind).lower(),
            options,
        )

    raise ValueError(
        "Invalid question definition. "
        f"Expected 3 or 4 values, received {len(question)}."
    )


# ============================================================
# QUESTIONNAIRE
# ============================================================

total_questions = 0

for raw_section in SECTIONS:

    _, _, questions = normalize_section(raw_section)

    total_questions += len(questions)


answered_questions = len(
    [
        key
        for key, value in st.session_state.profile.items()
        if value not in ("", None, [])
    ]
)


# ============================================================
# PROGRESS
# ============================================================

if total_questions > 0:

    progress = min(
        answered_questions / total_questions,
        1.0,
    )

    st.progress(
        progress,
        text=(
            f"Profile completion: "
            f"{int(progress * 100)}%"
        ),
    )


# ============================================================
# RENDER SECTIONS
# ============================================================

for raw_section in SECTIONS:

    section_id, title, questions = normalize_section(
        raw_section
    )

    # --------------------------------------------------------
    # Section number
    # --------------------------------------------------------

    if section_id:

        st.markdown(
            f"""
            <div class="vellum-section-label">
                Section {section_id}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.header(title)

    # --------------------------------------------------------
    # Section card
    # --------------------------------------------------------

    with st.container(border=True):

        for raw_question in questions:

            key, label, kind, options = normalize_question(
                raw_question
            )

            old_value = (
                st.session_state.profile.get(key)
            )

            widget_key = f"vellum_{key}"

            # =================================================
            # TEXT
            # =================================================

            if kind == "text":

                value = st.text_input(
                    label,
                    value=old_value or "",
                    key=widget_key,
                )

            # =================================================
            # TEXTAREA
            # =================================================

            elif kind == "textarea":

                value = st.text_area(
                    label,
                    value=old_value or "",
                    height=120,
                    key=widget_key,
                )

            # =================================================
            # SELECT
            # =================================================

            elif kind == "select":

                choices = list(
                    options or []
                )

                if not choices:
                    choices = [
                        "Not specified"
                    ]

                current_index = (
                    choices.index(old_value)
                    if old_value in choices
                    else 0
                )

                value = st.selectbox(
                    label,
                    choices,
                    index=current_index,
                    key=widget_key,
                )

            # =================================================
            # MULTISELECT
            # =================================================

            elif kind == "multiselect":

                choices = list(
                    options or []
                )

                previous = (
                    old_value
                    if isinstance(old_value, list)
                    else []
                )

                defaults = [
                    item
                    for item in previous
                    if item in choices
                ]

                value = st.multiselect(
                    label,
                    choices,
                    default=defaults,
                    key=widget_key,
                )

            # =================================================
            # SLIDER
            # =================================================

            elif kind == "slider":

                if (
                    isinstance(options, tuple)
                    and len(options) == 2
                ):

                    low, high = options

                else:

                    low, high = 0, 10

                try:

                    default_value = (
                        int(old_value)
                        if old_value is not None
                        else (low + high) // 2
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    default_value = (
                        low + high
                    ) // 2

                default_value = max(
                    low,
                    min(
                        default_value,
                        high,
                    ),
                )

                value = st.slider(
                    label,
                    min_value=low,
                    max_value=high,
                    value=default_value,
                    key=widget_key,
                )

            # =================================================
            # UNKNOWN TYPE
            # =================================================

            else:

                value = st.text_input(
                    label,
                    value=old_value or "",
                    key=widget_key,
                )

            # ------------------------------------------------
            # SAVE RESPONSE
            # ------------------------------------------------

            st.session_state.profile[key] = value


# ============================================================
# ASSESSMENT AREA
# ============================================================

st.divider()

st.markdown(
    """
    <div class="vellum-assessment">

        <h2>
            Ready for your VELLUM AI assessment?
        </h2>

        <p>
            Your answers will be evaluated to produce a
            structured education, career and international
            study advisory report.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ACTION BUTTONS
# ============================================================

col1, col2 = st.columns(
    [4, 1]
)


with col1:

    run_assessment = st.button(
        "Run VELLUM AI Assessment",
        type="primary",
        use_container_width=True,
    )


with col2:

    reset_profile = st.button(
        "Reset",
        use_container_width=True,
    )


# ============================================================
# RESET
# ============================================================

if reset_profile:

    st.session_state.profile = {}
    st.session_state.report = None

    st.rerun()


# ============================================================
# RUN AI ASSESSMENT
# ============================================================

if run_assessment:

    if not st.session_state.profile:

        st.warning(
            "Please complete your profile before "
            "running the assessment."
        )

    else:

        with st.spinner(
            "VELLUM AI is analysing your profile "
            "and generating your advisory report..."
        ):

            try:

                result = analyze(
                    st.session_state.profile
                )

                if not result:

                    raise ValueError(
                        "The AI returned an empty assessment."
                    )

                st.session_state.report = result

            except Exception as exc:

                st.session_state.report = None

                st.error(
                    "VELLUM AI could not complete the assessment."
                )

                st.exception(exc)


# ============================================================
# DISPLAY REPORT
# ============================================================

if st.session_state.get("report"):

    st.markdown(
        """
        <div class="vellum-assessment">

            <h2>
                VELLUM AI Assessment
            </h2>

            <p>
                Your personalized advisory analysis
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        st.session_state.report
    )

    st.download_button(
        label="Download VELLUM AI Report",
        data=st.session_state.report,
        file_name="vellum_ai_assessment.md",
        mime="text/markdown",
        use_container_width=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="vellum-footer">

        <strong>VELLUM AI</strong> ·
        Student & International Education Advisor

        <br>

        A Project by Avenor ·
        Made by Muhammad Talal Irfan

    </div>
    """,
    unsafe_allow_html=True,
)
