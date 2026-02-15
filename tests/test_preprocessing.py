"""
Unit tests for preprocessing functionality.
"""

import pytest
import pandas as pd
import numpy as np

from src.preprocessing import (
    calculate_returns,
    calculate_rolling_volatility,
    calculate_rolling_mean,
)
from src.config import PreprocessingConfig
from src.constants import RETURN_METHOD_LOG, RETURN_METHOD_SIMPLE


class TestCalculateReturns:
    """Test cases for calculate_returns function."""
    
    def test_calculate_log_returns(self):
        """Test log returns calculation."""
        dates = pd.date_range('2020-01-01', periods=5, freq='D')
        prices = pd.Series([100, 110, 105, 120, 115], index=dates)
        df = pd.DataFrame({'Price': prices})
        
        returns = calculate_returns(df, method=RETURN_METHOD_LOG)
        
        assert isinstance(returns, pd.Series)
        assert len(returns) == 4  # One less than prices due to diff
        assert not returns.isna().any()
        # Log returns should be approximately log(price_t / price_{t-1})
        expected_first = np.log(110 / 100)
        assert np.isclose(returns.iloc[0], expected_first, rtol=1e-5)
    
    def test_calculate_simple_returns(self):
        """Test simple returns calculation."""
        dates = pd.date_range('2020-01-01', periods=5, freq='D')
        prices = pd.Series([100, 110, 105, 120, 115], index=dates)
        df = pd.DataFrame({'Price': prices})
        
        returns = calculate_returns(df, method=RETURN_METHOD_SIMPLE)
        
        assert isinstance(returns, pd.Series)
        assert len(returns) == 4
        assert not returns.isna().any()
        # Simple returns should be (price_t / price_{t-1}) - 1
        expected_first = (110 / 100) - 1
        assert np.isclose(returns.iloc[0], expected_first, rtol=1e-5)
    
    def test_calculate_returns_invalid_method(self):
        """Test that ValueError is raised for invalid method."""
        dates = pd.date_range('2020-01-01', periods=5, freq='D')
        prices = pd.Series([100, 110, 105, 120, 115], index=dates)
        df = pd.DataFrame({'Price': prices})
        
        with pytest.raises(ValueError, match="method must be"):
            calculate_returns(df, method="invalid_method")
    
    def test_calculate_returns_missing_price_column(self):
        """Test that ValueError is raised when Price column is missing."""
        df = pd.DataFrame({'OtherColumn': [1, 2, 3]})
        
        with pytest.raises(ValueError, match="Price"):
            calculate_returns(df)
    
    def test_calculate_returns_with_config(self):
        """Test returns calculation with PreprocessingConfig."""
        dates = pd.date_range('2020-01-01', periods=5, freq='D')
        prices = pd.Series([100, 110, 105, 120, 115], index=dates)
        df = pd.DataFrame({'Price': prices})
        
        config = PreprocessingConfig(return_method=RETURN_METHOD_SIMPLE)
        returns = calculate_returns(df, config=config)
        
        assert isinstance(returns, pd.Series)
        assert len(returns) == 4


class TestRollingVolatility:
    """Test cases for calculate_rolling_volatility function."""
    
    def test_calculate_rolling_volatility(self):
        """Test rolling volatility calculation."""
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        returns = pd.Series(np.random.randn(10), index=dates)
        
        vol = calculate_rolling_volatility(returns, window=5)
        
        assert isinstance(vol, pd.Series)
        assert len(vol) == 10
        # First few values should be NaN due to rolling window
        assert vol.iloc[:4].isna().all()
        # Later values should be non-NaN
        assert not vol.iloc[5:].isna().any()


class TestRollingMean:
    """Test cases for calculate_rolling_mean function."""
    
    def test_calculate_rolling_mean(self):
        """Test rolling mean calculation."""
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        prices = pd.Series([100 + i for i in range(10)], index=dates)
        
        rolling = calculate_rolling_mean(prices, window=5)
        
        assert isinstance(rolling, pd.Series)
        assert len(rolling) == 10
        # First few values should be NaN due to rolling window
        assert rolling.iloc[:4].isna().all()
        # Later values should be non-NaN
        assert not rolling.iloc[5:].isna().any()

