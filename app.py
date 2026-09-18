from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)


def get_stock_data(symbol="RELIANCE.NS", period="1y"):

    data = yf.download(
        symbol,
        period=period,
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    # Data cleaning
    data = data.dropna()
    data = data.drop_duplicates()

    # Data transformation
    data["Price Change"] = data["Close"].diff()

    data["Return %"] = (
        data["Close"].pct_change() * 100
    )

    data["MA20"] = (
        data["Close"].rolling(20).mean()
    )

    data["MA50"] = (
        data["Close"].rolling(50).mean()
    )

    return data


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/stock")
def stock_api():

    symbol = request.args.get(
        "symbol",
        "RELIANCE.NS"
    ).upper()

    period = request.args.get(
        "period",
        "1y"
    )

    data = get_stock_data(
        symbol,
        period
    )

    if data is None:

        return jsonify({
            "error": "No stock data found."
        }), 404

    latest = data.iloc[-1]

    previous = (
        data.iloc[-2]
        if len(data) > 1
        else latest
    )

    close = float(
        latest["Close"]
    )

    previous_close = float(
        previous["Close"]
    )

    change = (
        close - previous_close
    )

    change_percentage = (
        change / previous_close * 100
        if previous_close != 0
        else 0
    )

    result = {

        "symbol": symbol,

        "records": len(data),

        "latest": {

            "date":
                str(latest["Date"])[:10],

            "open":
                float(latest["Open"]),

            "high":
                float(latest["High"]),

            "low":
                float(latest["Low"]),

            "close":
                close,

            "volume":
                int(latest["Volume"]),

            "change":
                change,

            "change_pct":
                change_percentage,

            "ma20":
                float(latest["MA20"])
                if pd.notna(latest["MA20"])
                else None,

            "ma50":
                float(latest["MA50"])
                if pd.notna(latest["MA50"])
                else None
        },

        "chart": {

            "dates": [
                str(x)[:10]
                for x in data["Date"]
            ],

            "close": [
                round(float(x), 2)
                for x in data["Close"]
            ],

            "volume": [
                int(x)
                for x in data["Volume"]
            ],

            "ma20": [
                None
                if pd.isna(x)
                else round(float(x), 2)
                for x in data["MA20"]
            ],

            "ma50": [
                None
                if pd.isna(x)
                else round(float(x), 2)
                for x in data["MA50"]
            ]
        },

        "pipeline": {

            "raw_records":
                len(data),

            "cleaned_records":
                len(data),

            "missing_values":
                int(
                    data.isnull()
                    .sum()
                    .sum()
                ),

            "duplicate_rows":
                int(
                    data.duplicated()
                    .sum()
                )
        }
    }

    return jsonify(result)
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )