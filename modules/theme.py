import streamlit as st

THEME_PALETTES = {
    "dark": {
        "bg": "#0E1117",
        "card_bg": "#161B22",
        "card_border": "#30363D",
        "text": "#F0F6FC",
        "text_muted": "#8B949E",
        "primary": "#00C9A7",
        "primary_gradient": "linear-gradient(135deg, #00C9A7 0%, #008080 100%)",
        "secondary": "#A27BFF",
        "grid": "#21262D",
        "paper_bg": "#161B22",
        "plot_bg": "#161B22",
        "hover_bg": "#1F242D"
    },
    "light": {
        "bg": "#F3F4F6",             # Soft neutral grey (comfortable, not blinding)
        "card_bg": "#FFFFFF",        # Crisp card container
        "card_border": "#D1D5DB",    # Clear visible borders
        "text": "#111827",           # Deep dark text for maximum contrast & readability
        "text_muted": "#4B5563",     # Clear secondary grey
        "primary": "#00897B",        # Deep high-contrast teal
        "primary_gradient": "linear-gradient(135deg, #00897B 0%, #005B52 100%)",
        "secondary": "#6D28D9",      # Deep purple
        "grid": "#E5E7EB",
        "paper_bg": "#FFFFFF",
        "plot_bg": "#F9FAFB",
        "hover_bg": "#E5E7EB"
    }
}

def init_theme():
    """
    Ensure theme state is initialized in Streamlit session_state.
    Defaults to 'dark'.
    """
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    return st.session_state["theme"]

def get_current_theme():
    """Return the active theme palette ('dark' or 'light')."""
    theme_name = init_theme()
    return THEME_PALETTES.get(theme_name, THEME_PALETTES["dark"])

def render_theme_toggle():
    """
    Renders a clean theme toggle button in the sidebar.
    Persists selection in st.session_state['theme'].
    """
    init_theme()
    is_dark = st.session_state["theme"] == "dark"
    label = "☀️ Switch to Light Mode" if is_dark else "🌙 Switch to Dark Mode"

    with st.sidebar:
        st.markdown("---")
        if st.button(label, key="theme_toggle_btn", use_container_width=True):
            st.session_state["theme"] = "light" if is_dark else "dark"
            st.rerun()

def apply_custom_css():
    """
    Injects custom CSS styling matching the active theme into the current page.
    Forces high-contrast typography and visible borders in both light & dark modes.
    """
    theme = get_current_theme()
    is_dark = st.session_state.get("theme", "dark") == "dark"

    css = f"""
    <style>
        /* Force CSS variables so Streamlit internals match active mode */
        :root {{
            --text-color: {theme['text']} !important;
            --background-color: {theme['bg']} !important;
            --secondary-background-color: {theme['card_bg']} !important;
        }}

        /* Base page background and typography */
        .stApp {{
            background-color: {theme['bg']} !important;
            color: {theme['text']} !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}

        /* Headings & markdown text */
        h1, h2, h3, h4, h5, h6 {{
            color: {theme['text']} !important;
            font-weight: 700 !important;
        }}

        p, span, label, li, [data-testid="stMarkdownContainer"] p {{
            color: {theme['text']} !important;
        }}

        /* Sidebar background & navigation */
        section[data-testid="stSidebar"] {{
            background-color: {theme['card_bg']} !important;
            border-right: 1px solid {theme['card_border']} !important;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebarNav"] span {{
            color: {theme['text']} !important;
        }}

        /* Hero banner container */
        .hero-container {{
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 14px;
            padding: 32px 28px;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, {"0.35" if is_dark else "0.08"});
        }}

        .hero-badge {{
            display: inline-block;
            background: rgba(0, 201, 167, {"0.15" if is_dark else "0.12"});
            color: {theme['primary']};
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            border: 1px solid {theme['primary']};
        }}

        .hero-title {{
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0 0 10px 0;
            line-height: 1.2;
            color: {theme['text']} !important;
        }}

        .hero-subtitle {{
            font-size: 1.05rem;
            color: {theme['text_muted']} !important;
            line-height: 1.6;
            margin: 0;
            max-width: 850px;
        }}

        /* Custom Cards */
        .custom-card {{
            background-color: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 12px;
            padding: 20px;
            height: 100%;
            box-shadow: 0 2px 8px rgba(0, 0, 0, {"0.25" if is_dark else "0.06"});
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}

        .custom-card:hover {{
            border-color: {theme['primary']};
            transform: translateY(-2px);
        }}

        .card-icon {{
            font-size: 1.8rem;
            margin-bottom: 8px;
            display: inline-block;
        }}

        .card-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {theme['text']} !important;
            margin: 0 0 8px 0;
        }}

        .card-body {{
            font-size: 0.92rem;
            color: {theme['text_muted']} !important;
            line-height: 1.5;
            margin: 0;
        }}

        /* KPI Metric Callouts */
        .kpi-container {{
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 12px;
            padding: 18px 20px;
            text-align: left;
            margin-bottom: 16px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, {"0.2" if is_dark else "0.05"});
        }}

        .kpi-label {{
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: {theme['text_muted']} !important;
            margin-bottom: 4px;
            font-weight: 600;
        }}

        .kpi-value {{
            font-size: 1.85rem;
            font-weight: 800;
            color: {theme['primary']} !important;
            line-height: 1.1;
        }}

        .kpi-subtitle {{
            font-size: 0.8rem;
            color: {theme['text_muted']} !important;
            margin-top: 4px;
        }}

        /* Pipeline Step Card */
        .step-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            background: {theme['primary']};
            color: #FFFFFF !important;
            font-weight: 700;
            border-radius: 50%;
            margin-right: 8px;
            font-size: 0.9rem;
        }}

        /* Streamlit Native Metric elements */
        div[data-testid="stMetricLabel"] * {{
            color: {theme['text_muted']} !important;
        }}

        div[data-testid="stMetricValue"] * {{
            font-size: 1.85rem !important;
            font-weight: 800 !important;
            color: {theme['primary']} !important;
        }}

        /* Selectboxes & Dropdowns */
        div[data-baseweb="select"] > div {{
            background-color: {theme['card_bg']} !important;
            border: 1px solid {theme['card_border']} !important;
        }}

        div[data-baseweb="select"] * {{
            color: {theme['text']} !important;
        }}

        /* Expanders */
        div[data-testid="stExpander"] {{
            background-color: {theme['card_bg']} !important;
            border: 1px solid {theme['card_border']} !important;
            border-radius: 8px;
        }}

        div[data-testid="stExpander"] summary span {{
            color: {theme['text']} !important;
            font-weight: 600 !important;
        }}

        /* Buttons */
        div[data-testid="stButton"] > button {{
            background-color: {theme['card_bg']} !important;
            border: 1px solid {theme['card_border']} !important;
            color: {theme['text']} !important;
            font-weight: 600;
        }}

        div[data-testid="stButton"] > button:hover {{
            border-color: {theme['primary']} !important;
            color: {theme['primary']} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def style_plotly_chart(fig):
    """
    Applies current theme styling (fonts, grid lines, backgrounds)
    to a Plotly Figure instance and returns it.
    """
    theme = get_current_theme()
    is_dark = st.session_state.get("theme", "dark") == "dark"

    fig.update_layout(
        paper_bgcolor=theme["paper_bg"],
        plot_bgcolor=theme["plot_bg"],
        font=dict(
            family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
            color=theme["text"],
            size=12
        ),
        title=dict(
            font=dict(
                family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
                color=theme["text"],
                size=16
            )
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=11)
        ),
        margin=dict(l=40, r=30, t=50, b=40),
        hoverlabel=dict(
            bgcolor=theme["card_bg"],
            font_color=theme["text"],
            bordercolor=theme["card_border"]
        )
    )

    fig.update_xaxes(
        gridcolor=theme["grid"],
        zerolinecolor=theme["grid"],
        linecolor=theme["card_border"],
        tickfont=dict(color=theme["text"])
    )
    fig.update_yaxes(
        gridcolor=theme["grid"],
        zerolinecolor=theme["grid"],
        linecolor=theme["card_border"],
        tickfont=dict(color=theme["text"])
    )

    return fig
