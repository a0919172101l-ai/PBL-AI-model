import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Lyle – Business Problem Solver",
    page_icon="💼",
    layout="centered"
)

# =========================================================
# CUSTOM STYLE
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">💼 Lyle – Business Problem Solver</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An AI assistant designed to analyze business problems and provide practical recommendations.'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# PURPOSE
# =========================================================

with st.expander("🎯 What does Lyle do?"):
    st.write(
        """
        Lyle is a Business AI assistant designed to help students and beginner
        business users understand and analyze business problems.

        It focuses on:
        • Marketing
        • Finance
        • Management
        • Operations
        • Business Strategy
        • Customer Problems
        • Business Decision-Making

        Instead of simply giving a short answer, Lyle analyzes the problem,
        identifies possible causes, and provides practical recommendations.
        """
    )

# =========================================================
# API KEY
# =========================================================

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error(
        "⚠️ GROQ_API_KEY is missing. "
        "Please add your Groq API key to Streamlit Secrets."
    )
    st.stop()

# =========================================================
# GROQ CLIENT
# =========================================================

try:
    client = Groq(api_key=api_key)
except Exception:
    st.error(
        "⚠️ The AI service could not be initialized. "
        "Please check your GROQ_API_KEY."
    )
    st.stop()

# =========================================================
# MODEL
# =========================================================

MODEL_NAME = "openai/gpt-oss-120b"

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Lyle, a Business Problem Solver.

Your purpose is to help students and beginner business users
understand and analyze BUSINESS problems.

You are NOT a general-purpose chatbot.

Your main areas are:
- Marketing
- Finance
- Management
- Operations
- Business strategy
- Customer problems
- Business decision-making
- Entrepreneurship
- Business ethics

IMPORTANT RULES:

1. Focus primarily on business-related questions.

2. If the user's question is unrelated to business,
politely explain that Lyle is designed for business problems
and ask the user to connect the question to a business situation.

3. Do not invent statistics, company financial data, market data,
or research results.

4. If the user does not provide enough information,
clearly state what information is missing.

5. Explain business concepts in clear and student-friendly language.

6. Do not pretend that you have real-time company or market data.

7. When appropriate, use simple business frameworks such as:
   - SWOT
   - PESTEL
   - 4Ps
   - Porter's Five Forces
   - Cost-benefit analysis
   - Risk analysis
   - Customer analysis

8. For a business problem, structure the answer using:

   Problem
   Possible Causes
   Business Analysis
   Possible Solutions
   Risks
   Recommendation

9. Give practical recommendations instead of only defining concepts.

10. If the user asks about investing or financial decisions,
provide educational analysis only and clearly explain that
the response is not professional financial advice.

11. Keep answers organized and easy for a high-school student
to understand.

12. You may answer in English or Chinese depending on the user's language.
"""

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.subheader("💡 Try a Business Question")

examples = [
    "Why are customers buying less from a company?",
    "How can a small business attract more customers?",
    "Use SWOT analysis to analyze Starbucks.",
    "How can a company reduce operating costs?",
    "Why might a company's sales decrease?",
    "How can a business improve customer satisfaction?"
]

cols = st.columns(2)

for i, example in enumerate(examples):
    if cols[i % 2].button(example, key=f"example_{i}"):
        st.session_state.pending_question = example

# =========================================================
# CLEAR CHAT
# =========================================================

if st.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

pending_question = st.session_state.pop("pending_question", None)

user_input = st.chat_input(
    "Describe your business problem..."
)

if pending_question:
    user_input = pending_question

# =========================================================
# AI RESPONSE
# =========================================================

if user_input:

    user_input = user_input.strip()

    if not user_input:
        st.warning("Please enter a business question.")
        st.stop()

    # Prevent extremely long input
    if len(user_input) > 4000:
        st.warning(
            "Your question is too long. "
            "Please keep it under 4,000 characters."
        )
        st.stop()

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare messages
    messages_for_api = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Keep recent conversation
    messages_for_api.extend(
        st.session_state.messages[-10:]
    )

    # Generate response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:

            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages_for_api,
                temperature=0.4,
                max_completion_tokens=1800
            )

            answer = completion.choices[0].message.content

            if not answer:
                answer = (
                    "I could not generate an answer. "
                    "Please try asking your business question again."
                )

            response_placeholder.markdown(answer)

            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            error_text = str(e).lower()

            if "401" in error_text or "authentication" in error_text:
                error_message = (
                    "🔐 **API authentication error**\n\n"
                    "The Groq API key is invalid or has not been configured correctly.\n\n"
                    "Please check `GROQ_API_KEY` in Streamlit Secrets."
                )

            elif "429" in error_text or "rate limit" in error_text:
                error_message = (
                    "⏳ **API rate limit reached**\n\n"
                    "The AI service is temporarily limiting requests. "
                    "Please wait a moment and try again."
                )

            elif "model" in error_text:
                error_message = (
                    "⚠️ **Model error**\n\n"
                    "The selected AI model may not be available. "
                    "Please check the model configuration."
                )

            else:
                error_message = (
                    "⚠️ **The AI could not generate a response.**\n\n"
                    "Please try again. If the problem continues, "
                    "check the Groq API key and Streamlit Secrets."
                )

            response_placeholder.error(error_message)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Lyle is a student business-analysis prototype. "
    "It uses an AI model to provide educational business analysis "
    "and may require additional real-world data for accurate decisions."
)
