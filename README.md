# Financial Chatbot: AI-Powered Investment Insights

This project introduces a Financial Chatbot designed to empower investors—both beginners and experienced—with real-time stock insights, investment analytics, and financial knowledge through an intuitive conversational interface. The chatbot integrates NLP, machine learning, financial APIs, and time-series forecasting to help users make informed decisions efficiently.

---

## Objective

To develop a conversational AI tool that:

- Understands user queries about stocks and investing
- Delivers real-time financial data and market trends
- Offers investment analytics like P/E ratios, earnings analysis, and sentiment trends
- Supports financial literacy by answering beginner-level investment questions
- Provides an intuitive and accessible user interface for seamless user interaction

---

## Key Features and Use Cases

### 1. **Stock Price Trend Analysis**
- Provides historical stock prices through interactive time-series plots
- Helps users identify bullish/bearish trends, volatility, and long-term growth
- Assists traders in spotting entry/exit points using trend visualization

### 2. **Earnings Report Analysis**
- Displays earnings dates and recent earnings summaries
- Helps users assess market movement post-earnings
- Example: NVIDIA's stock rose 15% after a strong earnings call in 2024

### 3. **P/E Ratio Comparison**
- Calculates and compares P/E ratios across companies and sectors
- Indicates under/over-valued stocks
- Helps users determine valuation in context of financial health and growth

### 4. **Real-Time Financial News**
- Aggregates breaking financial news from Yahoo Finance API
- Tracks announcements, monetary policy shifts, and macroeconomic signals
- Offers insights into market-impacting events

### 5. **Beginner-Friendly Financial Education**
- Explains core investment concepts like stocks vs. bonds, bullish/bearish trends
- Tailors responses to new users with simple, understandable language

---

## Technical Architecture

### NLP & AI Techniques

- **Large Language Model (LLM)**: OpenAI’s GPT API is used for natural, contextual responses
- **Retrieval-Augmented Generation (RAG)**: Enhances accuracy by retrieving financial data before generating answers
- **Multi-Agent System**: Routes user queries to specialized task agents (e.g., news agent, earnings agent, P/E agent)

### Forecasting & Analysis

- **Machine Learning Models**:
  - ARIMA, LSTM, and Transformer-based models for time-series trend forecasting
  - Sentiment analysis using social media/news text
  - Feature extraction (volatility, volume, technical indicators)

### Data Integration

- **Primary Source**: Yahoo Finance API
- **Data Pulled**: Real-time prices, earnings reports, historical stock data, market news
- **Future Integrations**: SEC filings, macroeconomic indicators, alternative data sources

---

## Front-End (User Interface)

- **Framework**: Built with [Streamlit](https://streamlit.io/)
- Clean, minimalist chat interface
- Real-time interaction via typing simulation (`time.sleep`)
- Persistent conversation using session state
- Emoji-based enhancements for UX (toggle-able in production)

---

## Back-End & System Design

- GPT-3.5/4 agent-based routing system
- Custom agents for:
  - Stock data retrieval
  - News parsing
  - Earnings report summary
  - Ratio calculations
  - General financial literacy
- Uses prompt templates for consistent and robust responses
- Handles routing ambiguity and malformed queries gracefully

---

## Evaluation and Testing

### Performance Metrics
- **Inquiry Classification Accuracy**: ~92% correctly routed
- **Data Retrieval Accuracy**: ~96% correct financial data pulled
- **Response Time**: ~10–20 seconds average (ongoing optimization)
- **Relevance Scoring**: Manual evaluation for alignment with query intent

### Robustness Measures
- Hallucination mitigation via answer constraints
- Confidence scoring on sentiment/forecast predictions
- Feedback loops for user corrections (under development)

---

## Future Enhancements

1. **Multi-Stock Comparison Graphs**  
   - Visualize multiple stock trends side by side

2. **Earnings Call Summarization**  
   - Extract key financial statements from transcripts: revenue, guidance, YoY metrics

3. **Purchase Volume Analysis**  
   - Gauge investor interest through real-time volume and momentum tracking

4. **API Expansion**  
   - Incorporate macroeconomic and alternative data (e.g., Reddit, SEC filings)

---

## Example Prompts

What’s the latest news on Microsoft?
Show me Tesla’s price trend for the last 6 months.
Is Google’s P/E ratio high compared to Apple?
When is Nvidia’s next earnings report?
What’s the difference between stocks and bonds?

---

## Technologies Used

- **Languages**: Python
- **Libraries**: Streamlit, yfinance, NumPy, Pandas, scikit-learn, Plotly
- **AI Models**: GPT (OpenAI API), ARIMA, LSTM
- **NLP Tools**: NLTK, TextBlob, Regex, Transformers
- **Deployment Tools**: Streamlit Sharing / AWS (optional)

---

## Contributors

- **Sorasak Joshi**  
- Dylan Lee, Yiwei Lu, Qui Nguyen, Jerry Zhu  
