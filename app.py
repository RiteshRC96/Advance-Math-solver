import asyncio
import nest_asyncio
import streamlit as st
import sympy
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import plotly.graph_objs as go
from langchain_groq import ChatGroq

# ==============================
#      CONFIGURATION
# ==============================
GROQ_API_KEY = "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"

# ==============================
#    SYSTEM PROMPT
# ==============================
SYSTEM_PROMPT = """
your name is Ritesh who is mathematics expert and advanced mathematics tutor and problem solver, capable of handling any math question—from basic arithmetic to advanced calculus, 
graph analysis, and beyond. Your answers must be clear, step-by-step, and use LaTeX for all mathematical notation. Maintain a warm, 
helpful tone with occasional light emojis, but keep the focus on delivering well-structured solutions.

**keep in mind:-
1. if user ask the name then only give the name not more information about you only give name and greatings
2. use various emojies between the conversion.
"""

# ==============================
#    INITIAL SETUP
# ==============================
nest_asyncio.apply()

st.set_page_config(page_title="EasyStep Math", page_icon="🧮", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
.sidebar .sidebar-content {
    background-color: #0f172a;
    color: white;
}
.block-container {
    padding: 2rem 4rem;
}
.chat-box {
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 1rem;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
}
.chat-box.user {
    border-left: 5px solid #6366f1;
    background-color: #334155;
    color: white;
}
.chat-box.assistant {
    border-left: 5px solid #10b981;
    background-color: #1e293b;
    color: white;
}
</style>

""", unsafe_allow_html=True)

# ==============================
#    SIDEBAR - CHAT HISTORY
# ==============================
with st.sidebar:
    st.title("🧠 Advance Math Solver")
    st.markdown("Your friendly AI math tutor ✨")

    st.markdown("---")
    st.subheader("🧾 Chat History")
    if "chat_history" in st.session_state and st.session_state["chat_history"]:
        user_queries = [item["content"] for item in st.session_state["chat_history"] if item["role"] == "user"]
        if user_queries:
            for i, q in enumerate(user_queries[::-1], 1):
                st.markdown(f"**{i}.** {q}")
        else:
            st.info("No questions yet.")
    else:
        st.info("Start by asking a math question below.")

    if st.button("🆕 New Chat"):
        st.session_state.pop("chat_history", None)
        st.rerun()


# ==============================
#    MAIN INTERFACE
# ==============================
st.title("🧮 Advance Math Solver")
st.markdown("Type your math question below and I'll solve it step-by-step. 🤓")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state["chat_history"]:
    with st.container():
        role_class = "user" if msg["role"] == "user" else "assistant"
        st.markdown(f"<div class='chat-box {role_class}'><strong>{msg['role'].capitalize()}</strong>:<br>{msg['content']}</div>", unsafe_allow_html=True)

user_input = st.chat_input("Ask your math question here...")

if user_input and user_input.strip():
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    with st.container():
        st.markdown(f"<div class='chat-box user'><strong>You</strong>:<br>{user_input}</div>", unsafe_allow_html=True)

    with st.spinner("Solving your question..."):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state["chat_history"]

        llm = ChatGroq(
            temperature=0.7,
            groq_api_key=GROQ_API_KEY,
            model_name="llama3-8b-8192"
        )

        try:
            response = asyncio.run(llm.ainvoke(messages))
            assistant_response = response.content
        except Exception as e:
            assistant_response = f"❌ Error: {str(e)}"

    st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
    with st.container():
        st.markdown(f"<div class='chat-box assistant'><strong>Assistant</strong>:<br>{assistant_response}</div>", unsafe_allow_html=True)
