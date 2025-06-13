import streamlit as st
import os
from PIL import Image
import requests
from main import load_text_from_file, process_file
from export_pdf import export_summary_to_pdf, export_quiz_to_pdf
from quiz_gen import generate_questions
import random

def main():
    # Set page config
    st.set_page_config(
        page_title="StudySage",
        page_icon="📚",
        layout="wide"
    )

    # Initialize session state variables
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'questions' not in st.session_state:
        st.session_state.questions = None
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False
    if 'scroll_to_summary' not in st.session_state:
        st.session_state.scroll_to_summary = False

    # Create header with logo and text
    col1, col2 = st.columns([1, 2])
    with col1:
        logo_path = "logo.png"
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
        file_path = os.path.join("output", uploaded_file.name)
        os.makedirs("output", exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Processing options
        st.subheader("Processing Options")
        
        # Summary length options
        col1, col2 = st.columns(2)
        with col1:
            min_length = st.number_input("Minimum summary length (words)", min_value=10, max_value=500, value=50)
            max_length = st.number_input("Maximum summary length (words)", min_value=50, max_value=1000, value=200)
        
        # Quiz options
        generate_quiz = st.checkbox("Generate quiz questions", value=False)
        num_questions = None
        if generate_quiz:
            num_questions = st.number_input("Number of questions", min_value=1, max_value=20, value=5)
        
        # Process the file
        if st.button("Process File"):
            with st.spinner("Processing..."):
                try:
                    # Process the file
                    summary = process_file(
                        file_path,
                        mode="online",
                        api_key=st.session_state.api_key,
                        min_length=min_length,
                        max_length=max_length
                    )
                    
                    # Store results in session state
                    st.session_state.summary = summary
                    st.session_state.file_processed = True
                    st.session_state.scroll_to_summary = True
                    
                    if generate_quiz:
                        questions = generate_questions(summary, num_questions)
                        st.session_state.questions = questions
                    else:
                        st.session_state.questions = None
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

    # Display results if file has been processed
    if st.session_state.file_processed and st.session_state.summary:
        # Add unique ID to summary header for scrolling
        st.markdown('<h2 id="generated-summary">Generated Summary</h2>', unsafe_allow_html=True)
        st.write(st.session_state.summary)
        
        # Auto-scroll to summary section with improved reliability
        if st.session_state.scroll_to_summary:
            st.markdown(
                """
                <script>
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(function() {
                        const element = document.getElementById('generated-summary');
                        if (element) {
                            element.scrollIntoView({behavior: 'smooth', block: 'start'});
                        }
                    }, 100);
                });
                </script>
                """,
                unsafe_allow_html=True
            )
            # Reset scroll flag to prevent repeated scrolling
            st.session_state.scroll_to_summary = False
        
        # Download summary PDF button
        if st.button("Download Summary PDF"):
            try:
                pdf_path = export_summary_to_pdf(st.session_state.summary)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Click here to download Summary PDF",
                        data=f,
                        file_name="summary_output.pdf",
                        mime="application/pdf",
                        key="summary_download"
                    )
            except Exception as e:
                st.error(f"Error generating summary PDF: {str(e)}")
        
        # Display quiz if generated
        if st.session_state.questions:
            st.subheader("Quiz Questions")
            quiz_col1, quiz_col2 = st.columns([3, 1])
            
            with quiz_col1:
                for i, q in enumerate(st.session_state.questions, 1):
                    st.markdown(f"**Question {i}**")
                    st.write(q["question"])
                    
                    # Display options
                    options = q["options"]
                    random.shuffle(options)
                    for j, option in enumerate(options, 1):
                        st.write(f"{j}. {option}")
                    
                    # Show answer in a collapsible section
                    with st.expander("Show Answer"):
                        st.write(f"Correct Answer: {q['answer']}")
                    
                    st.markdown("---")
            
            with quiz_col2:
                st.markdown("### Download Options")
                if st.button("Download Quiz PDF", key="quiz_download_button"):
                    try:
                        quiz_pdf_path = export_quiz_to_pdf(st.session_state.questions)
                        with open(quiz_pdf_path, "rb") as f:
                            st.download_button(
                                label="Click here to download Quiz PDF",
                                data=f,
                                file_name="quiz_output.pdf",
                                mime="application/pdf",
                                key="quiz_download"
                            )
                    except Exception as e:
                        st.error(f"Error generating quiz PDF: {str(e)}")

if __name__ == "__main__":
    main()