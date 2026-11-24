"""Project-wide settings. Edit weights here to test how sensitive results are."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

# County FIPS (state 12 = Florida)
STATE_FIPS = "12"
COUNTIES = {"Miami-Dade": "086", "Broward": "011"}

# Projected CRS for area calculations: NAD83 / Florida East (ftUS)
AREA_CRS = "EPSG:2236"
WEB_CRS = "EPSG:4326"

# FEMA NFHL: "Flood Hazard Zones" layer
NFHL_URL = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query"

# OpenFEMA NFIP claims (v2)
OPENFEMA_CLAIMS_URL = "https://www.fema.gov/api/open/v2/FimaNfipClaims"

# Sea-level-rise screening scenarios (feet above the NAVD88 datum)
SLR_SCENARIOS_FT = [1, 2, 3]
FT_TO_M = 0.3048
DEM_RESOLUTION_M = 30

# Weights (each group sums to 1)
EXPOSURE_WEIGHTS = {
    "sfha_share": 0.40,       # FEMA special flood hazard area share
    "low_elev_share": 0.35,   # share of tract at/below +2 ft
    "claims_rate": 0.25,      # NFIP claims per 1,000 housing units
}
RISK_WEIGHTS = {"exposure": 0.6, "vulnerability": 0.4}

# Quadrant cutoff on the 0-1 scaled scores
HIGH_THRESHOLD = 0.5
