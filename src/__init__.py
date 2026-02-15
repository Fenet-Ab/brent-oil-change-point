"""
Brent Oil Change Point Analysis Package

A comprehensive package for detecting structural breaks in Brent oil prices
and associating them with geopolitical and economic events.
"""

from .config import (
    BayesianModelConfig,
    DataConfig,
    EventMatchingConfig,
    PreprocessingConfig,
    ProjectConfig,
)
from .constants import (
    API_HOST,
    API_PORT,
    BRENT_OIL_PRICES_CSV,
    CHANGE_POINTS_CSV,
    DATA_DIR,
    DEFAULT_EVENT_WINDOW_DAYS,
    DEFAULT_MCMC_DRAWS,
    DEFAULT_MCMC_TUNE,
    KEY_EVENTS_CSV,
    PROCESSED_DATA_DIR,
    PROJECT_ROOT,
    RAW_DATA_DIR,
)
from .data_loader import load_brent_data, load_events_data
from .event_matching import (
    associate_change_points_with_events,
    find_nearest_event,
    match_events_to_change_point,
)
from .modeling import (
    build_change_point_model,
    check_model_convergence,
    extract_change_point_results,
    run_mcmc_sampling,
)
from .preprocessing import (
    calculate_returns,
    calculate_rolling_mean,
    calculate_rolling_volatility,
)

__version__ = "1.0.0"

__all__ = [
    # Config
    "DataConfig",
    "PreprocessingConfig",
    "BayesianModelConfig",
    "EventMatchingConfig",
    "ProjectConfig",
    # Constants
    "PROJECT_ROOT",
    "DATA_DIR",
    "RAW_DATA_DIR",
    "PROCESSED_DATA_DIR",
    "BRENT_OIL_PRICES_CSV",
    "KEY_EVENTS_CSV",
    "CHANGE_POINTS_CSV",
    "DEFAULT_EVENT_WINDOW_DAYS",
    "DEFAULT_MCMC_DRAWS",
    "DEFAULT_MCMC_TUNE",
    "API_HOST",
    "API_PORT",
    # Data loading
    "load_brent_data",
    "load_events_data",
    # Preprocessing
    "calculate_returns",
    "calculate_rolling_volatility",
    "calculate_rolling_mean",
    # Modeling
    "build_change_point_model",
    "run_mcmc_sampling",
    "extract_change_point_results",
    "check_model_convergence",
    # Event matching
    "match_events_to_change_point",
    "find_nearest_event",
    "associate_change_points_with_events",
]
