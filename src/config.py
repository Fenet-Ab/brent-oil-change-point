"""
Configuration dataclasses for the Brent Oil Change Point Analysis project.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .constants import (
    DEFAULT_EVENT_WINDOW_DAYS,
    DEFAULT_HDI_PROB,
    DEFAULT_MCMC_DRAWS,
    DEFAULT_MCMC_TUNE,
    DEFAULT_RANDOM_SEED,
    DEFAULT_ROLLING_WINDOW,
    PRIOR_MU_MEAN,
    PRIOR_MU_SIGMA,
    PRIOR_SIGMA_SIGMA,
    RETURN_METHOD_LOG,
)


@dataclass
class DataConfig:
    """Configuration for data loading and paths."""
    
    brent_oil_prices_path: Optional[Path] = None
    key_events_path: Optional[Path] = None
    change_points_path: Optional[Path] = None
    
    def __post_init__(self):
        """Set default paths if not provided."""
        from .constants import BRENT_OIL_PRICES_CSV, KEY_EVENTS_CSV, CHANGE_POINTS_CSV
        
        if self.brent_oil_prices_path is None:
            self.brent_oil_prices_path = BRENT_OIL_PRICES_CSV
        if self.key_events_path is None:
            self.key_events_path = KEY_EVENTS_CSV
        if self.change_points_path is None:
            self.change_points_path = CHANGE_POINTS_CSV


@dataclass
class PreprocessingConfig:
    """Configuration for data preprocessing."""
    
    return_method: str = RETURN_METHOD_LOG
    rolling_window: int = DEFAULT_ROLLING_WINDOW
    drop_na: bool = True
    
    def __post_init__(self):
        """Validate return method."""
        from .constants import VALID_RETURN_METHODS
        if self.return_method not in VALID_RETURN_METHODS:
            raise ValueError(
                f"return_method must be one of {VALID_RETURN_METHODS}, "
                f"got {self.return_method}"
            )


@dataclass
class BayesianModelConfig:
    """Configuration for Bayesian change point model."""
    
    draws: int = DEFAULT_MCMC_DRAWS
    tune: int = DEFAULT_MCMC_TUNE
    random_seed: int = DEFAULT_RANDOM_SEED
    hdi_prob: float = DEFAULT_HDI_PROB
    mu_prior_mean: float = PRIOR_MU_MEAN
    mu_prior_sigma: float = PRIOR_MU_SIGMA
    sigma_prior_sigma: float = PRIOR_SIGMA_SIGMA
    
    def __post_init__(self):
        """Validate configuration values."""
        if self.draws <= 0:
            raise ValueError("draws must be positive")
        if self.tune <= 0:
            raise ValueError("tune must be positive")
        if not 0 < self.hdi_prob < 1:
            raise ValueError("hdi_prob must be between 0 and 1")
        if self.mu_prior_sigma <= 0:
            raise ValueError("mu_prior_sigma must be positive")
        if self.sigma_prior_sigma <= 0:
            raise ValueError("sigma_prior_sigma must be positive")


@dataclass
class EventMatchingConfig:
    """Configuration for event matching."""
    
    window_days: int = DEFAULT_EVENT_WINDOW_DAYS
    match_nearest: bool = True
    
    def __post_init__(self):
        """Validate window_days."""
        from .constants import MAX_EVENT_WINDOW_DAYS, MIN_EVENT_WINDOW_DAYS
        
        if not MIN_EVENT_WINDOW_DAYS <= self.window_days <= MAX_EVENT_WINDOW_DAYS:
            raise ValueError(
                f"window_days must be between {MIN_EVENT_WINDOW_DAYS} and "
                f"{MAX_EVENT_WINDOW_DAYS}, got {self.window_days}"
            )


@dataclass
class ProjectConfig:
    """Main project configuration combining all sub-configurations."""
    
    data: DataConfig = field(default_factory=DataConfig)
    preprocessing: PreprocessingConfig = field(default_factory=PreprocessingConfig)
    model: BayesianModelConfig = field(default_factory=BayesianModelConfig)
    event_matching: EventMatchingConfig = field(default_factory=EventMatchingConfig)

