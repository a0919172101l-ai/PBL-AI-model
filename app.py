import streamlit as st
from openai import OpenAI


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Service Assistant",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# OpenAI Client
# -----------------------------

try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    client = None


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .feature-box {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
        background-color: #fafafa;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">🤖 AI Service Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An AI assistant designed to help people solve a wide range of problems.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    model = st.selectbox(
        "AI Model",
        [
            "gpt-5-mini",
            "gpt-5"
        ]
    )

    st.divider()

    st.subheader("💡 What can I help with?")

    st.write("📚 School & Learning")
    st.write("💼 Business")
    st.write("💰 Finance")
    st.write("✍️ Writing")
    st.write("🌎 Translation")
    st.write("🧠 Problem Solving")
    st.write("💡 Ideas & Planning")
    st.write("💻 Coding")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -----------------------------
# System Prompt
# -----------------------------

SYSTEM_PROMPT = """
You are an AI Service Assistant.

Your purpose is to help people solve a wide range of problems.

You should:

1. Understand the user's problem before answering.
2. Give practical, clear, and useful solutions.
3. Break difficult problems into smaller steps.
4. Explain complicated ideas in simple language when appropriate.
5. Give examples when they help understanding.
6. If the user asks for writing, provide a polished answer.
7. If the user asks for coding, provide working code and explain how to use it.
8. If the user asks a math or academic question, explain the reasoning clearly.
9. If there are multiple possible solutions, compare them.
10. If you do not know something, say so instead of inventing information.
11. Never claim that you can solve literally every problem.
12. For medical, legal, financial, or other high-risk issues, provide general information
    and recommend consulting a qualified professional when appropriate.

Always prioritize accuracy, safety, clarity, and usefulness.
"""


# -----------------------------
# Initialize Chat History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Welcome Screen
# -----------------------------

if len(st.session_state.messages) == 0:

    st.markdown("### 👋 Welcome!")

    st.write(
        "Tell me your problem and I will try to help you find a solution."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="feature-box">
            <h4>📚 Learn</h4>
            Get help with school subjects and difficult concepts.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-box">
            <h4>💼 Business</h4>
            Analyze business ideas, strategies, and problems.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-box">
            <h4>✍️ Create</h4>
            Write, rewrite, summarize, and organize information.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="feature-box">
            <h4>💻 Build</h4>
            Get help with programming and technology.
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# Display Previous Messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------
# User Input
# -----------------------------

user_input = st.chat_input(
    "What problem can I help you solve?"
)


# -----------------------------
# Process User Message
# -----------------------------

if user_input:

    # Check API key
    if client is None:

        st.error(
            "OpenAI API key is missing. "
            "Please add OPENAI_API_KEY to Streamlit Secrets."
        )

        st.stop()


    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)


    # Prepare messages for AI
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(
        st.session_state.messages
    )


    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.chat.completions.create(
                    model=model,
                    messages=messages
                )

                answer = response.choices[0].message.content

                st.markdown(answer)


                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "Sorry, something went wrong."
                )

                st.caption(
                    f"Error: {str(e)}"
                )
