import streamlit as st

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
:root{
  --navy:#0a1220;
  --navy-2:#0f1c33;
  --navy-3:#142744;
  --brass:#c9a227;
  --brass-light:#e8cf7a;
  --teal:#1f8a8c;
  --crimson:#9b2226;
  --paper:#f4efe2;
  --ink:#eae3d1;
  --muted:#93a1bd;
  --glass-border:rgba(201,162,39,0.28);
}

#MainMenu, footer, header{visibility:hidden;}

.stApp{
  background:
    radial-gradient(1200px 600px at 15% -10%, rgba(31,138,140,0.16), transparent 60%),
    radial-gradient(1000px 700px at 110% 10%, rgba(155,34,38,0.12), transparent 55%),
    linear-gradient(120deg, var(--navy) 0%, var(--navy-2) 45%, var(--navy-3) 100%);
  background-size: 200% 200%, 200% 200%, 200% 200%;
  animation: driftGradient 26s ease-in-out infinite;
  color: var(--ink);
  font-family: 'IBM Plex Sans', sans-serif;
}

@keyframes driftGradient{
  0%{background-position:0% 0%, 100% 0%, 0% 0%;}
  50%{background-position:100% 100%, 0% 100%, 100% 100%;}
  100%{background-position:0% 0%, 100% 0%, 0% 0%;}
}

h1, h2, h3, .avenor-serif{
  font-family:'Fraunces', serif;
  color: var(--brass-light);
  letter-spacing: 0.01em;
}

.avenor-mark{
  text-align:center;
  padding: 2.2rem 0 0.6rem 0;
}
.avenor-mark .eyebrow{
  font-family:'IBM Plex Sans', sans-serif;
  font-size:0.72rem;
  letter-spacing:0.32em;
  text-transform:uppercase;
  color:var(--teal);
  margin-bottom:0.4rem;
}
.avenor-mark h1{
  font-size:2.6rem;
  font-weight:600;
  margin:0;
  background:linear-gradient(120deg, var(--brass-light), var(--paper) 55%, var(--brass));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
}
.avenor-mark .subline{
  font-family:'IBM Plex Sans', sans-serif;
  color:var(--muted);
  font-size:0.95rem;
  margin-top:0.35rem;
}

.glass-card{
  background: linear-gradient(165deg, rgba(20,39,68,0.62), rgba(10,18,32,0.72));
  border: 1px solid var(--glass-border);
  border-radius: 18px;
  padding: 1.9rem 2.1rem;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
  animation: stampReveal 0.55s cubic-bezier(.2,.8,.2,1);
  margin-bottom: 1.1rem;
}

@keyframes stampReveal{
  0%{opacity:0; transform:scale(0.94) translateY(10px) rotate(-0.4deg);}
  60%{opacity:1;}
  100%{opacity:1; transform:scale(1) translateY(0) rotate(0deg);}
}

.section-kicker{
  display:flex;
  align-items:baseline;
  gap:0.6rem;
  margin-bottom:0.2rem;
}
.section-kicker .num{
  font-family:'Fraunces', serif;
  color: var(--brass);
  font-size:1.1rem;
  font-weight:600;
}
.section-kicker .title{
  font-family:'Fraunces', serif;
  font-size:1.55rem;
  color: var(--paper);
  font-weight:500;
}
.section-rule{
  height:1px;
  background:linear-gradient(90deg, var(--brass) 0%, transparent 70%);
  margin: 0.35rem 0 1.3rem 0;
  opacity:0.55;
}

.stamps{
  display:flex;
  justify-content:center;
  gap:0.42rem;
  flex-wrap:wrap;
  margin: 0.4rem 0 1.6rem 0;
}
.stamp{
  width:30px; height:30px;
  border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-family:'IBM Plex Sans', sans-serif;
  font-size:0.72rem;
  font-weight:600;
  border:1px solid rgba(201,162,39,0.35);
  color: var(--muted);
  transition: all .35s ease;
}
.stamp.done{
  background: linear-gradient(140deg, var(--brass), var(--brass-light));
  color: var(--navy);
  border-color: transparent;
  box-shadow: 0 0 14px rgba(201,162,39,0.45);
}
.stamp.active{
  background: linear-gradient(140deg, var(--teal), #2fb3b5);
  color: var(--navy);
  border-color: transparent;
  box-shadow: 0 0 18px rgba(31,138,140,0.55);
  transform: scale(1.12);
}

.field-label{
  font-family:'IBM Plex Sans', sans-serif;
  font-size:0.86rem;
  color: var(--ink);
  opacity:0.92;
  margin-bottom: -0.4rem;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-baseweb="select"] > div{
  background: rgba(9,16,29,0.55) !important;
  border: 1px solid rgba(147,161,189,0.28) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus{
  border-color: var(--teal) !important;
  box-shadow: 0 0 0 1px var(--teal) !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"]{
  background-color: var(--brass) !important;
  box-shadow: 0 0 10px rgba(201,162,39,0.6);
}
.stSlider [data-baseweb="slider"] > div > div{
  background: var(--teal) !important;
}

div.stButton > button{
  font-family:'IBM Plex Sans', sans-serif;
  font-weight:500;
  border-radius: 999px;
  padding: 0.55rem 1.6rem;
  border: 1px solid var(--brass);
  background: linear-gradient(140deg, rgba(201,162,39,0.16), rgba(201,162,39,0.04));
  color: var(--brass-light);
  transition: all 0.25s ease;
}
div.stButton > button:hover{
  background: linear-gradient(140deg, var(--brass), var(--brass-light));
  color: var(--navy);
  box-shadow: 0 8px 24px rgba(201,162,39,0.35);
  border-color: var(--brass-light);
}
div.stButton > button:focus{
  color: var(--navy) !important;
}

.primary-cta button{
  border: 1px solid var(--teal) !important;
  background: linear-gradient(140deg, var(--teal), #17696b) !important;
  color: var(--paper) !important;
}
.primary-cta button:hover{
  background: linear-gradient(140deg, #2fb3b5, var(--teal)) !important;
  box-shadow: 0 8px 24px rgba(31,138,140,0.4) !important;
}

.dossier-divider{
  border:none;
  height:1px;
  background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
  margin: 1.6rem 0;
}

.verdict-chip{
  display:inline-block;
  font-family:'IBM Plex Sans', sans-serif;
  font-size:0.72rem;
  letter-spacing:0.14em;
  text-transform:uppercase;
  padding: 0.28rem 0.85rem;
  border-radius: 999px;
  border:1px solid var(--glass-border);
  color: var(--brass-light);
  margin-right:0.5rem;
}

.score-ring{
  font-family:'Fraunces', serif;
  font-size: 3.2rem;
  color: var(--brass-light);
  text-align:center;
  line-height:1;
}
.score-caption{
  text-align:center;
  color:var(--muted);
  font-size:0.8rem;
  letter-spacing:0.12em;
  text-transform:uppercase;
  margin-top:0.3rem;
}

[data-testid="stDataFrame"]{
  border-radius:14px;
  overflow:hidden;
  border:1px solid var(--glass-border);
}
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def mark(eyebrow: str, title: str, subline: str):
    st.markdown(
        f"""<div class="avenor-mark">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <div class="subline">{subline}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def stamps(total: int, current_index: int):
    cells = []
    for i in range(total):
        cls = "stamp"
        if i < current_index:
            cls += " done"
        elif i == current_index:
            cls += " active"
        cells.append(f'<div class="{cls}">{i+1:02d}</div>')
    st.markdown(f'<div class="stamps">{"".join(cells)}</div>', unsafe_allow_html=True)


def section_header(num: str, title: str):
    st.markdown(
        f"""<div class="section-kicker"><span class="num">{num}</span><span class="title">{title}</span></div>
        <div class="section-rule"></div>""",
        unsafe_allow_html=True,
    )
