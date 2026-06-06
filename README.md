# 🌍 City Agent

> An AI-powered city assistant that fetches real-time weather and latest news for any city — with a conversational chat interface powered by Mistral AI and LangChain Agents.


## 🖥️ Demo

<!-- Add your screenshots here -->
<!-- Place screenshot images in the same folder as this README -->

| Chat Interface | Weather & News Response |
|---|---|
| ![Screenshot 1](City%20Agent/Demo1.jpg) | ![Screenshot 2](City%20Agent/Demo2.jpg) |



---

## 🔍 What Is This?

**City Agent** is an AI agent that uses real-time tool calling to answer queries about any city. Ask it about the weather or latest news — the agent decides which tool to call, fetches live data from external APIs, and returns a natural language response.

It is available as both a **terminal CLI app** and a **Streamlit web chat interface**.

---

## ✨ Features

- **Real-Time Weather** — Fetches live temperature and weather conditions via OpenWeatherMap API
- **Latest News** — Retrieves top 3 current news stories for any city via Tavily Search API
- **LangChain Agent** — LLM autonomously decides which tool to call based on user query
- **Mistral AI LLM** — Powered by `mistral-small-2603` for fast, accurate responses
- **Streamlit Chat UI** — Full multi-turn conversation with persistent chat history
- **Human Approval Mode** — CLI version prompts for approval before each tool call
- **LangChain Runnables** — Query preprocessing via `RunnableLambda` before agent invocation
- **Custom Styling** — Dark-themed Streamlit UI with centered header and footer

---

## 🏗️ How It Works

```
User Query
    ↓
LangChain Agent (Mistral AI)
    ↓
Agent decides which tool to call
    ↓
    ├── get_weather(city)
    │       ↓
    │   OpenWeatherMap API
    │       ↓
    │   temp + description
    │
    └── get_news(city)
            ↓
        Tavily Search API
            ↓
        Top 3 news results
    ↓
Agent formats response
    ↓
Chat UI / Terminal Output
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Mistral AI (`mistral-small-2603`) |
| Agent Framework | LangChain `create_agent` |
| Weather API | OpenWeatherMap API |
| News Search | Tavily Search API |
| Query Processing | LangChain `RunnableLambda` |
| UI | Streamlit |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
City Agent/
├── Agents_UI.py          # Streamlit web chat interface (main entry point)
├── Agents.py             # CLI version with human approval before tool calls
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/harshit8204/RAG-book-assistant.git
cd "RAG-book-assistant/City Agent"
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install streamlit tavily-python requests rich
```

### 4. Set Up Environment Variables

Create a `.env` file inside the `City Agent/` folder:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Get your API keys:**
- Mistral AI → [console.mistral.ai](https://console.mistral.ai)
- OpenWeatherMap → [openweathermap.org/api](https://openweathermap.org/api) (free tier available)
- Tavily → [tavily.com](https://tavily.com) (free tier available)

---

## 🖥️ Usage

### Streamlit Web App

```bash
streamlit run Agents_UI.py
```

Open `http://localhost:8501` and start chatting:

```
You: What's the weather in Mumbai?
Bot: Weather in Mumbai: light rain, 28°C

You: Any news from Delhi?
Bot: Latest news in Delhi:
     - Title of article 1 ...
     - Title of article 2 ...
```

### CLI Mode (with Human Approval)

```bash
python Agents.py
```

Before each tool call, the agent asks for your approval:

```
Agent wants to call 'get_weather'. Approve? (yes/no): yes
Agent wants to call 'get_news'. Approve? (yes/no): yes

Bot: Weather in Bangalore: clear sky, 24°C
```

Type `exit` to quit.

---

## ⚙️ Key Implementation Details

**Tool Calling** — Each tool is decorated with `@tool` so LangChain's agent can discover and call them automatically based on the user's intent:

```python
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    ...

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    ...
```

**RunnableLambda Preprocessing** — The Streamlit version uses a LangChain Runnable to clean the query before passing it to the agent:

```python
query_runnable = RunnableLambda(preprocess_query)
processed_query = query_runnable.invoke(user_input)
```

**Human-in-the-Loop (CLI)** — The CLI version wraps tool calls with a human approval middleware, demonstrating agentic safety patterns.

---

## 📦 Core Dependencies

```
langchain
langchain-core
langchain-mistralai
langchain-community
streamlit
tavily-python
requests
python-dotenv
rich
```

---

## 👤 Author

**Harshit Pal** — [@harshit8204](https://github.com/harshit8204)
