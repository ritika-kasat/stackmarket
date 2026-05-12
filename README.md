# 📈 StockPulse — Real-Time Stock Market Dashboard

<p align="center">
  <img src="https://img.logo.dev/ticker/AAPL?token=pk_free" width="40"/>
  <img src="https://img.logo.dev/ticker/GOOGL?token=pk_free" width="40"/>
  <img src="https://img.logo.dev/ticker/MSFT?token=pk_free" width="40"/>
  <img src="https://img.logo.dev/ticker/TSLA?token=pk_free" width="40"/>
  <img src="https://img.logo.dev/ticker/AMZN?token=pk_free" width="40"/>
</p>

<p align="center">
  <b>A beautiful, real-time stock market dashboard built with Streamlit & yfinance — completely free, no API key required.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/yfinance-Free%20API-green"/>
  <img src="https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow"/>
</p>

---

## 🌟 Features

| Feature | Status | Description |
|---|---|---|
| 🏠 Home Dashboard | ✅ Done | Feature cards, live watchlist, IST clock |
| 📊 Stock Analysis | 🔜 Step 2 | Live KPI cards, OHLCV data, metrics |
| 📉 Interactive Charts | 🔜 Step 3 | Candlestick, RSI, MACD, Bollinger Bands |
| ⚖️ Stock Comparison | 🔜 Step 4 | Normalized comparison, correlation heatmap |
| 📰 Market News | 🔜 Step 5 | Live headlines with sentiment tagging |
| 🖼️ Company Logos | 🔜 Step 5 | Auto-fetched via Logo.dev free API |
| ⬇️ CSV Export | 🔜 Step 5 | Download historical data in one click |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/stockpulse.git
cd stockpulse
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
stockpulse/
│
├── app.py                   # 🎯 Main Streamlit application
├── requirements.txt         # 📦 Python dependencies
├── README.md                # 📖 This file
│
└── .streamlit/
    └── config.toml          # 🎨 Dark theme configuration
```

> More files will be added in future steps (pages/, utils/, components/)

---

## 📦 Dependencies

```txt
streamlit>=1.32.0      # Web app framework
yfinance>=0.2.38       # Free stock data API (no key needed)
pandas>=2.0.0          # Data manipulation
plotly>=5.20.0         # Interactive charts
requests>=2.31.0       # HTTP requests
pytz>=2024.1           # Timezone support (IST clock)
```

Install all at once:
```bash
pip install streamlit yfinance pandas plotly requests pytz
```

---

## 🎨 Design System

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| Background | `#0a0e1a` | Main app background |
| Surface | `#111827` | Sidebar background |
| Card | `#1a2235` | Component cards |
| Accent Green | `#00f5a0` | Primary highlights, prices |
| Accent Cyan | `#00d4ff` | Secondary highlights |
| Danger Red | `#ff4d6d` | Negative % changes |
| Muted | `#64748b` | Subtext, labels |

### Typography

| Font | Usage |
|---|---|
| **Syne** (Google Fonts) | Headings, titles, display text |
| **Space Mono** (Google Fonts) | Data, tickers, timestamps, code |

---

## 🔌 APIs Used

### 1. yfinance (Primary Data Source)
- **Cost:** 100% Free — No API key needed
- **Data:** Stock prices, history, company info, news
- **Usage:**
```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
info    = ticker.info                        # Company details
history = ticker.history(period="1y")        # Historical OHLCV
news    = ticker.news                        # Latest headlines
```

### 2. Logo.dev (Company Logos)
- **Cost:** Free up to 500,000 requests/month
- **Usage:**
```python
# By stock ticker
logo_url = f"https://img.logo.dev/ticker/AAPL?token=pk_free"

# By domain
logo_url = f"https://img.logo.dev/apple.com?token=pk_free"
```

---

## 📊 Pages Overview

### 🏠 Home
- Live IST clock in the sidebar
- Feature overview cards
- Watchlist quick stats (AAPL, GOOGL, MSFT, TSLA, AMZN)
- Navigation to all sections

### 📊 Stock Analysis *(Coming in Step 2)*
- Real-time price, market cap, P/E ratio
- 52-week high/low, volume, dividend yield
- KPI metric cards with delta indicators
- Company info: sector, industry, website

### 📉 Interactive Charts *(Coming in Step 3)*
- Candlestick chart with Moving Averages (MA20, MA50)
- RSI indicator (overbought/oversold zones)
- MACD + Signal line
- Bollinger Bands overlay
- Volume bar chart (color-coded)

### ⚖️ Compare Stocks *(Coming in Step 4)*
- Multi-stock normalized price comparison
- Correlation heatmap
- Return %, Volatility, Sharpe Ratio, Beta table

### 📰 Market News *(Coming in Step 5)*
- Live news via yfinance feed
- Sentiment tagging (Positive / Neutral / Negative)
- Source, time, and article link display

---

## ⚙️ Configuration

Edit `.streamlit/config.toml` to customize the theme:

```toml
[theme]
base                  = "dark"
backgroundColor       = "#0a0e1a"
secondaryBackgroundColor = "#111827"
primaryColor          = "#00f5a0"
textColor             = "#e2e8f0"
```

---

## ☁️ Deployment (Free)

### Streamlit Community Cloud

1. Push your code to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → Select your repo → Set `app.py` as main file
4. Click **Deploy** — your app is live in minutes! 🚀

**No server setup. No cost. Fully managed.**

---

## 🗺️ Roadmap

- [x] **Step 1** — Project setup, dark theme, sidebar, navigation
- [ ] **Step 2** — Live yfinance data, KPI metric cards
- [ ] **Step 3** — Plotly charts (Candlestick, RSI, MACD, Bollinger Bands)
- [ ] **Step 4** — Stock comparison, sector heatmap, watchlist manager
- [ ] **Step 5** — News feed, Logo.dev integration, CSV export, deployment

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [yfinance](https://github.com/ranaroussi/yfinance) — Free Yahoo Finance data wrapper
- [Streamlit](https://streamlit.io) — Web app framework for data apps
- [Plotly](https://plotly.com) — Interactive charting library
- [Logo.dev](https://logo.dev) — Free company logo API
- [Google Fonts](https://fonts.google.com) — Syne & Space Mono typefaces

---

<p align="center">
  Built with ❤️ using Streamlit &amp; Python &nbsp;|&nbsp; Data by yfinance &nbsp;|&nbsp; Free to use
</p>
