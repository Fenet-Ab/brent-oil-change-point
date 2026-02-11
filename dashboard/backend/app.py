from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/prices")
def prices():
    df = pd.read_csv("../../data/raw/brent_oil_prices.csv")
    return df.to_json(orient="records")

@app.route("/changepoints")
def changepoints():
    return jsonify({"date": "2020-03-15", "impact": "High volatility"})
