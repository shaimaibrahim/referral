import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

# ════════════════════════════════════════════════════════════════════
#  PAGE CONFIGURATION
# ════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="تجمع جدة الصحي الأول",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════
#  PASSWORD GATE
# ════════════════════════════════════════════════════════════════════
PASS = "jedc1-2026"

def check_password():
    if st.session_state.get("auth"):
        return True
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html,body,[class*="css"],*{font-family:'Cairo',sans-serif!important;direction:rtl;}
    .stApp{background:linear-gradient(135deg,#e8f2fb,#d4e8f8);}
    </style>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="background:#fff;border:1px solid #c0d8f0;border-radius:18px;
            padding:44px 36px;box-shadow:0 8px 32px rgba(20,90,170,.13);
            text-align:center;margin-top:60px">
          <div style="font-size:3rem">🏥</div>
          <div style="color:#1560a0;font-size:.8rem;font-weight:700;
               letter-spacing:2px;margin:8px 0 2px">JEDDAH FIRST HEALTH CLUSTER</div>
          <div style="color:#0c2a4a;font-size:1.3rem;font-weight:900">تجمع جدة الصحي الأول</div>
          <div style="color:#5080a0;font-size:.8rem;margin-top:4px;margin-bottom:24px">
               إدارة الإحالات والطاقات الاستيعابية</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:14px'/>", unsafe_allow_html=True)
        pwd = st.text_input("", type="password",
                            placeholder="🔑  أدخل كلمة المرور للدخول",
                            label_visibility="collapsed")
        if st.button("دخول  →", use_container_width=True):
            if pwd == PASS:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة")
    return False

if not check_password():
    st.stop()

# ════════════════════════════════════════════════════════════════════
#  COLOUR PALETTE
#  BLUES     → bar & pie gradient (dark navy → light sky)
#  PIE_BLUE  → same palette for pie charts
#  STATUS_CLR→ ICU capacity status colours (lighter shades)
# ════════════════════════════════════════════════════════════════════
BLUES    = ["#0e3f7a","#1256a0","#1a6ab8","#2280d0","#3498e4",
            "#4db0f4","#72c4f8","#9dd6fb","#c0e8fe"]
PIE_BLUE = ["#0e3f7a","#1256a0","#1a6ab8","#2280d0","#3498e4",
            "#4db0f4","#72c4f8","#9dd6fb"]

# Lighter, softer status colours for ICU pies
STATUS_CLR = {
    "مشغول":        "#e05c5c",   # soft red
    "شاغر":         "#3ab87a",   # soft green
    "موقوف مؤقتا":  "#e8b040",   # soft amber
    "موقوف مؤقتاً": "#e8b040",
}

PAPER = "#f0f6fc"
PLOT  = "rgba(236,246,254,0.9)"
GRID  = "#c8ddf0"
FONT  = "#0d2840"

# ════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;900&display=swap');
html,body,[class*="css"],*{font-family:'Cairo',sans-serif!important;direction:rtl;}
.stApp{background:#eef5fc;color:#0d2840;}
section[data-testid="stMain"]>div{padding-top:.3rem;}
.block-container{padding:.5rem 1.4rem 2rem!important;max-width:100%!important;}

/* ── Remove the default Streamlit top toolbar / deploy bar ── */
[data-testid="stToolbar"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
header[data-testid="stHeader"]{background:transparent!important;height:0!important;
  min-height:0!important;overflow:hidden!important;}

/* ── Sidebar – slim width ── */
[data-testid="stSidebar"]{
  background:#fff;border-left:1px solid #bdd4ec;
  min-width:190px!important;max-width:200px!important;}
[data-testid="stSidebar"] *{color:#1a4060!important;font-size:.80rem!important;}
[data-testid="stSidebar"] h3{color:#1256a0!important;font-size:.86rem!important;font-weight:700!important;}
[data-testid="stSidebar"] section[data-testid="stSidebarContent"]{padding:.7rem .6rem;}

/* ── Dashboard header ── */
.dash-hdr{
  background:linear-gradient(110deg,#1256a0,#1e80d0,#1256a0);
  border-radius:12px;padding:12px 24px;margin-bottom:14px;
  display:flex;align-items:center;justify-content:space-between;
  box-shadow:0 4px 16px rgba(18,86,160,.22);}
.dash-hdr-t{color:#fff;font-size:1.35rem;font-weight:900;margin:0;}
.dash-hdr-s{color:#a8d0f0;font-size:.76rem;margin-top:1px;}

/* ── KPI cards ── */
.krow{display:flex;gap:10px;margin-bottom:14px;}
.kc{flex:1;border-radius:11px;padding:14px 12px 12px;text-align:center;
  position:relative;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.07);}
.kc.kb{background:linear-gradient(145deg,#e4f0fc,#cce4f8);border:1px solid #90bce8;}
.kc.kg{background:linear-gradient(145deg,#e4f6ee,#c8ecda);border:1px solid #70c098;}
.kc.ko{background:linear-gradient(145deg,#fef4e4,#fde3b8);border:1px solid #e8a830;}
.kc.kr{background:linear-gradient(145deg,#fcecea,#f8d4d0);border:1px solid #e08888;}
.kc::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;border-radius:0 0 11px 11px;}
.kc.kb::after{background:linear-gradient(90deg,#1256a0,#3498e4);}
.kc.kg::after{background:linear-gradient(90deg,#1a7840,#30b870);}
.kc.ko::after{background:linear-gradient(90deg,#c07810,#e8a830);}
.kc.kr::after{background:linear-gradient(90deg,#b02020,#e04040);}
.ki{font-size:1.2rem;margin-bottom:3px;}
.kl{color:#2a5878;font-size:.75rem;font-weight:700;margin-bottom:4px;
    text-transform:uppercase;letter-spacing:.4px;}
.kv{font-size:1.85rem;font-weight:900;line-height:1;}
.kb .kv{color:#1256a0;}.kg .kv{color:#166038;}
.ko .kv{color:#a06010;}.kr .kv{color:#a02020;}

/* ── Section title bar ── */
.st2{display:flex;align-items:center;gap:8px;
  background:linear-gradient(90deg,#dceef8,#eef5fc);
  border-right:4px solid #1e80d0;border-radius:7px;
  padding:8px 12px;color:#0c2a4a;font-weight:800;font-size:.9rem;margin-bottom:8px;}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{background:#ddedf8;border-radius:10px;
  padding:3px;gap:3px;border:1px solid #b8d4ec;}
.stTabs [data-baseweb="tab"]{color:#1a4060!important;font-weight:700;
  border-radius:7px;padding:8px 22px;font-size:.88rem;}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#1256a0,#1e80d0)!important;
  color:#fff!important;box-shadow:0 2px 8px rgba(18,86,160,.28);}

/* ── Filter panel ── */
.fp{background:#e4f0fb;border:1px solid #aecce8;border-radius:10px;
  padding:12px 16px 8px;margin-bottom:14px;}
.fp label,.stMultiSelect label,.stDateInput label,.stSelectbox label{
  color:#0c2a4a!important;font-size:.82rem!important;font-weight:700!important;}
[data-baseweb="tag"]{background:#1256a0!important;color:#fff!important;}
[data-baseweb="tag"] span{color:#fff!important;}

/* ── Dataframe: blue header, white rows, dark text ── */
[data-testid="stDataFrame"] table{border-collapse:collapse!important;}
[data-testid="stDataFrame"] thead tr th{
  background:#1256a0!important;color:#fff!important;
  font-size:.83rem!important;font-weight:700!important;
  border:1px solid #0e3f7a!important;padding:8px 10px!important;}
[data-testid="stDataFrame"] tbody tr td{
  background:#fff!important;color:#0d2840!important;
  font-size:.83rem!important;border:1px solid #ddeef8!important;
  padding:7px 10px!important;}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td{background:#f2f8fd!important;}

/* ── ICU unit card ── */
.icu-card{background:#fff;border:1.5px solid #b8d4ec;border-radius:12px;
  padding:10px 6px 8px;margin:2px;box-shadow:0 2px 8px rgba(18,86,160,.1);}
.icu-card-title{text-align:center;color:#0c2a4a;font-weight:800;
  font-size:.8rem;min-height:36px;line-height:1.35;margin-bottom:4px;}

/* ── Misc ── */
hr{border-color:#c0d8ee!important;margin:.7rem 0!important;}
.lrow{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;
  margin-top:5px;font-size:.78rem;color:#1a4060;padding:3px;}
.ld{display:inline-block;width:10px;height:10px;border-radius:50%;
  margin-left:4px;vertical-align:middle;}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  CHART LAYOUT HELPERS
#  _layout()  → shared plotly layout dict
#  _xax()     → x-axis style dict
#  _yax()     → y-axis style dict
# ════════════════════════════════════════════════════════════════════
def _layout(h, ml=14, mr=20, mt=28, mb=80):
    return dict(
        paper_bgcolor=PAPER, plot_bgcolor=PLOT,
        font=dict(family="Cairo", color=FONT, size=12),
        height=h,
        margin=dict(l=ml, r=mr, t=mt, b=mb),
        hoverlabel=dict(bgcolor="#ddeef8", font_family="Cairo",
                        font_size=13, font_color="#0d2840"),
    )

def _xax(**kw):
    return dict(gridcolor=GRID, linecolor="#a8c8e0",
                tickfont=dict(size=11, family="Cairo", color=FONT), **kw)

def _yax(**kw):
    return dict(gridcolor=GRID, linecolor="#a8c8e0",
                tickfont=dict(size=11, family="Cairo", color=FONT), **kw)

# ════════════════════════════════════════════════════════════════════
#  VERTICAL BAR CHART
#  • Blue gradient colours per bar
#  • Value labels as annotations ABOVE bars (never drawn ON the bar face)
# ════════════════════════════════════════════════════════════════════
def bar_v(series, h=480, top_n=None, angle=-40):
    counts = series.value_counts()
    if top_n:
        counts = counts.head(top_n)
    n    = len(counts)
    clrs = [BLUES[min(i, len(BLUES)-1)] for i in range(n)]
    mx   = int(counts.values.max()) if n > 0 else 1

    fig = go.Figure(go.Bar(
        x=counts.index.astype(str),
        y=counts.values,
        marker_color=clrs,
        marker_line_color="#a8c8e0",
        marker_line_width=.8,
        text=None,                          # ← no text ON the bars
        hovertemplate="<b>%{x}</b><br>العدد: %{y:,}<extra></extra>",
    ))

    # Annotations appear above each bar – completely separate from the bar body
    annotations = [
        dict(
            x=str(label), y=int(val),
            text=f"<b>{int(val):,}</b>",
            xanchor="center", yanchor="bottom",
            showarrow=False,
            font=dict(size=10, family="Cairo", color=FONT),
            yshift=5,
        )
        for label, val in counts.items()
    ]

    fig.update_layout(**_layout(h, mb=110), annotations=annotations)
    fig.update_xaxes(**_xax(tickangle=angle))
    fig.update_yaxes(**_yax(range=[0, mx * 1.22]))
    return fig

# ════════════════════════════════════════════════════════════════════
#  HORIZONTAL BAR CHART
#  • Blue gradient colours per bar
#  • Value labels as annotations to the RIGHT of bars (never ON the bar face)
# ════════════════════════════════════════════════════════════════════
def bar_h(series, h=460, top_n=10):
    counts = series.value_counts().head(top_n)
    n    = len(counts)
    clrs = [BLUES[min(i, len(BLUES)-1)] for i in range(n)]
    mx   = int(counts.values.max()) if n > 0 else 1

    fig = go.Figure(go.Bar(
        x=counts.values,
        y=counts.index.astype(str),
        orientation="h",
        marker_color=clrs,
        marker_line_color="#a8c8e0",
        marker_line_width=.8,
        text=None,                          # ← no text ON the bars
        hovertemplate="<b>%{y}</b><br>العدد: %{x:,}<extra></extra>",
    ))

    # Annotations appear to the right of each bar – completely separate
    annotations = [
        dict(
            x=int(val), y=str(label),
            text=f"<b>{int(val):,}</b>",
            xanchor="left", yanchor="middle",
            showarrow=False,
            font=dict(size=10, family="Cairo", color=FONT),
            xshift=7,
        )
        for label, val in counts.items()
    ]

    fig.update_layout(**_layout(h, ml=10, mr=90, mb=30, mt=20), annotations=annotations)
    fig.update_xaxes(**_xax(range=[0, mx * 1.25]))
    fig.update_yaxes(**_yax(autorange="reversed"))
    return fig

# ════════════════════════════════════════════════════════════════════
#  PIE CHART  (referral dashboards – blue gradient palette)
#  • No text drawn ON slices
#  • Legend built as an HTML table injected via st.markdown so that
#    the colour swatch and label text are always on the SAME LINE
# ════════════════════════════════════════════════════════════════════
def _pie_legend_html(counts, colors, max_h=460):
    """Return an HTML <table> where every row is:
       [■ swatch] [Name] [Count] [(pct%)]  – all on one line."""
    total = counts.sum()
    rows  = ""
    for (lbl, val), clr in zip(counts.items(), colors):
        pct = 100 * val / total
        rows += (
            f"<tr>"
            f"<td style='padding:4px 6px 4px 0;vertical-align:middle;white-space:nowrap'>"
            f"<span style='display:inline-block;width:13px;height:13px;"
            f"border-radius:3px;background:{clr};vertical-align:middle'></span></td>"
            f"<td style='padding:4px 8px 4px 0;color:#0d2840;font-weight:600;"
            f"font-size:.82rem;vertical-align:middle;white-space:nowrap'>{lbl}</td>"
            f"<td style='padding:4px 6px;color:#1256a0;font-weight:700;"
            f"font-size:.82rem;vertical-align:middle;text-align:left;"
            f"white-space:nowrap'>{val:,}</td>"
            f"<td style='padding:4px 2px;color:#4a7090;font-size:.76rem;"
            f"vertical-align:middle;white-space:nowrap'>({pct:.1f}%)</td>"
            f"</tr>"
        )
    return (
        f"<div style='overflow-y:auto;max-height:{max_h}px;direction:rtl;"
        f"padding-top:6px'>"
        f"<table style='border-collapse:collapse;font-family:Cairo,sans-serif;"
        f"width:100%'>{rows}</table></div>"
    )

def pie_chart(series, h=460, colors=None, col_key=""):
    """
    Renders the pie chart + HTML legend side-by-side using st.columns.
    Must be called directly (not inside st.plotly_chart wrapper).
    Returns nothing – renders in place.
    """
    counts = series.value_counts()
    clrs   = (colors or PIE_BLUE)[:len(counts)]

    fig = go.Figure(go.Pie(
        labels=counts.index.tolist(),
        values=counts.values.tolist(),
        hole=0.44,
        marker=dict(colors=clrs, line=dict(color="#fff", width=2.5)),
        textinfo="none",                    # ← nothing drawn ON slices
        hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
        sort=True,
    ))
    fig.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font=dict(family="Cairo", color=FONT, size=12),
        margin=dict(l=8, r=8, t=12, b=12),
        height=h,
        showlegend=False,                   # legend handled via HTML table below
        hoverlabel=dict(bgcolor="#ddeef8", font_family="Cairo",
                        font_size=13, font_color="#0d2840"),
    )

    # Split: pie on left, HTML legend on right
    col_a, col_b = st.columns([1.6, 1])
    with col_a:
        st.plotly_chart(fig, use_container_width=True, key=f"pie_{col_key}")
    with col_b:
        st.markdown(_pie_legend_html(counts, clrs, max_h=h), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  ICU STATUS PIE  (capacity dashboard – red / green / amber palette)
#  • Percent labels shown ON slices (white text, readable on dark colours)
#  • Legend built as HTML table: swatch + label + count on ONE line
# ════════════════════════════════════════════════════════════════════
def _status_legend_html(labels, vals, clrs):
    total = sum(vals) or 1
    rows  = ""
    for lbl, val, clr in zip(labels, vals, clrs):
        pct = 100 * val / total
        rows += (
            f"<tr>"
            f"<td style='padding:3px 5px 3px 0;vertical-align:middle;white-space:nowrap'>"
            f"<span style='display:inline-block;width:12px;height:12px;"
            f"border-radius:2px;background:{clr};vertical-align:middle'></span></td>"
            f"<td style='padding:3px 6px 3px 0;font-size:.79rem;color:#0d2840;"
            f"font-weight:600;vertical-align:middle;white-space:nowrap'>{lbl}</td>"
            f"<td style='padding:3px 4px;font-size:.79rem;color:#1256a0;"
            f"font-weight:700;vertical-align:middle;white-space:nowrap'>{val:,}</td>"
            f"<td style='padding:3px 2px;font-size:.74rem;color:#4a7090;"
            f"vertical-align:middle;white-space:nowrap'>({pct:.0f}%)</td>"
            f"</tr>"
        )
    return (
        f"<table style='border-collapse:collapse;"
        f"font-family:Cairo,sans-serif;direction:rtl'>{rows}</table>"
    )

def pie_status(series, h=230, key=""):
    """
    Renders the ICU pie + HTML legend side-by-side.
    Must be called directly (renders in place inside current column).
    """
    counts = series.value_counts()
    labels = counts.index.tolist()
    vals   = counts.values.tolist()
    clrs   = [STATUS_CLR.get(l, "#6090b0") for l in labels]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=vals,
        hole=0.48,
        marker=dict(colors=clrs, line=dict(color="#fff", width=2)),
        textinfo="percent",
        textfont=dict(size=11, family="Cairo", color="#fff"),
        hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
        sort=False,
    ))
    fig.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Cairo", color=FONT, size=10),
        margin=dict(l=4, r=4, t=6, b=6),
        height=h,
        showlegend=False,                   # legend handled via HTML table
        hoverlabel=dict(bgcolor="#ddeef8", font_family="Cairo", font_size=11),
    )

    col_a, col_b = st.columns([1.3, 1])
    with col_a:
        st.plotly_chart(fig, use_container_width=True, key=f"pst_{key}")
    with col_b:
        st.markdown(
            _status_legend_html(labels, vals, clrs),
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════
def sec(txt, icon="📊"):
    """Render a styled section-title bar."""
    st.markdown(f'<div class="st2"><span>{icon}</span>{txt}</div>',
                unsafe_allow_html=True)

def kpi4(vals, labels, cls, icons):
    """Render a row of 4 KPI cards."""
    h = '<div class="krow">'
    for v, l, c, i in zip(vals, labels, cls, icons):
        h += (f'<div class="kc {c}"><div class="ki">{i}</div>'
              f'<div class="kl">{l}</div><div class="kv">{v:,}</div></div>')
    st.markdown(h + '</div>', unsafe_allow_html=True)

def load_file(f):
    """Load CSV or Excel upload into a DataFrame."""
    if f is None:
        return None
    try:
        if f.name.endswith(".csv"):
            for enc in ["utf-8-sig", "utf-8", "cp1256", "iso-8859-6"]:
                try:
                    return pd.read_csv(f, encoding=enc)
                except Exception:
                    f.seek(0)
        else:
            return pd.read_excel(f)
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")
    return None

def to_dt(df, col):
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def apply_date(df, col, d0, d1):
    if col not in df.columns:
        return df
    df = to_dt(df.copy(), col)
    if d0:
        df = df[df[col] >= pd.Timestamp(d0)]
    if d1:
        df = df[df[col] <= pd.Timestamp(d1)]
    return df

def date_bounds(df, col):
    if col not in df.columns:
        return None, None
    tmp = to_dt(df.copy(), col)
    vd  = tmp[col].dropna()
    return (vd.min().date(), vd.max().date()) if not vd.empty else (None, None)

def nat_binary(df, col):
    """Map all nationalities → 'سعودي' / 'غير سعودي'."""
    return df[col].apply(
        lambda x: "سعودي" if "سعودي" in str(x) else "غير سعودي")

def count_kw(series, kws):
    """Count rows matching any keyword in kws list."""
    return int(series.str.contains("|".join(kws), na=False, case=False).sum())

def apply_multi(df, col, sel):
    """Filter df to rows where col is in sel list; empty sel → no filter."""
    if not sel:
        return df
    if col in df.columns:
        df = df[df[col].isin(sel)]
    return df

# ════════════════════════════════════════════════════════════════════
#  ICU UNIT KEYWORD MAP
#  Used to split bed data into Wards vs each ICU type
# ════════════════════════════════════════════════════════════════════
ICU_KEYS = {
    "أسرة الأجنحة": [],
    "ICU البالغين": [
        "وحدة العناية المركزة للبالغين", "عناية مركزة للبالغين",
        "عناية بالغين", "\\bicu\\b"],
    "PICU الأطفال": [
        "العناية المركزة للأطفال", "عناية أطفال", "picu"],
    "NICU حديثي الولادة": [
        "العناية المركزة لحديثي الولادة", "حديثي الولادة", "nicu"],
    "CCU القلب": [
        "وحدة العناية المركزة للقلب", "عناية القلب", "ccu"],
    "SDU العناية المتوسطة": [
        "وحدة العناية المتوسطة", "عناية متوسطة", "sdu"],
}
ALL_ICU = [k for lst in ICU_KEYS.values() for k in lst]

def icu_sub(df, kws, col="القسم الرئيسي"):
    if col not in df.columns or not kws:
        return pd.DataFrame()
    return df[df[col].str.contains("|".join(kws), na=False, case=False)]

def ward_sub(df, col="القسم الرئيسي"):
    if col not in df.columns:
        return df
    return df[~df[col].str.contains("|".join(ALL_ICU), na=False, case=False)]

# ════════════════════════════════════════════════════════════════════
#  SIDEBAR  – file uploaders only (slim)
# ════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 📂 ملفات البيانات")
    st.markdown("---")
    st.markdown("**📤 الإحالات المرسلة**")
    file_sent = st.file_uploader("", type=["csv","xlsx"], key="f_sent",
                                  label_visibility="collapsed")
    st.markdown("**📥 الإحالات المستقبلة**")
    file_recv = st.file_uploader("", type=["csv","xlsx"], key="f_recv",
                                  label_visibility="collapsed")
    st.markdown("**🛏️ الطاقة الاستيعابية**")
    file_beds = st.file_uploader("", type=["csv","xlsx"], key="f_beds",
                                  label_visibility="collapsed")
    st.markdown("---")
    if st.button("🔒 خروج", use_container_width=True):
        st.session_state.auth = False
        st.rerun()
    st.caption("© تجمع جدة الصحي الأول")

# ════════════════════════════════════════════════════════════════════
#  LOAD DATA FILES
# ════════════════════════════════════════════════════════════════════
df_s = load_file(file_sent)
df_r = load_file(file_recv)
df_b = load_file(file_beds)

# ════════════════════════════════════════════════════════════════════
#  DASHBOARD HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="dash-hdr">
  <div>
    <div class="dash-hdr-s">Jeddah First Health Cluster ·
      نظام إدارة الإحالات والطاقة الاستيعابية</div>
    <div class="dash-hdr-t">🏥 تجمع جدة الصحي الأول – لوحة التحكم</div>
  </div>
  <div style="color:#a8d0f0;font-size:.8rem;text-align:left;line-height:1.7">
    مؤشرات الأداء التشغيلي<br>
    <span style="color:#fff;font-weight:800">لحظي · تفاعلي</span>
  </div>
</div>""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "  📤  الإحالات المرسلة  ",
    "  📥  الإحالات المستقبلة  ",
    "  🛏️  الطاقة الاستيعابية  ",
])

# ════════════════════════════════════════════════════════════════════
#  TAB 1 – الإحالات المرسلة
# ════════════════════════════════════════════════════════════════════
with tab1:
    if df_s is None:
        st.info("⬆️ يرجى رفع ملف الإحالات المرسلة من الشريط الجانبي.")
    else:
        df0 = df_s.copy()
        DC = "تاريخ الإنشاء"
        NC = "جنسية المريض (العميل) (المريض)"

        # ── Filter panel ──────────────────────────────────────────
        st.markdown('<div class="fp">', unsafe_allow_html=True)
        fc = st.columns([1.2, 1.2, 2, 2.4, 2.4])
        mn, mx = date_bounds(df0, DC)
        d0 = fc[0].date_input("📅 من",  value=mn or datetime.date.today(), key="t1_d0")
        d1 = fc[1].date_input("📅 إلى", value=mx or datetime.date.today(), key="t1_d1")
        t_opts = sorted(df0["نوع الإحالة"].dropna().unique().tolist()) if "نوع الإحالة" in df0.columns else []
        sel_t  = fc[2].multiselect("نوع الإحالة",    t_opts, placeholder="الكل", key="t1_t")
        n_opts = sorted(df0[NC].dropna().unique().tolist()) if NC in df0.columns else []
        sel_n  = fc[3].multiselect("الجنسية",         n_opts, placeholder="الكل", key="t1_n")
        h_opts = sorted(df0["المستشفى المرسل"].dropna().unique().tolist()) if "المستشفى المرسل" in df0.columns else []
        sel_h  = fc[4].multiselect("المستشفى المرسل", h_opts, placeholder="الكل", key="t1_h")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Apply filters ─────────────────────────────────────────
        df = apply_date(df0.copy(), DC, d0, d1)
        df = apply_multi(df, "نوع الإحالة",     sel_t)
        df = apply_multi(df, NC,                 sel_n)
        df = apply_multi(df, "المستشفى المرسل", sel_h)

        # ── KPI row ───────────────────────────────────────────────
        tot = len(df)
        rr  = count_kw(df["نوع الإحالة"], ["روتين"]) if "نوع الإحالة" in df.columns else 0
        uu  = count_kw(df["نوع الإحالة"], ["طارئ"])  if "نوع الإحالة" in df.columns else 0
        ll  = count_kw(df["نوع الإحالة"], ["إنقاذ"]) if "نوع الإحالة" in df.columns else 0
        kpi4([tot, rr, uu, ll],
             ["عدد الإحالات","روتينية","طارئة","إنقاذ حياة"],
             ["kb","kg","ko","kr"], ["📋","✅","⚡","🚨"])
        st.markdown("---")

        # ── Chart: حالة الإحالة (full-width vertical bar) ────────
        if "حالة الإحالة" in df.columns:
            sec("حالة الإحالة", "📊")
            st.plotly_chart(bar_v(df["حالة الإحالة"], h=420),
                            use_container_width=True)
        st.markdown("---")

        # ── Charts: التخصص الرئيسي | الجنسية (pie + HTML legend) ─
        c1, c2 = st.columns([2.6, 1.6])
        with c1:
            if "التخصص الرئيسي" in df.columns:
                sec("التخصص الرئيسي", "🩺")
                pie_chart(df["التخصص الرئيسي"], h=460, col_key="t1_spec")
        with c2:
            if NC in df.columns:
                sec("الجنسية", "🌍")
                pie_chart(nat_binary(df, NC), h=460,
                          colors=["#1256a0","#72c4f8"], col_key="t1_nat")
        st.markdown("---")

        # ── Chart: سبب الإحالة (full-width vertical bar) ─────────
        if "سبب الإحالة" in df.columns:
            sec("سبب الإحالة", "📋")
            st.plotly_chart(bar_v(df["سبب الإحالة"], h=430),
                            use_container_width=True)
        st.markdown("---")

        # ── Charts: نوع السرير (horizontal bar) | جدول المستشفيات ─
        c3, c4 = st.columns([2.6, 1.6])
        with c3:
            if "نوع السرير المطلوب" in df.columns:
                sec("نوع السرير المطلوب", "🛏️")
                st.plotly_chart(bar_h(df["نوع السرير المطلوب"], h=380),
                                use_container_width=True)
        with c4:
            if "المستشفى المرسل" in df.columns:
                sec("أعلى المستشفيات المرسِلة", "🏥")
                t6 = df["المستشفى المرسل"].value_counts().head(8).reset_index()
                t6.columns = ["المستشفى","العدد"]
                st.dataframe(t6, use_container_width=True, hide_index=True, height=320)
        st.markdown("---")

        # ── Chart: المستشفى المستقبل (full-width horizontal bar) ──
        if "المستشفى المستقبل" in df.columns:
            sec("المستشفى المستقبل – أعلى 10", "🏥")
            st.plotly_chart(bar_h(df["المستشفى المستقبل"], h=400, top_n=10),
                            use_container_width=True)

# ════════════════════════════════════════════════════════════════════
#  TAB 2 – الإحالات المستقبلة
# ════════════════════════════════════════════════════════════════════
with tab2:
    if df_r is None:
        st.info("⬆️ يرجى رفع ملف الإحالات المستقبلة من الشريط الجانبي.")
    else:
        df0 = df_r.copy()
        DC = "تاريخ الإنشاء"
        NC = "جنسية المريض (العميل) (المريض)"

        # ── Filter panel ──────────────────────────────────────────
        st.markdown('<div class="fp">', unsafe_allow_html=True)
        fc = st.columns([1.2, 1.2, 2, 2.4, 2.4])
        mn, mx = date_bounds(df0, DC)
        d0r = fc[0].date_input("📅 من",  value=mn or datetime.date.today(), key="t2_d0")
        d1r = fc[1].date_input("📅 إلى", value=mx or datetime.date.today(), key="t2_d1")
        t_o2   = sorted(df0["نوع الإحالة"].dropna().unique().tolist()) if "نوع الإحالة" in df0.columns else []
        sel_t2 = fc[2].multiselect("نوع الإحالة",       t_o2, placeholder="الكل", key="t2_t")
        n_o2   = sorted(df0[NC].dropna().unique().tolist()) if NC in df0.columns else []
        sel_n2 = fc[3].multiselect("الجنسية",            n_o2, placeholder="الكل", key="t2_n")
        h_o2   = sorted(df0["المستشفى المستقبل"].dropna().unique().tolist()) if "المستشفى المستقبل" in df0.columns else []
        sel_h2 = fc[4].multiselect("المستشفى المستقبل", h_o2, placeholder="الكل", key="t2_h")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Apply filters ─────────────────────────────────────────
        df = apply_date(df0.copy(), DC, d0r, d1r)
        df = apply_multi(df, "نوع الإحالة",        sel_t2)
        df = apply_multi(df, NC,                    sel_n2)
        df = apply_multi(df, "المستشفى المستقبل",  sel_h2)

        # ── KPI row ───────────────────────────────────────────────
        tot2 = len(df)
        r2   = count_kw(df["نوع الإحالة"], ["روتين"]) if "نوع الإحالة" in df.columns else 0
        u2   = count_kw(df["نوع الإحالة"], ["طارئ"])  if "نوع الإحالة" in df.columns else 0
        l2   = count_kw(df["نوع الإحالة"], ["إنقاذ"]) if "نوع الإحالة" in df.columns else 0
        kpi4([tot2, r2, u2, l2],
             ["عدد الإحالات","روتينية","طارئة","إنقاذ حياة"],
             ["kb","kg","ko","kr"], ["📋","✅","⚡","🚨"])
        st.markdown("---")

        # ── Chart: حالة الإحالة ───────────────────────────────────
        if "حالة الإحالة" in df.columns:
            sec("حالة الإحالة", "📊")
            st.plotly_chart(bar_v(df["حالة الإحالة"], h=420),
                            use_container_width=True)
        st.markdown("---")

        # ── Charts: التخصص الرئيسي | الجنسية ────────────────────
        c1, c2 = st.columns([2.6, 1.6])
        with c1:
            if "التخصص الرئيسي" in df.columns:
                sec("التخصص الرئيسي", "🩺")
                pie_chart(df["التخصص الرئيسي"], h=460, col_key="t2_spec")
        with c2:
            if NC in df.columns:
                sec("الجنسية", "🌍")
                pie_chart(nat_binary(df, NC), h=460,
                          colors=["#1256a0","#72c4f8"], col_key="t2_nat")
        st.markdown("---")

        # ── Chart: سبب الإحالة ────────────────────────────────────
        if "سبب الإحالة" in df.columns:
            sec("سبب الإحالة", "📋")
            st.plotly_chart(bar_v(df["سبب الإحالة"], h=430),
                            use_container_width=True)
        st.markdown("---")

        # ── Charts: نوع السرير | جدول المستشفيات المستقبلة ───────
        c3, c4 = st.columns([2.6, 1.6])
        with c3:
            if "نوع السرير المطلوب" in df.columns:
                sec("نوع السرير المطلوب", "🛏️")
                st.plotly_chart(bar_h(df["نوع السرير المطلوب"], h=380),
                                use_container_width=True)
        with c4:
            if "المستشفى المستقبل" in df.columns:
                sec("أعلى المستشفيات المستقبِلة", "🏥")
                t7 = df["المستشفى المستقبل"].value_counts().head(8).reset_index()
                t7.columns = ["المستشفى","العدد"]
                st.dataframe(t7, use_container_width=True, hide_index=True, height=320)
        st.markdown("---")

        # ── Chart: المستشفى المرسل ────────────────────────────────
        if "المستشفى المرسل" in df.columns:
            sec("المستشفى المرسل – أعلى 10", "🏥")
            st.plotly_chart(bar_h(df["المستشفى المرسل"], h=400, top_n=10),
                            use_container_width=True)

        # ── Optional pies: إحالة عكسية / حاج ─────────────────────
        ext = [c for c in ["هل الإحالة عكسية؟","هل المريض معتمر / حاج ؟"]
               if c in df.columns]
        if ext:
            st.markdown("---")
            ec = st.columns(len(ext))
            for idx, (ew, en) in enumerate(zip(ec, ext)):
                with ew:
                    sec(en, "🔄")
                    pie_chart(df[en], h=340, col_key=f"t2_ext{idx}")

# ════════════════════════════════════════════════════════════════════
#  TAB 3 – مؤشرات الطاقة الاستيعابية
# ════════════════════════════════════════════════════════════════════
with tab3:
    if df_b is None:
        st.info("⬆️ يرجى رفع ملف مؤشرات الطاقة الاستيعابية من الشريط الجانبي.")
    else:
        df0  = df_b.copy()
        OCC  = "حالة السرير"
        DC_B = "تاريخ الإنشاء"

        # ── Filter panel ──────────────────────────────────────────
        st.markdown('<div class="fp">', unsafe_allow_html=True)
        bf = st.columns([2, 2, 2.5, 1.4, 1.4])
        f_opts = sorted(df0["المنشأة"].dropna().unique().tolist())    if "المنشأة"        in df0.columns else []
        d_opts = sorted(df0["القسم العام"].dropna().unique().tolist()) if "القسم العام"    in df0.columns else []
        m_opts = sorted(df0["القسم الرئيسي"].dropna().unique().tolist()) if "القسم الرئيسي" in df0.columns else []
        sel_f  = bf[0].multiselect("المنشأة",        f_opts, placeholder="الكل", key="t3_f")
        sel_d  = bf[1].multiselect("القسم العام",    d_opts, placeholder="الكل", key="t3_d")
        sel_m  = bf[2].multiselect("القسم الرئيسي", m_opts, placeholder="الكل", key="t3_m")
        mn_b, mx_b = date_bounds(df0, DC_B)
        d0b = bf[3].date_input("📅 من",  value=mn_b or datetime.date.today(), key="t3_d0")
        d1b = bf[4].date_input("📅 إلى", value=mx_b or datetime.date.today(), key="t3_d1")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Apply filters ─────────────────────────────────────────
        df = apply_date(df0.copy(), DC_B, d0b, d1b)
        df = apply_multi(df, "المنشأة",        sel_f)
        df = apply_multi(df, "القسم العام",    sel_d)
        df = apply_multi(df, "القسم الرئيسي", sel_m)

        # ── KPI row ───────────────────────────────────────────────
        tot_b = len(df)
        occ_b = count_kw(df[OCC], ["مشغول"]) if OCC in df.columns else 0
        vac_b = count_kw(df[OCC], ["شاغر"])  if OCC in df.columns else 0
        sus_b = count_kw(df[OCC], ["موقوف"]) if OCC in df.columns else 0
        kpi4([tot_b, vac_b, occ_b, sus_b],
             ["إجمالي الأسرة","الشاغرة","المشغولة","موقوف مؤقتاً"],
             ["kb","kg","kr","ko"], ["🛏️","✅","🔴","⏸️"])
        st.markdown("---")

        # ── ICU + Ward occupancy cards ────────────────────────────
        Q     = "القسم الرئيسي"
        units = [("أسرة الأجنحة", ward_sub(df, Q))] + [
            (lbl, icu_sub(df, kws, Q))
            for lbl, kws in ICU_KEYS.items() if kws
        ]

        sec("إشغال أسرة الأجنحة والعنايات المركزة", "🏥")
        pcols = st.columns(6)

        for i, (lbl, sub) in enumerate(units):
            with pcols[i]:
                has_data = not sub.empty and OCC in sub.columns

                # Card wrapper
                st.markdown(
                    f'<div class="icu-card">'
                    f'<div class="icu-card-title">{lbl}</div>',
                    unsafe_allow_html=True)

                if has_data:
                    # Pie with HTML legend (swatch + label on same line)
                    pie_status(sub[OCC], h=230, key=f"icu_{i}")

                    # Summary numbers below pie
                    t_u = len(sub)
                    o_u = count_kw(sub[OCC], ["مشغول"])
                    v_u = count_kw(sub[OCC], ["شاغر"])
                    s_u = t_u - o_u - v_u
                    summary = (
                        f"الإجمالي: <b style='color:#1256a0'>{t_u}</b><br>"
                        f"مشغول: <b style='color:#c03030'>{o_u}</b> · "
                        f"شاغر: <b style='color:#1a7040'>{v_u}</b>"
                        + (f" · موقوف: <b style='color:#b06010'>{s_u}</b>"
                           if s_u > 0 else "")
                    )
                    st.markdown(
                        f"<div style='text-align:center;font-size:.73rem;"
                        f"color:#1a4060;line-height:1.9;background:#f0f8ff;"
                        f"border-radius:7px;padding:6px 4px;margin-top:2px'>"
                        f"{summary}</div>",
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        "<div style='text-align:center;color:#88aac0;"
                        "padding:40px 0;font-size:.78rem'>لا توجد<br>بيانات</div>",
                        unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)   # close .icu-card

        st.markdown("---")

        # ── أسرة العزل ───────────────────────────────────────────
        if "هل عزل" in df.columns:
            sec("أسرة العزل", "🔒")
            iso = df[df["هل عزل"].astype(str)
                     .str.contains("نعم|yes|true|1", case=False, na=False)]
            it = len(iso)
            io = count_kw(iso[OCC], ["مشغول"]) if OCC in iso.columns else 0
            iv = count_kw(iso[OCC], ["شاغر"])  if OCC in iso.columns else 0
            ik = st.columns([1, 1, 1, 3.5])
            ik[0].markdown(
                f'<div class="kc kb" style="margin:0;padding:11px 8px">'
                f'<div class="kl">إجمالي العزل</div>'
                f'<div class="kv" style="font-size:1.5rem;color:#1256a0">{it}</div></div>',
                unsafe_allow_html=True)
            ik[1].markdown(
                f'<div class="kc kg" style="margin:0;padding:11px 8px">'
                f'<div class="kl">الشاغرة</div>'
                f'<div class="kv" style="font-size:1.5rem;color:#166038">{iv}</div></div>',
                unsafe_allow_html=True)
            ik[2].markdown(
                f'<div class="kc kr" style="margin:0;padding:11px 8px">'
                f'<div class="kl">المشغولة</div>'
                f'<div class="kv" style="font-size:1.5rem;color:#a02020">{io}</div></div>',
                unsafe_allow_html=True)
            with ik[3]:
                if "المنشأة" in iso.columns and "القسم العام" in iso.columns:
                    it2 = iso.groupby(["المنشأة","القسم العام"]).size().reset_index(name="العدد")
                    it2 = it2.sort_values("العدد", ascending=False).head(12)
                    st.dataframe(it2, use_container_width=True, hide_index=True, height=180)
            st.markdown("---")

        # ── معدل إشغال الأسرة لكل قسم ───────────────────────────
        if OCC in df.columns and Q in df.columns:
            sec("معدل إشغال الأسرة لكل قسم", "📊")
            rate = (
                df.groupby(Q)
                  .apply(lambda g: round(
                      100 * count_kw(g[OCC], ["مشغول"]) / len(g), 1)
                      if len(g) > 0 else 0.0)
                  .reset_index(name="pct")
            )
            rate = rate.sort_values("pct", ascending=False)

            def bclr(v):
                if v >= 90: return "#d94040"
                if v >= 75: return "#e09020"
                if v >= 50: return "#c0a820"
                return "#2aaa60"

            mx_r = rate["pct"].max() if len(rate) > 0 else 100
            annots_r = [
                dict(x=row[Q], y=row["pct"],
                     text=f"<b>{row['pct']}%</b>",
                     xanchor="center", yanchor="bottom",
                     showarrow=False,
                     font=dict(size=9, family="Cairo", color=FONT),
                     yshift=4)
                for _, row in rate.iterrows()
            ]
            fig_r = go.Figure(go.Bar(
                x=rate[Q], y=rate["pct"],
                marker_color=[bclr(v) for v in rate["pct"]],
                marker_line_color="#a8c8e0", marker_line_width=.8,
                text=None,
                hovertemplate="<b>%{x}</b><br>%{y}%<extra></extra>",
            ))
            fig_r.update_layout(**_layout(480, mb=100), annotations=annots_r)
            fig_r.update_xaxes(**_xax(tickangle=-42))
            fig_r.update_yaxes(**_yax(range=[0, mx_r * 1.24], ticksuffix="%"))
            st.plotly_chart(fig_r, use_container_width=True)

            st.markdown("""<div class="lrow">
              <span><span class="ld" style="background:#d94040"></span>≥ 90% ممتلئ</span>
              <span><span class="ld" style="background:#e09020"></span>75–90% مرتفع</span>
              <span><span class="ld" style="background:#c0a820"></span>50–75% متوسط</span>
              <span><span class="ld" style="background:#2aaa60"></span>&lt; 50% منخفض</span>
            </div>""", unsafe_allow_html=True)
            st.markdown("---")

        # ── حالة السرير حسب المنشأة (stacked bar) ────────────────
        if "المنشأة" in df.columns and OCC in df.columns:
            sec("حالة السرير حسب المنشأة", "🏨")
            cross = df.groupby(["المنشأة", OCC]).size().reset_index(name="العدد")
            fig_c = px.bar(
                cross, x="المنشأة", y="العدد", color=OCC, barmode="stack",
                color_discrete_map={
                    "مشغول":        "#e05c5c",
                    "شاغر":         "#3ab87a",
                    "موقوف مؤقتا":  "#e8b040",
                    "موقوف مؤقتاً": "#e8b040",
                })
            fig_c.update_layout(**_layout(460, mb=70))
            fig_c.update_xaxes(**_xax(tickangle=-30))
            fig_c.update_yaxes(**_yax())
            fig_c.update_layout(
                legend=dict(font=dict(family="Cairo", size=11, color=FONT),
                            bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_c, use_container_width=True)
