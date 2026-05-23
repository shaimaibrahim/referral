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

/* ── Dashboard header – deep navy matching JFHC brand ── */
.dash-hdr{
  background:linear-gradient(110deg,#061e3a 0%,#0d3a70 50%,#061e3a 100%);
  border-radius:12px;padding:14px 26px;margin-bottom:14px;
  display:flex;align-items:center;justify-content:space-between;
  border:1px solid #1a4a80;
  box-shadow:0 6px 28px rgba(4,20,50,.55);}
.dash-hdr-t{color:#ffffff;font-size:1.42rem;font-weight:900;margin:0;
  letter-spacing:.3px;text-shadow:0 1px 6px rgba(0,0,0,.3);}
.dash-hdr-s{color:#7ab8e0;font-size:.76rem;margin-top:2px;}

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

/* ── Dataframe: navy header, very light rows, dark text ── */
[data-testid="stDataFrame"] table{border-collapse:collapse!important;}
[data-testid="stDataFrame"] thead tr th{
  background:#0e3f7a!important;color:#ffffff!important;
  font-size:.83rem!important;font-weight:700!important;
  border:1px solid #0a2e5a!important;padding:8px 10px!important;}
[data-testid="stDataFrame"] tbody tr td{
  background:#f8fbff!important;color:#0d2840!important;
  font-size:.83rem!important;border:1px solid #ddeef8!important;
  padding:7px 10px!important;}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td{background:#edf4fc!important;}
[data-testid="stDataFrame"] [data-testid="stDataFrameGlideDataEditor"]{
  --gdg-bg-cell:#f8fbff!important;
  --gdg-bg-cell-medium:#edf4fc!important;
  --gdg-bg-header:#0e3f7a!important;
  --gdg-text-header:#ffffff!important;
  --gdg-text-dark:#0d2840!important;
  --gdg-border-color:#ddeef8!important;}

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
    """HTML legend table – every item on ONE ROW: [■] [Name] [Count] [(pct%)].
    All items are shown regardless of count (no truncation).
    Only blue/navy/sky shades are used (passed via 'colors')."""

    total = counts.sum()
    rows  = ""
    for (lbl, val), clr in zip(counts.items(), colors):
        pct = 100 * val / total
        rows += (
            f"<tr>"
            f"<td style='padding:3px 6px 3px 0;vertical-align:middle;white-space:nowrap'>"
            f"<span style='display:inline-block;width:13px;height:13px;"
            f"border-radius:3px;background:{clr};flex-shrink:0;"
            f"vertical-align:middle'></span></td>"
            f"<td style='padding:3px 8px 3px 0;color:#0d2840;font-weight:600;"
            f"font-size:.81rem;vertical-align:middle;white-space:nowrap'>{lbl}</td>"
            f"<td style='padding:3px 6px;color:#1256a0;font-weight:700;"
            f"font-size:.81rem;vertical-align:middle;text-align:left;"
            f"white-space:nowrap'>{val:,}</td>"
            f"<td style='padding:3px 2px;color:#4a7090;font-size:.75rem;"
            f"vertical-align:middle;white-space:nowrap'>({pct:.1f}%)</td>"
            f"</tr>"
        )
    # No max-height cap – show all items; container scrolls if truly needed
    return (
        f"<div style='overflow-y:auto;direction:rtl;padding-top:4px'>"
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
    # Build a full palette that covers ALL items using only blue/navy/sky tones.
    # If there are more items than base colours, cycle through the palette.
    base_palette = colors or PIE_BLUE
    n = len(counts)
    clrs = [base_palette[i % len(base_palette)] for i in range(n)]

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

    # Split: pie on left (wider), HTML legend on right showing ALL items
    col_a, col_b = st.columns([1.5, 1])
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
        # Add end-of-day so the chosen end date is fully included
        end = pd.Timestamp(d1) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        df = df[df[col] <= end]
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
  <div style="display:flex;align-items:center;gap:18px">
    <img src="data:image/png;base64,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" height="58" style="object-fit:contain;display:block"/>
    <div>
      <div class="dash-hdr-s">Jeddah First Health Cluster · إدارة الإحالات والطاقات الاستيعابية</div>
      <div class="dash-hdr-t">تجمع جـــدة الصحي الأول</div>
    </div>
  </div>
  <div style="color:#80b8e0;font-size:.78rem;text-align:left;line-height:1.9">
    لوحة التحكم التشغيلية<br>
    <span style="color:#c8e8ff;font-weight:800;font-size:.82rem">
      مؤشرات الإحالات والطاقة الاستيعابية
    </span>
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

        # Row 1: first 3 units
        row1 = st.columns(3)
        # Row 2: next 3 units
        row2 = st.columns(3)
        pcols = row1 + row2

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

        # ── معدل إشغال الأسرة لكل قسم (مصنف بالقسم الرئيسي + المنشأة) ────
        if OCC in df.columns and Q in df.columns and "المنشأة" in df.columns:
            sec("معدل إشغال الأسرة لكل قسم", "📊")

            # Group by القسم الرئيسي + المنشأة for full context
            rate = (
                df.groupby([Q, "المنشأة"])
                  .apply(lambda g: round(
                      100 * count_kw(g[OCC], ["مشغول"]) / len(g), 1)
                      if len(g) > 0 else 0.0)
                  .reset_index(name="pct")
            )
            # Abbreviation map for hospital names → short code
            HOSP_ABBR = {
                "مستشفى الملك عبد العزيز بجدة":           "KAH",
                "مستشفى الملك عبدالعزيز بجدة":            "KAH",
                "مستشفى الثغر العام":                      "ALTHAG",
                "مستشفى شرق جدة":                         "EJH",
                "مستشفى أضم العام":                        "ADAM",
                "مجمع إرادة والصحة النفسية بجدة":          "MHH",
                "مجمع ارادة والصحة النفسية بجدة":          "MHH",
                "مستشفى الليث العام":                      "ALLAITH",
            }
            def abbr(name):
                for full, short in HOSP_ABBR.items():
                    if full in str(name):
                        return short
                # fallback: take first word if still long
                words = str(name).split()
                return words[-1] if words else str(name)

            # Combined label: "القسم – اختصار المستشفى"
            rate["label"] = rate[Q] + "  –  " + rate["المنشأة"].apply(abbr)
            rate = rate.sort_values("pct", ascending=False)

            def bclr(v):
                if v >= 90: return "#d94040"
                if v >= 75: return "#e09020"
                if v >= 50: return "#c0a820"
                return "#2aaa60"

            mx_r = rate["pct"].max() if len(rate) > 0 else 100
            annots_r = [
                dict(x=row["label"], y=row["pct"],
                     text=f"<b>{row['pct']}%</b>",
                     xanchor="center", yanchor="bottom",
                     showarrow=False,
                     font=dict(size=9, family="Cairo", color=FONT),
                     yshift=4)
                for _, row in rate.iterrows()
            ]
            fig_r = go.Figure(go.Bar(
                x=rate["label"], y=rate["pct"],
                marker_color=[bclr(v) for v in rate["pct"]],
                marker_line_color="#a8c8e0", marker_line_width=.8,
                text=None,
                hovertemplate="<b>%{x}</b><br>معدل الإشغال: %{y}%<extra></extra>",
            ))
            fig_r.update_layout(**_layout(520, mb=130), annotations=annots_r)
            fig_r.update_xaxes(**_xax(tickangle=-45))
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
