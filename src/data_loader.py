"""
Data loading utilities for Brent oil price analysis.

This module provides functions to load and parse Brent oil price data
and event data from CSV files.
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from .config import DataConfig
from .constants import DATE_FORMAT_1, DATE_FORMAT_2


def load_brent_data(data_path: Optional[Path] = None, config: Optional[DataConfig] = None) -> pd.DataFrame:
    """
    Load Brent oil price data from CSV file.
    
    Handles mixed date formats in the CSV file:
    - "20-May-87" format (most common)
    - "Apr 22, 2020" format (later dates)
    
    Parameters:
    -----------
    data_path : Path, optional
        Path to the CSV file. If None, uses path from config or default.
    config : DataConfig, optional
        Configuration object. If None, uses default DataConfig.
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with Date as index and Price column, sorted by date.
    
    Raises:
    -------
    FileNotFoundError
        If the data file does not exist.
    ValueError
        If the data cannot be parsed.
    """
    if config is None:
        config = DataConfig()
    
    if data_path is None:
        data_path = config.brent_oil_prices_path
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    # Read CSV with proper quote handling
    df = pd.read_csv(data_path, quotechar='"')
    
    if 'Date' not in df.columns:
        raise ValueError("CSV file must contain a 'Date' column")
    if 'Price' not in df.columns:
        raise ValueError("CSV file must contain a 'Price' column")
    
    # Handle mixed date formats in the CSV
    # Clean up any quotes and whitespace from date strings
    date_strings = df['Date'].astype(str).str.strip().str.strip('"').str.strip("'")
    
    # Try parsing with the most common format first: "20-May-87" -> '%d-%b-%y'
    parsed_dates = pd.to_datetime(date_strings, format=DATE_FORMAT_1, errors='coerce')
    df['Date'] = parsed_dates
    
    # For any dates that couldn't be parsed (NaT), try alternative format: "Apr 22, 2020" -> '%b %d, %Y'
    mask = df['Date'].isna()
    if mask.any():
        alternative_dates = pd.to_datetime(
            date_strings.loc[mask], 
            format=DATE_FORMAT_2, 
            errors='coerce'
        )
        df.loc[mask, 'Date'] = alternative_dates
    
    # If still some NaT values, use pandas' automatic inference (fallback)
    mask = df['Date'].isna()
    if mask.any():
        fallback_dates = pd.to_datetime(
            date_strings.loc[mask], 
            errors='coerce'
        )
        df.loc[mask, 'Date'] = fallback_dates
    
    # Remove any rows with invalid dates
    df = df.dropna(subset=['Date'])
    
    if len(df) == 0:
        raise ValueError("No valid dates found in the data file")
    
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    
    return df


def load_events_data(data_path: Optional[Path] = None, config: Optional[DataConfig] = None) -> pd.DataFrame:
    """
    Load key events data from CSV file.
    
    Parameters:
    -----------
    data_path : Path, optional
        Path to the events CSV file. If None, uses path from config or default.
    config : DataConfig, optional
        Configuration object. If None, uses default DataConfig.
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with event information, including Date, Event, and Description columns.
    
    Raises:
    -------
    FileNotFoundError
        If the events file does not exist.
    """
    if config is None:
        config = DataConfig()
    
    if data_path is None:
        data_path = config.key_events_path
    
    if not data_path.exists():
        raise FileNotFoundError(f"Events file not found: {data_path}")
    
    df = pd.read_csv(data_path)
    
    if 'Date' not in df.columns:
        raise ValueError("Events CSV file must contain a 'Date' column")
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df
