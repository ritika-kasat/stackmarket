import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import requests
import time

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

@st.cache_data(ttl=300)
def get_market_overview():
    indices = {"S&P 500": "^GSPC", "Dow Jones": "^DJI", "NASDAQ": "^IXIC", "Russell 2000": "^RUT"}
    sectors = {"Tech": "XLK", "Financials": "XLF", "Energy": "XLE", "Health": "XLV", "Industrials": "XLI", "Consumer Disc": "XLY"}
    movers = ["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","V","JNJ","WMT","JPM","PG","MA","UNH","DIS","HD","VZ","NFLX","INTC","CRM"]
    
    all_tickers = list(indices.values()) + list(sectors.values()) + movers
    try:
        df = yf.download(all_tickers, period="5d", progress=False)['Close']
        return df, indices, sectors, movers
    except:
        return pd.DataFrame(), indices, sectors, movers

# 1. Page Configuration (must be first streamlit command)
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme touches if needed, Streamlit handles dark mode natively though.
st.markdown("""
    <style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
    }
    /* Styled metric cards */
    div[data-testid="metric-container"] {
        background-color: #1e222d;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #2d313f;
    }
    /* Custom sidebar */
    [data-testid="stSidebar"] {
        background-color: #12141b;
        border-right: 1px solid #2d313f;
    }
    /* Logo container */
    .logo-container {
        background-color: #1a2235;
        border: 1px solid rgba(0,245,160,0.3);
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 0 12px rgba(0,245,160,0.15);
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .logo-container img {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Navigation and Inputs
st.sidebar.title("📈 Stock Market Dashboard")

# Navigation
page = st.sidebar.radio("Navigation", ["Home", "Stock Analysis", "Compare Stocks", "Market News"])

# Ticker Search
st.sidebar.markdown("---")
st.sidebar.header("Stock Selection")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", value="AAPL")
ticker_symbol = ticker_symbol.upper()

st.sidebar.markdown("---")

@st.cache_data(ttl=3600)
def get_logo_url(ticker):
    # The logo.dev pk_free token returns 401 Unauthorized, so we use a free alternative
    url = f"https://financialmodelingprep.com/image-stock/{ticker}.png"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return url
    except:
        pass
    return None

@st.cache_data(ttl=86400)
def get_company_name(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info.get('shortName', ticker)
    except:
        return ticker

with st.sidebar:
    with st.spinner("Fetching company logo..."):
        logo_url = get_logo_url(ticker_symbol)
        
    if logo_url:
        st.markdown(f'<div class="logo-container"><img src="{logo_url}" width="80" height="80"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="logo-container" style="font-size: 50px;">🏢</div>', unsafe_allow_html=True)

auto_refresh = st.sidebar.checkbox("Auto-Refresh (60s)")

# 3. Header with Real-time Date and Time
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.header(f"📈 Stock Market Dashboard")
st.markdown(f"**Current Date & Time:** `{current_time}`")
st.markdown("---")

def format_large_number(num):
    if not num or pd.isna(num): return "N/A"
    try:
        num = float(num)
        if num >= 1_000_000_000_000:
            return f"${num/1_000_000_000_000:.2f}T"
        elif num >= 1_000_000_000:
            return f"${num/1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"${num/1_000_000:.2f}M"
        else:
            return f"${num:,.2f}"
    except:
        return "N/A"

def get_sentiment(text):
    positive_words = ['up', 'gain', 'jump', 'surge', 'soar', 'beat', 'growth', 'bull', 'buy', 'positive', 'higher']
    negative_words = ['down', 'loss', 'drop', 'fall', 'plunge', 'miss', 'decline', 'bear', 'sell', 'negative', 'lower']
    text = text.lower()
    score = sum(1 for w in positive_words if w in text) - sum(1 for w in negative_words if w in text)
    if score > 0: return "🟢 Positive"
    elif score < 0: return "🔴 Negative"
    return "⚪ Neutral"

# Helper function to load data
@st.cache_data(ttl=300)
def load_stock_data(ticker, period="1y"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        return None

# 4. Main Content based on Navigation
if page == "Home":
    st.subheader("Market Overview")
    with st.spinner("Fetching market data..."):
        df_market, indices, sectors, movers = get_market_overview()
    
    if not df_market.empty:
        # Indices
        cols = st.columns(len(indices))
        for col, (name, ticker) in zip(cols, indices.items()):
            if ticker in df_market.columns:
                s = df_market[ticker].dropna()
                if len(s) >= 2:
                    curr = s.iloc[-1]
                    prev = s.iloc[-2]
                    pct = (curr - prev)/prev * 100
                    col.metric(name, f"{curr:,.2f}", f"{curr-prev:,.2f} ({pct:.2f}%)")
                    
        st.markdown("---")
        col_m1, col_m2 = st.columns(2)
        
        # Top Movers
        with col_m1:
            st.subheader("Top Movers (Large Cap)")
            mover_pcts = {}
            for t in movers:
                if t in df_market.columns:
                    s = df_market[t].dropna()
                    if len(s) >= 2:
                        mover_pcts[t] = (s.iloc[-1] - s.iloc[-2]) / s.iloc[-2] * 100
            
            sorted_movers = sorted(mover_pcts.items(), key=lambda x: x[1], reverse=True)
            if sorted_movers:
                st.write("**Top Gainers**")
                for t, pct in sorted_movers[:3]:
                    st.write(f"🟢 **{t}**: +{pct:.2f}%")
                st.write("**Top Losers**")
                for t, pct in sorted_movers[-3:]:
                    st.write(f"🔴 **{t}**: {pct:.2f}%")
        
        # Sector Performance
        with col_m2:
            st.subheader("Sector Performance")
            sector_data = []
            for name, t in sectors.items():
                if t in df_market.columns:
                    s = df_market[t].dropna()
                    if len(s) >= 2:
                        sector_data.append({"Sector": name, "Change %": (s.iloc[-1] - s.iloc[-2]) / s.iloc[-2] * 100})
            if sector_data:
                sector_df = pd.DataFrame(sector_data)
                fig = px.bar(sector_df, x="Sector", y="Change %", color="Change %", color_continuous_scale="RdYlGn")
                fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0), height=300)
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("My Watchlist")
    col1, col2 = st.columns(2)
    with col1:
        new_ticker = st.text_input("Add Ticker to Watchlist")
        if st.button("Add") and new_ticker:
            if new_ticker.upper() not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(new_ticker.upper())
                st.toast(f"Added {new_ticker.upper()} to watchlist!", icon="✅")
                time.sleep(0.5)
                st.rerun()
    with col2:
        rem_ticker = st.selectbox("Remove Ticker from Watchlist", st.session_state['watchlist'] if st.session_state['watchlist'] else [""])
        if st.button("Remove") and rem_ticker in st.session_state['watchlist']:
            st.session_state['watchlist'].remove(rem_ticker)
            st.toast(f"Removed {rem_ticker} from watchlist!", icon="❌")
            time.sleep(0.5)
            st.rerun()
            
    wl_data = []
    wl_tickers = st.session_state['watchlist']
    
    if wl_tickers:
        cols = st.columns(len(wl_tickers))
        for i, t in enumerate(wl_tickers):
            hist = load_stock_data(t, "3mo")
            if hist is not None and not hist.empty:
                curr = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist)>1 else curr
                chg = (curr - prev) / prev * 100
                
                # Fetch logo for watchlist pill
                l_url = get_logo_url(t)
                comp_name = get_company_name(t)
                
                with cols[i]:
                    st.markdown("""<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #1e222d; padding: 10px; border-radius: 10px; border: 1px solid #2d313f;'>""", unsafe_allow_html=True)
                    if l_url:
                        st.markdown(f'<img src="{l_url}" width="32" height="32" style="border-radius:4px; margin-bottom:5px;">', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="font-size:24px; margin-bottom:5px;">🏢</div>', unsafe_allow_html=True)
                    st.markdown(f"**{t}**", unsafe_allow_html=True)
                    st.markdown(f"<span style='font-size:0.8em; color:#a0aab2; text-align:center; margin-bottom:5px;'>{comp_name}</span>", unsafe_allow_html=True)
                    
                    color = "green" if chg >= 0 else "red"
                    st.markdown(f"<span style='color:{color}; font-weight:bold;'>{chg:+.2f}%</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                wl_data.append({
                    "Logo": l_url,
                    "Ticker": t, 
                    "Company": comp_name,
                    "Price": float(curr), 
                    "Change %": float(chg), 
                    "Trend": hist['Close'].tolist()
                })
            
    if wl_data:
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(wl_data), 
            column_config={
                "Logo": st.column_config.ImageColumn("Logo", width="small"),
                "Trend": st.column_config.LineChartColumn("3-Month Trend")
            }, 
            hide_index=True, 
            use_container_width=True
        )

elif page == "Stock Analysis":
    col_hdr1, col_hdr2 = st.columns([1, 15])
    l_url = get_logo_url(ticker_symbol)
    
    with col_hdr1:
        if l_url:
            st.markdown(f'<img src="{l_url}" width="48" height="48" style="border-radius:8px; margin-top:15px;">', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:36px; margin-top:15px;">🏢</div>', unsafe_allow_html=True)
            
    with col_hdr2:
        st.subheader(f"Stock Analysis: {ticker_symbol}")
    
    period = st.selectbox("Select Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"], index=5)
    hist = load_stock_data(ticker_symbol, period=period)
    
    if hist is not None and not hist.empty:
        stock = yf.Ticker(ticker_symbol)
        # Display Company Info
        info = stock.info
        name = info.get('longName', ticker_symbol)
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        website = info.get('website', 'N/A')
        
        st.markdown(f"**Company:** [{name}]({website}) | **Sector:** {sector} | **Industry:** {industry}")
        st.markdown("---")
        
        # KPI metric cards in a 4-column layout
        col1, col2, col3, col4 = st.columns(4)
        
        # 1. Current Price
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - prev_price
        pct_change = (change / prev_price) * 100
        col1.metric("Current Price", f"${current_price:,.2f}", f"{change:,.2f} ({pct_change:.2f}%)")
        
        # 2. Market Cap
        market_cap = info.get('marketCap')
        col2.metric("Market Cap", format_large_number(market_cap))
        
        # 3. 52-Week High & Low
        high_52 = info.get('fiftyTwoWeekHigh', 'N/A')
        low_52 = info.get('fiftyTwoWeekLow', 'N/A')
        col3.metric("52-Week High / Low", f"${high_52:,.2f} / ${low_52:,.2f}" if isinstance(high_52, (int, float)) else "N/A")
        
        # 4. Volume & Average Volume
        volume = info.get('volume', 'N/A')
        avg_volume = info.get('averageVolume', 'N/A')
        def fmt_vol(v): return f"{v:,.0f}" if isinstance(v, (int, float)) else "N/A"
        col4.metric("Volume / Avg Vol", f"{fmt_vol(volume)} / {fmt_vol(avg_volume)}")
        
        st.markdown(" ") # Spacer
        
        # Row 2 of KPIs
        col5, col6, col7, col8 = st.columns(4)
        
        pe_ratio = info.get('trailingPE', 'N/A')
        col5.metric("P/E Ratio", f"{pe_ratio:.2f}" if isinstance(pe_ratio, (float, int)) else "N/A")
        
        div_yield = info.get('dividendYield', 'N/A')
        col6.metric("Dividend Yield", f"{div_yield * 100:.2f}%" if isinstance(div_yield, (float, int)) else "N/A")
        
        st.markdown("---")
        
        # Interactive Chart
        chart_type = st.radio("Select Chart Type", ["Candlestick", "Line", "Area"], horizontal=True)
        
        # Calculate Technical Indicators
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        
        # Bollinger Bands
        hist['BB_STD'] = hist['Close'].rolling(window=20).std()
        hist['BB_Upper'] = hist['SMA_20'] + 2 * hist['BB_STD']
        hist['BB_Lower'] = hist['SMA_20'] - 2 * hist['BB_STD']
        
        # MACD
        exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = exp1 - exp2
        hist['Signal_Line'] = hist['MACD'].ewm(span=9, adjust=False).mean()
        
        # RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # Volume Colors
        colors = ['green' if row['Close'] >= row['Open'] else 'red' for index, row in hist.iterrows()]
        
        # Create Subplots
        fig = make_subplots(rows=4, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.5, 0.15, 0.15, 0.2],
                            subplot_titles=(f"{ticker_symbol} Price", "Volume", "MACD", "RSI (14)"))
        
        # 1. Main Chart
        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], 
                                         low=hist['Low'], close=hist['Close'], name='Price',
                                         increasing_line_color='green', decreasing_line_color='red'), 
                          row=1, col=1)
        elif chart_type == "Line":
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Price', line=dict(color='blue')), row=1, col=1)
        elif chart_type == "Area":
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', mode='lines', name='Price', line=dict(color='cyan')), row=1, col=1)
            
        # Add Overlays
        fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_20'], mode='lines', name='SMA 20', line=dict(color='orange', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_50'], mode='lines', name='SMA 50', line=dict(color='purple', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=hist.index, y=hist['BB_Upper'], mode='lines', name='BB Upper', line=dict(color='rgba(250,250,250,0.2)', width=1, dash='dot')), row=1, col=1)
        fig.add_trace(go.Scatter(x=hist.index, y=hist['BB_Lower'], mode='lines', name='BB Lower', line=dict(color='rgba(250,250,250,0.2)', width=1, dash='dot'), fill='tonexty', fillcolor='rgba(250,250,250,0.05)'), row=1, col=1)
        
        # 2. Volume
        fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], marker_color=colors, name='Volume'), row=2, col=1)
        
        # 3. MACD
        fig.add_trace(go.Scatter(x=hist.index, y=hist['MACD'], mode='lines', name='MACD', line=dict(color='blue')), row=3, col=1)
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Signal_Line'], mode='lines', name='Signal', line=dict(color='orange')), row=3, col=1)
        fig.add_trace(go.Bar(x=hist.index, y=hist['MACD'] - hist['Signal_Line'], name='MACD Hist', marker_color='gray'), row=3, col=1)
        
        # 4. RSI
        fig.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], mode='lines', name='RSI', line=dict(color='purple')), row=4, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=4, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=4, col=1)
        
        fig.update_layout(template="plotly_dark", height=800, xaxis_rangeslider_visible=False, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display Data
        with st.expander("View Historical Data"):
            st.dataframe(hist.sort_index(ascending=False))
            csv = hist.to_csv()
            st.download_button(label="Download Data as CSV", data=csv, file_name=f"{ticker_symbol}_data.csv", mime="text/csv")
            
    else:
        st.error(f"Could not load data for {ticker_symbol}. Please check the ticker symbol.")

elif page == "Compare Stocks":
    st.subheader("Compare Multiple Stocks")
    
    default_options = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "NFLX", "AMD", "INTC", "V", "JPM", "JNJ", "WMT", "PG"]
    all_options = list(set(default_options + st.session_state.get('watchlist', [])))
    
    compare_tickers = st.multiselect("Select 2-5 Stocks to Compare", options=all_options, default=st.session_state.get('watchlist', [])[:3])
    period = st.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3)
    
    if len(compare_tickers) >= 2:
        combined_df = pd.DataFrame()
        metrics_data = []
        
        spy_hist = load_stock_data("^GSPC", period=period)
        spy_pct = spy_hist['Close'].pct_change().dropna() if spy_hist is not None else None
        
        for ticker in compare_tickers:
            hist = load_stock_data(ticker, period=period)
            if hist is not None and not hist.empty:
                # Normalize
                normalized = hist['Close'] / hist['Close'].iloc[0] * 100
                combined_df[ticker] = normalized
                
                # Metrics
                ret = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100
                pct_change = hist['Close'].pct_change().dropna()
                vol = pct_change.std() * np.sqrt(252) * 100
                sharpe = (pct_change.mean() / pct_change.std()) * np.sqrt(252) if pct_change.std() != 0 else 0
                
                beta = "N/A"
                if spy_pct is not None and len(pct_change) > 10:
                    aligned = pd.concat([pct_change, spy_pct], axis=1).dropna()
                    if len(aligned) > 10:
                        cov = np.cov(aligned.iloc[:,0], aligned.iloc[:,1])[0][1]
                        var = np.var(aligned.iloc[:,1])
                        beta = cov / var if var != 0 else "N/A"
                        
                metrics_data.append({
                    "Ticker": ticker,
                    "Return (%)": ret,
                    "Volatility (%)": vol,
                    "Sharpe Ratio": sharpe,
                    "Beta": beta if isinstance(beta, str) else float(beta)
                })
                
        if not combined_df.empty:
            fig = px.line(combined_df, title=f"Relative Performance ({period}) - Base 100", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Comparison Metrics")
            st.dataframe(pd.DataFrame(metrics_data).set_index("Ticker").style.format("{:.2f}", na_rep="N/A"), use_container_width=True)
            
            st.subheader("Correlation Heatmap")
            corr = combined_df.pct_change().corr()
            fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", template="plotly_dark", title="Daily Return Correlation", color_continuous_scale="RdBu_r")
            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("Please select at least 2 stocks to compare.")

elif page == "Market News":
    st.subheader(f"Latest News for {ticker_symbol}")
    
    with st.spinner("Fetching latest news..."):
        stock = yf.Ticker(ticker_symbol)
        news = stock.news
    
    if news:
        for item in news[:10]:
            article = item.get('content', item)
            title = article.get('title', 'No Title')
            
            # Parse link
            link = article.get('clickThroughUrl', {}).get('url', article.get('link', '#'))
            
            # Parse publisher
            publisher = article.get('provider', {}).get('displayName', article.get('publisher', 'Unknown'))
            
            # Parse date
            pub_date = article.get('pubDate', '')
            if not pub_date and 'providerPublishTime' in article:
                try:
                    pub_date = datetime.datetime.fromtimestamp(article['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pub_date = 'Unknown Date'
            elif not pub_date:
                pub_date = 'Unknown Date'
                
            # Parse thumbnail
            thumbnail = ""
            if 'thumbnail' in article and article['thumbnail']:
                if 'originalUrl' in article['thumbnail']:
                    thumbnail = article['thumbnail']['originalUrl']
                elif 'resolutions' in article['thumbnail'] and article['thumbnail']['resolutions']:
                    thumbnail = article['thumbnail']['resolutions'][0].get('url', '')
            
            sentiment = get_sentiment(title)
            
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    if thumbnail:
                        st.image(thumbnail, use_container_width=True)
                    else:
                        st.write("📰")
                with col2:
                    st.markdown(f"#### [{title}]({link})")
                    st.write(f"**{publisher}** | {pub_date}")
                    st.markdown(f"**Sentiment:** {sentiment}")
                st.markdown("---")
    else:
        st.info(f"No recent news found for {ticker_symbol}.")

if auto_refresh:
    time.sleep(60)
    st.rerun()