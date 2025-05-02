import streamlit as st
import yfinance as yf
import requests
import datetime
from rapidfuzz import process
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

NEWS_API_KEY = "0188884d6ae14c748f2eb7ac2c93db56"
ALPHA_VANTAGE_KEY = "EO6OGF7HGY44HOZK"

SYMBOLS = {
    "apple": "AAPL", "tesla": "TSLA", "google": "GOOGL",
    "microsoft": "MSFT", "nvidia": "NVDA", "alibaba": "BABA",
    "nio": "NIO", "sp500": "SPY", "nasdaq": "QQQ", "dowjones": "^DJI"
}

def show_prompt_menu():
    st.sidebar.title("📝 What to ask?")
    st.sidebar.markdown("""
- Greeting
- Apple price
- Tesla 5 year trend
- Nvidia news
- Compare AAPL and MSFT 
stream
(This feature is maintaining)
- Show me AAPL 3 year trend
- AAPL financials

--------

- Tell me a joke
- Who created you?
- What can you do?
    """)

def get_best_match(word):
    all_symbols = list(SYMBOLS.keys()) + list(SYMBOLS.values())
    match, score, _ = process.extractOne(word.lower(), all_symbols)
    return SYMBOLS.get(match.lower(), match.upper()) if score > 60 else None

def extract_symbols_for_compare(user_input):
    words = user_input.replace(",", " ").replace("&", "and").split()
    symbols = [get_best_match(word) for word in words]
    return [sym for sym in symbols if sym]

def get_current_price(symbol):
    try:
        price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
        return f"${price:.2f}"
    except:
        return "Price unavailable."

def get_stock_trend(symbol, period="1y"):
    end = datetime.date.today()
    days = {"1y": 365, "3y": 3*365, "5y": 5*365}
    start = end - datetime.timedelta(days=days.get(period, 365))
    data = yf.download(symbol, start=start, end=end)
    return data['Close'] if not data.empty else None

def get_stock_news(symbol):
    url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get('articles', [])
    return articles[:5]

def analyze_sentiment(news_list):
    scores = [sia.polarity_scores(article['title'])['compound'] for article in news_list]
    avg_score = sum(scores) / len(scores) if scores else 0
    if avg_score > 0.05:
        return "😊 Positive"
    elif avg_score < -0.05:
        return "😟 Negative"
    else:
        return "😐 Neutral"

def get_alpha_vantage_financials(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    response = requests.get(url).json()
    if "PERatio" in response:
        pe = response.get("PERatio", "N/A")
        eps = response.get("EPS", "N/A")
        return f"📊 {symbol} Financials: PE Ratio: {pe}, EPS: {eps}"
    else:
        return f"⚠️ Failed to fetch financials for {symbol}."

def detect_intent(user_input):
    lower = user_input.lower()
    if any(kw in lower for kw in ["hi", "hello", "hey"]):
        return "greeting"
    elif "price" in lower:
        return "price"
    elif "trend" in lower or "history" in lower:
        return "trend"
    elif "news" in lower:
        return "news"
    elif "compare" in lower and ("and" in lower or "with" in lower or "&" in lower):
        return "compare"
    elif "financials" in lower or "pe ratio" in lower:
        return "financials"
    elif "who made you" in lower or "who created you" in lower:
        return "creator"
    elif "joke" in lower:
        return "joke"
    elif "what can you do" in lower:
        return "capability"
    else:
        return "unknown"

def compare_stocks(symbol1, symbol2):
    try:
        trend1 = yf.Ticker(symbol1).history(period="1y")['Close']
        trend2 = yf.Ticker(symbol2).history(period="1y")['Close']
        change1 = (trend1.iloc[-1] - trend1.iloc[0]) / trend1.iloc[0] * 100
        change2 = (trend2.iloc[-1] - trend2.iloc[0]) / trend2.iloc[0] * 100
        return f"📊 Comparing {symbol1} vs {symbol2}\n1-Year Change: {change1:.2f}% vs {change2:.2f}%"
    except:
        return "⚠️ Failed to compare these stocks."

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Financial ChatBot")
show_prompt_menu()

user_input = st.chat_input("Ask me anything about stocks...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    intent = detect_intent(user_input)
    symbols = extract_symbols_for_compare(user_input) if intent == "compare" else [get_best_match(word) for word in user_input.split()]
    symbols = [sym for sym in symbols if sym]

    reply = ""

    if intent == "greeting":
        reply = "👋 Hi there! Ready to explore the market?"
    elif intent == "price" and symbols:
        reply = f"📊 {symbols[0]} Price: {get_current_price(symbols[0])}"
    elif intent == "trend" and symbols:
        period = "5y" if "5 year" in user_input else "3y" if "3 year" in user_input else "1y"
        trend_data = get_stock_trend(symbols[0], period)
        reply = f"📈 {symbols[0]} Trend ({period})"
        st.session_state.chat_history.append(("bot", reply))
        st.session_state.chat_history.append(("bot_chart", trend_data))
    elif intent == "news" and symbols:
        news_articles = get_stock_news(symbols[0])
        sentiment = analyze_sentiment(news_articles)
        news_text = "\n".join([f"- {article['title']} ({article['source']['name']})" for article in news_articles])
        reply = f"📰 {symbols[0]} News:\n{news_text}\n\nSentiment: {sentiment}"
    elif intent == "financials" and symbols:
        reply = get_alpha_vantage_financials(symbols[0])
    elif intent == "compare" and len(symbols) == 2:
        reply = compare_stocks(symbols[0], symbols[1])
    elif intent == "creator":
        reply = "🤖 I was proudly created by Yiwei Lu!"
    elif intent == "joke":
        reply = random.choice(["Why did the stock split? It couldn't handle the pressure!", "Why do traders love nature? Bull and bear markets!"])
    elif intent == "capability":
        reply = "📚 I can provide stock prices, trends, news, financials, comparisons, and more!"
    else:
        reply = "🤖 Sorry, I didn't understand. Check the sidebar for ideas!"

    st.session_state.chat_history.append(("bot", reply))

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        if role == "bot_chart":
            st.line_chart(message)
        else:
            st.markdown(message)