import streamlit as st
import sqlite3
import tempfile

from lib.ingestion_pipeline import ingestion_pipeline
from lib.backend import backend_pipeline

st.set_page_config(
    page_title="QueryGenie",
    page_icon="🧞",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F7F6F3 !important;
    color: #1A1A1A;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3rem 4rem 3rem !important;
    max-width: 1200px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #EFEDE9 !important;
    border-right: 1px solid #E2E0DB !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.25rem !important;
}

/* ── Wordmark ── */
.qg-wordmark {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.25rem;
}
.qg-wordmark h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: #1A1A1A;
    margin: 0;
    line-height: 1;
}
.qg-wordmark span.accent { color: #4F46E5; }
.qg-tagline {
    font-size: 0.875rem;
    color: #6B7280;
    margin-bottom: 2rem;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.01em;
}
.qg-divider {
    border: none;
    border-top: 1px solid #E2E0DB;
    margin: 1.5rem 0;
}

/* ── Sidebar step card ── */
.step-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 0.75rem 0.9rem;
    border-radius: 10px;
    margin-bottom: 0.6rem;
    background: transparent;
    transition: background 0.15s;
}
.step-card.active {
    background: #EEF2FF;
}
.step-card.done {
    background: #F0FDF4;
}
.step-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
    background: #E2E0DB;
    color: #6B7280;
}
.step-card.active .step-num {
    background: #4F46E5;
    color: #fff;
}
.step-card.done .step-num {
    background: #16A34A;
    color: #fff;
}
.step-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #6B7280;
    line-height: 1.35;
}
.step-card.active .step-text { color: #3730A3; }
.step-card.done .step-text  { color: #15803D; }
.step-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.73rem;
    color: #9CA3AF;
    margin-top: 2px;
    font-weight: 400;
}
.step-card.active .step-sub { color: #6366F1; }
.step-card.done .step-sub   { color: #4ADE80; }

/* ── Sidebar section heading ── */
.sb-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #B0ABA3;
    margin: 1.5rem 0 0.6rem 0.2rem;
}

/* ── Sidebar info chip ── */
.sb-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #4B5563;
    background: #E9E6E0;
    border-radius: 6px;
    padding: 0.25rem 0.6rem;
    margin-bottom: 0.35rem;
}

/* ── Upload Zone ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #C4C0B8 !important;
    border-radius: 12px !important;
    background: #FDFCFB !important;
    padding: 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #4F46E5 !important;
}

/* ── Labels ── */
.qg-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 0.5rem;
}

/* ── Query textarea ── */
[data-testid="stTextArea"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    background: #FDFCFB !important;
    border: 1.5px solid #E2E0DB !important;
    border-radius: 10px !important;
    padding: 0.875rem 1rem !important;
    color: #1A1A1A !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    resize: vertical !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
    outline: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

/* ── Primary button ── */
[data-testid="stButton"] > button {
    background: #4F46E5 !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.625rem 1.75rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stButton"] > button:hover {
    background: #4338CA !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Code block ── */
[data-testid="stCode"] {
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #E2E0DB !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
}

/* ── DB badge ── */
.qg-db-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EEF2FF;
    color: #4338CA;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 1.5rem;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: #F0FDF4 !important;
    color: #15803D !important;
    border: 1.5px solid #86EFAC !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    border-radius: 8px !important;
    transition: background 0.15s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #DCFCE7 !important;
}

h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    color: #1A1A1A !important;
    letter-spacing: -0.02em !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.2rem">
        <span style="font-size:1.4rem">🧞</span>
        <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                     font-size:1.1rem;letter-spacing:-0.03em;color:#1A1A1A">
            Query<span style="color:#4F46E5">Genie</span>
        </span>
    </div>
    <p style="font-size:0.73rem;color:#9CA3AF;margin:0 0 1.5rem 0;
              font-family:'Inter',sans-serif;">
        Text-to-SQL · RAG-powered
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sb-heading">How it works</p>', unsafe_allow_html=True)

    db_uploaded   = "db_ready"   in st.session_state and st.session_state["db_ready"]
    query_done    = "query_done" in st.session_state and st.session_state["query_done"]

    step1_class = "done"   if db_uploaded else "active"
    step2_class = ("done"  if query_done  else "active") if db_uploaded else ""
    step3_class = "active" if query_done  else ""

    def step_card(cls, num, label, sub):
        return f"""
        <div class="step-card {cls}">
            <div class="step-num">{num if cls != "done" else "✓"}</div>
            <div>
                <div class="step-text">{label}</div>
                <div class="step-sub">{sub}</div>
            </div>
        </div>"""

    st.markdown(
        step_card(step1_class, "1", "Upload Database",  ".db · .sqlite · .sqlite3") +
        step_card(step2_class, "2", "Ask a Question",   "Plain English — no SQL needed") +
        step_card(step3_class, "3", "Inspect Results",  "SQL + live data table"),
        unsafe_allow_html=True
    )
    st.markdown('<p class="sb-heading">Tips</p>', unsafe_allow_html=True)
    tips = [
        ("💡", "Be specific with column names"),
        ("💡", "You can ask aggregate questions"),
        ("💡", "INSERT / UPDATE / DELETE work too"),
        ("💡", "Download the DB after writes"),
    ]
    for icon, tip in tips:
        st.markdown(f'<div class="sb-chip">{icon} {tip}</div>', unsafe_allow_html=True)

    st.markdown('<p class="sb-heading">Supported Formats</p>', unsafe_allow_html=True)
    for fmt in [".db", ".sqlite", ".sqlite3"]:
        st.markdown(f'<div class="sb-chip">🗄️ {fmt}</div>', unsafe_allow_html=True)


st.markdown("""
<div class="qg-wordmark">
    <span style="font-size:1.8rem">🧞</span>
    <h1>Query<span class="accent">Genie</span></h1>
</div>
<p class="qg-tagline">Ask your database anything — in plain English.</p>
""", unsafe_allow_html=True)

st.markdown('<hr class="qg-divider">', unsafe_allow_html=True)

st.markdown('<p class="qg-label">📁 Database</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload SQLite Database",
    type=["db", "sqlite", "sqlite3"],
    label_visibility="collapsed"
)

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as temp_db:
        temp_db.write(uploaded_file.read())
        db_path = temp_db.name

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with st.spinner("Building schema embeddings…"):
        collection = ingestion_pipeline(cursor)

    st.session_state["db_ready"] = True
    st.success("Database loaded successfully!")

    st.markdown('<hr class="qg-divider">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="qg-db-badge">🗄️ {uploaded_file.name}</div>',
        unsafe_allow_html=True
    )

    st.markdown('<p class="qg-label">✦ Ask a question</p>', unsafe_allow_html=True)

    query = st.text_area(
        "Ask a question about your database",
        placeholder="e.g.  Show me the top 10 customers by revenue last quarter",
        height=100,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if st.button("🧞 Generate Result"):

        if query.strip() == "":
            st.warning("Please enter a question before casting your wish.")

        else:
            with st.spinner("The Genie is thinking…"):
                response = backend_pipeline(query, collection, conn)

            st.session_state["query_done"] = True

            st.markdown('<hr class="qg-divider">', unsafe_allow_html=True)
            st.markdown('<p class="qg-label">Generated SQL</p>', unsafe_allow_html=True)
            st.code(response["sql_query"], language="sql")

            result = response["result"]

            if result["status"] == "Success":

                if result["operation"] == "SELECT":
                    st.markdown('<p class="qg-label" style="margin-top:1.25rem">Result</p>', unsafe_allow_html=True)
                    st.dataframe(result["data"], use_container_width=True)

                else:
                    st.success(f"{result['operation']} executed successfully — {result['rows affected']} row(s) affected.")

                    with open(db_path, "rb") as f:
                        st.download_button(
                            "⬇ Download Updated Database",
                            data=f,
                            file_name=f"updated_{uploaded_file.name}",
                            mime="application/octet-stream"
                        )

            else:
                st.error(result["message"])

    conn.close()

else:
    st.session_state["db_ready"]   = False
    st.session_state["query_done"] = False

    st.markdown("""
    <div style="
        margin-top: 2rem;
        padding: 2.5rem 2rem;
        border: 1.5px dashed #D1CEC8;
        border-radius: 14px;
        text-align: center;
        background: #FDFCFB;
    ">
        <div style="font-size:2.5rem; margin-bottom:0.75rem">🗄️</div>
        <p style="
            font-family:'Space Grotesk',sans-serif;
            font-weight:600;
            font-size:1rem;
            color:#374151;
            margin:0 0 0.4rem 0;
        ">Drop your SQLite database above</p>
        <p style="font-size:0.82rem;color:#9CA3AF;margin:0;">
            Accepts .db · .sqlite · .sqlite3
        </p>
    </div>
    """, unsafe_allow_html=True)