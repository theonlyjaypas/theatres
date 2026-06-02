# LARGE FORMAT THEATRES DASHBOARD (UPDATED OCT 2021)

An interactive Streamlit dashboard analyzing **1,100+ large-format theaters** across **50+ countries**. Explore global cinema infrastructure, projector technology, and theater trends with comprehensive data visualization and search capabilities.

## FEATURES

### OVERVIEW
- Key performance metrics (total theaters, countries, average capacity, top formats)
- Projector brand distribution
- Theater type breakdown
- 2D/3D capability analysis
- Screen type comparison (Flat vs Dome)

### GEOGRAPHIC ANALYSIS
- **Top 10 Countries** distribution with theater counts
- **Top 20 Cities** breakdown by location
- Format distribution by country visualization
- Regional insights and patterns

### TECHNICAL ANALYSIS
- **Projector Brand** analysis and market share
- **Screen Specifications** distribution
- **Seating Capacity** analytics
- **Format Distribution** across all theaters
- **Theater Type** breakdown by brand and location
- Technical specifications by venue type

### TIMELINE
- Theater openings over time (historical trends)
- Cumulative growth visualization
- Peak opening years analysis
- Format adoption trends

### THEATRE SEARCH
- Advanced multi-filter search with:
  - Country selection
  - Projector brand filtering
  - Format selection
  - 2D/3D capability filter
  - Screen type (Flat/Dome)
  - Seating capacity range
  - Opening date range
- Sort by any column
- Export results as CSV

## DATA

- **Total Theaters**: 1,100+
- **Countries**: 50+
- **Data Source**: Large-format cinema database
- **Last Updated**: October 2021

### DATA COLUMNS
- Organization, Country, City, State
- Projector Brand & Supplier
- Format (1070, 1570, 870, D, DL, DL2, DLx)
- 2D/3D capability
- Screen type (Flat, Dome, Both)
- Seating capacity
- Screen size
- Opening date
- Theater type (Commercial multiplex, Commercial non-multiplex, Institutional)

## INSTALLATION

### PREREQUISITES
- Python 3.8+
- pip or conda

### SETUP

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/theaters-dashboard.git
   cd theaters-dashboard
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## USAGE

### Local Development

Run the dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Docker Deployment (Recommended for Production)

For production deployments, use Docker:

```bash
# Build and run
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

**See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions.**

## NAVIGATION

Use the sidebar to navigate between pages:
- **Overview** — Market overview with key metrics
- **Geographic Analysis** — Theater distribution by country and city
- **Technical Analysis** — Projector brands, specifications, and theater types
- **Timeline** — Historical growth trends and opening patterns
- **Theater Search** — Advanced filtering and search

## COLOR SCHEME

The dashboard uses a professional pastel color palette:
- **Pastel Blue** (#A8D8FF)
- **Pastel Teal** (#A0E7E5)
- **Pastel Orange** (#FFD4B8)
- **Pastel Purple** (#E8C4FF)
- **Pastel Pink** (#FFB8D9)
- **Pastel Green** (#C4F5D9)

## FORMAT LEGEND

### PROJECTION FORMATS
- **1070** — 10-perf, 70mm film
- **1570** — 15-perf, 70mm film
- **870** — 8-perf, 70mm film
- **D** — Digital (xenon)
- **DL** — Digital, single laser projector
- **DL2** — Digital, dual laser projectors
- **DLx** — Digital, multiple laser projectors

### THEATRE TYPES
- **C** — Commercial, non-multiplex
- **CM** — Commercial, multiplex
- **N** — Institutional

### SCREEN TYPES
- **Flat** — Flat screen
- **Dome** — Dome/curved screen
- **Both** — Both flat and dome configurations

## TECH STACK

- **[Streamlit](https://streamlit.io/)** — Interactive web framework
- **[Pandas](https://pandas.pydata.org/)** — Data manipulation
- **[Plotly](https://plotly.com/)** — Interactive visualizations
- **Python 3.13** — Core language

## PROJECT STRUCTURE

```
theaters-dashboard/
├── app.py                 # Main Streamlit application
├── theaters.csv          # Theater data
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```

## DATA UPDATES

To update the data:
1. Replace `theaters.csv` with new data
2. Restart the Streamlit app
3. The dashboard will automatically refresh with new data

## TROUBLESHOOTING

### COMMON ISSUES

**Dashboard won't load**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+): `python --version`
- Try clearing Streamlit cache: `streamlit cache clear`

**Charts not displaying**
- Check internet connection (Plotly CDN)
- Verify data integrity in `theaters.csv`
- Try refreshing the page

**Slow performance**
- Close other applications
- Clear browser cache
- Restart the Streamlit server

## CONFIGURATION

### Environment Variables

Create a `.env` file (copy from `.env.example`) to configure:

```bash
cp .env.example .env
```

Key variables:
- `ENVIRONMENT` — Set to `production` for production deployments
- `LOG_LEVEL` — Control logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `DATA_PATH` — Path to the CSV data file
- `PORT` — Server port (default 8501)

See `.env.example` for all available options.

### Logging

- Logs are written to `logs/app.log`
- Console output is enabled for monitoring
- Log level controlled by `LOG_LEVEL` environment variable

## REQUIREMENTS

See `requirements.txt`:
- streamlit==1.36.0
- pandas==2.2.0
- plotly==5.18.0
- gunicorn==21.2.0 (for production)
- python-dotenv==1.0.0 (for environment configuration)

## LICENSE

This project is open source. Feel free to use and modify as needed.


---

**Last Updated**: 2026-06-01  
**Version**: 1.0.0  
**Status**: Active & Maintained
