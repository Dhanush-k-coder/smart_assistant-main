import streamlit as st
import base64
import os
from openai import OpenAI
from nltk.tokenize import sent_tokenize

from modules.file_handler import extract_text_from_file
from modules.summarizer import summarize_text
from modules.qa_module import answer_question
from modules.question_gen import generate_questions
from modules.evaluator import evaluate_answer

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%);
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    
    /* Animated Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 60%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
        animation: backgroundShift 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes backgroundShift {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        padding: 3rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        from { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.3)); }
        to { filter: drop-shadow(0 0 30px rgba(118, 75, 162, 0.4)); }
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 400;
        opacity: 0.9;
    }
    
    /* Enhanced Card Styles */
    .card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 1.5rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transition: left 0.5s ease;
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 16px 48px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .summary-card {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.08) 0%, 
            rgba(118, 75, 162, 0.08) 50%, 
            rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 12px 40px rgba(102, 126, 234, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .summary-card::before {
        content: '✨';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.7;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.7; }
        50% { transform: scale(1.2) rotate(180deg); opacity: 1; }
    }
    
    .question-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, rgba(16, 185, 129, 0.08) 100%);
        border: 1px solid rgba(34, 197, 94, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.1);
        position: relative;
    }
    
    .question-card::before {
        content: '🎯';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.2rem;
        opacity: 0.8;
    }
    
    .answer-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(99, 102, 241, 0.08) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
        position: relative;
    }
    
    .answer-card::before {
        content: '💡';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.2rem;
        opacity: 0.8;
    }
    
    /* Enhanced Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #10b981 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 6px 24px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 12px 36px rgba(102, 126, 234, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Enhanced Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.3) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: inset -1px 0 0 rgba(102, 126, 234, 0.1);
    }
    
    /* Enhanced Status Indicators */
    .status-success {
        color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(34, 197, 94, 0.1) 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
        font-weight: 500;
    }
    
    .status-warning {
        color: #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(251, 191, 36, 0.1) 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(245, 158, 11, 0.2);
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.1);
        font-weight: 500;
    }
    
    .status-info {
        color: #3b82f6;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.1);
        font-weight: 500;
    }
    
    /* Enhanced Input Styles */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Enhanced Metrics */
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Enhanced Animations */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(30px) scale(0.95); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1); 
        }
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateX(-30px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    .fade-in {
        animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .slide-in {
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Enhanced Footer */
    .footer {
        text-align: center;
        padding: 3rem 0;
        margin-top: 4rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.2) 0%, rgba(255, 255, 255, 0.02) 100%);
        color: #94a3b8;
    }
    
    .footer p {
        margin: 0.5rem 0;
        font-size: 1rem;
    }
    
    .footer strong {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Enhanced File Uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(102, 126, 234, 0.5);
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Enhanced Radio Buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Section Headers */
    .section-header {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -0.5rem;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize session state variables"""
    if "doc_text" not in st.session_state:
        st.session_state.doc_text = ""
    if "qna_log" not in st.session_state:
        st.session_state.qna_log = []
    if "challenge_questions" not in st.session_state:
        st.session_state.challenge_questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "summary_filename" not in st.session_state:
        st.session_state.summary_filename = ""

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_download_link(text, filename, link_text="📥 Download"):
    """Create a download link for text content"""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}" style="text-decoration: none; color: #667eea; font-weight: 600;">{link_text}</a>'
    return href

def display_status(message, status_type="info"):
    """Display status message with appropriate styling"""
    status_class = f"status-{status_type}"
    st.markdown(f'<div class="{status_class}">{message}</div>', unsafe_allow_html=True)

# ============================================================================
# API FUNCTIONS
# ============================================================================

class OpenRouterAPI:
    """Handle OpenRouter API interactions"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.headers = {
            "HTTP-Referer": "https://charan-genai-assistant.streamlit.app/",
            "X-Title": "SmartResearchAssistant"
        }
    
    def answer_question(self, question, context):
        """Get answer from OpenRouter API"""
        prompt = f"""You are a research assistant. Answer based only on the document below:

DOCUMENT:
\"\"\"
{context[:3000]}
\"\"\"

Q: {question}
A:"""

        completion = self.client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers=self.headers
        )

        return {
            "answer": completion.choices[0].message.content,
            "score": 1.0
        }
    
    def generate_questions(self, context):
        """Generate questions from document"""
        prompt = f"""Generate 3 logic-based or comprehension questions from this document:

\"\"\"
{context[:3000]}
\"\"\"

Return the questions numbered as 1., 2., 3."""

        completion = self.client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers=self.headers
        )

        raw = completion.choices[0].message.content.strip()
        questions = [line.split('.', 1)[1].strip() for line in raw.splitlines() if '.' in line]
        return questions
    
    def evaluate_answer(self, user_answer, context, question):
        """Evaluate user's answer"""
        prompt = f"""Evaluate the user's answer based only on this document:

\"\"\"
{context[:3000]}
\"\"\"

Question: {question}
Answer: {user_answer}

Give a short evaluation like 'Correct', 'Partially correct', or 'Incorrect' with a one-line justification."""

        completion = self.client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers=self.headers
        )

        return completion.choices[0].message.content.strip()

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">🧠 Smart Research Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✨ Upload a document and unlock intelligent insights — ask questions or test your knowledge ✨</p>', unsafe_allow_html=True)
    
    # Add a subtle divider
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="display: inline-block; width: 100px; height: 2px; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #10b981 100%); border-radius: 1px;"></div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar configuration"""
    with st.sidebar:
        st.markdown("### 🛠️ Configuration")
        
        mode_choice = st.radio(
            "Choose model mode:",
            ["💻 Local (Free)", "☁️ Cloud (OpenRouter)"],
            help="Select your preferred AI model"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        
        if st.session_state.qna_log:
            st.metric("Questions Asked", len(st.session_state.qna_log))
        
        if st.session_state.doc_text:
            word_count = len(st.session_state.doc_text.split())
            st.metric("Document Words", f"{word_count:,}")
        
        return mode_choice

def render_file_upload():
    """Render file upload section"""
    st.markdown('<h3 class="section-header">📤 Document Upload</h3>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"],
        help="Upload your document to get started with AI-powered analysis"
    )
    
    if uploaded_file:
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                display_status("✅ File uploaded successfully", "success")
            with col2:
                st.metric("📄 File Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                file_type = "📋 TXT" if uploaded_file.type == "text/plain" else "📑 PDF"
                st.metric("📁 Type", file_type)
        
        # Process file with enhanced feedback
        if ("doc_text" not in st.session_state or 
            st.session_state.get("uploaded_filename") != uploaded_file.name):
            
            with st.spinner("🔄 Processing document... This may take a moment"):
                text = extract_text_from_file(uploaded_file)
                st.session_state.doc_text = text
                st.session_state.uploaded_filename = uploaded_file.name
                # Clear old summary when new file is uploaded
                st.session_state.summary = ""
                st.session_state.challenge_questions = []
                display_status("✅ Document processed and ready for analysis", "success")
        else:
            display_status("⚡ Using cached document from memory", "info")
    
    return uploaded_file

def render_document_summary():
    """Render document summary section"""
    if not st.session_state.doc_text:
        return
    
    st.markdown('<h3 class="section-header">📝 Document Summary</h3>', unsafe_allow_html=True)
    
    # Check if summary needs to be regenerated for new document
    current_filename = st.session_state.get("uploaded_filename", "")
    if (not st.session_state.summary or 
        st.session_state.get("summary_filename") != current_filename):
        
        with st.spinner("🧠 Generating intelligent summary..."):
            summary = summarize_text(st.session_state.doc_text)
            st.session_state.summary = summary
            st.session_state.summary_filename = current_filename
    
    # Display summary in a beautiful card
    st.markdown(f"""
    <div class="summary-card fade-in">
        <h4 style="color: #667eea; margin-bottom: 1rem;">📋 Summary</h4>
        <p style="color: #e2e8f0; font-size: 1.1rem; line-height: 1.6; margin: 0;">
            {st.session_state.summary}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary statistics and download
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        word_count = len(st.session_state.summary.split())
        if word_count <= 150:
            display_status(f"✅ Summary generated ({word_count} words)", "success")
        else:
            display_status(f"⚠️ Summary is lengthy ({word_count} words)", "warning")
    
    with col3:
        st.markdown(
            create_download_link(st.session_state.summary, "summary.txt", "📥 Download Summary"),
            unsafe_allow_html=True
        )

def render_interaction_mode():
    """Render interaction mode selection"""
    st.markdown("### 🧭 Choose Your Interaction Mode")
    
    col1, col2 = st.columns(2)
    with col1:
        ask_mode = st.button("💬 Ask Anything", help="Ask questions about your document", use_container_width=True)
    with col2:
        challenge_mode = st.button("🧠 Challenge Me", help="Test your understanding", use_container_width=True)
    
    return ask_mode, challenge_mode

def render_ask_anything_mode(api_client, mode_choice):
    """Render Ask Anything mode interface"""
    st.markdown("### 💬 Ask Anything Mode")
    
    with st.container():
        question = st.text_input(
            "🗨️ What would you like to know?",
            placeholder="Ask any question about your document...",
            help="Type your question here"
        )
        
        if question.strip() and st.session_state.doc_text.strip():
            with st.spinner("🤔 Thinking..."):
                try:
                    if mode_choice == "💻 Local (Free)":
                        result = answer_question(question, st.session_state.doc_text)
                    else:
                        result = api_client.answer_question(question, st.session_state.doc_text)
                    
                    # Display answer in a beautiful card
                    st.markdown(f"""
                    <div class="answer-card fade-in">
                        <h4 style="color: #3b82f6; margin-bottom: 1rem;">✅ Answer</h4>
                        <p style="color: #e2e8f0; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                            {result["answer"]}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add justification for local mode
                    if mode_choice == "💻 Local (Free)":
                        sentences = sent_tokenize(st.session_state.doc_text)
                        relevant = [s for s in sentences if result["answer"] in s]
                        if relevant:
                            st.markdown(f"""
                            <div style="background: rgba(34, 197, 94, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #22c55e;">
                                <strong>🧠 Justification:</strong> {relevant[0]}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Log the QnA
                    st.session_state.qna_log.append(f"Q: {question}\nA: {result['answer']}\n\n")
                    
                except Exception as e:
                    st.error(f"❌ Failed to get answer: {e}")
        
        elif question.strip():
            display_status("ℹ️ Please upload a document first", "info")
    
    # Show QnA history download option
    if st.session_state.qna_log:
        st.markdown("---")
        qna_text = "\n".join(st.session_state.qna_log)
        st.markdown(
            create_download_link(qna_text, "qna_history.txt", "📥 Download Q&A History"),
            unsafe_allow_html=True
        )

def render_challenge_mode(api_client, mode_choice):
    """Render Challenge Mode interface"""
    st.markdown("### 🧠 Challenge Mode")
    
    if st.button("⚡ Generate 3 Questions", use_container_width=True):
        with st.spinner("🎯 Generating challenging questions..."):
            try:
                if mode_choice == "☁️ Cloud (OpenRouter)":
                    questions = api_client.generate_questions(st.session_state.doc_text)
                else:
                    questions = generate_questions(st.session_state.doc_text)
                
                st.session_state.challenge_questions = questions
                st.session_state.user_answers = [""] * len(questions)
                display_status("✅ Questions generated successfully!", "success")
                
            except Exception as e:
                st.error(f"❌ Failed to generate questions: {e}")
    
    # Display questions and answers
    if st.session_state.challenge_questions:
        st.markdown("---")
        for i, question in enumerate(st.session_state.challenge_questions):
            with st.container():
                st.markdown(f"""
                <div class="question-card fade-in">
                    <h4 style="color: #22c55e; margin-bottom: 1rem;">Question {i+1}</h4>
                    <p style="color: #e2e8f0; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                        {question}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                user_input = st.text_area(
                    f"Your Answer to Question {i+1}",
                    key=f"ans{i}",
                    height=100,
                    placeholder="Type your answer here..."
                )
                
                if user_input.strip():
                    try:
                        if mode_choice == "☁️ Cloud (OpenRouter)":
                            feedback = api_client.evaluate_answer(user_input, st.session_state.doc_text, question)
                        else:
                            feedback = evaluate_answer(user_input, st.session_state.doc_text)
                        
                        # Color code feedback
                        feedback_color = "#22c55e" if "correct" in feedback.lower() else "#f59e0b"
                        st.markdown(f"""
                        <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid {feedback_color};">
                            <strong>🧾 Feedback:</strong> {feedback}
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Failed to evaluate answer: {e}")
                
                st.markdown("---")

def render_footer():
    """Render the footer"""
    st.markdown("""
    <div class="footer">
        <p>🚀 Built with ❤️ by <strong>Dhanush Korlepara</strong> using Streamlit & AI</p>
        <p>Powered by OpenRouter API & Local Transformers</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get mode choice
    mode_choice = render_sidebar()
    
    # Initialize API client
    api_key = os.getenv("API_KEY")
    api_client = OpenRouterAPI(api_key) if mode_choice == "☁️ Cloud (OpenRouter)" else None
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload section
        uploaded_file = render_file_upload()
        
        if uploaded_file and st.session_state.doc_text:
            # Document summary
            render_document_summary()
            
            # Interaction modes
            st.markdown("---")
            mode = st.radio(
                "Select your interaction mode:",
                ["Ask Anything", "Challenge Me"],
                horizontal=True,
                help="Choose how you want to interact with your document"
            )
            
            if mode == "Ask Anything":
                render_ask_anything_mode(api_client, mode_choice)
            else:
                render_challenge_mode(api_client, mode_choice)
    
    with col2:
        # Raw text viewer (collapsible)
        if st.session_state.doc_text:
            with st.expander("📄 View Raw Text", expanded=False):
                st.text_area(
                    "Document Content",
                    st.session_state.doc_text,
                    height=300,
                    disabled=True
                )
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
