🧠 StudySage – AI Note Assistant
StudySage is a versatile Python tool designed for students to summarize lecture notes and generate quizzes using AI, supporting both online and offline modes. It offers a command-line interface (CLI), a graphical user interface (GUI), and a web-based interface via Streamlit, making it accessible for various user preferences.
✨ Features

File Support: Processes .txt, .md, .pdf, .png, .jpg, and .jpeg files. Uses OCR for image files and PDFs with scanned content.
Summarization: Generates concise summaries using the distilbart-cnn-12-6 model from Hugging Face, with customizable minimum and maximum word lengths.
Quiz Generation: Creates multiple-choice questions based on the summary, with configurable question counts (1-20).
Interfaces:
CLI: Interactive terminal interface with minimal logs, user-controlled PDF exports, and a streamlined flow for summary and quiz generation.
GUI: User-friendly desktop app built with customtkinter, supporting file loading, summarization, OCR, and PDF/text exports.
Web: Streamlit-based interface with a modern design, auto-scroll to summaries, persistent data, and separate PDF download buttons.


Modes:
Online: Faster processing using Hugging Face API (requires API key).
Offline: Local processing with no internet required (slower but lightweight).


PDF Export: Exports summaries and quizzes to formatted PDFs with timestamps and optional logos, with user consent to prevent automatic saving.
OCR: Extracts text from images and scanned PDFs using Tesseract OCR, with support for multiple languages.
Cross-Platform: Compatible with Windows, macOS, and Linux.

🛠️ Recent Updates

Streamlit Web Interface:
Reliable auto-scroll to the "Generated Summary" section after processing files.
Persistent summary and quiz data using session state, preventing data loss on PDF downloads.
User-triggered PDF downloads instead of automatic saves.


CLI Improvements:
Streamlined flow: After generating a summary, users are prompted to generate quizzes without re-entering file paths.
Minimal logs for a cleaner interface.
User-controlled PDF exports with confirmation prompts.


General Enhancements:
Improved error handling across all interfaces.
Consistent file handling for text, PDFs, and images with OCR support.
Updated quiz generation logic for better question diversity.



🔧 Setup
Prerequisites

Python 3.8 or higher
Tesseract OCR installed (for image and PDF text extraction):
Windows: Install from Tesseract at UB Mannheim and add to PATH.
Linux: sudo apt-get install tesseract-ocr
macOS: brew install tesseract


Optional: Hugging Face API key for online mode (get one from Hugging Face).

Installation

Clone the repository:git clone https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant.git
cd StudySage-Offline-AI-Note-Assistant


Install dependencies:pip install -r requirements.txt


Ensure NLTK resources are downloaded (run once):import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')



Running the Application

Command-Line Interface:python main.py


Choose online/offline mode, enter file paths, and select features (summary or quiz).


Graphical User Interface:python gui.py


Use buttons to load files, generate summaries, perform OCR, and export results.


Streamlit Web Interface:streamlit run app.py


Access via browser (typically http://localhost:8501), upload files, and interact with the web UI.



📦 Packaging as an Executable
You can package StudySage into a standalone executable using PyInstaller, allowing users to run the CLI or GUI without installing Python or dependencies.
Steps to Package

Install PyInstaller:pip install pyinstaller


Package the CLI (main.py):pyinstaller -F main.py


-F creates a single executable file.
The executable will be in the dist/ folder (e.g., dist/main.exe on Windows).


Package the GUI (gui.py):pyinstaller -F gui.py


Ensure logo.png (if used) is in the same directory, or modify the .spec file to include it.


Run the executable:
Navigate to dist/ and run the generated file (e.g., ./main on Linux/macOS or main.exe on Windows).



Notes

Generated files (main.spec, build/, dist/, etc.) are excluded from Git via .gitignore to keep the repository clean.
For better packaging, you can customize the .spec file (e.g., to include logo.png or Tesseract binaries) and rerun PyInstaller with pyinstaller main.spec.

📂 Project Structure

.gitignore: Excludes generated files, models, and sensitive data from version control.
app.py: Streamlit web interface.
main.py: CLI with summarization and quiz generation.
gui.py: GUI using customtkinter.
summarize_text.py: Core summarization logic.
quiz_gen.py: Quiz question generation.
export_pdf.py: PDF export for summaries and quizzes.
ocr_reader.py: OCR for images and scanned PDFs.
requirements.txt: Project dependencies.
output/: Directory for generated PDFs and temporary files (excluded from Git).
models/: Directory for offline AI models (excluded from Git).
logo.png: Optional logo for PDF exports (add your own).

📖 Usage
CLI

Select online (requires API key) or offline mode.
Enter summary length preferences (e.g., 30,200 for min/max words).
Provide a file path (.txt, .md, .pdf, .png, etc.).
Choose to generate a summary or quiz, or change the file.
After a summary, opt to generate a quiz without re-entering the file path.
Confirm PDF exports when prompted.

GUI

Click "Choose File" to load a supported file.
Use "Generate Summary" for summarization, "OCR" for images, or export results as PDF/text.
View results in the textbox.

Web

Enter your Hugging Face API key (for online mode).
Upload a file and set summary length or quiz options.
Click "Process File" to generate results, which auto-scroll to the summary.
Download PDFs using dedicated buttons.

🤝 Contributing
Contributions are welcome! Fork the repository, make changes, and submit a pull request. Report issues or suggest features via GitHub Issues.
📜 License
MIT License. See LICENSE for details.
🙌 Acknowledgments

Hugging Face for the distilbart-cnn-12-6 model.
Tesseract OCR for text extraction.
Streamlit and customtkinter for user interfaces.

