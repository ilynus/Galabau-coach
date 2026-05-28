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
</style>
"""
