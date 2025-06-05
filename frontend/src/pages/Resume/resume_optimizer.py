import streamlit as st
import base64
import os
import json
import time
from datetime import datetime
import io
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from PyPDF2 import PdfReader

# Set up logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session state keys
RESUME_DATA = 'resume_optimizer_data'
CURRENT_STEP = 'resume_optimizer_step'

def initialize_session_state():
    """Initialize session state for resume optimizer if not already done."""
    if RESUME_DATA not in st.session_state:
        st.session_state[RESUME_DATA] = {
            'resume_text': '',
            'optimized_resume': '',
            'score': 0,
            'suggestions': [],
        }
    if CURRENT_STEP not in st.session_state:
        st.session_state[CURRENT_STEP] = 0

def show_header():
    """Display the header with page title and description."""
    # Main CSS styles
    css = """
    <style>
        /* Base styles */
        body, .main, .block-container, .stApp {
            background: #fff !important;
            color: #222 !important;
        }
        
        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            background: #fff !important;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #4CAF50 !important;
        }
        
        /* Buttons */
        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(90deg, #4CAF50 0%, #388E3C 100%) !important;
            color: #fff !important;
            font-weight: 600;
            border-radius: 6px;
            border: none;
            padding: 0.6em 1.5em;
            transition: all 0.2s;
            box-shadow: 0 2px 6px rgba(76,175,80,0.07);
        }
        
        .stButton > button[disabled], .stDownloadButton > button[disabled] {
            background: #e0e0e0 !important;
            color: #bdbdbd !important;
            cursor: not-allowed !important;
        }
        
        .stButton > button:hover:enabled, 
        .stDownloadButton > button:hover:enabled {
            background: linear-gradient(90deg, #388E3C 0%, #4CAF50 100%) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .stDownloadButton > button {
            margin-top: 10px;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            margin-bottom: 1.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #000000 !important;
            font-weight: 600;
            padding: 10px 16px;
            border-radius: 8px 8px 0 0;
            transition: all 0.2s ease;
            background: #f8f9fa;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #f0f2f6 !important;
            border-bottom: 3px solid #4CAF50 !important;
            color: #000 !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #f0f2f6 !important;
        }
        
        /* Score card */
        .score-card {
            padding: 20px;
            border-radius: 12px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 24px;
        }
        
        .score-value {
            font-size: 3rem;
            font-weight: 700;
            color: #2c3e50;
            margin: 0;
            line-height: 1;
        }
        
        .score-label {
            font-size: 1rem;
            color: #6c757d;
            margin: 0 0 8px 0;
        }
        
        .progress-container {
            height: 12px;
            background-color: #e9ecef;
            border-radius: 6px;
            margin: 20px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 6px;
            background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
            transition: width 0.6s ease;
        }
        
        /* Form elements */
        .stTextArea > div > div > textarea {
            min-height: 200px;
        }
        
        /* File uploader */
        .stFileUploader > div {
            border: 2px dashed #dee2e6;
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
        }
        
        .stFileUploader > div:hover {
            border-color: #4CAF50;
        }
    </style>
    """
    
    # Apply CSS
    st.markdown(css, unsafe_allow_html=True)
    
    # Page header
    st.title("📝 Resume Optimizer")
    st.markdown("""
    Upload your resume to get an instant ATS score and personalized suggestions to improve it. 
    You can also download the improved version in multiple formats.
    """)

def show_upload_step():
    """Display the resume upload step with improved UI and error handling."""
    st.markdown("### 📤 Upload Your Resume")
    st.markdown("Get instant feedback and optimization suggestions for your resume based on ATS best practices.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a PDF or TXT file", 
            type=["pdf", "txt"],
            key="resume_uploader",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("\u2190 Back to Home", key="back_to_home", use_container_width=True, 
                   help="Go back to the home page"):
            st.session_state.page = "home"
            st.rerun()
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing your resume..."):
                logger.info(f"Processing uploaded file: {uploaded_file.name} (type: {uploaded_file.type})")
                
                # Read the file content
                try:
                    if uploaded_file.type == "application/pdf":
                        logger.info("Extracting text from PDF file")
                        pdf_reader = PdfReader(uploaded_file)
                        resume_text = "\n\n".join([page.extract_text() for page in pdf_reader.pages])
                        logger.info(f"Extracted {len(resume_text)} characters from PDF")
                    else:  # txt file
                        logger.info("Reading text file content")
                        resume_text = uploaded_file.read().decode("utf-8")
                        logger.info(f"Read {len(resume_text)} characters from text file")
                except Exception as e:
                    logger.error(f"Error reading file: {str(e)}", exc_info=True)
                    st.error(f"Error reading file: {str(e)}")
                    return
                
                # Validate resume text
                if len(resume_text.strip()) < 50:
                    error_msg = f"The uploaded file doesn't contain enough text. Only found {len(resume_text.strip())} characters."
                    logger.warning(error_msg)
                    st.error(error_msg)
                    return
                
                logger.info("Storing resume data in session state")
                # Store the resume text and filename in session state
                st.session_state[RESUME_DATA].update({
                    'resume_text': resume_text,
                    'original_filename': uploaded_file.name,
                    # Clear previous results
                    'optimized_resume': '',
                    'score': 0,
                    'suggestions': []
                })
                
                # Move to the results step (which will trigger analysis)
                st.session_state[CURRENT_STEP] = 1
                st.rerun()
                
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)
            st.error(f"Error processing file: {str(e)}")
            st.session_state[RESUME_DATA].update({
                'resume_text': '',
                'optimized_resume': '',
                'score': 0,
                'suggestions': []
            })


def get_download_filename(extension='txt'):
    """Generate a download filename with timestamp."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"resume_optimized_{timestamp}.{extension}"

def show_results():
    """Display optimization results and suggestions with enhanced download options."""
    data = st.session_state[RESUME_DATA]
    resume_text = data.get('resume_text', '').strip()
    
    # Validate resume text length
    if len(resume_text) < 50:
        error_msg = "Resume text must be at least 50 characters long. " \
                  f"Current length: {len(resume_text)} characters."
        logger.warning(error_msg)
        st.error(error_msg)
        st.session_state[CURRENT_STEP] = 0
        st.rerun()
        return

    # Call backend to score and suggest improvements if not already done
    if 'optimization_in_progress' not in st.session_state[RESUME_DATA]:
        st.session_state[RESUME_DATA]['optimization_in_progress'] = True
        
        with st.spinner("Analyzing your resume and generating suggestions..."):
            from services.api import APIService
            
            try:
                logger.info("Sending resume for optimization...")
                result = APIService.optimize_resume(
                    resume_text=resume_text,
                    token=st.session_state.get('token')
                )
                
                logger.debug(f"Optimization result: {json.dumps({k: v for k, v in result.items() if k != 'optimized_text'}, indent=2)[:500]}...")
                
                if result.get('status') == 'success':
                    st.session_state[RESUME_DATA].update({
                        'optimized_resume': result.get('optimized_text', resume_text),
                        'score': float(result.get('score', 0)),
                        'suggestions': result.get('suggestions', []),
                        'missing_keywords': result.get('missing_keywords', []),
                        'last_optimized': datetime.now().isoformat(),
                        'optimization_error': None
                    })
                    logger.info(f"Optimization successful. Score: {st.session_state[RESUME_DATA]['score']}")
                else:
                    error_msg = result.get('message', 'Unknown error occurred during analysis')
                    logger.error(f"Optimization failed: {error_msg}")
                    st.session_state[RESUME_DATA]['optimization_error'] = error_msg
                    
            except Exception as e:
                error_msg = f"An unexpected error occurred: {str(e)}"
                logger.error(f"Error during optimization: {error_msg}", exc_info=True)
                st.session_state[RESUME_DATA]['optimization_error'] = error_msg
            finally:
                st.session_state[RESUME_DATA]['optimization_in_progress'] = False
                st.rerun()  # Rerun to update the UI
    
    # Handle optimization errors
    if 'optimization_error' in st.session_state[RESUME_DATA] and st.session_state[RESUME_DATA]['optimization_error']:
        st.error(f"Failed to analyze resume: {st.session_state[RESUME_DATA]['optimization_error']}")
        
        # Show retry button
        if st.button("↻ Try Again"):
            del st.session_state[RESUME_DATA]['optimization_error']
            del st.session_state[RESUME_DATA]['optimization_in_progress']
            if 'optimized_resume' in st.session_state[RESUME_DATA]:
                del st.session_state[RESUME_DATA]['optimized_resume']
            st.rerun()
        return
        
    # If we're still optimizing, show a loading spinner
    if st.session_state[RESUME_DATA].get('optimization_in_progress', False):
        with st.spinner("Optimizing your resume. This may take a minute..."):
            st.write("We're analyzing your resume to provide the best optimization.")
            st.progress(0.5)
        return

    # UI Styling
    st.markdown("""
    <style>
        .score-card {
            padding: 24px;
            border-radius: 12px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 24px;
        }
        .score-value {
            font-size: 3.5rem;
            font-weight: 700;
            color: #2c3e50;
            margin: 0;
            line-height: 1;
        }
        .score-label {
            font-size: 1.1rem;
            color: #6c757d;
            margin: 0 0 8px 0;
            font-weight: 500;
        }
        .progress-container {
            height: 12px;
            background-color: #e9ecef;
            border-radius: 6px;
            margin: 20px 0;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            border-radius: 6px;
            background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
            transition: width 0.6s ease;
        }
        .suggestion-card {
            background: white;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 4px solid #4CAF50;
        }
        .download-btn {
            margin: 8px 0;
            width: 100%;
        }
        .tab-content {
            padding: 16px 0;
        }
        .resume-preview {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 16px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: auto;
        }
    </style>
    """, unsafe_allow_html=True)

    # Get data from session state
    score = float(st.session_state[RESUME_DATA].get('score', 0))
    suggestions = st.session_state[RESUME_DATA].get('suggestions', [])
    optimized_resume = st.session_state[RESUME_DATA].get('optimized_resume', '')

    # Score Card
    st.markdown(f"""
    <div class="score-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <p class="score-label">YOUR ATS SCORE</p>
                <h1 class="score-value">{int(score)}<span style="font-size: 1.5rem; color: #6c757d;">/100</span></h1>
            </div>
            <div style="text-align: right; font-size: 1.5rem;">
                {'🎉 Excellent!' if score >= 80 else '👍 Good' if score >= 50 else '👎 Needs Work'}
            </div>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {score}%;"></div>
        </div>
        <p style="color: #495057; margin: 8px 0 0 0; font-size: 1.1rem;">
            {'Your resume is well-optimized! 🚀' if score >= 80 
             else 'Your resume is on the right track!' if score >= 50 
             else 'Consider implementing the suggestions below to improve your score.'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestions Section
    with st.expander("📝 Suggestions to Improve Your Resume", expanded=True):
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"""
                <div class="suggestion-card">
                    <strong>Suggestion {i}:</strong> {suggestion}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific suggestions available. Your resume looks great!")

    # Resume Tabs
    tab1, tab2 = st.tabs(["✨ Optimized Resume", "📋 Original Resume"])
    
    with tab1:
        st.markdown("### Your Optimized Resume")
        st.markdown(f"<div class='resume-preview'>{optimized_resume}</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Original Resume")
        st.markdown(f"<div class='resume-preview'>{resume_text}</div>", unsafe_allow_html=True)

    # Download Section
    st.markdown("### 📥 Download Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download as TXT
        st.download_button(
            label="⬇️ Download as Text",
            data=optimized_resume.encode('utf-8'),
            file_name=get_download_filename('txt'),
            mime="text/plain",
            key="download_txt",
            use_container_width=True,
            help="Download the optimized resume as a plain text file"
        )
    
    with col2:
        # Download as PDF (placeholder - would require reportlab or similar)
        if st.button("⬇️ Download as PDF (Coming Soon)", 
                    use_container_width=True,
                    disabled=True,
                    help="PDF download will be available in the next update"):
            pass
    
    # Start Over Button
    if st.button("🔄 Start Over", 
                type="primary", 
                use_container_width=True,
                help="Upload a different resume"):
        st.session_state[RESUME_DATA] = {
            'resume_text': '',
            'optimized_resume': '',
            'score': 0,
            'suggestions': [],
        }
        st.session_state[CURRENT_STEP] = 0
        st.rerun()


def show_resume_optimizer():
    """Main function to display the resume optimizer."""
    initialize_session_state()
    show_header()
    
    if st.session_state[CURRENT_STEP] == 0:
        show_upload_step()
    else:
        show_results()

# This allows the file to be run directly for testing
if __name__ == "__main__":
    show_resume_optimizer()
