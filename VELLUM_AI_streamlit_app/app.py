import streamlit as st

from src.questions import SECTIONS
from src.ai import analyze


st.set_page_config(
    page_title="AVENOR Student Advisor",
    page_icon="◈",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f7faff, #ffffff 45%);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 34px;
        border: 1px solid #e7ebf3;
        border-radius: 24px;
        background: linear-gradient(135deg, #ffffff, #edf4ff);
        box-shadow: 0 18px 60px rgba(20, 35, 70, 0.08);
        margin-bottom: 18px;
    }

    .badge {
        display: inline-block;
        background: #172033;
        color: #ffffff;
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 12px;
        letter-spacing: 0.08em;
    }

    .section-number {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <span class="badge">AVENOR · STRICT ADVISORY ENGINE</span>
        <h1>Student & International Education Advisor</h1>
        <p>
            Career fit • degrees • scholarships • countries •
            university strategy • reality checks
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("A Project of Avenor · Made by Muhammad Talal Irfan")


if "profile" not in st.session_state:
    st.session_state.profile = {}

if "report" not in st.session_state:
    st.session_state.report = None


def parse_question_spec(spec):
    """
    Convert the compact question definition used by questions.py
    into a question type and its optional choices/range.
    """

    if not isinstance(spec, str):
        return "text", None

    parts = spec.split("|")
    kind = parts[0].strip().lower()

    if kind in {"text", "textarea"}:
        return kind, None

    if kind in {"select", "multiselect"}:
        return kind, parts[1:]

    if kind == "slider":
        if len(parts) >= 3:
            try:
                return "slider", (int(parts[1]), int(parts[2]))
            except ValueError:
                pass

    return "text", None


for section_id, title, questions in SECTIONS:

    st.markdown(
        f'<div class="section-number">SECTION {section_id}</div>',
        unsafe_allow_html=True,
    )

    st.header(title)

    with st.container(border=True):

        for key, label, spec in questions:

            kind, options = parse_question_spec(spec)
            old = st.session_state.profile.get(key)

            if kind == "text":

                value = st.text_input(
                    label,
                    value=old or "",
                    key=f"input_{key}",
                )

            elif kind == "textarea":

                value = st.text_area(
                    label,
                    value=old or "",
                    key=f"input_{key}",
                )

            elif kind == "select":

                choices = options or [""]

                current_index = (
                    choices.index(old)
                    if old in choices
                    else 0
                )

                value = st.selectbox(
                    label,
                    choices,
                    index=current_index,
                    key=f"input_{key}",
                )

            elif kind == "multiselect":

                choices = options or []

                default = [
                    item
                    for item in (old or [])
                    if item in choices
                ]

                value = st.multiselect(
                    label,
                    choices,
                    default=default,
                    key=f"input_{key}",
                )

            elif kind == "slider":

                low, high = options
                default = int(old) if old is not None else (low + high) // 2

                value = st.slider(
                    label,
                    min_value=low,
                    max_value=high,
                    value=default,
                    key=f"input_{key}",
                )

            else:

                value = st.text_input(
                    label,
                    value=old or "",
                    key=f"input_{key}",
                )

            st.session_state.profile[key] = value

    st.divider()


st.subheader("Ready for your assessment?")

if st.button(
    "Run AVENOR Assessment",
    type="primary",
    use_container_width=True,
):

    with st.spinner(
        "Running strict assessment + current research grounding..."
    ):

        try:
            st.session_state.report = analyze(
                st.session_state.profile
            )

        except Exception as exc:
            st.error(
                f"Assessment failed: {exc}"
            )


if st.session_state.report:

    st.markdown("---")
    st.header("AVENOR Assessment")

    st.markdown(st.session_state.report)

    st.download_button(
        "Download Report",
        st.session_state.report,
        file_name="avenor_assessment.md",
        mime="text/markdown",
        use_container_width=True,
    )
