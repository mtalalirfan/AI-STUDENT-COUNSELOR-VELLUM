import streamlit as st
from urllib.parse import quote

from src.questions import SECTIONS
from src.ai import analyze
from src.config import secret


st.set_page_config(
    page_title="VELLUM AI — Student Advisor",
    page_icon="◈",
    layout="wide",
)


st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f6f9ff 0%, #ffffff 50%, #f8faff 100%);
}

.block-container {
    max-width: 1180px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

.hero {
    padding: 38px;
    border: 1px solid #e5eaf3;
    border-radius: 26px;
    background: linear-gradient(135deg, #ffffff, #edf4ff);
    box-shadow: 0 18px 55px rgba(20, 35, 70, .08);
    margin-bottom: 18px;
}

.badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: #172033;
    color: white;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .08em;
}

.hero h1 {
    margin: 18px 0 8px;
    font-size: 42px;
    line-height: 1.1;
}

.hero p {
    margin: 0;
    color: #586174;
    font-size: 17px;
}

.section-title {
    margin-top: 28px;
}

.email-button {
    display: block;
    width: 100%;
    padding: 13px 20px;
    margin-top: 10px;
    border-radius: 12px;
    background: #172033;
    color: white !important;
    text-align: center;
    text-decoration: none !important;
    font-weight: 700;
}

.email-button:hover {
    background: #293650;
}

.footer {
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid #e5eaf3;
    color: #697386;
    text-align: center;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <span class="badge">VELLUM AI · STRICT ADVISORY ENGINE</span>
    <h1>Student & International Education Advisor</h1>
    <p>
        Career fit • degrees • scholarships • countries • university strategy • reality checks
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("A Project of Avenor · Made by Muhammad Talal Irfan")


if "profile" not in st.session_state:
    st.session_state.profile = {}

if "report" not in st.session_state:
    st.session_state.report = ""


for section_id, title, questions in SECTIONS:

    st.markdown(
        f'<h2 class="section-title">{section_id} · {title}</h2>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        for question in questions:

            key, label, definition = question

            parts = definition.split("|")
            kind = parts[0]
            options = parts[1:]

            old = st.session_state.profile.get(key)

            if kind == "text":
                value = st.text_input(label, value=old or "")

            elif kind == "textarea":
                value = st.text_area(label, value=old or "")

            elif kind == "select":
                index = options.index(old) if old in options else 0
                value = st.selectbox(
                    label,
                    options,
                    index=index,
                    key=f"select_{key}",
                )

            elif kind == "multiselect":
                default = [
                    item for item in (old or [])
                    if item in options
                ]

                value = st.multiselect(
                    label,
                    options,
                    default=default,
                    key=f"multi_{key}",
                )

            elif kind == "slider":
                low = int(options[0])
                high = int(options[1])

                default = (
                    int(old)
                    if old is not None
                    else (low + high) // 2
                )

                value = st.slider(
                    label,
                    low,
                    high,
                    default,
                    key=f"slider_{key}",
                )

            else:
                value = st.text_input(
                    label,
                    value=old or "",
                    key=f"fallback_{key}",
                )

            st.session_state.profile[key] = value


st.divider()


if st.button(
    "Run VELLUM AI Assessment",
    type="primary",
    use_container_width=True,
):

    with st.spinner(
        "VELLUM AI is analysing your profile and researching relevant information..."
    ):

        try:
            st.session_state.report = analyze(
                st.session_state.profile
            )

        except Exception as error:
            st.session_state.report = ""
            st.error(
                f"VELLUM AI could not complete the assessment: {error}"
            )


if st.session_state.report:

    st.markdown("## Your VELLUM AI Assessment")

    st.markdown(st.session_state.report)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download Assessment",
            st.session_state.report,
            "vellum_ai_assessment.md",
            "text/markdown",
            use_container_width=True,
        )

    recipient = secret("VELLUM_EMAIL", "")

    if recipient:

        subject = "VELLUM AI Student Assessment"

        body = f"""Hello,

I am sending my VELLUM AI Student Assessment.

Assessment result:

{st.session_state.report}

Generated by VELLUM AI.
A Project of Avenor · Made by Muhammad Talal Irfan
"""

        gmail_url = (
            "https://mail.google.com/mail/"
            "?view=cm"
            "&fs=1"
            f"&to={quote(recipient)}"
            f"&su={quote(subject)}"
            f"&body={quote(body[:12000])}"
        )

        with col2:
            st.markdown(
                f"""
                <a class="email-button"
                   href="{gmail_url}"
                   target="_blank">
                    Open Gmail & Email Assessment
                </a>
                """,
                unsafe_allow_html=True,
            )

        st.caption(
            "Gmail opens with the recipient, subject and assessment "
            "already filled in. Review the message and press Send."
        )

    else:
        with col2:
            st.warning(
                "Add VELLUM_EMAIL to Streamlit Secrets to enable Gmail sharing."
            )


st.markdown(
    """
    <div class="footer">
        VELLUM AI · A Project of Avenor · Made by Muhammad Talal Irfan
    </div>
    """,
    unsafe_allow_html=True,
)
