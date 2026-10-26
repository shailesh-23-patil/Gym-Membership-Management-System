import html
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from database import (
    init_db,
    query_df,
    execute,
    get_one,
    add_membership,
    refresh_membership_statuses,
)
from auth import authenticate, create_user


# ======================================================================
#  APP CONFIGURATION
# ======================================================================

st.set_page_config(
    page_title="Gym Membership Management",
    page_icon="🏋️",
    layout="wide",
)

init_db()
refresh_membership_statuses()


# ======================================================================
#  THEME / CSS
# ======================================================================

ACCENT = "#ff5a1f"
ACCENT_2 = "#ffb020"
GREEN = "#22c55e"
RED = "#ef4444"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap');

:root {
    --bg: #0b0d12;
    --panel: #141821;
    --panel-2: #1a1f2b;
    --border: #262c3a;
    --text: #eef1f6;
    --muted: #8b93a7;
    --accent: #ff5a1f;
    --accent-2: #ffb020;
    --ok: #22c55e;
    --bad: #ef4444;
}

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

.stApp {
    background:
        radial-gradient(1000px 500px at 85% -10%, rgba(255,90,31,0.14), transparent 60%),
        radial-gradient(800px 400px at -10% 110%, rgba(255,176,32,0.08), transparent 60%),
        var(--bg);
}

#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1300px; }

h1, h2, h3 { font-family: 'Oswald', sans-serif !important; letter-spacing: .5px; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10141c 0%, #0b0d12 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

.brand { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.brand-logo {
    width: 44px; height: 44px; border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; box-shadow: 0 6px 20px rgba(255,90,31,.35);
}
.brand-text {
    font-family: 'Oswald', sans-serif; font-size: 22px; font-weight: 700;
    letter-spacing: 1.5px; line-height: 1;
}
.brand-sub { font-size: 11px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; }

.user-card {
    display: flex; align-items: center; gap: 12px;
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 14px; padding: 12px 14px; margin-bottom: 18px;
}
.avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; color: #fff; font-size: 16px;
}
.user-name { font-weight: 600; font-size: 14px; }
.role-pill {
    display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 1px;
    padding: 2px 8px; border-radius: 99px; margin-top: 2px;
    background: rgba(255,90,31,.15); color: var(--accent); text-transform: uppercase;
}

[data-testid="stSidebar"] [role="radiogroup"] { gap: 6px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent; border: 1px solid transparent;
    border-radius: 12px; padding: 10px 14px; width: 100%;
    transition: all .18s ease; cursor: pointer;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: var(--panel); border-color: var(--border);
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label p { font-weight: 500; font-size: 15px; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(255,90,31,.22), rgba(255,90,31,.04));
    border-color: rgba(255,90,31,.45);
    box-shadow: inset 3px 0 0 var(--accent);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #fff; font-weight: 600;
}

/* ---------- Page header ---------- */
.page-header { margin-bottom: 22px; }
.page-title {
    font-family: 'Oswald', sans-serif; font-size: 38px; font-weight: 700;
    letter-spacing: 1px; margin: 0; line-height: 1.1;
}
.page-title span { color: var(--accent); }
.page-sub { color: var(--muted); font-size: 14px; margin-top: 4px; }

.section-title {
    font-family: 'Oswald', sans-serif; font-size: 20px; font-weight: 600;
    letter-spacing: .8px; margin: 26px 0 12px 0;
    display: flex; align-items: center; gap: 10px;
}
.section-title::before {
    content: ""; width: 4px; height: 20px; border-radius: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}

/* ---------- Stat cards ---------- */
.stat-card {
    position: relative; overflow: hidden;
    background: linear-gradient(145deg, var(--panel-2), var(--panel));
    border: 1px solid var(--border); border-radius: 18px;
    padding: 20px 22px; height: 100%;
    transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}
.stat-card:hover {
    transform: translateY(-4px); border-color: rgba(255,90,31,.5);
    box-shadow: 0 14px 34px rgba(0,0,0,.45);
}
.stat-card::after {
    content: ""; position: absolute; right: -40px; top: -40px;
    width: 120px; height: 120px; border-radius: 50%;
    background: var(--glow, rgba(255,90,31,.18)); filter: blur(12px);
}
.stat-icon {
    width: 42px; height: 42px; border-radius: 12px; font-size: 20px;
    display: flex; align-items: center; justify-content: center;
    background: var(--glow, rgba(255,90,31,.18)); margin-bottom: 14px;
}
.stat-label {
    color: var(--muted); font-size: 12px; font-weight: 600;
    letter-spacing: 1.4px; text-transform: uppercase;
}
.stat-value {
    font-family: 'Oswald', sans-serif; font-size: 34px; font-weight: 700;
    margin-top: 4px; line-height: 1.1;
}
.stat-hint { color: var(--muted); font-size: 12px; margin-top: 6px; }

/* ---------- Plan cards ---------- */
.plan-card {
    background: linear-gradient(160deg, var(--panel-2), var(--panel));
    border: 1px solid var(--border); border-radius: 20px;
    padding: 24px; height: 100%; position: relative; overflow: hidden;
    transition: transform .2s ease, border-color .2s ease;
}
.plan-card:hover { transform: translateY(-5px); border-color: rgba(255,90,31,.55); }
.plan-card.off { opacity: .5; filter: grayscale(.6); }
.plan-name {
    font-family: 'Oswald', sans-serif; font-size: 22px; font-weight: 600; letter-spacing: 1px;
}
.plan-price {
    font-family: 'Oswald', sans-serif; font-size: 40px; font-weight: 700;
    margin: 8px 0 2px 0;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.plan-duration { color: var(--muted); font-size: 13px; margin-bottom: 14px; }
.plan-desc { font-size: 14px; color: #c3c9d6; min-height: 40px; }
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 99px;
    font-size: 11px; font-weight: 700; letter-spacing: .8px; text-transform: uppercase;
}
.badge.on  { background: rgba(34,197,94,.15); color: var(--ok); }
.badge.off { background: rgba(239,68,68,.15); color: var(--bad); }

/* ---------- Login ---------- */
.hero {
    background:
        linear-gradient(160deg, rgba(255,90,31,.92), rgba(255,176,32,.85)),
        #ff5a1f;
    border-radius: 26px; padding: 48px 42px; min-height: 520px;
    color: #fff; position: relative; overflow: hidden;
    box-shadow: 0 24px 60px rgba(255,90,31,.25);
}
.hero::after {
    content: "🏋️"; position: absolute; right: -10px; bottom: -30px;
    font-size: 180px; opacity: .18; transform: rotate(-12deg);
}
.hero-tag {
    display: inline-block; background: rgba(0,0,0,.25); padding: 6px 14px;
    border-radius: 99px; font-size: 12px; letter-spacing: 2px; font-weight: 600;
    text-transform: uppercase; margin-bottom: 22px;
}
.hero h1 {
    font-size: 56px !important; line-height: 1.02 !important; margin: 0 0 16px 0;
    text-transform: uppercase; color: #fff;
}
.hero p { font-size: 16px; opacity: .95; max-width: 420px; }
.chips { margin-top: 26px; display: flex; flex-wrap: wrap; gap: 10px; }
.chip {
    background: rgba(0,0,0,.22); padding: 8px 14px; border-radius: 99px;
    font-size: 13px; font-weight: 600;
}
.login-title {
    font-family: 'Oswald', sans-serif; font-size: 32px; font-weight: 700; margin-bottom: 2px;
}
.login-sub { color: var(--muted); font-size: 14px; margin-bottom: 18px; }
.hint-box {
    background: rgba(255,176,32,.08); border: 1px dashed rgba(255,176,32,.45);
    border-radius: 12px; padding: 12px 14px; font-size: 13px; color: #ffd98a; margin-top: 14px;
}

/* ---------- Role picker cards ---------- */
.role-card {
    background: linear-gradient(160deg, var(--panel-2), var(--panel));
    border: 1px solid var(--border); border-radius: 22px;
    padding: 28px 22px; text-align: center; margin-bottom: 12px;
    transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}
.role-card:hover {
    transform: translateY(-5px); border-color: rgba(255,90,31,.6);
    box-shadow: 0 16px 36px rgba(0,0,0,.45);
}
.role-icon {
    width: 70px; height: 70px; border-radius: 20px; margin: 0 auto 16px auto;
    display: flex; align-items: center; justify-content: center; font-size: 34px;
    background: linear-gradient(135deg, rgba(255,90,31,.25), rgba(255,176,32,.15));
}
.role-title {
    font-family: 'Oswald', sans-serif; font-size: 24px; font-weight: 600; letter-spacing: 1px;
}
.role-desc { color: var(--muted); font-size: 13px; margin-top: 6px; min-height: 54px; }

/* ---------- Inputs ---------- */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input,
[data-baseweb="select"] > div {
    background: var(--panel) !important; color: var(--text) !important;
    border: 1px solid var(--border) !important; border-radius: 12px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(255,90,31,.2) !important;
}
[data-testid="stWidgetLabel"] p { color: #c3c9d6; font-weight: 500; font-size: 13px; }

/* ---------- Forms & containers ---------- */
[data-testid="stForm"] {
    background: linear-gradient(160deg, var(--panel-2), var(--panel));
    border: 1px solid var(--border); border-radius: 20px; padding: 26px;
}

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    border-radius: 12px; font-weight: 600; padding: .6rem 1.2rem;
    border: 1px solid var(--border); background: var(--panel-2); color: var(--text);
    transition: all .18s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
    border-color: var(--accent); color: #fff; transform: translateY(-1px);
}
button[kind="primary"], button[kind="primaryFormSubmit"] {
    background: linear-gradient(90deg, var(--accent), var(--accent-2)) !important;
    color: #fff !important; border: none !important;
    box-shadow: 0 8px 22px rgba(255,90,31,.35);
}
button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {
    box-shadow: 0 12px 28px rgba(255,90,31,.5); filter: brightness(1.08);
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: var(--panel); padding: 6px;
    border-radius: 14px; border: 1px solid var(--border); width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; padding: 8px 20px; background: transparent; font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, var(--accent), var(--accent-2)) !important; color: #fff !important;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* ---------- Tables / alerts ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border); border-radius: 16px; overflow: hidden;
}
[data-testid="stAlert"] { border-radius: 14px; border: 1px solid var(--border); }
hr { border-color: var(--border) !important; }
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ======================================================================
#  HELPERS
# ======================================================================

def money(value):
    """Format a number as Indian rupees."""
    return f"₹{float(value or 0):,.2f}"


def esc(value):
    """Escape user data before placing it inside HTML."""
    return html.escape(str(value if value is not None else ""))


def page_header(icon, title, subtitle=""):
    first, *rest = title.split(" ", 1)
    styled = f"<span>{esc(first)}</span> {esc(rest[0])}" if rest else f"<span>{esc(first)}</span>"
    st.markdown(
        f'<div class="page-header">'
        f'<div class="page-title">{icon} {styled}</div>'
        f'<div class="page-sub">{esc(subtitle)}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="section-title">{esc(title)}</div>', unsafe_allow_html=True)


def stat_card(icon, label, value, hint="", glow="rgba(255,90,31,.18)"):
    st.markdown(
        f'<div class="stat-card" style="--glow:{glow}">'
        f'<div class="stat-icon">{icon}</div>'
        f'<div class="stat-label">{esc(label)}</div>'
        f'<div class="stat-value">{esc(value)}</div>'
        f'<div class="stat-hint">{esc(hint)}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


STATUS_ICON = {
    "Active": "🟢 Active",
    "Expired": "🔴 Expired",
    "Inactive": "⚪ Inactive",
}


def with_status_icons(df, column="status"):
    df = df.copy()
    if column in df.columns:
        df[column] = df[column].map(lambda s: STATUS_ICON.get(s, s))
    return df


def style_fig(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#c3c9d6"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        height=340,
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


# ======================================================================
#  LOGIN PAGE (ROLE PICKER -> STAFF LOGIN / ADMIN LOGIN)
# ======================================================================

def set_login_mode(mode):
    st.session_state["login_mode"] = mode


def login_hero():
    st.markdown(
        """
<div class="hero">
<div class="hero-tag">Gym Management Suite</div>
<h1>Train hard.<br>Manage smart.</h1>
<p>Members, plans, payments and renewals, all in one powerful dashboard built for your gym team.</p>
<div class="chips">
<span class="chip">🧑‍💼 Staff Desk</span>
<span class="chip">🛡️ Admin Panel</span>
<span class="chip">💳 Payments</span>
<span class="chip">📈 Reports</span>
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def role_login_form(expected_role, icon, title, subtitle, form_key, hint_html):
    """Shared login form. Only accepts accounts that match expected_role."""
    st.button(
        "← Back",
        key=f"back_{form_key}",
        on_click=set_login_mode,
        args=(None,),
    )

    st.markdown(
        f'<div class="login-title">{title} {icon}</div>'
        f'<div class="login-sub">{subtitle}</div>',
        unsafe_allow_html=True,
    )

    with st.form(form_key):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input(
            "Password", type="password", placeholder="Enter your password"
        )
        submitted = st.form_submit_button(
            f"Sign in as {expected_role} →",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        account = authenticate(username, password)

        if account is None:
            st.error("Incorrect username or password.")
        elif account["role"] != expected_role:
            other = "Admin" if expected_role == "Staff" else "Staff"
            st.error(
                f"This is a {other} account. Please go back and use the "
                f"{other} login."
            )
        else:
            st.session_state["user"] = account
            st.session_state.pop("login_mode", None)
            st.rerun()

    st.markdown(hint_html, unsafe_allow_html=True)


def login_screen():
    mode = st.session_state.get("login_mode")

    st.write("")
    left, right = st.columns([1.1, 1.1], gap="large")

    with left:
        login_hero()

    with right:
        st.write("")

        # ---------- STEP 1: choose role ----------
        if mode is None:
            st.markdown(
                '<div class="login-title">Welcome 👋</div>'
                '<div class="login-sub">Choose how you would like to sign in.</div>',
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2, gap="medium")

            with c1:
                st.markdown(
                    '<div class="role-card">'
                    '<div class="role-icon">🧑‍💼</div>'
                    '<div class="role-title">Staff</div>'
                    '<div class="role-desc">Register members, record payments and handle renewals.</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )
                st.button(
                    "Staff Login →",
                    type="primary",
                    use_container_width=True,
                    key="pick_staff",
                    on_click=set_login_mode,
                    args=("staff",),
                )

            with c2:
                st.markdown(
                    '<div class="role-card">'
                    '<div class="role-icon">🛡️</div>'
                    '<div class="role-title">Admin</div>'
                    '<div class="role-desc">Full control: plans, reports and user accounts.</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )
                st.button(
                    "Admin Login →",
                    use_container_width=True,
                    key="pick_admin",
                    on_click=set_login_mode,
                    args=("admin",),
                )

        # ---------- STEP 2a: staff login ----------
        elif mode == "staff":
            role_login_form(
                expected_role="Staff",
                icon="🧑‍💼",
                title="Staff Login",
                subtitle="Sign in with the Staff account created by your Admin.",
                form_key="staff_login_form",
                hint_html=(
                    '<div class="hint-box">💡 Don\'t have a Staff account? '
                    "Ask your Admin to create one under "
                    "<b>User Management</b>.</div>"
                ),
            )

        # ---------- STEP 2b: admin login ----------
        else:
            role_login_form(
                expected_role="Admin",
                icon="🛡️",
                title="Admin Login",
                subtitle="Authorized Admin accounts only.",
                form_key="admin_login_form",
                hint_html=(
                    '<div class="hint-box">🔑 First-run Admin credentials: '
                    "<b>admin / Admin@123</b><br>"
                    "Educational demo only. Change the starter password "
                    "before using real information.</div>"
                ),
            )


# ======================================================================
#  SESSION CHECK
# ======================================================================

if "user" not in st.session_state:
    login_screen()
    st.stop()


user = st.session_state["user"]
is_admin = user["role"] == "Admin"


# ======================================================================
#  DASHBOARD
# ======================================================================

def dashboard():
    page_header(
        "📊",
        "Dashboard Overview",
        f"Today is {date.today().strftime('%A, %d %B %Y')}",
    )

    today = date.today()
    month_start = today.replace(day=1).isoformat()

    members = query_df("SELECT * FROM members")

    active_count = query_df(
        """SELECT COUNT(*) AS total
           FROM memberships
           WHERE status = 'Active' AND end_date >= ?""",
        (today.isoformat(),),
    ).iloc[0]["total"]

    expiring_count = query_df(
        """SELECT COUNT(*) AS total
           FROM memberships
           WHERE status = 'Active' AND end_date BETWEEN ? AND ?""",
        (
            today.isoformat(),
            (today + timedelta(days=7)).isoformat(),
        ),
    ).iloc[0]["total"]

    monthly_revenue = query_df(
        """SELECT COALESCE(SUM(amount), 0) AS total
           FROM payments
           WHERE payment_date >= ?""",
        (month_start,),
    ).iloc[0]["total"]

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        stat_card("👥", "Total Members", int(len(members)),
                  "All registered members", "rgba(255,90,31,.20)")
    with col2:
        stat_card("✅", "Active Memberships", int(active_count),
                  "Currently valid", "rgba(34,197,94,.20)")
    with col3:
        stat_card("⏳", "Expiring in 7 Days", int(expiring_count),
                  "Needs renewal soon", "rgba(255,176,32,.22)")
    with col4:
        stat_card("💰", "Revenue This Month", money(monthly_revenue),
                  f"Since {date.today().replace(day=1).strftime('%d %b')}",
                  "rgba(99,102,241,.22)")

    left, right = st.columns(2, gap="large")

    with left:
        section("Membership Status")

        status_data = query_df(
            """SELECT status, COUNT(*) AS count
               FROM memberships
               GROUP BY status"""
        )

        if not status_data.empty:
            fig = px.pie(
                status_data,
                names="status",
                values="count",
                hole=0.62,
                color="status",
                color_discrete_map={
                    "Active": GREEN,
                    "Expired": RED,
                    "Inactive": "#6b7280",
                },
            )
            fig.update_traces(
                textinfo="percent+label",
                marker=dict(line=dict(color="#0b0d12", width=3)),
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)
        else:
            st.info("Membership information will appear here.")

    with right:
        section("Monthly Revenue")

        revenue_data = query_df(
            """SELECT substr(payment_date, 1, 7) AS month,
                      SUM(amount) AS revenue
               FROM payments
               GROUP BY substr(payment_date, 1, 7)
               ORDER BY month DESC
               LIMIT 6"""
        ).sort_values("month")

        if not revenue_data.empty:
            fig = px.bar(
                revenue_data,
                x="month",
                y="revenue",
                labels={"month": "Month", "revenue": "Revenue (₹)"},
                color_discrete_sequence=[ACCENT],
            )
            fig.update_layout(bargap=0.35)
            st.plotly_chart(style_fig(fig), use_container_width=True)
        else:
            st.info("Payment information will appear here.")

    section("Recent Members")

    recent_members = query_df(
        """SELECT id, full_name, phone, email, joined_on, status
           FROM members
           ORDER BY id DESC
           LIMIT 8"""
    )

    st.dataframe(
        with_status_icons(recent_members),
        use_container_width=True,
        hide_index=True,
    )


# ======================================================================
#  MEMBER MANAGEMENT
# ======================================================================

def members_page():
    page_header("👥", "Member Management", "Register, search and update gym members.")

    register_tab, manage_tab = st.tabs(
        ["➕  Register Member", "🔍  Search / Edit Members"]
    )

    with register_tab:
        st.write("")
        with st.form("member_form", clear_on_submit=True):
            full_name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")

            col1, col2 = st.columns(2)
            phone = col1.text_input("Phone Number *", placeholder="10-digit mobile number")
            email = col2.text_input("Email", placeholder="name@example.com")

            col3, col4 = st.columns(2)
            gender = col3.selectbox(
                "Gender",
                ["Prefer not to say", "Female", "Male", "Other"],
            )
            joining_date = col4.date_input(
                "Joining Date",
                value=date.today(),
            )

            address = st.text_area("Address", placeholder="Street, city, PIN")

            submitted = st.form_submit_button(
                "Register Member",
                type="primary",
            )

        if submitted:
            if not full_name.strip() or not phone.strip():
                st.error("Full name and phone number are required.")
            else:
                execute(
                    """INSERT INTO members
                       (full_name, phone, email, gender, address,
                        joined_on, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        full_name.strip(),
                        phone.strip(),
                        email.strip(),
                        gender,
                        address.strip(),
                        joining_date.isoformat(),
                        "Active",
                    ),
                )
                st.toast("Member registered successfully.", icon="✅")
                st.rerun()

    with manage_tab:
        st.write("")
        search_term = st.text_input(
            "Search by member name or phone number",
            placeholder="🔍  Type a name or phone number...",
        )

        if search_term.strip():
            member_data = query_df(
                """SELECT id, full_name, phone, email, gender,
                          joined_on, status
                   FROM members
                   WHERE full_name LIKE ? OR phone LIKE ?
                   ORDER BY id DESC""",
                (
                    f"%{search_term.strip()}%",
                    f"%{search_term.strip()}%",
                ),
            )
        else:
            member_data = query_df(
                """SELECT id, full_name, phone, email, gender,
                          joined_on, status
                   FROM members
                   ORDER BY id DESC"""
            )

        st.caption(f"{len(member_data)} member(s) found")

        st.dataframe(
            with_status_icons(member_data),
            use_container_width=True,
            hide_index=True,
        )

        if not member_data.empty:
            section("Edit Member")

            selected_id = st.selectbox(
                "Select member to edit",
                member_data["id"].tolist(),
                format_func=lambda value: (
                    f"{value} - "
                    f"{member_data.loc[member_data.id == value, 'full_name'].iloc[0]}"
                ),
            )

            member = get_one(
                "SELECT * FROM members WHERE id = ?",
                (int(selected_id),),
            )

            if member is not None:
                with st.form("edit_member_form"):
                    updated_name = st.text_input(
                        "Full Name",
                        value=member["full_name"],
                    )

                    c1, c2 = st.columns(2)
                    updated_phone = c1.text_input(
                        "Phone Number",
                        value=member["phone"],
                    )
                    updated_email = c2.text_input(
                        "Email",
                        value=member["email"] or "",
                    )

                    updated_address = st.text_area(
                        "Address",
                        value=member["address"] or "",
                    )

                    status_options = ["Active", "Inactive"]
                    status_index = (
                        0 if member["status"] == "Active" else 1
                    )

                    updated_status = st.selectbox(
                        "Member Status",
                        status_options,
                        index=status_index,
                    )

                    save_changes = st.form_submit_button(
                        "Save Changes",
                        type="primary",
                    )

                if save_changes:
                    if not updated_name.strip() or not updated_phone.strip():
                        st.error("Name and phone number are required.")
                    else:
                        execute(
                            """UPDATE members
                               SET full_name = ?, phone = ?, email = ?,
                                   address = ?, status = ?
                               WHERE id = ?""",
                            (
                                updated_name.strip(),
                                updated_phone.strip(),
                                updated_email.strip(),
                                updated_address.strip(),
                                updated_status,
                                int(selected_id),
                            ),
                        )
                        st.toast("Member updated successfully.", icon="✅")
                        st.rerun()


# ======================================================================
#  MEMBERSHIP PLANS
# ======================================================================

def plans_page():
    page_header("📅", "Membership Plans", "Pricing and duration options for your members.")

    plan_data = query_df(
        """SELECT id, name, duration_days, price,
                  description, active
           FROM plans
           ORDER BY duration_days"""
    )

    if not plan_data.empty:
        rows = [plan_data.iloc[i:i + 4] for i in range(0, len(plan_data), 4)]

        for chunk in rows:
            cols = st.columns(4, gap="medium")
            for col, (_, plan) in zip(cols, chunk.iterrows()):
                is_on = bool(plan["active"])
                with col:
                    st.markdown(
                        f'<div class="plan-card {"" if is_on else "off"}">'
                        f'<span class="badge {"on" if is_on else "off"}">'
                        f'{"Active" if is_on else "Inactive"}</span>'
                        f'<div class="plan-name" style="margin-top:12px">{esc(plan["name"])}</div>'
                        f'<div class="plan-price">{money(plan["price"])}</div>'
                        f'<div class="plan-duration">⏱ {int(plan["duration_days"])} days</div>'
                        f'<div class="plan-desc">{esc(plan["description"])}</div>'
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            st.write("")

    if not is_admin:
        st.info("Only Admin users can add or deactivate plans.")
        return

    section("Add New Plan")

    with st.form("add_plan_form", clear_on_submit=True):
        plan_name = st.text_input("Plan Name", placeholder="e.g. Student Monthly")

        col1, col2 = st.columns(2)

        duration_days = col1.number_input(
            "Duration (days)",
            min_value=1,
            max_value=2000,
            value=30,
        )

        price = col2.number_input(
            "Price (₹)",
            min_value=0.0,
            value=1200.0,
            step=100.0,
        )

        description = st.text_input("Description", placeholder="Short description")

        add_plan = st.form_submit_button(
            "Add Plan",
            type="primary",
        )

    if add_plan:
        if not plan_name.strip():
            st.error("Plan name is required.")
        else:
            try:
                execute(
                    """INSERT INTO plans
                       (name, duration_days, price, description)
                       VALUES (?, ?, ?, ?)""",
                    (
                        plan_name.strip(),
                        int(duration_days),
                        float(price),
                        description.strip(),
                    ),
                )
                st.toast("Plan added successfully.", icon="✅")
                st.rerun()
            except Exception:
                st.error(
                    "Could not add the plan. Check whether its name "
                    "already exists."
                )

    section("Activate / Deactivate Plan")

    all_plans = query_df(
        "SELECT id, name, active FROM plans ORDER BY name"
    )

    if not all_plans.empty:
        selected_plan_id = st.selectbox(
            "Select plan",
            all_plans["id"].tolist(),
            format_func=lambda value: (
                f"{value} - "
                f"{all_plans.loc[all_plans.id == value, 'name'].iloc[0]}"
            ),
        )

        selected_plan = all_plans[
            all_plans["id"] == selected_plan_id
        ].iloc[0]

        plan_is_active = bool(selected_plan["active"])
        button_text = (
            "Deactivate Plan" if plan_is_active else "Reactivate Plan"
        )

        if st.button(button_text):
            execute(
                "UPDATE plans SET active = ? WHERE id = ?",
                (
                    0 if plan_is_active else 1,
                    int(selected_plan_id),
                ),
            )
            st.toast("Plan status updated.", icon="✅")
            st.rerun()


# ======================================================================
#  PAYMENTS AND RENEWALS
# ======================================================================

def payments_page():
    page_header("💳", "Payments & Renewals", "Register new memberships and track every payment.")

    members = query_df(
        """SELECT id, full_name, phone
           FROM members
           WHERE status = 'Active'
           ORDER BY full_name"""
    )

    plans = query_df(
        """SELECT id, name, duration_days, price
           FROM plans
           WHERE active = 1
           ORDER BY duration_days"""
    )

    if members.empty or plans.empty:
        st.warning(
            "Register at least one active member and make sure an "
            "active membership plan exists."
        )
    else:
        with st.form("membership_payment_form"):
            st.subheader("Register Membership / Renewal")

            member_id = st.selectbox(
                "Member",
                members["id"].tolist(),
                format_func=lambda value: (
                    f"{value} - "
                    f"{members.loc[members.id == value, 'full_name'].iloc[0]} "
                    f"({members.loc[members.id == value, 'phone'].iloc[0]})"
                ),
            )

            plan_id = st.selectbox(
                "Membership Plan",
                plans["id"].tolist(),
                format_func=lambda value: (
                    f"{plans.loc[plans.id == value, 'name'].iloc[0]} - "
                    f"{money(plans.loc[plans.id == value, 'price'].iloc[0])} "
                    f"({int(plans.loc[plans.id == value, 'duration_days'].iloc[0])} days)"
                ),
            )

            c1, c2 = st.columns(2)

            start_date = c1.date_input(
                "Start Date",
                value=date.today(),
            )

            default_price = float(
                plans.loc[plans.id == plan_id, "price"].iloc[0]
            )

            amount = c2.number_input(
                "Amount Paid (₹)",
                min_value=0.0,
                value=default_price,
                step=100.0,
            )

            c3, c4 = st.columns(2)

            payment_method = c3.selectbox(
                "Payment Method",
                ["Cash", "UPI", "Card", "Bank Transfer", "Other"],
            )

            note = c4.text_input(
                "Payment Reference (Optional)",
                placeholder="Txn ID / receipt no.",
            )

            submitted = st.form_submit_button(
                "Save Membership and Payment",
                type="primary",
            )

        if submitted:
            try:
                expiry_date = add_membership(
                    int(member_id),
                    int(plan_id),
                    start_date.isoformat(),
                    float(amount),
                    payment_method,
                    note.strip(),
                )

                st.toast(
                    f"Membership saved. Expiry date: {expiry_date}",
                    icon="✅",
                )
                st.rerun()
            except (ValueError, TypeError) as error:
                st.error(f"Could not save membership: {error}")

    section("Payment History")

    payment_history = query_df(
        """SELECT
               p.id AS payment_id,
               m.full_name,
               pl.name AS plan,
               p.amount,
               p.payment_date,
               p.method,
               ms.start_date,
               ms.end_date,
               ms.status
           FROM payments p
           JOIN memberships ms ON p.membership_id = ms.id
           JOIN members m ON ms.member_id = m.id
           JOIN plans pl ON ms.plan_id = pl.id
           ORDER BY p.payment_date DESC, p.id DESC"""
    )

    st.dataframe(
        with_status_icons(payment_history),
        use_container_width=True,
        hide_index=True,
        column_config={
            "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
        },
    )


# ======================================================================
#  REPORTS
# ======================================================================

def reports_page():
    page_header("📈", "Reports & Analytics", "Export membership and payment data.")

    if not is_admin:
        st.warning("Only Admin can access financial reports.")
        return

    memberships = query_df(
        """SELECT
               ms.id AS membership_id,
               m.full_name,
               m.phone,
               pl.name AS plan,
               ms.start_date,
               ms.end_date,
               ms.status
           FROM memberships ms
           JOIN members m ON ms.member_id = m.id
           JOIN plans pl ON ms.plan_id = pl.id
           ORDER BY ms.end_date"""
    )

    payments = query_df(
        """SELECT
               p.id AS payment_id,
               m.full_name,
               pl.name AS plan,
               p.amount,
               p.payment_date,
               p.method
           FROM payments p
           JOIN memberships ms ON p.membership_id = ms.id
           JOIN members m ON ms.member_id = m.id
           JOIN plans pl ON ms.plan_id = pl.id
           ORDER BY p.payment_date DESC"""
    )

    tab1, tab2 = st.tabs(
        ["🧾  Membership Report", "💵  Payment Report"]
    )

    with tab1:
        st.write("")
        st.dataframe(
            with_status_icons(memberships),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇  Download Membership CSV",
            memberships.to_csv(index=False).encode("utf-8"),
            file_name="membership_report.csv",
            mime="text/csv",
        )

    with tab2:
        st.write("")
        st.dataframe(
            payments,
            use_container_width=True,
            hide_index=True,
            column_config={
                "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
            },
        )

        st.download_button(
            "⬇  Download Payment CSV",
            payments.to_csv(index=False).encode("utf-8"),
            file_name="payment_report.csv",
            mime="text/csv",
        )

    section("Memberships Expiring Within 7 Days")

    today = date.today().isoformat()
    next_week = (date.today() + timedelta(days=7)).isoformat()

    expiring_members = query_df(
        """SELECT
               m.full_name,
               m.phone,
               pl.name AS plan,
               ms.end_date
           FROM memberships ms
           JOIN members m ON ms.member_id = m.id
           JOIN plans pl ON ms.plan_id = pl.id
           WHERE ms.status = 'Active'
             AND ms.end_date BETWEEN ? AND ?
           ORDER BY ms.end_date""",
        (today, next_week),
    )

    st.dataframe(
        expiring_members,
        use_container_width=True,
        hide_index=True,
    )

    if not expiring_members.empty:
        st.download_button(
            "⬇  Download Expiring Members CSV",
            expiring_members.to_csv(index=False).encode("utf-8"),
            file_name="expiring_members.csv",
            mime="text/csv",
        )


# ======================================================================
#  USER MANAGEMENT
# ======================================================================

def users_page():
    page_header("🔐", "User Management", "Create and review Admin and Staff accounts.")

    if not is_admin:
        st.error("Admin access required.")
        return

    with st.form("create_user_form", clear_on_submit=True):
        st.subheader("Create Admin or Staff Account")

        username = st.text_input("Username", placeholder="At least 3 characters")
        password = st.text_input(
            "Password (minimum 8 characters)",
            type="password",
        )
        role = st.selectbox("Account Role", ["Staff", "Admin"])

        submitted = st.form_submit_button(
            "Create Account",
            type="primary",
        )

    if submitted:
        try:
            create_user(username, password, role)
            st.success(f"{role} account created successfully.")
        except ValueError as error:
            st.error(str(error))

    section("Registered Users")

    users = query_df(
        "SELECT id, username, role FROM users ORDER BY id"
    )

    st.dataframe(
        users,
        use_container_width=True,
        hide_index=True,
    )


# ======================================================================
#  SIDEBAR + ROUTING
# ======================================================================

ROUTES = {
    "📊  Dashboard": dashboard,
    "👥  Members": members_page,
    "📅  Membership Plans": plans_page,
    "💳  Payments & Renewals": payments_page,
    "📈  Reports": reports_page,
    "🔐  User Management": users_page,
}

with st.sidebar:
    panel_name = "Admin Panel" if is_admin else "Staff Desk"

    st.markdown(
        f'<div class="brand">'
        f'<div class="brand-logo">🏋️</div>'
        f'<div><div class="brand-text">GYM MANAGER</div>'
        f'<div class="brand-sub">{panel_name}</div></div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="user-card">'
        f'<div class="avatar">{esc(user["username"][:1].upper())}</div>'
        f'<div><div class="user-name">{esc(user["username"])}</div>'
        f'<span class="role-pill">{esc(user["role"])}</span></div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    pages = [
        "📊  Dashboard",
        "👥  Members",
        "📅  Membership Plans",
        "💳  Payments & Renewals",
        "📈  Reports",
    ]

    if is_admin:
        pages.append("🔐  User Management")

    page = st.radio("Navigation", pages, label_visibility="collapsed")

    st.divider()

    if st.button("🚪  Log out", use_container_width=True):
        st.session_state.pop("user", None)
        st.session_state.pop("login_mode", None)
        st.rerun()

ROUTES[page]()