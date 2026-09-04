import urllib.parse

import streamlit as st

import theme
from questions import SECTIONS
from rankings_data import load_dataframe, search, composite_score, SOURCES
from gemini_client import generate_report
from report_generator import to_markdown, to_pdf_bytes

st.set_page_config(page_title="Avenor — Study Abroad Dossier", page_icon="🜂", layout="centered", initial_sidebar_state="collapsed")
theme.inject()

if "page" not in st.session_state:
    st.session_state.page = "assessment"
if "step" not in st.session_state:
    st.session_state.step = 0
if "report" not in st.session_state:
    st.session_state.report = None
if "selected_universities" not in st.session_state:
    st.session_state.selected_universities = []


def field_key(key: str) -> str:
    return f"f_{key}"


def collect_answers() -> dict:
    answers = {}
    for _, _, fields in SECTIONS:
        for key, label, _ in fields:
            answers[label] = st.session_state.get(field_key(key), "")
    return answers


def render_field(key: str, label: str, spec: str):
    fk = field_key(key)
    parts = spec.split("|")
    kind = parts[0]
    st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
    if kind == "text":
        st.text_input(label, key=fk, label_visibility="collapsed")
    elif kind == "textarea":
        st.text_area(label, key=fk, label_visibility="collapsed", height=90)
    elif kind == "select":
        st.selectbox(label, options=parts[1:], key=fk, label_visibility="collapsed")
    elif kind == "multiselect":
        st.multiselect(label, options=parts[1:], key=fk, label_visibility="collapsed")
    elif kind == "slider":
        lo, hi = int(parts[1]), int(parts[2])
        st.slider(label, min_value=lo, max_value=hi, value=(lo + hi) // 2, key=fk, label_visibility="collapsed")


def heuristic_fallback(answers: dict) -> dict:
    numeric_vals = [v for v in answers.values() if isinstance(v, int)]
    avg = sum(numeric_vals) / len(numeric_vals) if numeric_vals else 5
    score = int(min(100, max(10, avg * 9)))
    return {
        "overall_score": score,
        "verdict": "Offline preview — connect Gemini for a full dossier",
        "summary": "This is a locally generated placeholder summary. No Gemini API key was available, so scoring is derived from questionnaire sliders only, without qualitative analysis of your written answers.",
        "strengths": ["Questionnaire completed in full", "Self-assessed discipline and adaptability captured"],
        "risks": ["No AI-driven analysis of written answers yet", "Financial and country-fit reasoning not yet generated"],
        "financial_reality_check": "Add a Gemini API key in the sidebar to generate a grounded financial reality check based on your stated budget and funding sources.",
        "recommended_pathways": [],
        "country_fit": [],
        "immediate_next_steps": ["Add a Gemini API key in the sidebar", "Re-generate the dossier for a full assessment"],
        "single_most_important_risk": "This preview does not reflect your actual answers in depth — treat it as a placeholder only.",
    }


def nav():
    cols = st.columns(3)
    labels = [("assessment", "Assessment"), ("comparator", "University Comparator"), ("report", "Dossier")]
    for col, (key, label) in zip(cols, labels):
        with col:
            active = st.session_state.page == key
            if st.button(("● " if active else "") + label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()


with st.sidebar:
    st.markdown("#### Gemini API")
    default_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
    api_key = st.text_input("API key", value=default_key, type="password")
    st.caption("Stored only for this session. Add GEMINI_API_KEY to .streamlit/secrets.toml to skip this on deploy.")

theme.mark("Avenor", "Study Abroad Assessment", "A rigorous, honest dossier on your readiness to study abroad")
nav()
st.markdown('<hr class="dossier-divider">', unsafe_allow_html=True)

if st.session_state.page == "assessment":
    total = len(SECTIONS)
    step = st.session_state.step
    theme.stamps(total, step)

    num, title, fields = SECTIONS[step]
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    theme.section_header(num, title)
    for key, label, spec in fields:
        render_field(key, label, spec)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if step > 0 and st.button("← Back", use_container_width=True):
            st.session_state.step -= 1
            st.rerun()
    with c3:
        if step < total - 1:
            if st.button("Continue →", use_container_width=True):
                st.session_state.step += 1
                st.rerun()
        else:
            st.markdown('<div class="primary-cta">', unsafe_allow_html=True)
            if st.button("Generate Dossier", use_container_width=True):
                answers = collect_answers()
                with st.spinner("Compiling your assessment..."):
                    if api_key:
                        try:
                            st.session_state.report = generate_report(answers, api_key)
                        except Exception as exc:
                            st.error(f"Gemini request failed: {exc}")
                            st.session_state.report = heuristic_fallback(answers)
                    else:
                        st.session_state.report = heuristic_fallback(answers)
                st.session_state.page = "report"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "comparator":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    theme.section_header("★", "University Ranking Comparator")
    st.caption("Sample dataset for demonstration — refresh with official QS / THE / ARWU / US News / CWUR data before relying on it.")
    df = load_dataframe()
    query = st.text_input("Search university or country", label_visibility="collapsed", placeholder="Search university or country")
    filtered = search(df, query)
    options = filtered["University"].tolist()
    chosen = st.multiselect("Select up to 4 universities to compare", options=options, default=st.session_state.selected_universities, max_selections=4)
    st.session_state.selected_universities = chosen
    st.markdown("</div>", unsafe_allow_html=True)

    if chosen:
        subset = df[df["University"].isin(chosen)].copy()
        subset["Composite"] = subset.apply(composite_score, axis=1).round(1)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.dataframe(subset[["University", "Country"] + SOURCES + ["Composite"]].set_index("University"), use_container_width=True)
        st.bar_chart(subset.set_index("University")["Composite"])
        st.caption("Composite is the mean rank across available sources — lower is better.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Search and select universities above to compare them side by side.")

elif st.session_state.page == "report":
    report = st.session_state.report
    if not report:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("No dossier generated yet. Complete the assessment first.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        cols = st.columns([1, 2])
        with cols[0]:
            st.markdown(f'<div class="score-ring">{report.get("overall_score","–")}</div>', unsafe_allow_html=True)
            st.markdown('<div class="score-caption">Overall Score</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f'<span class="verdict-chip">{report.get("verdict","")}</span>', unsafe_allow_html=True)
            st.write(report.get("summary", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            theme.section_header("+", "Strengths")
            for s in report.get("strengths", []):
                st.markdown(f"- {s}")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            theme.section_header("!", "Risks")
            for r in report.get("risks", []):
                st.markdown(f"- {r}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        theme.section_header("$", "Financial Reality Check")
        st.write(report.get("financial_reality_check", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        if report.get("recommended_pathways"):
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            theme.section_header("→", "Recommended Pathways")
            for p in report["recommended_pathways"]:
                st.markdown(f"**{p.get('path','')}**  \n{p.get('why','')}  \n*Timeline: {p.get('timeline','')}*")
                st.markdown('<hr class="dossier-divider">', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if report.get("country_fit"):
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            theme.section_header("◎", "Country / Region Fit")
            for c in report["country_fit"]:
                st.markdown(f"**{c.get('region_or_country','')}** — {c.get('fit_score','')}/100  \n{c.get('reason','')}")
                st.markdown('<hr class="dossier-divider">', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        theme.section_header("✓", "Immediate Next Steps")
        for i, step in enumerate(report.get("immediate_next_steps", []), 1):
            st.markdown(f"{i}. {step}")
        st.markdown('<hr class="dossier-divider">', unsafe_allow_html=True)
        st.markdown(f"**Single most important risk:** {report.get('single_most_important_risk','')}")
        st.markdown("</div>", unsafe_allow_html=True)

        name = st.session_state.get(field_key("preferred_name"), "Candidate")
        df = load_dataframe()
        universities = df[df["University"].isin(st.session_state.selected_universities)].to_dict("records") if st.session_state.selected_universities else None

        md_text = to_markdown(name, report, universities)
        pdf_bytes = to_pdf_bytes(name, report, universities)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        theme.section_header("⇩", "Export & Share")
        d1, d2, d3 = st.columns(3)
        with d1:
            st.download_button("Download Markdown", data=md_text, file_name="avenor_dossier.md", mime="text/markdown", use_container_width=True)
        with d2:
            st.download_button("Download PDF", data=pdf_bytes, file_name="avenor_dossier.pdf", mime="application/pdf", use_container_width=True)
        with d3:
            subject = urllib.parse.quote(f"Avenor Dossier — {name}")
            body = urllib.parse.quote(md_text[:1800] + ("\n\n[Truncated — attach the downloaded PDF for the full dossier]" if len(md_text) > 1800 else ""))
            mailto = f"mailto:?subject={subject}&body={body}"
            st.link_button("Email Dossier", mailto, use_container_width=True)
        st.caption("Email opens a pre-filled draft in your mail client — attach the downloaded PDF manually before sending.")
        st.markdown("</div>", unsafe_allow_html=True)
