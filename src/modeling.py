"""
Bayesian change point detection modeling utilities.

This module provides functions for building and running Bayesian
change point models using PyMC.
"""

from typing import Dict, Optional, Tuple

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm

from .config import BayesianModelConfig


def build_change_point_model(
    returns: np.ndarray,
    config: Optional[BayesianModelConfig] = None
) -> pm.Model:
    """
    Build a Bayesian change point model for detecting structural breaks.
    
    Parameters:
    -----------
    returns : np.ndarray
        Array of log returns.
    config : BayesianModelConfig, optional
        Configuration object. If None, uses default BayesianModelConfig.
    
    Returns:
    --------
    pm.Model
        PyMC model object.
    """
    if config is None:
        config = BayesianModelConfig()
    
    n = len(returns)
    
    with pm.Model() as model:
        # Prior for change point location (discrete uniform over all time points)
        tau = pm.DiscreteUniform("tau", lower=1, upper=n-1)
        
        # Priors for mean returns before and after change point
        mu_1 = pm.Normal(
            "mu_1", 
            mu=config.mu_prior_mean, 
            sigma=config.mu_prior_sigma
        )  # Before change point
        mu_2 = pm.Normal(
            "mu_2", 
            mu=config.mu_prior_mean, 
            sigma=config.mu_prior_sigma
        )  # After change point
        
        # Prior for standard deviation (shared across regimes)
        sigma = pm.HalfNormal("sigma", sigma=config.sigma_prior_sigma)
        
        # Switch function: use mu_1 before tau, mu_2 after tau
        mu = pm.math.switch(tau > np.arange(n), mu_1, mu_2)
        
        # Likelihood
        obs = pm.Normal("obs", mu=mu, sigma=sigma, observed=returns)
    
    return model


def run_mcmc_sampling(
    model: pm.Model,
    config: Optional[BayesianModelConfig] = None,
    progressbar: bool = True
) -> az.InferenceData:
    """
    Run MCMC sampling for the change point model.
    
    Parameters:
    -----------
    model : pm.Model
        PyMC model object.
    config : BayesianModelConfig, optional
        Configuration object. If None, uses default BayesianModelConfig.
    progressbar : bool, optional
        Whether to show progress bar. Default is True.
    
    Returns:
    --------
    az.InferenceData
        ArviZ InferenceData object containing MCMC samples.
    """
    if config is None:
        config = BayesianModelConfig()
    
    with model:
        trace = pm.sample(
            draws=config.draws,
            tune=config.tune,
            return_inferencedata=True,
            random_seed=config.random_seed,
            progressbar=progressbar
        )
    
    return trace


def extract_change_point_results(
    trace: az.InferenceData,
    returns_dates: pd.DatetimeIndex,
    config: Optional[BayesianModelConfig] = None
) -> Dict:
    """
    Extract change point results from MCMC trace.
    
    Parameters:
    -----------
    trace : az.InferenceData
        ArviZ InferenceData object from MCMC sampling.
    returns_dates : pd.DatetimeIndex
        Datetime index corresponding to the returns array.
    config : BayesianModelConfig, optional
        Configuration object. If None, uses default BayesianModelConfig.
    
    Returns:
    --------
    Dict
        Dictionary containing change point results:
        - change_point_date: pd.Timestamp
        - change_point_index: int
        - mu_1: float (mean before change)
        - mu_2: float (mean after change)
        - sigma: float (volatility)
        - impact: float (mu_2 - mu_1)
        - impact_pct: float (impact as percentage)
    """
    if config is None:
        config = BayesianModelConfig()
    
    # Get posterior distribution of tau
    tau_samples = trace.posterior['tau'].values.flatten()
    tau_mean = int(np.mean(tau_samples))
    
    # Convert to date
    change_date = returns_dates[tau_mean]
    
    # Get posterior means for parameters
    mu1_samples = trace.posterior['mu_1'].values.flatten()
    mu2_samples = trace.posterior['mu_2'].values.flatten()
    sigma_samples = trace.posterior['sigma'].values.flatten()
    
    mu1_mean = float(np.mean(mu1_samples))
    mu2_mean = float(np.mean(mu2_samples))
    sigma_mean = float(np.mean(sigma_samples))
    
    # Calculate impact
    impact = mu2_mean - mu1_mean
    impact_pct = impact * 100
    
    return {
        'change_point_date': change_date,
        'change_point_index': tau_mean,
        'mu_1': mu1_mean,
        'mu_2': mu2_mean,
        'sigma': sigma_mean,
        'impact': impact,
        'impact_pct': impact_pct
    }


def check_model_convergence(trace: az.InferenceData, threshold: float = 1.01) -> Dict[str, bool]:
    """
    Check MCMC convergence using R-hat statistics.
    
    Parameters:
    -----------
    trace : az.InferenceData
        ArviZ InferenceData object from MCMC sampling.
    threshold : float, optional
        R-hat threshold for convergence. Default is 1.01.
    
    Returns:
    --------
    Dict[str, bool]
        Dictionary mapping parameter names to convergence status (True = converged).
    """
    summary = az.summary(trace)
    rhat_values = summary['r_hat']
    
    convergence = {
        param: (0.99 < rhat < threshold) 
        for param, rhat in rhat_values.items()
    }
    
    return convergence

