# =========================================================
# JEDDAH FIRST HEALTH CLUSTER DASHBOARD
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="تجمع جدة الصحي الأول",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PASSWORD
# =========================================================

DASHBOARD_PASSWORD = "jfhc2025"

def check_password():

    if st.session_state.get("authenticated"):
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

    html, body, [class*="css"], * {
        font-family:'Cairo',sans-serif !important;
        direction:rtl;
    }

    .stApp {
        background:linear-gradient(135deg,#eaf2fb 0%,#dbeaf7 100%);
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1,2,1])

    with col:

        st.markdown("""
        <div style="
            background:#fff;
            border:1px solid #c8dff0;
            border-radius:18px;
            padding:48px 40px;
            box-shadow:0 8px 32px rgba(30,100,180,0.12);
            text-align:center;
            margin-top:60px">

          <div style="font-size:3rem">🏥</div>

          <div style="
              color:#1a6ab0;
              font-size:0.82rem;
              font-weight:700;
              letter-spacing:2px;
              margin:6px 0 2px">
              JEDDAH FIRST HEALTH CLUSTER
          </div>

          <div style="
              color:#0d2f54;
              font-size:1.35rem;
              font-weight:900">
              تجمع جدة الصحي الأول
          </div>

          <div style="
              color:#5a8aaa;
              font-size:0.82rem;
              margin-top:4px;
              margin-bottom:28px">
              نظام إدارة الإحالات والطاقة الاستيعابية
          </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        password = st.text_input(
            "",
            type="password",
            placeholder="🔑 أدخل كلمة المرور",
            label_visibility="collapsed"
        )

        if st.button("دخول →", use_container_width=True):

            if password == DASHBOARD_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()

            else:
                st.error("❌ كلمة المرور غير صحيحة")

    return False


if not check_password():
    st.stop()

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;900&display=swap');

html, body, [class*="css"], * {
    font-family:'Cairo',sans-serif !important;
    direction:rtl;
}

.stApp {
    background:#f0f5fb;
    color:#1a3050;
}

.block-container {
    padding:1rem 1.5rem 2rem 1.5rem !important;
    max-width:100% !important;
}

[data-testid="stSidebar"] {
    background:#ffffff;
    border-left:1px solid #d0e0ef;
}

[data-testid="stSidebar"] * {
    color:#234b6d !important;
}

.dash-header {
    background:linear-gradient(120deg,#1a6ab0,#2080d0);
    border-radius:16px;
    padding:18px 28px;
    margin-bottom:20px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    box-shadow:0 4px 20px rgba(26,106,176,.25);
}

.dash-header-title {
    color:white;
    font-size:1.5rem;
    font-weight:900;
}

.dash-header-sub {
    color:#dceeff;
    font-size:.82rem;
}

.kpi-row {
    display:flex;
    gap:12px;
    margin-bottom:16px;
}

.kpi-card {
    flex:1;
    padding:18px;
    border-radius:14px;
    text-align:center;
    box-shadow:0 3px 12px rgba(0,0,0,.08);
}

.kblue {
    background:linear-gradient(145deg,#e8f3fc,#d0e8f8);
    border:1px solid #9ac8ee;
}

.kgreen {
    background:linear-gradient(145deg,#e8f8f0,#cceedd);
    border:1px solid #80ccaa;
}

.korange {
    background:linear-gradient(145deg,#fff4e5,#ffe5c0);
    border:1px solid #f0b060;
}

.kred {
    background:linear-gradient(145deg,#fdecea,#fad8d8);
    border:1px solid #f09090;
}

.kpi-val {
    font-size:2rem;
    font-weight:900;
}

.sec-title {
    display:flex;
    align-items:center;
    gap:8px;
    background:#e7f1fb;
    border-right:5px solid #2080d0;
    border-radius:8px;
    padding:10px 14px;
    font-weight:800;
    margin-bottom:12px;
    color:#0f3760;
}

.filter-panel {
    background:#e8f2fb;
    border:1px solid #b8d5ee;
    border-radius:12px;
    padding:14px;
    margin-bottom:18px;
}

.stTabs [data-baseweb="tab-list"] {
    background:#dcecf9;
    border-radius:12px;
    padding:4px;
}

.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#1a6ab0,#2080d0) !important;
    color:white !important;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# COLORS
# =========================================================

C = dict(
    blue1="#1a5a9a",
    blue2="#2080d0",
    green="#1a9060",
    orange="#d08010",
    red="#c03030",
    yellow="#b09010",
    teal="#1098a0",
    purple="#6040b0",
)

# =========================================================
# HELPERS
# =========================================================

def section(title, icon="📊"):

    st.markdown(
        f'<div class="sec-title">{icon} {title}</div>',
        unsafe_allow_html=True
    )


def kpi_cards(values, labels, classes, icons):

    html = '<div class="kpi-row">'

    for v, l, c, i in zip(values, labels, classes, icons):

        html += f"""
        <div class="kpi-card {c}">
            <div style="font-size:1.3rem">{i}</div>
            <div style="font-size:.75rem;font-weight:700;margin:5px 0">
                {l}
            </div>
            <div class="kpi-val">{v:,}</div>
        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


def load_file(file):

    if file is None:
        return None

    try:

        if file.name.endswith(".csv"):

            for enc in ["utf-8-sig","utf-8","cp1256","iso-8859-6"]:

                try:
                    return pd.read_csv(file, encoding=enc)

                except:
                    file.seek(0)

        else:
            return pd.read_excel(file)

    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")

    return None


def to_datetime(df, col):

    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def apply_date_filter(df, col, start_date, end_date):

    if col not in df.columns:
        return df

    df = to_datetime(df.copy(), col)

    if start_date:
        df = df[df[col] >= pd.Timestamp(start_date)]

    if end_date:
        df = df[df[col] <= pd.Timestamp(end_date)]

    return df


def get_date_bounds(df, col):

    if col not in df.columns:
        return None, None

    df = to_datetime(df.copy(), col)

    valid_dates = df[col].dropna()

    if valid_dates.empty:
        return None, None

    return valid_dates.min().date(), valid_dates.max().date()


def count_keyword(series, keywords):

    return int(
        series.astype(str).str.contains(
            "|".join(keywords),
            na=False,
            case=False
        ).sum()
    )


# =========================================================
# CHARTS
# =========================================================

def bar_chart(series, color="#2080d0", height=420):

    counts = series.value_counts()

    fig = go.Figure(go.Bar(
        x=counts.index.astype(str),
        y=counts.values,
        marker_color=color,
        text=counts.values,
        textposition="outside"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.7)",
        height=height,
        font=dict(family="Cairo"),
        margin=dict(l=10,r=10,t=30,b=50),
    )

    return fig


def pie_chart(series, height=380):

    counts = series.value_counts()

    fig = go.Figure(go.Pie(
        labels=counts.index.astype(str),
        values=counts.values,
        hole=.45,
        textinfo="percent+label"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        font=dict(family="Cairo")
    )

    return fig


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📂 رفع الملفات")

    st.markdown("---")

    st.markdown("### 📤 الإحالات المرسلة")

    file_sent = st.file_uploader(
        "",
        type=["csv","xlsx"],
        key="sent",
        label_visibility="collapsed"
    )

    st.markdown("### 📥 الإحالات المستقبلة")

    file_received = st.file_uploader(
        "",
        type=["csv","xlsx"],
        key="recv",
        label_visibility="collapsed"
    )

    st.markdown("### 🛏️ الطاقة الاستيعابية")

    file_beds = st.file_uploader(
        "",
        type=["csv","xlsx"],
        key="beds",
        label_visibility="collapsed"
    )

    st.markdown("---")

    if st.button("🔒 تسجيل الخروج", use_container_width=True):

        st.session_state.authenticated = False
        st.rerun()

# =========================================================
# LOAD DATA
# =========================================================

df_sent_raw = load_file(file_sent)
df_received_raw = load_file(file_received)
df_beds_raw = load_file(file_beds)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="dash-header">

    <div>
        <div class="dash-header-sub">
            Jeddah First Health Cluster Dashboard
        </div>

        <div class="dash-header-title">
            🏥 تجمع جدة الصحي الأول
        </div>
    </div>

    <div style="color:white;font-weight:700">
        لوحة التحكم التشغيلية
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "📤 الإحالات المرسلة",
    "📥 الإحالات المستقبلة",
    "🛏️ الطاقة الاستيعابية"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    if df_sent_raw is None:

        st.info("⬆️ يرجى رفع ملف الإحالات المرسلة")

    else:

        df = df_sent_raw.copy()

        DATE_COL = "تاريخ الإنشاء"

        mn, mx = get_date_bounds(df, DATE_COL)

        st.markdown('<div class="filter-panel">', unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        start_date = c1.date_input(
            "📅 من",
            value=mn or datetime.date.today()
        )

        end_date = c2.date_input(
            "📅 إلى",
            value=mx or datetime.date.today()
        )

        st.markdown('</div>', unsafe_allow_html=True)

        df = apply_date_filter(df, DATE_COL, start_date, end_date)

        total = len(df)

        routine = count_keyword(df["نوع الإحالة"], ["روتين"]) \
            if "نوع الإحالة" in df.columns else 0

        emergency = count_keyword(df["نوع الإحالة"], ["طارئ"]) \
            if "نوع الإحالة" in df.columns else 0

        life = count_keyword(df["نوع الإحالة"], ["إنقاذ"]) \
            if "نوع الإحالة" in df.columns else 0

        kpi_cards(
            [total, routine, emergency, life],
            ["عدد الإحالات", "روتينية", "طارئة", "إنقاذ حياة"],
            ["kblue","kgreen","korange","kred"],
            ["📋","✅","⚡","🚨"]
        )

        st.markdown("---")

        col1, col2 = st.columns([2,1])

        with col1:

            if "حالة الإحالة" in df.columns:

                section("حالة الإحالة")

                st.plotly_chart(
                    bar_chart(df["حالة الإحالة"]),
                    use_container_width=True
                )

        with col2:

            if "التخصص الرئيسي" in df.columns:

                section("التخصص الرئيسي")

                st.plotly_chart(
                    pie_chart(df["التخصص الرئيسي"]),
                    use_container_width=True
                )

# =========================================================
# TAB 2
# =========================================================

with tab2:

    if df_received_raw is None:

        st.info("⬆️ يرجى رفع ملف الإحالات المستقبلة")

    else:

        df = df_received_raw.copy()

        total = len(df)

        routine = count_keyword(df["نوع الإحالة"], ["روتين"]) \
            if "نوع الإحالة" in df.columns else 0

        emergency = count_keyword(df["نوع الإحالة"], ["طارئ"]) \
            if "نوع الإحالة" in df.columns else 0

        life = count_keyword(df["نوع الإحالة"], ["إنقاذ"]) \
            if "نوع الإحالة" in df.columns else 0

        kpi_cards(
            [total, routine, emergency, life],
            ["عدد الإحالات", "روتينية", "طارئة", "إنقاذ حياة"],
            ["kblue","kgreen","korange","kred"],
            ["📋","✅","⚡","🚨"]
        )

        st.markdown("---")

        col1, col2 = st.columns([2,1])

        with col1:

            if "حالة الإحالة" in df.columns:

                section("حالة الإحالة")

                st.plotly_chart(
                    bar_chart(df["حالة الإحالة"]),
                    use_container_width=True
                )

        with col2:

            if "التخصص الرئيسي" in df.columns:

                section("التخصص الرئيسي")

                st.plotly_chart(
                    pie_chart(df["التخصص الرئيسي"]),
                    use_container_width=True
                )

# =========================================================
# TAB 3
# =========================================================

with tab3:

    if df_beds_raw is None:

        st.info("⬆️ يرجى رفع ملف الطاقة الاستيعابية")

    else:

        df = df_beds_raw.copy()

        OCC = "حالة السرير"

        total_beds = len(df)

        occupied = count_keyword(df[OCC], ["مشغول"]) \
            if OCC in df.columns else 0

        available = count_keyword(df[OCC], ["شاغر"]) \
            if OCC in df.columns else 0

        suspended = count_keyword(
            df[OCC],
            ["موقوف","موقوف مؤقتا","موقوف مؤقتاً"]
        ) if OCC in df.columns else 0

        kpi_cards(
            [total_beds, available, occupied, suspended],
            ["إجمالي الأسرة", "الشاغرة", "المشغولة", "الموقوفة"],
            ["kblue","kgreen","kred","korange"],
            ["🛏️","✅","🔴","⏸️"]
        )

        st.markdown("---")

        if OCC in df.columns:

            section("حالة الأسرة")

            st.plotly_chart(
                pie_chart(df[OCC]),
                use_container_width=True
            )

        if "القسم الرئيسي" in df.columns:

            section("الأقسام الرئيسية")

            st.plotly_chart(
                bar_chart(df["القسم الرئيسي"]),
                use_container_width=True
            )

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    color:#6b8aa8;
    font-size:.85rem">

    © تجمع جدة الصحي الأول — لوحة التحكم التشغيلية

</div>
""", unsafe_allow_html=True)