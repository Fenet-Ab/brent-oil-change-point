"""
Flask Backend API for Brent Oil Change Point Analysis Dashboard
Provides endpoints for historical prices, change points, events, and metrics.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root / "src"))

from data_loader import load_brent_data, calculate_returns, load_events_data

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load data once at startup
print("Loading data...")
df_prices = load_brent_data()
df_prices['log_return'] = calculate_returns(df_prices, method='log')
df_events = load_events_data()
print("Data loaded successfully!")


@app.route("/")
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "Brent Oil Change Point Analysis API",
        "endpoints": [
            "/prices",
            "/changepoints",
            "/events",
            "/associations",
            "/metrics"
        ]
    })


@app.route("/prices")
def prices():
    """
    Get historical Brent oil price data.
    Optional query parameters:
    - start_date: YYYY-MM-DD format
    - end_date: YYYY-MM-DD format
    """
    try:
        result_df = df_prices.copy()
        
        # Filter by date range if provided
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = pd.to_datetime(start_date)
            result_df = result_df[result_df.index >= start_date]
        
        if end_date:
            end_date = pd.to_datetime(end_date)
            result_df = result_df[result_df.index <= end_date]
        
        # Convert to JSON-friendly format
        result = result_df.reset_index().to_dict(orient='records')
        
        # Format dates as strings
        for record in result:
            if isinstance(record['Date'], pd.Timestamp):
                record['Date'] = record['Date'].strftime('%Y-%m-%d')
            # Handle NaN values
            if pd.isna(record.get('log_return')):
                record['log_return'] = None
        
        return jsonify({
            "status": "success",
            "count": len(result),
            "data": result
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/changepoints")
def changepoints():
    """
    Get detected change points.
    For now, returns example change points. In production, these would come
    from the Bayesian model results saved after running notebook 03.
    """
    try:
        # Example change points (should be loaded from saved model results)
        # In production, load from a saved file like:
        # change_points_df = pd.read_csv("../../data/processed/change_points.csv")
        
        change_points = [
            {
                "date": "2008-09-15",
                "index": 5000,
                "mu_1": 0.0001,
                "mu_2": -0.0005,
                "sigma": 0.02,
                "impact": -0.0006,
                "impact_pct": -0.06,
                "confidence": 0.95
            },
            {
                "date": "2014-11-27",
                "index": 6500,
                "mu_1": -0.0002,
                "mu_2": -0.0008,
                "sigma": 0.025,
                "impact": -0.0006,
                "impact_pct": -0.06,
                "confidence": 0.92
            },
            {
                "date": "2020-03-08",
                "index": 8000,
                "mu_1": 0.0003,
                "mu_2": -0.0015,
                "sigma": 0.03,
                "impact": -0.0018,
                "impact_pct": -0.18,
                "confidence": 0.98
            },
            {
                "date": "2022-02-24",
                "index": 8500,
                "mu_1": -0.0005,
                "mu_2": 0.0012,
                "sigma": 0.028,
                "impact": 0.0017,
                "impact_pct": 0.17,
                "confidence": 0.94
            }
        ]
        
        return jsonify({
            "status": "success",
            "count": len(change_points),
            "data": change_points
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/events")
def events():
    """
    Get key geopolitical and economic events.
    Optional query parameters:
    - start_date: YYYY-MM-DD format
    - end_date: YYYY-MM-DD format
    """
    try:
        result_df = df_events.copy()
        
        # Filter by date range if provided
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = pd.to_datetime(start_date)
            result_df = result_df[result_df['Date'] >= start_date]
        
        if end_date:
            end_date = pd.to_datetime(end_date)
            result_df = result_df[result_df['Date'] <= end_date]
        
        # Convert to JSON-friendly format
        result = result_df.to_dict(orient='records')
        
        # Format dates as strings
        for record in result:
            if isinstance(record['Date'], pd.Timestamp):
                record['Date'] = record['Date'].strftime('%Y-%m-%d')
        
        return jsonify({
            "status": "success",
            "count": len(result),
            "data": result
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/associations")
def associations():
    """
    Get change point-event associations.
    Matches change points with events within a time window.
    """
    try:
        # Get change points (from /changepoints endpoint logic)
        change_points = [
            {"date": "2008-09-15", "index": 5000},
            {"date": "2014-11-27", "index": 6500},
            {"date": "2020-03-08", "index": 8000},
            {"date": "2022-02-24", "index": 8500}
        ]
        
        window_days = int(request.args.get('window_days', 30))
        
        associations = []
        
        for cp in change_points:
            cp_date = pd.to_datetime(cp['date'])
            start = cp_date - timedelta(days=window_days)
            end = cp_date + timedelta(days=window_days)
            
            # Find events within window
            matched_events = df_events[
                (df_events['Date'] >= start) & 
                (df_events['Date'] <= end)
            ].copy()
            
            if not matched_events.empty:
                for _, event in matched_events.iterrows():
                    days_diff = (event['Date'] - cp_date).days
                    associations.append({
                        "change_point_date": cp['date'],
                        "event_date": event['Date'].strftime('%Y-%m-%d'),
                        "event": event['Event'],
                        "description": event['Description'],
                        "days_from_change": days_diff
                    })
        
        return jsonify({
            "status": "success",
            "window_days": window_days,
            "count": len(associations),
            "data": associations
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/metrics")
def metrics():
    """
    Get summary statistics and key metrics.
    """
    try:
        # Calculate metrics
        price_stats = {
            "mean": float(df_prices['Price'].mean()),
            "std": float(df_prices['Price'].std()),
            "min": float(df_prices['Price'].min()),
            "max": float(df_prices['Price'].max()),
            "min_date": df_prices['Price'].idxmin().strftime('%Y-%m-%d'),
            "max_date": df_prices['Price'].idxmax().strftime('%Y-%m-%d')
        }
        
        returns_stats = {
            "mean": float(df_prices['log_return'].mean()),
            "std": float(df_prices['log_return'].std()),
            "min": float(df_prices['log_return'].min()),
            "max": float(df_prices['log_return'].max())
        }
        
        # Volatility metrics
        rolling_vol = df_prices['log_return'].rolling(window=30).std()
        volatility_stats = {
            "mean_30day": float(rolling_vol.mean()),
            "max_30day": float(rolling_vol.max()),
            "max_vol_date": rolling_vol.idxmax().strftime('%Y-%m-%d')
        }
        
        # Date range
        date_range = {
            "start": df_prices.index.min().strftime('%Y-%m-%d'),
            "end": df_prices.index.max().strftime('%Y-%m-%d'),
            "total_days": int((df_prices.index.max() - df_prices.index.min()).days),
            "total_observations": len(df_prices)
        }
        
        return jsonify({
            "status": "success",
            "price_statistics": price_stats,
            "returns_statistics": returns_stats,
            "volatility_statistics": volatility_stats,
            "date_range": date_range,
            "total_events": len(df_events)
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Starting Flask API Server")
    print("=" * 60)
    print("API will be available at: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET /")
    print("  GET /prices?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD")
    print("  GET /changepoints")
    print("  GET /events?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD")
    print("  GET /associations?window_days=30")
    print("  GET /metrics")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=6000)
