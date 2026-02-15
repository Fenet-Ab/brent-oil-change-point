"""
Unit tests for data loading functionality.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import csv

from src.data_loader import load_brent_data, load_events_data
from src.config import DataConfig


class TestLoadBrentData:
    """Test cases for load_brent_data function."""
    
    def test_load_brent_data_default_path(self):
        """Test loading data with default path."""
        df = load_brent_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'Price' in df.columns
        assert isinstance(df.index, pd.DatetimeIndex)
        assert df.index.is_monotonic_increasing
    
    def test_load_brent_data_custom_path(self):
        """Test loading data with custom path."""
        # Create a temporary CSV file with test data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Price'])
            writer.writerow(['20-May-87', '18.63'])
            writer.writerow(['21-May-87', '18.45'])
            temp_path = Path(f.name)
        
        try:
            df = load_brent_data(data_path=temp_path)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert 'Price' in df.columns
            assert isinstance(df.index, pd.DatetimeIndex)
        finally:
            temp_path.unlink()
    
    def test_load_brent_data_mixed_date_formats(self):
        """Test loading data with mixed date formats."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Price'])
            writer.writerow(['20-May-87', '18.63'])
            writer.writerow(['"Apr 22, 2020"', '13.77'])
            temp_path = Path(f.name)
        
        try:
            df = load_brent_data(data_path=temp_path)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert isinstance(df.index, pd.DatetimeIndex)
        finally:
            temp_path.unlink()
    
    def test_load_brent_data_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_brent_data(data_path=Path("nonexistent_file.csv"))
    
    def test_load_brent_data_missing_columns(self):
        """Test that ValueError is raised for missing required columns."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'WrongColumn'])
            writer.writerow(['20-May-87', '18.63'])
            temp_path = Path(f.name)
        
        try:
            with pytest.raises(ValueError, match="Price"):
                load_brent_data(data_path=temp_path)
        finally:
            temp_path.unlink()


class TestLoadEventsData:
    """Test cases for load_events_data function."""
    
    def test_load_events_data_default_path(self):
        """Test loading events data with default path."""
        df = load_events_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'Date' in df.columns
        assert isinstance(df['Date'].dtype, pd.DatetimeTZDtype) or pd.api.types.is_datetime64_any_dtype(df['Date'])
    
    def test_load_events_data_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_events_data(data_path=Path("nonexistent_file.csv"))

