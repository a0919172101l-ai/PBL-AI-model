import streamlit as st
from openai import OpenAI


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Lyle – AI Business & Finance Study Assistant",
    page_icon="📚",
    layout="centered"
)


# ==========================================
# OPENAI CONNECTION
# ==========================================

try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    client = None


# ==========================================
# TITLE
# ==========================================

st.title("📚 Lyle – AI Business & Finance Study Assistant")

st.write(
    "An AI study assistant designed to help high-school students "
    "understand business and finance concepts."
)

st.info(
    "This AI focuses on Business & Finance learning. "
    "It is not a general-purpose chatbot."
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("📖 Study Topics")

    topic = st.selectbox(
        "Choose a topic",
        [
            "General Business",
            "Economics",
            "Finance",
            "Business Ethics",
            "PESTEL Analysis",
            "Investment Basics",
            "Business Strategy"
        ]
    )

    difficulty = st.selectbox(
        "Explanation Level",
        [
            "Simple",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.write("### 🎯 What Lyle can do")

    st.write("• Explain business concepts")
    st.write("• Give real-world examples")
    st.write("• Analyze business problems")
    st.write("• Create practice questions")
    st.write("• Explain finance concepts")
    st.write("• Help students understand mistakes")

    st.divider()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


# ==========================================
# AI INSTRUCTIONS
# ==========================================

SYSTEM_PROMPT = f"""
You are Lyle, an AI Business and Finance Study Assistant.

Your specific purpose is to help high-school students learn
Business, Economics, and Finance.

You are NOT a general-purpose chatbot.

Main areas you should help with:

1. Business
2. Economics
3. Finance
4. Business Ethics
5. PESTEL Analysis
6. Investment Basics
7. Business Strategy

The student's selected topic is:
{topic}

The student's preferred difficulty level is:
{difficulty}

IMPORTANT RULES:

- Stay mainly within Business, Economics, and Finance education.
- If the user asks something unrelated, politely explain that
  you are designed for Business and Finance learning.
- Explain difficult concepts using simple language when appropriate.
- Give real-world business examples.
- Break difficult problems into steps.
- When useful, use tables or bullet points.
- Do not simply give an answer to academic questions.
  Explain the reasoning so the student can learn.
- For calculations, show the important steps.
- For investment questions, provide educational information,
  not personalized financial advice.
- For current financial information, explain that information
  may change over time.
- Do not invent facts or sources.
- If you are uncertain, say that you are uncertain.

Your goal is to help the student UNDERSTAND business and finance,
not simply provide answers.
"""


# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# EXAMPLE QUESTIONS
# ==========================================

if len(st.session_state.messages) == 0:

    st.subheader("💡 Try asking:")

    examples = [
        "What is PESTEL analysis?",
        "Explain opportunity cost with a business example.",
        "What is the difference between revenue and profit?",
        "Why is business ethics important?",
        "How does inflation affect businesses?",
        "Explain P/E ratio in simple English."
    ]

    for example in examples:
        st.write("• " + example)


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# USER INPUT
# ==========================================

user_input = st.chat_input(
    "Ask Lyle a Business or Finance question..."
)


# ==========================================
# AI RESPONSE
# ==========================================

if user_input:

    if client is None:

        st.error(
            "OpenAI API key is missing. "
            "Please add OPENAI_API_KEY to Streamlit Secrets."
        )

        st.stop()


    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Display user message

    with st.chat_message("user"):
        st.markdown(user_input)


    # Prepare conversation

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(
        st.session_state.messages
    )


    # Generate answer

    with st.chat_message("assistant"):

        with st.spinner("Lyle is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="gpt-5-mini",
                    messages=messages,
                    temperature=0.3
                )

                answer = response.choices[0].message.content

                st.markdown(answer)


                # Save response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "Lyle could not generate a response."
                )

                st.caption(str(e))
