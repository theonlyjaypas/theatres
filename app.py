import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import logging
import sys
from pathlib import Path

# Configure logging
from config import Config

logger = Config.setup_logging()
logger.info("Starting Theatres Dashboard application")

try:
    Config.validate()
except FileNotFoundError as e:
    logger.error(f"Startup failed: {e}")
    st.error(f"Application startup failed: {e}")
    sys.exit(1)

st.set_page_config(
    page_title="LARGE FORMAT DASHBOARD",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS SETUP FOR FONT AND POLISHED LOOK
st.markdown("""
<style>
html, body, [class*="css"], .stMarkdown, .stText, button, input, select, textarea {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
}

/* Sidebar shell */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.06);
    padding-top: 2rem;
    min-width: 200px;
}

/* Sidebar brand title */
section[data-testid="stSidebar"] h3 {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    color: #fff !important;
    margin-bottom: 0.1rem !important;
    padding-left: 1rem;
}

/* "Navigate" radio group label — hidden, section divider only */
.stRadio > label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #555;
    padding-left: 1rem;
    margin-bottom: 0.5rem;
    margin-top: 0.75rem;
}

/* Nav item row — hide the radio circle entirely */
.stRadio > div { gap: 0; flex-direction: column; }
.stRadio > div > label > div:first-child { display: none !important; }

/* Nav item label */
.stRadio > div > label {
    display: flex;
    align-items: center;
    padding: 0.55rem 0.75rem 0.55rem 1rem;
    margin: 1px 0.75rem;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #aaa;
    cursor: pointer;
    border-left: 3px solid transparent;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.stRadio > div > label:hover {
    background: rgba(255,255,255,0.05);
    color: #fff;
}

/* Active nav item — blue left accent */
.stRadio > div > label:has(input:checked) {
    background: rgba(10,102,194,0.15);
    border-left: 3px solid #0A66C2;
    color: #fff;
    font-weight: 600;
    margin: 1px 0.75rem;
}

/* KPI metric cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 1.1rem 1.4rem 1rem;
}
[data-testid="metric-container"] > div:first-child {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #999;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
}

/* Page title */
h1 { font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
h2 { font-weight: 600; letter-spacing: 0.03em; text-transform: uppercase; }
h3 { font-weight: 600; letter-spacing: 0.02em; text-transform: uppercase; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
.stTabs [data-baseweb="tab"] { font-size: 0.88rem; font-weight: 500; padding: 0.5rem 1rem; border-radius: 8px 8px 0 0; }

/* Divider */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.5rem 0 !important; }

/* Main title and subtitle alignment */
.main-title {
    text-align: center;
    margin-bottom: 0.5rem;
}
.main-subtitle {
    text-align: center;
    color: rgba(255, 255, 255, 0.6);
    font-size: 1.1rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# CENTER TITLE AND SUBTITLE
st.markdown("""
<div class="main-title">
    <h1 style="margin: 0; padding-top: 1rem;">LARGE FORMAT DASHBOARD</h1>
</div>
<div class="main-subtitle">
    GLOBAL ANALYSIS [UPDATED OCT 2021]
</div>
""", unsafe_allow_html=True)

st.markdown("")

# SIDEBAR NAVIGATION
st.sidebar.markdown("### LARGE FORMAT DASHBOARD")
st.sidebar.caption("GLOBAL ANALYSIS [UPDATED OCT 2021]")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Geographic Analysis", "Technical Analysis", "Timeline", "Theater Search"],
)
st.sidebar.markdown("---")
st.sidebar.caption("Theater data compiled from LFExaminer (https://lfexaminer.com/theaters/)")

# Load data with error handling
@st.cache_data
def load_data():
    try:
        logger.info(f"Loading data from {Config.DATA_PATH}")
        df = pd.read_csv(Config.DATA_PATH)

        # Validate required columns
        required_columns = {
            'Organization', 'Country', 'City', 'Projector_Brand', 'Fmt',
            '2D_3D', 'Flat_Dome', 'Seats', 'Screen_Size', 'Opened', 'Type'
        }
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            error_msg = f"Missing required columns: {', '.join(missing_columns)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        df['Opened'] = pd.to_datetime(df['Opened'], errors='coerce')
        logger.info(f"Loaded {len(df)} theater records successfully")
        return df
    except FileNotFoundError:
        logger.error(f"Data file not found: {Config.DATA_PATH}")
        st.error(f"❌ Data file not found: {Config.DATA_PATH}")
        st.stop()
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        st.error(f"❌ Error loading data: {e}")
        st.stop()

df = load_data()

# COLOR PALETTE - PASTEL
BLUE   = "#A8D8FF"
TEAL   = "#A0E7E5"
ORANGE = "#FFD4B8"
PURPLE = "#E8C4FF"
PINK   = "#FFB8D9"
GREEN  = "#C4F5D9"

# Pastel color scales for charts
PASTEL_SCALE_SOFT = ["#FFB8D9", "#FFD4B8", "#FFFAB8", "#D9F5B8", "#B8F5D9", "#B8F5FF", "#B8D9FF", "#D9B8FF", "#FFB8D9"]
PASTEL_SCALE_BLUES = ["#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5", "#2196F3", "#1E88E5"]
PASTEL_SCALE_PURPLES = ["#F3E5F5", "#E1BEE7", "#CE93D8", "#BA68C8", "#AB47BC", "#9C27B0", "#8E24AA"]
PASTEL_SCALE_GREENS = ["#E8F5E9", "#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A", "#4CAF50", "#43A047"]

# PAGE DESCRIPTIONS
PAGE_DESCRIPTIONS = {
    "Overview": "Market overview with key metrics, projector brands, and theater type distribution",
    "Geographic Analysis": "Theater distribution by country and city with regional insights",
    "Theater Search": "Advanced filtering and search across all theaters with sorting options",
    "Technical Analysis": "Projector brands, screen specifications, and seating capacity analysis",
    "Timeline": "Historical growth trends and opening patterns over time",
    "Theater Types": "Breakdown of theaters by operational type and location",
}

# FORMAT LEGEND
FORMAT_LEGEND = {
    "1070": "10-perf, 70mm film",
    "1570": "15-perf, 70mm film",
    "870": "8-perf, 70mm film",
    "D": "Digital (xenon)",
    "DL": "Digital, single laser projector (IMAX+DL='Commercial' or Laser Dome)",
    "DL2": "Digital, dual laser projectors (IMAX+DL2='GT' Laser)",
    "DLx": "Digital, multiple laser projectors (IMAX+DLx='GT' Laser)",
}

# THEATER TYPE LEGEND
THEATER_TYPE_LEGEND = {
    "C": "Commercial, non-multiplex",
    "CM": "Commercial, multiplex",
    "N": "Institutional",
}

def show_format_legend():
    """Display format and theater type legends as expandable cards"""
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("FORMAT LEGEND", expanded=False):
            legend_text = ""
            for code, description in FORMAT_LEGEND.items():
                legend_text += f"**{code}**: {description}\n\n"
            st.markdown(legend_text)

    with col2:
        with st.expander("THEATRE TYPE LEGEND", expanded=False):
            legend_text = ""
            for code, description in THEATER_TYPE_LEGEND.items():
                legend_text += f"**{code}**: {description}\n\n"
            st.markdown(legend_text)

# ==================== OVERVIEW PAGE ====================
if page == "Overview":
    st.title("OVERVIEW")
    st.caption("This dashboard includes IMAX theaters, whether film or digital, and theaters that originally had one of the 70mm film formats listed below, as well as digital fulldome theaters larger than 60 feet in diameter.")

    show_format_legend()

    # FETCH DATA
    df_skills     = df['Projector_Brand'].value_counts().head(10).reset_index()
    df_skills.columns = ['Brand', 'count']
    df_countries  = df['Country'].value_counts().head(10).reset_index()
    df_countries.columns = ['Country', 'count']
    df_2d3d       = df['2D_3D'].value_counts().reset_index()
    df_2d3d.columns = ['Type', 'count']

    avg_seats = int(df['Seats'].mean() or 0)
    total_countries = df['Country'].nunique()
    top_brand = df['Projector_Brand'].value_counts().index[0] if len(df) > 0 else "N/A"
    top_country = df['Country'].value_counts().index[0] if len(df) > 0 else "N/A"

    # KPI CARDS
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Theaters", f"{len(df):,}")
    col2.metric("Countries", total_countries)
    col3.metric("Avg Seating Capacity", f"{avg_seats:,}")
    col4.metric("Top Projector Brand", top_brand)
    top_fmt = df['Fmt'].value_counts().index[0] if len(df) > 0 else "N/A"
    col5.metric("Top Format", top_fmt)

    st.markdown("---")

    # INSIGHTS CALLOUT
    c1, c2, c3, c4 = st.columns(4)
    c1.info(f"**Most common brand:** {top_brand} dominates the market")
    c2.info(f"**Top country:** {top_country} has the most theaters")
    c3.info(f"**Average capacity:** {avg_seats} seats per theater")
    c4.info(f"**Most common format:** {top_fmt} is the primary format")

    st.markdown("---")

    # ROW 1: Top brands [LEFT] + Top countries [RIGHT]
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Most Common Projector Brands")
        fig = px.bar(
            df_skills, x="count", y="Brand", orientation="h",
            text="count",
            labels={"count": "Number of Theaters", "Brand": ""},
            color_discrete_sequence=[BLUE]
        )
        fig.update_traces(textposition="outside", textfont_size=10, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
        fig.update_layout(
            height=380,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Theaters",
            showlegend=False,
            margin=dict(t=20, r=60, b=20, l=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Top Countries by Theater Count")
        fig = px.bar(
            df_countries, x="count", y="Country", orientation="h",
            text="count",
            labels={"count": "Number of Theaters", "Country": ""},
            color_discrete_sequence=[TEAL]
        )
        fig.update_traces(textposition="outside", textfont_size=10, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
        fig.update_layout(
            height=380,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Theaters",
            showlegend=False,
            margin=dict(t=20, r=60, b=20, l=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ROW 2: 2D/3D [LEFT] + Screen Type [MIDDLE] + Theater Type [RIGHT]
    col_left2, col_mid2, col_right2 = st.columns(3)

    with col_left2:
        st.subheader("2D vs 3D Capability")
        fig = px.pie(
            df_2d3d,
            values='count',
            names='Type',
            hole=0.4,
            color_discrete_map={'3D': PINK, '2D': TEAL},
            color_discrete_sequence=[PINK, TEAL]
        )
        fig.update_layout(height=340, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_mid2:
        st.subheader("Screen Type Distribution")
        df_screen = df['Flat_Dome'].value_counts().reset_index()
        df_screen.columns = ['Screen Type', 'count']
        fig = px.pie(
            df_screen,
            values='count',
            names='Screen Type',
            hole=0.4,
            color_discrete_map={'F': BLUE, 'D': PURPLE},
            color_discrete_sequence=[BLUE, PURPLE]
        )
        fig.update_layout(height=340, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_right2:
        st.subheader("Theater Type Distribution")
        type_counts = df['Type'].value_counts().head(5).reset_index()
        type_counts.columns = ['Type', 'count']
        fig = px.bar(
            type_counts, x='Type', y='count',
            color_discrete_sequence=[GREEN],
            labels={'count': 'Count', 'Type': 'Type'}
        )
        fig.update_traces(textposition="outside", textfont_size=9, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
        fig.update_layout(height=340, showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Recent Theater Openings")
    recent = df.dropna(subset=['Opened']).sort_values('Opened', ascending=False).head(10)
    st.dataframe(
        recent[['Organization', 'Country', 'City', 'Projector_Brand', 'Opened']].rename(
            columns={'Organization': 'Theater', 'Projector_Brand': 'Brand', 'Opened': 'Opening Date'}
        ),
        
        hide_index=True,
    )

# ==================== GEOGRAPHIC ANALYSIS ====================
elif page == "Geographic Analysis":
    st.title("Geographic Distribution")
    st.caption("This reveals how cinema infrastructure is distributed across countries and cities, highlighting the most densely populated theater regions and regional variations in projector technology adoption.")

    show_format_legend()

    country_counts = df['Country'].value_counts().reset_index().sort_values('count', ascending=False)
    country_counts.columns = ['Country', 'count']
    top_country = country_counts.iloc[0]

    # Get top 10 for main chart
    country_counts_top10 = country_counts.head(10)

    # INSIGHTS CALLOUT
    c1, c2 = st.columns(2)
    c1.info(f"**Highest concentration:** {top_country['Country']} with {top_country['count']} theaters")
    c2.info(f"**Global reach:** {df['Country'].nunique()} countries represented")

    st.markdown("---")

    st.subheader("Format Distribution by Top Countries")
    top_countries_fmt = df['Country'].value_counts().head(10).index
    fmt_by_country = df[df['Country'].isin(top_countries_fmt)].groupby(['Country', 'Fmt']).size().reset_index(name='count')
    fmt_by_country.columns = ['Country', 'Format', 'count']

    # Sort by total count per country in descending order
    country_totals = fmt_by_country.groupby('Country')['count'].sum().sort_values(ascending=False)
    fmt_by_country['Country'] = pd.Categorical(fmt_by_country['Country'], categories=country_totals.index, ordered=True)
    fmt_by_country = fmt_by_country.sort_values('Country')

    fig = px.bar(
        fmt_by_country,
        x='Country',
        y='count',
        color='Format',
        barmode='stack',
        labels={'count': 'Theaters', 'Country': 'Country', 'Format': 'Format'},
        color_discrete_sequence=[PINK, TEAL, BLUE, ORANGE, PURPLE, GREEN, "#FFE4B8", "#B8FFE4", "#E4B8FF", "#FFB8E4"]
    )
    fig.update_layout(
        height=380,
        hovermode='x unified',
        margin=dict(t=20, b=20),
        xaxis={'categoryorder': 'array', 'categoryarray': list(country_totals.index)}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Top 10 Theaters by Country")
        fig = px.bar(
            country_counts_top10,
            x='count',
            y='Country',
            orientation='h',
            color='count',
            color_continuous_scale=PASTEL_SCALE_BLUES,
            text='count',
            labels={'count': 'Theaters', 'Country': ''}
        )
        fig.update_traces(
            textposition="outside",
            textfont_size=10,
            marker=dict(
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            )
        )
        fig.update_layout(
            height=420,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Number of Theaters",
            showlegend=False,
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(
                title="Theaters",
                thickness=12,
                len=0.7
            ),
            margin=dict(t=20, r=80, b=20, l=10),
            hoverlabel=dict(namelength=-1),
        )
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Top 10 Countries")
        st.dataframe(
            country_counts_top10.rename(columns={'count': 'Theaters'}),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    st.subheader("Top Cities")
    city_counts = df.groupby(['City', 'Country']).size().reset_index(name='count').sort_values('count', ascending=False).head(20)
    city_counts['city_country'] = city_counts['City'] + ', ' + city_counts['Country']

    fig = px.bar(
        city_counts,
        x='count',
        y='city_country',
        orientation='h',
        color='count',
        color_continuous_scale=PASTEL_SCALE_PURPLES,
        text='count',
        labels={'count': 'Theaters', 'city_country': ''}
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=10,
        marker=dict(
            line=dict(color='rgba(255,255,255,0.3)', width=1)
        )
    )
    fig.update_layout(
        height=520,
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Number of Theaters",
        showlegend=False,
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="Theaters",
            thickness=12,
            len=0.7
        ),
        margin=dict(t=20, r=80, b=20, l=10),
        hoverlabel=dict(namelength=-1),
    )
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig, use_container_width=True)

# ==================== THEATER SEARCH ====================
elif page == "Theater Search":
    st.title("Theater Search")
    st.caption("Filter and search across all theaters using any combination of location, projector brand, capabilities, and seating capacity. Results can be sorted and exported, enabling detailed market research and venue comparisons.")

    show_format_legend()

    st.markdown("---")

    # GENERAL SEARCH BAR
    st.subheader("QUICK SEARCH")
    search_term = st.text_input(
        "Search by theater name, city, country, or any other field",
        placeholder="e.g., IMAX, Tokyo, USA",
        key="general_search"
    )

    st.markdown("---")

    # FILTER CONTROLS
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        selected_country = st.multiselect(
            "Country",
            sorted(df['Country'].dropna().unique()),
            default=[]
        )
    with col2:
        selected_brand = st.multiselect(
            "Projector Brand",
            sorted(df['Projector_Brand'].dropna().unique()),
            default=[]
        )
    with col3:
        selected_format = st.multiselect(
            "Format",
            sorted(df['Fmt'].dropna().unique()),
            default=[]
        )
    with col4:
        selected_2d3d = st.multiselect(
            "2D/3D",
            sorted(df['2D_3D'].dropna().unique()),
            default=[]
        )
    with col5:
        selected_screen = st.multiselect(
            "Screen Type",
            sorted(df['Flat_Dome'].dropna().unique()),
            default=[]
        )

    col1, col2 = st.columns(2)
    with col1:
        min_seats, max_seats = st.slider(
            "Seating Capacity Range",
            int(df['Seats'].min() or 0),
            int(df['Seats'].max() or 1000),
            (int(df['Seats'].min() or 0), int(df['Seats'].max() or 1000))
        )
    with col2:
        date_range = st.date_input(
            "Opening Date Range",
            value=[df['Opened'].min(), df['Opened'].max()],
            min_value=df['Opened'].min(),
            max_value=df['Opened'].max()
        )

    # Apply filters
    filtered_df = df.copy()

    if selected_country:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_country)]
    if selected_brand:
        filtered_df = filtered_df[filtered_df['Projector_Brand'].isin(selected_brand)]
    if selected_format:
        filtered_df = filtered_df[filtered_df['Fmt'].isin(selected_format)]
    if selected_2d3d:
        filtered_df = filtered_df[filtered_df['2D_3D'].isin(selected_2d3d)]
    if selected_screen:
        filtered_df = filtered_df[filtered_df['Flat_Dome'].isin(selected_screen)]

    filtered_df = filtered_df[
        (filtered_df['Seats'].fillna(0) >= min_seats) &
        (filtered_df['Seats'].fillna(0) <= max_seats)
    ]

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Opened'] >= pd.Timestamp(date_range[0])) &
            (filtered_df['Opened'] <= pd.Timestamp(date_range[1]))
        ]

    # Apply general search term across all columns
    if search_term:
        search_term_lower = search_term.lower()
        mask = filtered_df.astype(str).apply(
            lambda x: x.str.contains(search_term_lower, case=False, na=False).any(),
            axis=1
        )
        filtered_df = filtered_df[mask]

    st.markdown("---")

    # RESULTS METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("Results Found", f"{len(filtered_df):,}")
    col2.metric("Avg Capacity", f"{int(filtered_df['Seats'].mean() or 0):,}")
    col3.metric("Countries", filtered_df['Country'].nunique())

    st.markdown("---")

    # SORT OPTIONS
    sort_col, sort_order = st.columns(2)
    with sort_col:
        sort_by = st.selectbox(
            "Sort by",
            ['Organization', 'Country', 'City', 'Seats', 'Opened', 'Screen_Size']
        )
    with sort_order:
        ascending = st.checkbox("Ascending", value=False)

    filtered_df = filtered_df.sort_values(sort_by, ascending=ascending, na_position='last')

    st.subheader(f"All Results — {len(filtered_df):,} theaters")
    st.dataframe(
        filtered_df[[
            'Organization', 'Country', 'City', 'Projector_Brand', 'Fmt',
            '2D_3D', 'Flat_Dome', 'Seats', 'Screen_Size', 'Opened'
        ]].rename(columns={
            'Organization': 'Theater',
            'Projector_Brand': 'Brand',
            'Fmt': 'Format',
            '2D_3D': '2D/3D',
            'Flat_Dome': 'Screen',
            'Screen_Size': 'Size'
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="filtered_theaters.csv",
        mime="text/csv"
    )

# ==================== TECHNICAL ANALYSIS ====================
elif page == "Technical Analysis":
    st.title("Technical Specifications")
    st.caption("This breaks down projector brands, screen specifications, formats, and seating configurations to reveal patterns in cinema technology adoption and venue sizing strategies worldwide.")

    show_format_legend()

    # FETCH DATA
    brand_counts = df['Projector_Brand'].value_counts().reset_index().head(15)
    brand_counts.columns = ['Brand', 'count']
    top_brands = df['Projector_Brand'].value_counts().head(10).reset_index()
    top_brands.columns = ['Brand', 'count']
    seats_data = df['Seats'].dropna()

    top_brand = brand_counts.iloc[0]
    avg_capacity = int(df['Seats'].mean() or 0)
    max_capacity = int(df['Seats'].max() or 0)

    # INSIGHTS CALLOUT
    c1, c2, c3 = st.columns(3)
    c1.info(f"**Dominant brand:** {top_brand['Brand']} with {top_brand['count']} installations")
    c2.info(f"**Average capacity:** {avg_capacity:,} seats")
    c3.info(f"**Largest venue:** {max_capacity:,} seats")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top Projector Brands")
        fig = px.bar(
            brand_counts,
            x='count',
            y='Brand',
            orientation='h',
            color='count',
            color_continuous_scale=PASTEL_SCALE_PURPLES,
            text='count',
            labels={'count': 'Theaters', 'Brand': ''}
        )
        fig.update_traces(textposition="outside", textfont_size=9, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
        fig.update_layout(
            height=420,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Number of Theaters",
            showlegend=False,
            margin=dict(t=20, r=60, b=20, l=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Market Share — Top 10 Brands")
        fig = px.pie(
            top_brands,
            values='count',
            names='Brand',
            color_discrete_sequence=[PINK, TEAL, BLUE, ORANGE, PURPLE, GREEN, "#FFE4B8", "#B8FFE4", "#E4B8FF", "#FFB8E4"],
            labels={'count': 'Count', 'Brand': 'Brand'}
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("Seating Capacity Distribution")
        fig = px.histogram(
            seats_data,
            nbins=35,
            color_discrete_sequence=[TEAL],
            labels={'value': 'Seating Capacity', 'count': 'Theaters'}
        )
        fig.update_traces(marker_line_width=1, marker_line_color='rgba(255,255,255,0.3)')
        fig.update_layout(
            height=380,
            xaxis_title="Seating Capacity",
            yaxis_title="Number of Theaters",
            bargap=0.05,
            showlegend=False,
            margin=dict(t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right2:
        st.subheader("Capacity Statistics")
        capacity_median = int(df['Seats'].median() or 0)
        st.metric("Average Capacity", f"{avg_capacity:,} seats")
        st.metric("Median Capacity", f"{capacity_median:,} seats")
        st.metric("Maximum Capacity", f"{max_capacity:,} seats")

    st.markdown("---")

    col_left3, col_right3 = st.columns(2)

    with col_left3:
        st.subheader("Format Distribution (All Formats)")
        fmt_counts_all = df['Fmt'].value_counts().reset_index()
        fmt_counts_all.columns = ['Format', 'count']

        fig = px.bar(
            fmt_counts_all,
            x='Format',
            y='count',
            color='count',
            color_continuous_scale=PASTEL_SCALE_GREENS,
            text='count',
            labels={'count': 'Theaters', 'Format': 'Format'}
        )
        fig.update_traces(textposition="outside", textfont_size=8, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
        fig.update_layout(
            height=360,
            xaxis_title="Format",
            yaxis_title="Number of Theaters",
            showlegend=False,
            margin=dict(t=20, b=80),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right3:
        st.subheader("Largest Theaters by Capacity")
        largest = df.nlargest(10, 'Seats')[['Organization', 'Country', 'Seats']].copy()
        largest.columns = ['Theater', 'Country', 'Seats']
        largest['Seats'] = largest['Seats'].astype(int)
        st.dataframe(largest, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.subheader("Theater Type Analysis")

    col_type1, col_type2 = st.columns(2)

    with col_type1:
        st.subheader("Theater Type Distribution")
        type_counts = df['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'count']

        fig = px.bar(
            type_counts,
            x='count',
            y='Type',
            orientation='h',
            color='count',
            color_continuous_scale=PASTEL_SCALE_BLUES,
            text='count',
            labels={'count': 'Theaters', 'Type': 'Theater Type'}
        )
        fig.update_traces(textposition="outside", textfont_size=10, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
        fig.update_layout(
            height=360,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Number of Theaters",
            showlegend=False,
            margin=dict(t=20, r=60, b=20, l=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_type2:
        st.subheader("Theater Type Market Share")
        fig = px.pie(
            type_counts,
            values='count',
            names='Type',
            color_discrete_sequence=[PINK, TEAL, BLUE, ORANGE, PURPLE, GREEN],
            labels={'count': 'Count', 'Type': 'Theater Type'}
        )
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Average Seating Capacity by Theater Type")
    type_seats = df.groupby('Type')['Seats'].agg(['mean', 'count']).reset_index()
    type_seats.columns = ['Type', 'Avg Capacity', 'Count']
    type_seats['Avg Capacity'] = type_seats['Avg Capacity'].astype(int)
    type_seats = type_seats.sort_values('Avg Capacity', ascending=False)

    fig = px.bar(
        type_seats,
        x='Type',
        y='Avg Capacity',
        color='Avg Capacity',
        color_continuous_scale=PASTEL_SCALE_PURPLES,
        text='Avg Capacity',
        labels={'Avg Capacity': 'Average Seating Capacity', 'Type': 'Theater Type'}
    )
    fig.update_traces(textposition="outside", textfont_size=10, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
    fig.update_layout(
        height=360,
        xaxis_title="Theater Type",
        yaxis_title="Average Seating Capacity",
        showlegend=False,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col_type_stats1, col_type_stats2 = st.columns(2)

    with col_type_stats1:
        st.subheader("Theater Type by Projector Brand")
        top_brands_type = df['Projector_Brand'].value_counts().head(8).index
        type_by_brand = df[df['Projector_Brand'].isin(top_brands_type)].groupby(['Projector_Brand', 'Type']).size().reset_index(name='count')
        type_by_brand.columns = ['Projector Brand', 'Theater Type', 'count']

        fig = px.bar(
            type_by_brand,
            x='Projector Brand',
            y='count',
            color='Theater Type',
            barmode='stack',
            labels={'count': 'Theaters', 'Projector Brand': 'Brand', 'Theater Type': 'Type'},
            color_discrete_sequence=[PINK, TEAL, BLUE, ORANGE, PURPLE, GREEN]
        )
        fig.update_layout(
            height=360,
            hovermode='x unified',
            margin=dict(t=20, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_type_stats2:
        st.subheader("Theater Type Statistics")
        st.dataframe(
            type_seats.rename(columns={'Type': 'Type', 'Avg Capacity': 'Avg Seats', 'Count': 'Theaters'}),
            use_container_width=True,
            hide_index=True
        )

# ==================== TIMELINE ====================
elif page == "Timeline":
    st.title("Timeline")
    st.caption("This tracks theater openings across years, revealing periods of rapid expansion, market consolidation, and regional variations in cinema infrastructure development.")

    show_format_legend()

    timeline_df = df.dropna(subset=['Opened']).copy()
    timeline_df['Year'] = timeline_df['Opened'].dt.year
    yearly_counts = timeline_df.groupby('Year').size().reset_index(name='count')
    yearly_counts.columns = ['Year', 'count']

    earliest_year = int(df['Opened'].min().year) if pd.notna(df['Opened'].min()) else 0
    latest_year = int(df['Opened'].max().year) if pd.notna(df['Opened'].max()) else 0
    years_span = int((df['Opened'].max() - df['Opened'].min()).days / 365) if pd.notna(df['Opened'].min()) else 0

    # INSIGHTS CALLOUT
    c1, c2, c3 = st.columns(3)
    c1.info(f"**Earliest opening:** {earliest_year}")
    c2.info(f"**Latest opening:** {latest_year}")
    c3.info(f"**Time span:** {years_span} years")

    st.markdown("---")

    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.subheader("Theaters Opened per Year")
        fig = px.line(
            yearly_counts,
            x='Year',
            y='count',
            markers=True,
            color_discrete_sequence=[ORANGE],
            labels={'count': 'Theaters Opened', 'Year': 'Year'}
        )
        fig.update_traces(line=dict(width=3, color=ORANGE), marker=dict(size=8, color=ORANGE, line=dict(width=1, color='rgba(255,255,255,0.5)')))
        fig.update_layout(
            height=360,
            yaxis_title="Number of Openings",
            showlegend=False,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Peak Year")
        peak_year = yearly_counts.loc[yearly_counts['count'].idxmax()]
        st.metric(
            f"{int(peak_year['Year'])}",
            f"{int(peak_year['count'])} openings",
            delta=None
        )

    st.markdown("---")

    st.subheader("Cumulative Theater Growth")
    timeline_df_sorted = timeline_df.sort_values('Opened').reset_index(drop=True)
    timeline_df_sorted['Cumulative'] = range(1, len(timeline_df_sorted) + 1)

    fig = px.area(
        timeline_df_sorted,
        x='Opened',
        y='Cumulative',
        color_discrete_sequence=[TEAL],
        labels={'Opened': 'Date', 'Cumulative': 'Total Theaters'}
    )
    fig.update_traces(fill='tozeroy', opacity=0.6, line=dict(color=TEAL, width=2))
    fig.update_layout(
        height=360,
        hovermode='x unified',
        yaxis_title="Cumulative Count",
        showlegend=False,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Format Trends Over Time")
    timeline_df_fmt = timeline_df.copy()
    fmt_by_year = timeline_df_fmt.groupby(['Year', 'Fmt']).size().reset_index(name='count')
    fmt_by_year.columns = ['Year', 'Format', 'count']

    fig = px.bar(
        fmt_by_year,
        x='Year',
        y='count',
        color='Format',
        barmode='stack',
        labels={'count': 'Theaters', 'Year': 'Year', 'Format': 'Format'},
        color_discrete_sequence=[PINK, TEAL, BLUE, ORANGE, PURPLE, GREEN, "#FFE4B8", "#B8FFE4", "#E4B8FF", "#FFB8E4"]
    )
    fig.update_layout(
        height=360,
        hovermode='x unified',
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Peak Opening Years")
    peak_years = yearly_counts.nlargest(15, 'count').sort_values('Year')
    fig = px.bar(
        peak_years,
        x='Year',
        y='count',
        color='count',
        color_continuous_scale=PASTEL_SCALE_PURPLES,
        text='count',
        labels={'count': 'Openings', 'Year': 'Year'}
    )
    fig.update_traces(textposition="outside", textfont_size=9, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
    fig.update_layout(
        height=360,
        yaxis_title="Number of Theaters",
        showlegend=False,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== THEATER TYPES ====================
elif page == "Theater Types":
    st.title("Theater Type Analysis")
    st.caption("Large-format venues operate across multiple contexts — commercial multiplexes, cultural institutions, and educational science centers. This analysis categorizes theaters by their operational type, revealing the diversity of venues that host immersive cinema experiences.")

    type_counts = df['Type'].value_counts().reset_index().sort_values('count', ascending=False)
    type_counts.columns = ['Type', 'count']
    top_type = type_counts.iloc[0]

    # INSIGHTS CALLOUT
    c1, c2 = st.columns(2)
    c1.info(f"**Most common type:** {top_type['Type']} with {top_type['count']} venues")
    c2.info(f"**Unique types:** {len(type_counts)} different categorizations")

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Theater Type Distribution")
        fig = px.bar(
            type_counts,
            x='count',
            y='Type',
            orientation='h',
            color='count',
            color_continuous_scale=PASTEL_SCALE_BLUES,
            text='count',
            labels={'count': 'Theaters', 'Type': ''}
        )
        fig.update_traces(textposition="outside", textfont_size=9, marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)))
        fig.update_layout(
            height=320,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Number of Theaters",
            showlegend=False,
            margin=dict(t=20, r=60, b=20, l=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Type Legend")
        type_legend = {
            'CM': 'Commercial Multiplex',
            'C': 'Cultural/Museum',
            'N': 'Nature/Science Center',
        }
        legend_text = "\n\n".join([f"**{k}**: {v}" for k, v in type_legend.items()])
        st.info(f"Categories:\n\n{legend_text}")

    st.markdown("---")

    st.subheader("Type Breakdown by Country (Top 15 Countries)")
    top_countries = df['Country'].value_counts().head(15).index
    type_by_country = df[df['Country'].isin(top_countries)].groupby(['Country', 'Type']).size().reset_index(name='count')
    type_by_country.columns = ['Country', 'Type', 'count']

    fig = px.bar(
        type_by_country,
        x='Country',
        y='count',
        color='Type',
        barmode='stack',
        labels={'count': 'Theaters', 'Country': 'Country', 'Type': 'Type'},
        color_discrete_sequence=[PINK, TEAL, BLUE, ORANGE, PURPLE, GREEN]
    )
    fig.update_layout(
        height=420,
        hovermode='x unified',
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Type Statistics")
    cols = st.columns(min(4, len(type_counts)))

    for idx, (type_code, count) in enumerate(type_counts.values):
        percentage = (count / len(df)) * 100
        with cols[idx % len(cols)]:
            st.metric(f"Type {type_code}", f"{int(count)} ({percentage:.1f}%)")
