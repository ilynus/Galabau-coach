"""GaLaBau Coach Design-System."""
from __future__ import annotations
import streamlit as st


def apply_theme() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root{
  --forest:#12382a;
  --forest-2:#1d5c43;
  --leaf:#4f9f5f;
  --moss:#dfead7;
  --sand:#fbfaf4;
  --paper:#ffffff;
  --soil:#5d4733;
  --clay:#c47a47;
  --ink:#18211d;
  --muted:#66756d;
  --line:#e5eadf;
  --shadow:0 8px 28px rgba(18,56,42,.10);
  --shadow-sm:0 3px 12px rgba(18,56,42,.08);
  --r:16px;
  --r-sm:10px;
}

html, body, [data-testid="stAppViewContainer"]{
  background:linear-gradient(180deg,#fbfaf4 0%,#f3f7ed 100%)!important;
  color:var(--ink)!important;
  font-family:'Inter',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif!important;
}
.main .block-container{padding-top:1.2rem!important;max-width:1240px!important;}
h1,h2{font-family:'Fraunces',serif!important;color:var(--forest)!important;letter-spacing:-.02em!important;}
h1{font-size:2.35rem!important;}
h3{color:var(--forest-2)!important;font-weight:700!important;}

[data-testid="stSidebar"]{
  background:linear-gradient(178deg,var(--forest) 0%,#173f30 55%,#10281f 100%)!important;
  border-right:1px solid rgba(255,255,255,.08)!important;
}
[data-testid="stSidebar"] *{color:rgba(255,255,255,.90)!important;}
[data-testid="stSidebar"] .stButton button{
  background:rgba(255,255,255,.08)!important;border:1px solid rgba(255,255,255,.15)!important;border-radius:var(--r-sm)!important;
}
[data-testid="stSidebar"] .stButton button:hover{background:rgba(79,159,95,.28)!important;border-color:rgba(255,255,255,.25)!important;}
[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.14)!important;}

.gbc-brand{padding:1rem 1rem .9rem 1rem;border:1px solid rgba(255,255,255,.13);border-radius:18px;background:rgba(255,255,255,.08);margin-bottom:.9rem;}
.gbc-brand-title{font-family:'Fraunces',serif;font-size:1.22rem;font-weight:700;color:#fff;}
.gbc-brand-sub{font-size:.82rem;color:rgba(255,255,255,.72);margin-top:.15rem;}
.gbc-user-card{border:1px solid rgba(255,255,255,.13);border-radius:16px;background:rgba(255,255,255,.07);padding:.8rem .9rem;margin:.6rem 0 1rem 0;}
.gbc-user-card strong{display:block;color:#fff!important}
.gbc-user-card small{color:rgba(255,255,255,.68)!important}

[data-testid="stMetric"]{background:var(--paper)!important;border:1px solid var(--line)!important;border-radius:var(--r)!important;padding:1rem 1.1rem!important;box-shadow:var(--shadow-sm)!important;}
[data-testid="stMetricLabel"]{color:var(--muted)!important;text-transform:uppercase!important;letter-spacing:.06em!important;font-size:.72rem!important;font-weight:700!important;}
[data-testid="stMetricValue"]{color:var(--forest)!important;font-family:'Fraunces',serif!important;}

.stButton button[kind="primary"]{
  background:linear-gradient(135deg,var(--forest) 0%,var(--forest-2) 100%)!important;
  border:0!important;border-radius:var(--r-sm)!important;color:white!important;font-weight:700!important;
  box-shadow:0 6px 18px rgba(18,56,42,.18)!important;
}
.stButton button[kind="primary"]:hover{transform:translateY(-1px);box-shadow:0 10px 24px rgba(18,56,42,.24)!important;}
.stButton button:not([kind="primary"]){border-radius:var(--r-sm)!important;}

[data-testid="stVerticalBlockBorderWrapper"]>div,[data-testid="stExpander"]{
  border:1px solid var(--line)!important;border-radius:var(--r)!important;background:var(--paper)!important;box-shadow:var(--shadow-sm)!important;
}
.stTabs [data-baseweb="tab-list"]{gap:.25rem!important;border-bottom:1px solid var(--line)!important;}
.stTabs [data-baseweb="tab"]{padding:.55rem 1rem!important;border-radius:999px 999px 0 0!important;font-weight:700!important;}
.stTabs [aria-selected="true"]{color:var(--forest)!important;border-bottom:3px solid var(--leaf)!important;}

.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]{border-radius:var(--r-sm)!important;}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:var(--leaf)!important;box-shadow:0 0 0 3px rgba(79,159,95,.18)!important;}

[data-testid="stInfo"]{background:#edf7ed!important;border-left:4px solid var(--leaf)!important;border-radius:var(--r-sm)!important;}
[data-testid="stWarning"]{border-left:4px solid var(--clay)!important;border-radius:var(--r-sm)!important;}
[data-testid="stSuccess"]{border-left:4px solid var(--forest-2)!important;border-radius:var(--r-sm)!important;}

.gbc-hero{
  background:radial-gradient(circle at 12% 18%, rgba(79,159,95,.28), transparent 28%),linear-gradient(135deg,#173f30 0%,#246347 58%,#4f9f5f 100%);
  color:white;border-radius:24px;padding:1.4rem 1.5rem;box-shadow:var(--shadow);margin-bottom:1.1rem;
}
.gbc-hero h1{color:white!important;margin:.1rem 0 .25rem 0!important;}
.gbc-hero p{margin:0;color:rgba(255,255,255,.84);font-size:1rem;}
.gbc-card{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:1rem 1.05rem;box-shadow:var(--shadow-sm);height:100%;}
.gbc-card h3{margin-top:0!important;}
.gbc-chip{display:inline-block;padding:.25rem .55rem;border-radius:999px;background:#edf7ed;color:var(--forest);border:1px solid #d4e8d2;font-weight:700;font-size:.78rem;margin:.12rem .18rem .12rem 0;}
.gbc-source{font-size:.84rem;color:var(--muted);border-top:1px solid var(--line);margin-top:1rem;padding-top:.75rem;}
.gbc-callout{background:#fff8ec;border:1px solid #f0dec1;border-left:4px solid var(--clay);border-radius:14px;padding:.85rem 1rem;}
hr{border-color:var(--line)!important;}

/* --- Kontrast-Fix für Eingabefelder und Labels --- */
label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p{
  color:var(--ink)!important;
  background:transparent!important;
  font-weight:700!important;
}
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
input,
textarea{
  background:#ffffff!important;
  color:#18211d!important;
  -webkit-text-fill-color:#18211d!important;
  caret-color:#18211d!important;
  border:1px solid #bfcabe!important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
input::placeholder,
textarea::placeholder{
  color:#7b887f!important;
  opacity:1!important;
  -webkit-text-fill-color:#7b887f!important;
}
[data-baseweb="input"],
[data-baseweb="textarea"]{
  background:#ffffff!important;
  color:#18211d!important;
}
[data-baseweb="input"] *,
[data-baseweb="textarea"] *{
  color:#18211d!important;
  -webkit-text-fill-color:#18211d!important;
}
[data-baseweb="select"]{
  background:#ffffff!important;
  color:#18211d!important;
}
[data-baseweb="select"] *{
  color:#18211d!important;
  -webkit-text-fill-color:#18211d!important;
}
[data-testid="stForm"],
[data-testid="stForm"] *{
  color:var(--ink)!important;
}


/* FINAL HIGH-CONTRAST FIX */
.stSelectbox div[data-baseweb="select"]{
    background:#ffffff !important;
    color:#18211d !important;
    border:1px solid #cfd8cf !important;
}
.stSelectbox div[data-baseweb="select"] *{
    color:#18211d !important;
    -webkit-text-fill-color:#18211d !important;
}
.stSelectbox svg{
    fill:#18211d !important;
}

.stButton button{
    color:#ffffff !important;
}

.stButton button p,
.stButton button span,
.stButton button div{
    color:#ffffff !important;
}

[data-testid="stMarkdownContainer"]{
    color:#18211d !important;
}

.stTextArea textarea{
    min-height:140px !important;
    background:#ffffff !important;
    color:#18211d !important;
}

.stTextInput input{
    background:#ffffff !important;
    color:#18211d !important;
}

div[role="listbox"]{
    background:#ffffff !important;
    color:#18211d !important;
}

div[role="option"]{
    background:#ffffff !important;
    color:#18211d !important;
}

div[role="option"]:hover{
    background:#edf7ed !important;
    color:#18211d !important;
}


/* =========================================================
   VERIFIED CONTRAST FIX
   Problem: In Streamlit Cloud/browser dark mode, BaseWeb widgets
   can keep dark backgrounds while text also becomes dark.
   This block forces readable combinations for all form widgets.
   ========================================================= */

/* Normal page text */
section.main,
section.main p,
section.main span,
section.main li,
section.main div,
section.main label,
section.main [data-testid="stWidgetLabel"],
section.main [data-testid="stWidgetLabel"] p {
  color:#18211d !important;
}

/* Hero and custom green blocks remain white text */
.gbc-hero,
.gbc-hero *,
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
.gbc-brand,
.gbc-brand *,
.gbc-user-card,
.gbc-user-card * {
  color:#ffffff !important;
}

/* Text inputs / textareas / number fields */
section.main input,
section.main textarea,
section.main [data-baseweb="input"],
section.main [data-baseweb="input"] > div,
section.main [data-baseweb="textarea"],
section.main [data-baseweb="textarea"] > div {
  background:#ffffff !important;
  color:#18211d !important;
  -webkit-text-fill-color:#18211d !important;
  caret-color:#18211d !important;
  border-color:#bfcabe !important;
}

section.main input::placeholder,
section.main textarea::placeholder {
  color:#6f7c74 !important;
  -webkit-text-fill-color:#6f7c74 !important;
  opacity:1 !important;
}

/* Selectbox closed state */
section.main div[data-baseweb="select"],
section.main div[data-baseweb="select"] > div,
section.main div[data-baseweb="select"] div,
section.main div[data-baseweb="select"] span,
section.main div[data-baseweb="select"] input {
  background:#ffffff !important;
  color:#18211d !important;
  -webkit-text-fill-color:#18211d !important;
  border-color:#bfcabe !important;
}

section.main div[data-baseweb="select"] svg {
  fill:#18211d !important;
}

/* Dropdown menu/open options */
div[role="listbox"],
ul[role="listbox"],
li[role="option"],
div[role="option"] {
  background:#ffffff !important;
  color:#18211d !important;
  -webkit-text-fill-color:#18211d !important;
}

li[role="option"]:hover,
div[role="option"]:hover,
li[aria-selected="true"],
div[aria-selected="true"] {
  background:#edf7ed !important;
  color:#18211d !important;
  -webkit-text-fill-color:#18211d !important;
}

/* Buttons: visible white text on green buttons */
section.main .stButton > button,
section.main button[kind],
section.main button {
  background:#1d5c43 !important;
  color:#ffffff !important;
  -webkit-text-fill-color:#ffffff !important;
  border:1px solid #174b37 !important;
  border-radius:10px !important;
  font-weight:700 !important;
}

section.main .stButton > button *,
section.main button[kind] *,
section.main button * {
  color:#ffffff !important;
  -webkit-text-fill-color:#ffffff !important;
}

section.main .stButton > button:hover,
section.main button:hover {
  background:#12382a !important;
  color:#ffffff !important;
  -webkit-text-fill-color:#ffffff !important;
}

/* Sidebar buttons stay readable */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] button {
  background:rgba(255,255,255,.10) !important;
  border:1px solid rgba(255,255,255,.20) !important;
  color:#ffffff !important;
  -webkit-text-fill-color:#ffffff !important;
}
[data-testid="stSidebar"] .stButton > button *,
[data-testid="stSidebar"] button * {
  color:#ffffff !important;
  -webkit-text-fill-color:#ffffff !important;
}

/* Dataframe/table fallback */
section.main table,
section.main th,
section.main td {
  color:#18211d !important;
  background:#ffffff !important;
}

/* Streamlit alert text stays readable */
section.main [data-testid="stInfo"] *,
section.main [data-testid="stWarning"] *,
section.main [data-testid="stSuccess"] *,
section.main [data-testid="stError"] * {
  color:#18211d !important;
  -webkit-text-fill-color:#18211d !important;
}


/* PREMIUM DASHBOARD + GAMIFICATION */
.gbc-premium-hero{
  position:relative;
  overflow:hidden;
  border-radius:28px;
  padding:1.8rem 1.7rem;
  margin-bottom:1.15rem;
  background:
    radial-gradient(circle at 85% 12%, rgba(255,255,255,.22), transparent 28%),
    radial-gradient(circle at 8% 70%, rgba(211,236,205,.24), transparent 26%),
    linear-gradient(135deg,#0d2a21 0%,#1f5d43 52%,#66aa6b 100%);
  color:white!important;
  box-shadow:0 18px 44px rgba(18,56,42,.22);
}
.gbc-premium-hero *{color:white!important;}
.gbc-eyebrow{
  display:inline-block;
  padding:.28rem .7rem;
  border-radius:999px;
  background:rgba(255,255,255,.14);
  border:1px solid rgba(255,255,255,.22);
  font-weight:800;
  font-size:.78rem;
  letter-spacing:.04em;
  text-transform:uppercase;
  margin-bottom:.55rem;
}
.gbc-premium-hero h1{
  font-size:2.7rem!important;
  line-height:1.04!important;
  margin:.15rem 0 .45rem 0!important;
}
.gbc-hero-grid{
  display:grid;
  grid-template-columns:1.4fr .8fr;
  gap:1rem;
  align-items:end;
}
.gbc-glass{
  background:rgba(255,255,255,.12);
  border:1px solid rgba(255,255,255,.20);
  border-radius:22px;
  padding:1rem;
  backdrop-filter: blur(8px);
}
.gbc-progress-track{
  height:12px;
  border-radius:999px;
  background:rgba(255,255,255,.24);
  overflow:hidden;
  margin:.45rem 0 .15rem 0;
}
.gbc-progress-fill{
  height:100%;
  border-radius:999px;
  background:linear-gradient(90deg,#dff3d8,#ffffff);
}
.gbc-dashboard-card{
  background:#ffffff;
  border:1px solid #e2eadf;
  border-radius:22px;
  padding:1.05rem;
  box-shadow:0 10px 28px rgba(18,56,42,.09);
  height:100%;
}
.gbc-dashboard-card h3{
  margin-top:0!important;
  margin-bottom:.35rem!important;
}
.gbc-big-number{
  font-family:'Fraunces',serif;
  font-size:2.15rem;
  color:#12382a!important;
  font-weight:800;
  line-height:1;
}
.gbc-mini-label{
  color:#66756d!important;
  font-size:.82rem;
  font-weight:800;
  text-transform:uppercase;
  letter-spacing:.06em;
}
.gbc-action-card{
  border:1px solid #e1eadc;
  border-radius:20px;
  background:linear-gradient(180deg,#ffffff 0%,#fbfdf8 100%);
  padding:1rem;
  min-height:150px;
  box-shadow:0 6px 18px rgba(18,56,42,.07);
}
.gbc-action-icon{
  font-size:1.85rem;
  margin-bottom:.35rem;
}
.gbc-badge{
  display:inline-flex;
  align-items:center;
  gap:.35rem;
  padding:.38rem .62rem;
  border-radius:999px;
  background:#edf7ed;
  color:#12382a!important;
  border:1px solid #d4e8d2;
  font-weight:800;
  margin:.15rem .12rem;
}
.gbc-quest{
  display:flex;
  align-items:center;
  gap:.75rem;
  border:1px solid #e1eadc;
  border-radius:16px;
  background:#ffffff;
  padding:.75rem .85rem;
  margin:.42rem 0;
}
.gbc-quest-emoji{
  font-size:1.5rem;
  background:#edf7ed;
  border-radius:14px;
  width:2.55rem;
  height:2.55rem;
  display:flex;
  align-items:center;
  justify-content:center;
}
.gbc-quest-title{
  font-weight:900;
  color:#12382a!important;
}
.gbc-quest-sub{
  color:#66756d!important;
  font-size:.88rem;
}
@media(max-width:800px){
  .gbc-hero-grid{grid-template-columns:1fr;}
  .gbc-premium-hero h1{font-size:2.1rem!important;}
}

</style>
"""
