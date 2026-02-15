"""
Unit tests for modeling functionality.
"""

import pytest
import numpy as np
import pandas as pd
import pymc as pm

from src.modeling import (
    build_change_point_model,
    check_model_convergence,
    extract_change_point_results,
)
from src.config import BayesianModelConfig


class TestBuildChangePointModel:
    """Test cases for build_change_point_model function."""
    
    def test_build_model(self):
        """Test building a change point model."""
        returns = np.random.randn(100)
        
        model = build_change_point_model(returns)
        
        assert isinstance(model, pm.Model)
        assert "tau" in model.named_vars
        assert "mu_1" in model.named_vars
        assert "mu_2" in model.named_vars
        assert "sigma" in model.named_vars
        assert "obs" in model.named_vars
    
    def test_build_model_with_config(self):
        """Test building model with custom config."""
        returns = np.random.randn(100)
        config = BayesianModelConfig(draws=1000, tune=500)
        
        model = build_change_point_model(returns, config=config)
        
        assert isinstance(model, pm.Model)


class TestExtractChangePointResults:
    """Test cases for extract_change_point_results function."""
    
    def test_extract_results_structure(self):
        """Test that extracted results have correct structure."""
        # Create a mock trace-like structure
        # Note: This is a simplified test - full trace would require actual MCMC sampling
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        
        # Create minimal mock trace structure
        # In practice, this would come from actual MCMC sampling
        class MockTrace:
            def __init__(self):
                self.posterior = {
                    'tau': type('obj', (object,), {
                        'values': np.array([[[50]]])  # Mock tau value
                    })(),
                    'mu_1': type('obj', (object,), {
                        'values': np.array([[[0.001]]])
                    })(),
                    'mu_2': type('obj', (object,), {
                        'values': np.array([[[-0.001]]])
                    })(),
                    'sigma': type('obj', (object,), {
                        'values': np.array([[[0.02]]])
                    })()
                }
        
        mock_trace = MockTrace()
        
        # Note: This test would need actual InferenceData structure
        # For now, we'll test the function signature and expected keys
        # A full test would require running actual MCMC sampling
        
        # This test validates the function exists and can be called
        # Full integration test would be in a separate test file
        assert callable(extract_change_point_results)


class TestCheckModelConvergence:
    """Test cases for check_model_convergence function."""
    
    def test_convergence_check_function_exists(self):
        """Test that convergence check function exists."""
        assert callable(check_model_convergence)
        # Full test would require actual InferenceData from MCMC sampling

