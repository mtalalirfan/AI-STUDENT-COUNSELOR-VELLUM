import streamlit as st
from src.questions import SECTIONS
from src.ai import analyze

st.set_page_config(page_title="AVENOR Student Advisor", page_icon="◈", layout="wide")
st.markdown("""
<style>
.main{background:linear-gradient(180deg,#f7faff,#fff 45%)} .block-container{max-width:1200px;padding-top:2rem}
.hero{padding:34px;border:1px solid #e7ebf3;border-radius:24px;background:linear-gradient(135deg,#fff,#edf4ff);box-shadow:0 18px 60px rgba(20,35,70,.08)}
.badge{display:inline-block;background:#172033;color:#fff;border-radius:999px;padding:7px 12px;font-size:12px;letter-spacing:.08em}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><span class="badge">AVENOR · STRICT ADVISORY ENGINE</span><h1>Student & International Education Advisor</h1><p>Career fit • degrees • scholarships • countries • university strategy • reality checks</p></div>', unsafe_allow_html=True)
st.caption("A Project of Avenor · Made by Muhammad Talal Irfan")

if "profile" not in st.session_state: st.session_state.profile={}
for title, questions in SECTIONS:
    st.header(title)
    with st.container(border=True):
        for key,label,kind,opts in questions:
            old=st.session_state.profile.get(key)
            if kind=="text": val=st.text_input(label,value=old or "")
            elif kind=="textarea": val=st.text_area(label,value=old or "")
            elif kind=="select":
                choices=opts; val=st.selectbox(label,choices,index=choices.index(old) if old in choices else 0)
            elif kind=="multiselect": val=st.multiselect(label,opts,default=[x for x in (old or []) if x in opts])
            else:
                lo,hi=opts; val=st.slider(label,lo,hi,int(old or ((lo+hi)//2)))
            st.session_state.profile[key]=val

st.divider()
if st.button("Run AVENOR Assessment",type="primary",use_container_width=True):
    with st.spinner("Running strict assessment + current research grounding..."):
        try: st.session_state.report=analyze(st.session_state.profile)
        except Exception as e: st.error(str(e))
if st.session_state.get("report"):
    st.markdown(st.session_state.report)
    st.download_button("Download report",st.session_state.report,"avenor_assessment.md","text/markdown")
