"""
Streamlit Web Interface for Document Analysis System V2
Enhanced UI with Parent-Child architecture and GPU-aware processing
"""

import streamlit as st
import os
import logging
import time
from document_analysis import (
    DocumentAnalysisV2,
    CHROMADB_AVAILABLE,
    HardwareDetector,
    create_dummy_pdf
)
import torch

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Configuration
st.set_page_config(
    page_title="DocuMind AI - Professional Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stChatMessage[data-testimonial="user"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }
    .stChatMessage[data-testimonial="assistant"] {
        background-color: #f0f7ff;
        border: 1px solid #d0e3ff;
    }
    .confidence-high { color: #28a745; font-weight: bold; }
    .confidence-med { color: #fd7e14; font-weight: bold; }
    .confidence-low { color: #dc3545; font-weight: bold; }
    
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
    }
    </style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'system' not in st.session_state:
        st.session_state.system = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'document_processed' not in st.session_state:
        st.session_state.document_processed = False
    if 'processing_info' not in st.session_state:
        st.session_state.processing_info = None
    if 'current_doc_text' not in st.session_state:
        st.session_state.current_doc_text = None

def process_uploaded_file(uploaded_file) -> str:
    """Save uploaded file to temp location and return path."""
    temp_path = os.path.join("/tmp", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path

def simulate_streaming(text):
    """Simulate streaming text effect for better UX."""
    placeholder = st.empty()
    full_text = ""
    for chunk in text.split():
        full_text += chunk + " "
        placeholder.markdown(full_text + "▌")
        time.sleep(0.05)
    placeholder.markdown(full_text)
    return full_text

def main():
    init_session_state()
    
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2811/2811194.png", width=80)
    with col2:
        st.title("DocuMind AI")
        st.markdown("*Advanced Hierarchical Document Intelligence*")
    
    st.divider()
    
    with st.sidebar:
        st.header("🛠️ Control Panel")
        
        # Hardware Status
        config = HardwareDetector.detect()
        device_color = "green" if config.device == "cuda" else "blue"
        st.markdown(f"**Compute Engine:** :{device_color}[{config.device.upper()}]")
        
        if config.device == "cuda":
            st.caption("🚀 GPU Acceleration Active")
        
        st.divider()
        
        # Document Stats
        if st.session_state.processing_info:
            st.subheader("📊 Document Insights")
            info = st.session_state.processing_info
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Total Chunks", info['num_chunks'])
            with c2:
                if 'num_parents' in info:
                    st.metric("Parents", info['num_parents'])
            
            st.info(f"Strategy: **{info['strategy'].title()}**")
            
            with st.expander("📄 Document Preview"):
                if st.session_state.current_doc_text:
                    st.text_area("Content", st.session_state.current_doc_text, height=300)
        
        st.divider()
        
        # Actions
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🔄 Reset Global System", use_container_width=True, type="primary"):
            st.session_state.system = None
            st.session_state.document_processed = False
            st.session_state.processing_info = None
            st.session_state.messages = []
            st.session_state.current_doc_text = None
            st.toast("System fully reset!", icon="🔄")
            st.rerun()

        st.divider()
        st.header("📖 Instructions")
        st.markdown("""
        1. **Upload** a document (PDF, TXT, MD).
        2. **Analyze**: The system will partition it hierarchically.
        3. **Chat**: Ask specific questions or broad topics.
        
        *Tip: Try asking 'Summarize the main points' or just keywords like 'Payment'.*
        """)
    
    # Main Workflow
    if not st.session_state.document_processed:
        c1, c2 = st.columns([2, 1])
        with c1:
            uploaded_file = st.file_uploader(
                "📥 Drop your document here",
                type=['pdf', 'txt', 'md'],
                label_visibility="collapsed"
            )
        with c2:
            if st.button("🧪 Try with Sample", use_container_width=True):
                create_dummy_pdf()
                # Simulate file upload with the dummy file
                with open("sample_document.pdf", "rb") as f:
                    class DummyFile:
                        def __init__(self, name, data):
                            self.name = name
                            self.data = data
                        def getbuffer(self): return self.data
                    
                    uploaded_file = DummyFile("sample_document.pdf", f.read())

        if uploaded_file:
            with st.status("🔍 Analyzing document structure...", expanded=True) as status:
                try:
                    pdf_path = process_uploaded_file(uploaded_file)
                    st.write("Extracting semantic layers...")
                    
                    # Initialize system
                    if not st.session_state.system:
                        st.session_state.system = DocumentAnalysisV2()
                    
                    # Process document
                    result = st.session_state.system.process_document(pdf_path)
                    
                    st.session_state.processing_info = result
                    st.session_state.document_processed = True
                    st.session_state.current_doc_text = st.session_state.system.current_text
                    
                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    st.toast("Document indexed successfully!", icon="✅")
                    st.rerun()
                    
                except Exception as e:
                    status.update(label="❌ Analysis Failed", state="error")
                    st.error(f"Error: {str(e)}")
                    logger.error(f"Processing error: {e}", exc_info=True)
    
    else:
        # Chat Interface
        st.subheader("💬 Interactive Query")
        
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"], unsafe_allow_html=True)
        
        # Input
        if prompt := st.chat_input("Ask anything about the document..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    with st.spinner("🧠 Processing deep context..."):
                        query_result = st.session_state.system.query(prompt, n_results=3)
                        
                        answer = query_result['answer']
                        confidence = query_result['confidence']
                        context = query_result['context']
                        
                        # Confidence styling
                        conf_class = "confidence-high" if confidence > 0.8 else "confidence-med" if confidence > 0.5 else "confidence-low"
                        
                        response_md = f"""
                        <div style="font-size: 1.1em; margin-bottom: 15px;">{answer}</div>
                        <div style="display: flex; gap: 20px; font-size: 0.85em; opacity: 0.8;">
                            <span>🎯 Confidence: <span class="{conf_class}">{confidence:.1%}</span></span>
                            <span>📚 Sources: {query_result['num_results']} sections ({query_result['source_type']})</span>
                        </div>
                        """
                        
                        st.markdown(response_md, unsafe_allow_html=True)
                        
                        with st.expander("🔍 View Source Context"):
                            st.info(f"Synthesized from **{query_result['source_type']}**:")
                            context_to_show = query_result['context'].split("\n---\n")
                            for i, chunk in enumerate(context_to_show):
                                st.markdown(f"**Section {i+1}**")
                                st.text(chunk)
                                st.divider()
                        
                        st.session_state.messages.append({"role": "assistant", "content": response_md})
                        
                except Exception as e:
                    st.error(f"Failed to generate answer: {str(e)}")
                    logger.error(f"QA error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
