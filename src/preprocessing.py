"""
Data preprocessing utilities for Brent oil price analysis.

This module provides functions for calculating returns, volatility,
and other preprocessing steps.
"""

from typing import Literal

import numpy as np
import pandas as pd

from .config import PreprocessingConfig
from .constants import RETURN_METHOD_LOG, RETURN_METHOD_SIMPLE, VALID_RETURN_METHODS


def calculate_returns(
    df: pd.DataFrame, 
    method: Literal["log", "simple"] = RETURN_METHOD_LOG,
    config: PreprocessingConfig = None
) -> pd.Series:
    """
    Calculate returns from price data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with Price column.
    method : str, optional
        'log' for log returns, 'simple' for simple returns. Default is 'log'.
    config : PreprocessingConfig, optional
        Configuration object. If None, uses default PreprocessingConfig.
    
    Returns:
    --------
    pd.Series
        Returns series with Date index.
    
    Raises:
    -------
    ValueError
        If method is not 'log' or 'simple', or if Price column is missing.
    """
    if config is not None:
        method = config.return_method
    
    if method not in VALID_RETURN_METHODS:
        raise ValueError(f"method must be one of {VALID_RETURN_METHODS}, got {method}")
    
    if 'Price' not in df.columns:
        raise ValueError("DataFrame must contain a 'Price' column")
    
    if method == RETURN_METHOD_LOG:
        returns = np.log(df['Price']).diff()
    elif method == RETURN_METHOD_SIMPLE:
        returns = df['Price'].pct_change()
    else:
        raise ValueError(f"method must be one of {VALID_RETURN_METHODS}, got {method}")
    
    if config is None or config.drop_na:
        returns = returns.dropna()
    
    return returns


def calculate_rolling_volatility(
    returns: pd.Series,
    window: int = 30
) -> pd.Series:
    """
    Calculate rolling volatility (standard deviation) of returns.
    
    Parameters:
    -----------
    returns : pd.Series
        Returns series.
    window : int, optional
        Rolling window size in days. Default is 30.
    
    Returns:
    --------
    pd.Series
        Rolling volatility series.
    """
    return returns.rolling(window=window).std()


def calculate_rolling_mean(
    prices: pd.Series,
    window: int = 30
) -> pd.Series:
    """
    Calculate rolling mean of prices.
    
    Parameters:
    -----------
    prices : pd.Series
        Price series.
    window : int, optional
        Rolling window size in days. Default is 30.
    
    Returns:
    --------
    pd.Series
        Rolling mean series.
    """
    return prices.rolling(window=window).mean()

