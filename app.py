import streamlit as st
from openai import OpenAI


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Lyle – AI Finance Assistant",
    page_icon="💰",
    layout="wide"
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
# CUSTOM STYLE
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 30px;
    }

    .card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">💰 Lyle – AI Finance Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An AI-powered finance learning and analysis assistant for students.'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "🎯 Lyle focuses on Finance, Investing, Economics, "
    "and Financial Literacy — not general-purpose questions."
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("📚 Finance Tools")

    mode = st.selectbox(
        "Choose a Finance Mode",
        [
            "📖 Finance Learning",
            "📊 Stock Analysis",
            "📈 Investment Analysis",
            "💰 Personal Finance",
            "🧮 Financial Calculations",
            "⚖️ Risk Analysis",
            "💼 Company Analysis"
        ]
    )

    difficulty = st.selectbox(
        "Explanation Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.subheader("💡 Topics")

    st.write("📈 Stocks & ETFs")
    st.write("📊 Financial Ratios")
    st.write("💰 Personal Finance")
    st.write("📉 Risk & Return")
    st.write("🏢 Company Analysis")
    st.write("🌎 Economics")
    st.write("🧮 Compound Interest")
    st.write("💼 Investment Strategy")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# ==========================================
# AI SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = f"""
You are Lyle, an AI Finance Learning and Analysis Assistant.

Your specific purpose is to help students understand finance,
investing, economics, and financial literacy.

You are NOT a general-purpose chatbot.

The user's selected mode is:

{mode}

The user's preferred difficulty level is:

{difficulty}

==================================================
MAIN AREAS
==================================================

You should mainly help with:

1. Financial literacy
2. Stocks
3. ETFs
4. Company analysis
5. Financial ratios
6. Investment concepts
7. Risk and return
8. Compound interest
9. Personal finance
10. Economics
11. Portfolio diversification
12. Business finance

==================================================
FINANCIAL RATIO EDUCATION
==================================================

You can explain:

- P/E ratio
- Forward P/E
- PEG ratio
- ROE
- ROA
- Profit margin
- Debt-to-equity ratio
- Current ratio
- Quick ratio
- EPS
- Dividend yield
- Free cash flow

When explaining a financial ratio:

1. Define it.
2. Explain what it measures.
3. Explain why investors may care about it.
4. Give a simple example.
5. Explain its limitations.

Do NOT assume that a higher or lower number is always better.

==================================================
STOCK AND COMPANY ANALYSIS
==================================================

When analyzing a company, consider:

- Revenue
- Profit
- Profit margin
- EPS
- P/E
- Growth
- ROE
- ROA
- Debt
- Cash flow
- Competitive advantages
- Industry conditions
- Risks

Organize analysis into:

1. Company overview
2. Financial performance
3. Valuation
4. Growth
5. Risks
6. Strengths
7. Weaknesses
8. Overall educational conclusion

Do not guarantee future stock performance.

==================================================
INVESTMENT ANALYSIS
==================================================

When discussing an investment:

Explain:

- Potential return
- Potential risks
- Volatility
- Diversification
- Time horizon
- Risk tolerance

Never tell the user that an investment is guaranteed to make money.

Use phrases such as:

"From an educational perspective..."

"This may suggest..."

"One possible risk is..."

==================================================
PERSONAL FINANCE
==================================================

You can help explain:

- Budgeting
- Saving
- Investing
- Emergency funds
- Compound interest
- Long-term investing
- Diversification

Focus on financial education rather than personalized financial advice.

==================================================
CALCULATIONS
==================================================

For financial calculations:

1. Show the formula.
2. Explain the variables.
3. Calculate step by step.
4. Explain the result in simple language.

==================================================
IMPORTANT SAFETY RULES
==================================================

You are an educational finance assistant.

Do not promise investment returns.

Do not claim that a stock will definitely rise or fall.

Do not present educational information as professional
financial advice.

If the user asks for a specific investment decision,
explain both potential benefits and risks.

For current stock prices or financial news, explain that
financial information can change over time and should be
verified using reliable current sources.

==================================================
OUT-OF-SCOPE QUESTIONS
==================================================

If the user asks about something completely unrelated to
finance, politely say:

"I am Lyle, a finance-focused AI assistant. I am designed
to help with finance, investing, economics, and financial
literacy questions."

Then redirect the user toward a finance-related question.

==================================================
MAIN GOAL
==================================================

Your goal is not simply to give answers.

Your goal is to help students DEVELOP FINANCIAL THINKING.

Explain:

WHY something happens,
HOW to analyze it,
and WHAT limitations the analysis has.
"""


# ==========================================
# INITIALIZE CHAT
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# WELCOME SCREEN
# ==========================================

if len(st.session_state.messages) == 0:

    st.subheader("👋 Welcome to Lyle")

    st.write(
        "Lyle helps students learn finance and understand "
        "investment concepts through AI-powered explanations."
    )

    st.markdown("### 💡 Try asking:")

    examples = [
        "What does the P/E ratio tell investors?",
        "Explain ROE in simple English.",
        "What is the difference between an ETF and a stock?",
        "How does compound interest work?",
        "Why is diversification important?",
        "How can I analyze a company's financial health?",
        "What are the risks of investing in technology stocks?"
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
    "Ask Lyle a finance question..."
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


    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner("Lyle is analyzing..."):

            try:

                response = client.chat.completions.create(
                    model="gpt-5-mini",
                    messages=messages,
                    temperature=0.2
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
