"""
Unit tests for configuration dataclasses.
"""

import pytest

from src.config import (
    DataConfig,
    PreprocessingConfig,
    BayesianModelConfig,
    EventMatchingConfig,
    ProjectConfig,
)
from src.constants import RETURN_METHOD_LOG, RETURN_METHOD_SIMPLE


class TestDataConfig:
    """Test cases for DataConfig."""
    
    def test_default_data_config(self):
        """Test default DataConfig initialization."""
        config = DataConfig()
        
        assert config.brent_oil_prices_path is not None
        assert config.key_events_path is not None
        assert config.change_points_path is not None


class TestPreprocessingConfig:
    """Test cases for PreprocessingConfig."""
    
    def test_default_preprocessing_config(self):
        """Test default PreprocessingConfig initialization."""
        config = PreprocessingConfig()
        
        assert config.return_method == RETURN_METHOD_LOG
        assert config.rolling_window == 30
        assert config.drop_na is True
    
    def test_invalid_return_method(self):
        """Test that invalid return method raises ValueError."""
        with pytest.raises(ValueError, match="return_method"):
            PreprocessingConfig(return_method="invalid_method")


class TestBayesianModelConfig:
    """Test cases for BayesianModelConfig."""
    
    def test_default_model_config(self):
        """Test default BayesianModelConfig initialization."""
        config = BayesianModelConfig()
        
        assert config.draws == 2000
        assert config.tune == 1000
        assert config.random_seed == 42
        assert config.hdi_prob == 0.95
    
    def test_invalid_draws(self):
        """Test that invalid draws raises ValueError."""
        with pytest.raises(ValueError, match="draws must be positive"):
            BayesianModelConfig(draws=-1)
    
    def test_invalid_hdi_prob(self):
        """Test that invalid hdi_prob raises ValueError."""
        with pytest.raises(ValueError, match="hdi_prob"):
            BayesianModelConfig(hdi_prob=1.5)


class TestEventMatchingConfig:
    """Test cases for EventMatchingConfig."""
    
    def test_default_event_matching_config(self):
        """Test default EventMatchingConfig initialization."""
        config = EventMatchingConfig()
        
        assert config.window_days == 30
        assert config.match_nearest is True
    
    def test_invalid_window_days(self):
        """Test that invalid window_days raises ValueError."""
        with pytest.raises(ValueError, match="window_days"):
            EventMatchingConfig(window_days=500)  # Exceeds max


class TestProjectConfig:
    """Test cases for ProjectConfig."""
    
    def test_default_project_config(self):
        """Test default ProjectConfig initialization."""
        config = ProjectConfig()
        
        assert isinstance(config.data, DataConfig)
        assert isinstance(config.preprocessing, PreprocessingConfig)
        assert isinstance(config.model, BayesianModelConfig)
        assert isinstance(config.event_matching, EventMatchingConfig)

