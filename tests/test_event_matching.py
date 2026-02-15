"""
Unit tests for event matching functionality.
"""

import pytest
import pandas as pd
from datetime import timedelta

from src.event_matching import (
    match_events_to_change_point,
    find_nearest_event,
    associate_change_points_with_events,
)
from src.config import EventMatchingConfig


class TestMatchEventsToChangePoint:
    """Test cases for match_events_to_change_point function."""
    
    def test_match_events_within_window(self):
        """Test matching events within time window."""
        change_point = pd.Timestamp('2020-01-15')
        
        events_df = pd.DataFrame({
            'Date': pd.to_datetime([
                '2020-01-01',  # Before window
                '2020-01-10',  # Within window
                '2020-01-20',  # Within window
                '2020-02-15',  # After window
            ]),
            'Event': ['Event1', 'Event2', 'Event3', 'Event4']
        })
        
        matched = match_events_to_change_point(change_point, events_df, window_days=30)
        
        assert isinstance(matched, pd.DataFrame)
        assert len(matched) == 2  # Only events within window
        assert 'days_from_change' in matched.columns
        assert all(matched['days_from_change'].abs() <= 30)
    
    def test_match_events_no_matches(self):
        """Test when no events are within window."""
        change_point = pd.Timestamp('2020-01-15')
        
        events_df = pd.DataFrame({
            'Date': pd.to_datetime(['2020-03-01', '2020-04-01']),
            'Event': ['Event1', 'Event2']
        })
        
        matched = match_events_to_change_point(change_point, events_df, window_days=30)
        
        assert isinstance(matched, pd.DataFrame)
        assert len(matched) == 0
    
    def test_match_events_with_config(self):
        """Test matching events with EventMatchingConfig."""
        change_point = pd.Timestamp('2020-01-15')
        
        events_df = pd.DataFrame({
            'Date': pd.to_datetime(['2020-01-10', '2020-01-20']),
            'Event': ['Event1', 'Event2']
        })
        
        config = EventMatchingConfig(window_days=10)
        matched = match_events_to_change_point(change_point, events_df, config=config)
        
        assert isinstance(matched, pd.DataFrame)
        assert len(matched) == 2


class TestFindNearestEvent:
    """Test cases for find_nearest_event function."""
    
    def test_find_nearest_event(self):
        """Test finding nearest event to change point."""
        change_point = pd.Timestamp('2020-01-15')
        
        events_df = pd.DataFrame({
            'Date': pd.to_datetime([
                '2020-01-10',  # 5 days before
                '2020-01-20',  # 5 days after
                '2020-01-16',  # 1 day after (nearest)
            ]),
            'Event': ['Event1', 'Event2', 'Event3']
        })
        
        nearest = find_nearest_event(change_point, events_df, window_days=30)
        
        assert isinstance(nearest, pd.Series)
        assert nearest['Event'] == 'Event3'
        assert nearest['days_from_change'] == 1
    
    def test_find_nearest_event_no_matches(self):
        """Test when no events are found."""
        change_point = pd.Timestamp('2020-01-15')
        
        events_df = pd.DataFrame({
            'Date': pd.to_datetime(['2020-03-01']),
            'Event': ['Event1']
        })
        
        nearest = find_nearest_event(change_point, events_df, window_days=30)
        
        assert nearest is None


class TestAssociateChangePointsWithEvents:
    """Test cases for associate_change_points_with_events function."""
    
    def test_associate_multiple_change_points(self):
        """Test associating multiple change points with events."""
        change_points_df = pd.DataFrame({
            'change_date': pd.to_datetime(['2020-01-15', '2020-06-15'])
        })
        
        events_df = pd.DataFrame({
            'Date': pd.to_datetime(['2020-01-10', '2020-06-20']),
            'Event': ['Event1', 'Event2'],
            'Description': ['Desc1', 'Desc2']
        })
        
        associations = associate_change_points_with_events(
            change_points_df, events_df, window_days=30
        )
        
        assert isinstance(associations, pd.DataFrame)
        assert len(associations) >= 2
        assert 'change_point_date' in associations.columns
        assert 'event_date' in associations.columns
        assert 'days_from_change' in associations.columns

