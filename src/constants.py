"""
Constants and configuration values for the Brent Oil Change Point Analysis project.
"""

from pathlib import Path
from typing import Final

# Project paths
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
RAW_DATA_DIR: Final[Path] = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Final[Path] = DATA_DIR / "processed"

# Data file paths
BRENT_OIL_PRICES_CSV: Final[Path] = RAW_DATA_DIR / "brent_oil_prices.csv"
KEY_EVENTS_CSV: Final[Path] = PROCESSED_DATA_DIR / "key_events.csv"
CHANGE_POINTS_CSV: Final[Path] = PROCESSED_DATA_DIR / "change_point_event_association.csv"

# Date formats
DATE_FORMAT_1: Final[str] = "%d-%b-%y"  # "20-May-87"
DATE_FORMAT_2: Final[str] = "%b %d, %Y"  # "Apr 22, 2020"
DATE_FORMAT_OUTPUT: Final[str] = "%Y-%m-%d"  # "2020-04-22"

# Event matching
DEFAULT_EVENT_WINDOW_DAYS: Final[int] = 30
MIN_EVENT_WINDOW_DAYS: Final[int] = 1
MAX_EVENT_WINDOW_DAYS: Final[int] = 365

# Returns calculation
RETURN_METHOD_LOG: Final[str] = "log"
RETURN_METHOD_SIMPLE: Final[str] = "simple"
VALID_RETURN_METHODS: Final[tuple] = (RETURN_METHOD_LOG, RETURN_METHOD_SIMPLE)

# Bayesian model parameters
DEFAULT_MCMC_DRAWS: Final[int] = 2000
DEFAULT_MCMC_TUNE: Final[int] = 1000
DEFAULT_RANDOM_SEED: Final[int] = 42
DEFAULT_HDI_PROB: Final[float] = 0.95

# Prior distributions
PRIOR_MU_MEAN: Final[float] = 0.0
PRIOR_MU_SIGMA: Final[float] = 0.1
PRIOR_SIGMA_SIGMA: Final[float] = 0.1

# Stationarity testing
ADF_SIGNIFICANCE_LEVEL: Final[float] = 0.05
KPSS_SIGNIFICANCE_LEVEL: Final[float] = 0.05

# Volatility calculation
DEFAULT_ROLLING_WINDOW: Final[int] = 30

# API configuration
API_HOST: Final[str] = "0.0.0.0"
API_PORT: Final[int] = 5000
API_DEBUG: Final[bool] = True

# Dashboard configuration
FRONTEND_PORT: Final[int] = 3000
FRONTEND_API_BASE_URL: Final[str] = f"http://localhost:{API_PORT}"

