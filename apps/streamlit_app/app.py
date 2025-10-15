import streamlit as st
import os
import tempfile
from pathlib import Path

# Import configuration
try:
    from config import OUTPUT_DIR
except ImportError:
    OUTPUT_DIR = "output"

from core.io import load_text_from_file, process_file
from core.quiz_gen import generate_questions
from core.export_pdf import export_summary_to_pdf, export_quiz_to_pdf

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False
if 'scroll_to_summary' not in st.session_state:
    st.session_state.scroll_to_summary = False

# Create output directory
OUTPUT_PATH = Path(OUTPUT_DIR)
OUTPUT_PATH.mkdir(exist_ok=True)

# Create header with logo and text
col1, col2 = st.columns([1, 2])
with col1:
    logo_path = "assets\\images\\logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=200, use_container_width=False)
    else:
        st.warning("Logo file not found.")
with col2:
    st.title("StudySage AI Note Assistant")
    st.subheader("by Sahaj33")
st.markdown("---")

# API Key input
api_key = st.text_input("Enter your Hugging Face API Key", value=st.session_state.api_key or "", type="password")
if api_key != st.session_state.api_key:
    st.session_state.api_key = api_key
    st.rerun()

# File upload
uploaded_file = st.file_uploader("Upload your notes (PDF, TXT, PNG, JPG)", type=['pdf', 'txt', 'png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Processing options
    st.markdown("### Processing Options")
    
    # Mode selection
    mode = st.radio("Processing Mode", ["Offline (Private)", "Online (Requires API Key)"], index=0)
    selected_mode = "offline" if mode == "Offline (Private)" else "online"
    
    # Summary length
    st.markdown("#### Summary Length")
    col1, col2 = st.columns(2)
    with col1:
        min_length = st.number_input("Min Length", min_value=10, max_value=100, value=30)
    with col2:
        max_length = st.number_input("Max Length", min_value=50, max_value=500, value=150)
    
    # Process button
    if st.button("🧠 Process Document"):
        try:
            with st.spinner("Processing..."):
                # Process the file
                summary = process_file(
                    file_path, 
                    mode=selected_mode, 
                    api_key=st.session_state.api_key if selected_mode == "online" else "",
                    min_length=min_length,
                    max_length=max_length
                )
                
                st.session_state.summary = summary
                st.session_state.file_processed = True
                st.session_state.scroll_to_summary = True
                
                st.success("✅ Document processed successfully!")
                
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
    
    # Display results if processed
    if st.session_state.file_processed:
        st.markdown("---")
        st.markdown("## 📝 Results")
        
        # Summary tab
        summary_tab, quiz_tab = st.tabs(["Summary", "Quiz"])
        
        with summary_tab:
            st.markdown("### Document Summary")
            st.text_area("Summary", value=st.session_state.summary, height=300, key="summary_display")
            
            # Export options
            st.markdown("### Export Options")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📄 Export Summary as PDF"):
                    try:
                        pdf_path = export_summary_to_pdf(st.session_state.summary)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="Download Summary PDF",
                                data=f,
                                file_name="study_sage_summary.pdf",
                                mime="application/pdf"
                            )
                        st.success("✅ Summary PDF exported!")
                    except Exception as e:
                        st.error(f"❌ Error exporting PDF: {str(e)}")
            
            with col2:
                if st.button("💾 Save Summary as Text"):
                    st.download_button(
                        label="Download Summary Text",
                        data=st.session_state.summary,
                        file_name="study_sage_summary.txt",
                        mime="text/plain"
                    )
        
        with quiz_tab:
            st.markdown("### Generate Quiz")
            num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5)
            
            if st.button("🧪 Generate Quiz Questions"):
                try:
                    with st.spinner("Generating quiz..."):
                        questions = generate_questions(st.session_state.summary, num_questions)
                        st.session_state.questions = questions
                        st.success("✅ Quiz generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating quiz: {str(e)}")
            
            # Display questions if generated
            if st.session_state.questions:
                st.markdown("### Quiz Questions")
                for i, q in enumerate(st.session_state.questions, 1):
                    st.markdown(f"**Question {i}:** {q['question']}")
                    st.markdown("**Options:**")
                    for j, option in enumerate(q['options'], 1):
                        st.markdown(f"{j}. {option}")
                    st.markdown(f"**Answer:** {q['answer']}")
                    st.markdown("---")
                
                # Quiz export options
                st.markdown("### Export Quiz")
                if st.button("📄 Export Quiz as PDF"):
                    try:
                        pdf_path = export_quiz_to_pdf(st.session_state.questions)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="Download Quiz PDF",
                                data=f,
                                file_name="study_sage_quiz.pdf",
                                mime="application/pdf"
                            )
                        st.success("✅ Quiz PDF exported!")
                    except Exception as e:
                        st.error(f"❌ Error exporting quiz PDF: {str(e)}")

# Footer
st.markdown("---")
st.markdown("🧠 StudySage - AI-Powered Study Assistant")