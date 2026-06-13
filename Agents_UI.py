import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="City Agent",
    page_icon="🌍",
    layout="wide"
)

from dotenv import load_dotenv
import os
import requests

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain_core.runnables import RunnableLambda

# =========================
# Custom Styling
# =========================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.title {
    text-align:center;
    font-size:3rem;
    font-weight:bold;
    color:#4F8BF9;
}

.subtitle {
    text-align:center;
    color:#808080;
    font-size:1.1rem;
    margin-bottom:2rem;
}

.footer {
    text-align:center;
    color:gray;
    margin-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Weather Tool
# =========================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# =========================
# News Tool
# =========================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"- {title}\n\n🔗 {url}\n\n📝 {snippet[:100]}..."
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# =========================
# Runnable
# =========================

def preprocess_query(query: str) -> str:
    return query.strip()

query_runnable = RunnableLambda(preprocess_query)

# =========================
# LLM + Agent
# =========================

llm = ChatMistralAI(
    model="mistral-small-2603"
)

agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="You are a helpful city assistant."
)

# =========================
# Header
# =========================

st.markdown(
    "<div class='title'>🌍 City Agent</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Weather & News Assistant powered by Mistral AI</div>",
    unsafe_allow_html=True
)

# =========================
# Session State
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Display Chat History
# =========================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# User Input
# =========================

user_input = st.chat_input(
    "Ask about any city..."
)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Fetching information..."):

            processed_query = query_runnable.invoke(
                user_input
            )

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": processed_query
                        }
                    ]
                }
            )

            response = result["messages"][-1].content

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

# =========================
# Footer
# =========================

st.markdown("---")

st.markdown(
    "<div class='footer'>Built with LangChain • Runnables • Mistral AI • Tavily • OpenWeather</div>",
    unsafe_allow_html=True
)