"""
Event matching utilities for associating change points with geopolitical events.
"""

from datetime import timedelta
from typing import List, Optional

import pandas as pd

from .config import EventMatchingConfig


def match_events_to_change_point(
    change_point_date: pd.Timestamp,
    events_df: pd.DataFrame,
    window_days: int = 30,
    config: Optional[EventMatchingConfig] = None
) -> pd.DataFrame:
    """
    Find events within a time window around a change point.
    
    Parameters:
    -----------
    change_point_date : pd.Timestamp
        The change point date.
    events_df : pd.DataFrame
        DataFrame with event dates (must have 'Date' column).
    window_days : int, optional
        Number of days before and after change point to search. Default is 30.
    config : EventMatchingConfig, optional
        Configuration object. If provided, window_days is taken from config.
    
    Returns:
    --------
    pd.DataFrame
        Matched events with 'days_from_change' column added.
    """
    if config is not None:
        window_days = config.window_days
    
    if 'Date' not in events_df.columns:
        raise ValueError("events_df must contain a 'Date' column")
    
    start = change_point_date - timedelta(days=window_days)
    end = change_point_date + timedelta(days=window_days)
    
    matched = events_df[
        (events_df['Date'] >= start) & 
        (events_df['Date'] <= end)
    ].copy()
    
    if not matched.empty:
        matched['days_from_change'] = (matched['Date'] - change_point_date).dt.days
    
    return matched


def find_nearest_event(
    change_point_date: pd.Timestamp,
    events_df: pd.DataFrame,
    window_days: int = 30,
    config: Optional[EventMatchingConfig] = None
) -> Optional[pd.Series]:
    """
    Find the nearest event to a change point within a time window.
    
    Parameters:
    -----------
    change_point_date : pd.Timestamp
        The change point date.
    events_df : pd.DataFrame
        DataFrame with event dates (must have 'Date' column).
    window_days : int, optional
        Number of days before and after change point to search. Default is 30.
    config : EventMatchingConfig, optional
        Configuration object. If provided, window_days is taken from config.
    
    Returns:
    --------
    pd.Series or None
        The nearest event as a Series, or None if no events found.
    """
    matched = match_events_to_change_point(change_point_date, events_df, window_days, config)
    
    if matched.empty:
        return None
    
    # Find event with minimum absolute days from change point
    nearest_idx = matched['days_from_change'].abs().idxmin()
    return matched.loc[nearest_idx]


def associate_change_points_with_events(
    change_points_df: pd.DataFrame,
    events_df: pd.DataFrame,
    window_days: int = 30,
    config: Optional[EventMatchingConfig] = None
) -> pd.DataFrame:
    """
    Associate multiple change points with events.
    
    Parameters:
    -----------
    change_points_df : pd.DataFrame
        DataFrame with change point dates (must have 'change_date' column).
    events_df : pd.DataFrame
        DataFrame with event dates (must have 'Date' column).
    window_days : int, optional
        Number of days before and after change point to search. Default is 30.
    config : EventMatchingConfig, optional
        Configuration object. If provided, window_days is taken from config.
    
    Returns:
    --------
    pd.DataFrame
        Association results with change_point_date, event_date, event, and days_from_change columns.
    """
    if config is not None:
        window_days = config.window_days
    
    if 'change_date' not in change_points_df.columns:
        raise ValueError("change_points_df must contain a 'change_date' column")
    
    associations = []
    
    for _, cp_row in change_points_df.iterrows():
        cp_date = pd.to_datetime(cp_row['change_date'])
        matched = match_events_to_change_point(cp_date, events_df, window_days, config)
        
        if not matched.empty:
            for _, event_row in matched.iterrows():
                associations.append({
                    "change_point_date": cp_date,
                    "event_date": event_row['Date'],
                    "event": event_row.get('Event', 'Unknown Event'),
                    "description": event_row.get('Description', ''),
                    "days_from_change": event_row['days_from_change']
                })
        else:
            associations.append({
                "change_point_date": cp_date,
                "event_date": None,
                "event": "No major recorded event",
                "description": None,
                "days_from_change": None
            })
    
    return pd.DataFrame(associations)

