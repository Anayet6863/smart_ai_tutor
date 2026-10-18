import streamlit as st
from dotenv import load_dotenv
from chatbot import build_chatbot
from schemas import ChatbotResponse

load_dotenv()

st.set_page_config(
    page_title="Smart AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(ellipse at 12% 0%, rgba(67,97,238,.13), transparent 36%),
                    radial-gradient(ellipse at 92% 8%, rgba(167,139,250,.10), transparent 32%),
                    #0b1020;
        color: #e8eefb;
    }
    [data-testid="stHeader"] { background: rgba(11,16,32,.75); }
    [data-testid="stSidebar"] { background: #0e1628; border-right: 1px solid rgba(148,163,184,.18); }
    .brand-row { display:flex; align-items:center; gap:12px; margin:.2rem 0 .4rem; }
    .brand-icon { display:flex; align-items:center; justify-content:center; width:46px; height:46px;
        border-radius:15px; background:linear-gradient(135deg,#6888ff,#a78bfa); color:white; font-size:24px; }
    .brand-title { font-size:1.18rem; font-weight:750; color:#f5f7ff; }
    .brand-subtitle { font-size:.79rem; color:#9aa9c2; margin-top:3px; }
    .hero { text-align:center; padding:3rem 1rem 1.5rem; }
    .hero-pill { display:inline-block; padding:6px 12px; border-radius:999px;
        border:1px solid rgba(124,156,255,.3); background:rgba(124,156,255,.09);
        color:#c6d3ff; font-size:.82rem; margin-bottom:1rem; }
    .hero h1 { font-size:clamp(2rem,4vw,3.2rem); letter-spacing:-.045em; line-height:1.12;
        margin:0; color:#f5f7ff; font-weight:800; }
    .hero h1 span { background:linear-gradient(90deg,#8ca9ff,#c4a7ff);
        -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero p { max-width:620px; margin:1rem auto 0; color:#a8b5ce; font-size:1rem; line-height:1.7; }
    .section-label { color:#a8b5ce; font-size:.82rem; font-weight:650; letter-spacing:.08em;
        text-transform:uppercase; margin:1.4rem 0 .65rem; }
    .suggestion-note { color:#a8b5ce; font-size:.9rem; text-align:center; margin-bottom:.8rem; }
    div[data-testid="stChatMessage"] { border:1px solid rgba(148,163,184,.13); border-radius:18px;
        padding:.8rem 1rem; margin-bottom:.8rem; background:rgba(17,26,46,.72); }
    div[data-testid="stChatInput"] { border-color:rgba(148,163,184,.25); border-radius:18px; }
    .sidebar-note { color:#9aa9c2; font-size:.86rem; line-height:1.6; }
    .sidebar-footer { color:#71819d; font-size:.75rem; line-height:1.5; padding-top:1rem;
        border-top:1px solid rgba(148,163,184,.18); margin-top:1rem; }
    .stButton > button { border-radius:12px; transition:all .15s ease; }
    .stButton > button:hover { border-color:rgba(124,156,255,.7); color:#dbe5ff; }
    #MainMenu { visibility:hidden; } footer { visibility:hidden; }
    @media (max-width:700px) { .hero { padding-top:1.6rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""

with st.sidebar:
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-icon">🎓</div>
            <div><div class="brand-title">Smart AI Tutor</div>
            <div class="brand-subtitle">Your learning companion</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("### Your workspace")
    st.markdown(
        '<div class="sidebar-note">Ask questions, explore concepts, '
        'and learn step by step with your AI tutor.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if st.button("＋  New conversation / Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = ""
        st.rerun()
    st.divider()
    st.markdown("### How I can help with")
    st.markdown(
        '<div class="sidebar-footer">Built with Streamlit, LangChain, Groq, and Pydantic.<br>',
        unsafe_allow_html=True,
    )

try:
    chatbot = build_chatbot()
except Exception as exc:
    st.error("The chatbot could not be initialized.")
    st.warning("Check your again,Something is wrong.")
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()

if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-pill">Your personal AI learning space</div>
            <h1>Learn something <span>new today.</span></h1>
            <p>Try math problems, ask a question
            and take the next step in your learning journey.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-label" style="text-align:center;">Start with a suggestion</div>', unsafe_allow_html=True)
    st.markdown('<div class="suggestion-note">Choose a topic below, or type your own question.</div>', unsafe_allow_html=True)

    left, middle, right = st.columns(3, gap="medium")
    with left:
        with st.container(border=True):
            st.markdown("### Programming")
            st.caption("Learn concepts and understand code.")
            if st.button("Explain Python functions", key="suggest_programming", use_container_width=True):
                st.session_state.pending_prompt = "Explain Python functions with a simple example."
                st.rerun()
    with middle:
        with st.container(border=True):
            st.markdown("### Mathematics")
            st.caption("Work through a problem step by step.")
            if st.button("Solve a quadratic equation", key="suggest_math", use_container_width=True):
                st.session_state.pending_prompt = "Solve x^2 - 5x + 6 = 0 step by step."
                st.rerun()
    with right:
        with st.container(border=True):
            st.markdown("###  General learning")
            st.caption("Explore ideas and everyday questions.")
            if st.button("How does memory work?", key="suggest_general", use_container_width=True):
                st.session_state.pending_prompt = "Explain how human memory works in beginner-friendly language."
                st.rerun()
else:
    st.markdown("## Your conversation")
    st.caption("Ask a follow-up question whenever you're ready.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

typed_prompt = st.chat_input("Message your AI tutor...")
user_input = typed_prompt or st.session_state.pending_prompt

if user_input:
    st.session_state.pending_prompt = ""
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking through your question..."):
            try:
                result: ChatbotResponse = chatbot.invoke({"question": user_input})
            
                st.markdown(result.answer)
                st.session_state.messages.append({"role": "assistant", "content": result.answer})
            except Exception as exc:
                st.error("Sorry, I couldn't complete that request. Check your connection, Groq API key, model availability, and API limits.")
                with st.expander("Technical details"):
                    st.code(str(exc))
