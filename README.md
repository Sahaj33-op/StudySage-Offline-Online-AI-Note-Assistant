# 🧠 StudySage - AI-Powered Note Assistant

<div align="center">

```
 ██████╗████████╗██╗░░░██╗██████╗░██╗░░░██╗  ░██████╗░█████╗░░██████╗░███████╗
██╔════╝╚══██╔══╝██║░░░██║██╔══██╗╚██╗░██╔╝  ██╔════╝██╔══██╗██╔════╝░██╔════╝
╚█████╗░░░░██║░░░██║░░░██║██║░░██║░╚████╔╝░  ╚█████╗░███████║██║░░██╗░█████╗░░
░╚═══██╗░░░██║░░░██║░░░██║██║░░██║░░╚██╔╝░░  ░╚═══██╗██╔══██║██║░░╚██╗██╔══╝░░
██████╔╝░░░██║░░░╚██████╔╝██████╔╝░░░██║░░░  ██████╔╝██║░░██║╚██████╔╝███████╗
╚═════╝░░░░╚═╝░░░░╚═════╝░╚═════╝░░░░╚═╝░░░  ╚═════╝░╚═╝░░╚═╝░╚═════╝░╚══════╝
```

**Transform your study materials with AI-powered summarization and intelligent quiz generation**


</div>

<p align="center">
  <a href="https://studysage-sahaj33.streamlit.app/" target="blank">
    <img src="https://img.shields.io/badge/Deployed%20on-Streamlit-ff4b4b?logo=streamlit" alt="Streamlit Deploy">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python Version">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Offline%20AI-Yes-green" alt="Offline AI">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-brightgreen" alt="MIT License">
  </a>

## 📖 Overview

StudySage is a comprehensive AI-powered note assistant that revolutionizes how you process and study your documents. With advanced text summarization, intelligent quiz generation, and OCR capabilities, it transforms any document into digestible summaries and interactive learning materials.

### 🎯 Key Highlights

- **🤖 Dual AI Modes**: Choose between offline privacy or online performance
- **📄 Universal File Support**: PDF, TXT, MD, images (PNG, JPG, JPEG)
- **🔍 Advanced OCR**: Extract text from images with multi-language support
- **🧪 Smart Quizzes**: Auto-generate MCQs with intelligent distractors
- **🖥️ Multiple Interfaces**: Web app, desktop GUI, and CLI
- **📱 Cross-Platform**: Windows, macOS, and Linux support

## ✨ Features

<table>
<tr>
<td width="50%">

### 🧠 AI-Powered Processing
- **Text Summarization**: Advanced AI models for concise summaries
- **Quiz Generation**: Intelligent MCQ creation with distractors
- **OCR Technology**: Extract text from images and scanned documents
- **Multi-language Support**: Process documents in multiple languages

</td>
<td width="50%">

### 🛠️ User Experience
- **Multiple Interfaces**: Streamlit web app, desktop GUI, CLI
- **Offline & Online Modes**: Work without internet or use cloud AI
- **PDF Export**: Professional PDF generation for summaries and quizzes
- **Customizable Output**: Adjustable summary length and question count

</td>
</tr>
</table>

## 🚀 Quick Start

### 🌐 Try Online (No Installation Required)
Visit our [**Live Demo**](https://studysage-sahaj33.streamlit.app/) and start processing your documents immediately!

### 💻 Local Installation

#### Prerequisites
- Python 3.10 or higher
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for image processing

#### 1. Clone Repository
```bash
git clone https://github.com/Sahaj33-op/StudySage-Offline-Online-AI-Note-Assistant.git
cd StudySage-Offline-Online-AI-Note-Assistant
```

#### 2. Set Up Environment
```bash
# Create virtual environment (recommended)
python -m venv studysage-env
source studysage-env/bin/activate  # On Windows: studysage-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Tesseract (Required for OCR)

<details>
<summary><strong>Windows Installation</strong></summary>

1. Download and install [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
2. Add to PATH or update `tesseract_cmd` in `ocr_reader.py`
</details>

<details>
<summary><strong>macOS Installation</strong></summary>

```bash
brew install tesseract
```
</details>

<details>
<summary><strong>Linux Installation</strong></summary>

```bash
sudo apt update
sudo apt install tesseract-ocr
# For additional languages
sudo apt install tesseract-ocr-[language-code]
```
</details>

## 🎮 Usage

### 🌐 Web Application (Recommended)
```bash
streamlit run app.py
```

**Features:**
- Drag-and-drop file upload
- Real-time processing
- Interactive quiz interface
- One-click PDF downloads
- Session memory retention

### 🖥️ Desktop GUI
```bash
python gui.py
```

**Features:**
- Native desktop experience
- File browser integration
- Offline processing
- Export capabilities

### 💻 Command Line Interface
```bash
python main.py
```

**Features:**
- Batch processing
- Scriptable automation
- Advanced configuration options
- Minimal resource usage

## 🔧 Configuration

### API Setup for Online Mode

1. **Get Hugging Face API Token**
   - Visit [Hugging Face Tokens](https://huggingface.co/settings/tokens)
   - Create a new token with read permissions
   - Use in online mode for enhanced performance

2. **Mode Comparison**

| Feature | Offline Mode | Online Mode |
|---------|-------------|-------------|
| **Internet Required** | ❌ No | ✅ Yes |
| **Speed** | Moderate | Fast |
| **Privacy** | 🔒 Complete | ⚠️ API-dependent |
| **Model Quality** | Good | Excellent |
| **Setup Complexity** | Low | Medium |

## 📁 Project Architecture

```
StudySage/
├── 🌐 Web Interface
│   ├── app.py                    # Streamlit web application
│   └── assets/                   # Web assets and logos
├── 🖥️ Desktop Interface
│   ├── gui.py                    # CustomTkinter GUI
│   └── main.py                   # CLI application
├── 🧠 Core Engine
│   ├── summarize_text.py         # AI summarization engine
│   ├── quiz_gen.py               # Quiz generation logic
│   ├── ocr_reader.py             # OCR text extraction
│   └── export_pdf.py             # PDF generation
├── 📊 Models & Data
│   ├── models/                   # Local AI models (auto-downloaded)
│   └── output/                   # Generated files (gitignored)
└── 📋 Configuration
    ├── requirements.txt          # Python dependencies
    ├── packages.txt              # System packages (Streamlit Cloud)
    └── config.json               # User configuration (gitignored)
```

## 🎯 Advanced Features

### 📊 Processing Modes

#### Offline Mode
- **Privacy First**: All processing happens locally
- **No Internet Required**: Perfect for sensitive documents
- **Model**: [DistilBART CNN](https://huggingface.co/sshleifer/distilbart-cnn-12-6) (lightweight, efficient)
- **Limits**: 20,000 words / 100,000 characters

#### Online Mode
- **Enhanced Performance**: Cloud-powered AI processing
- **Latest Models**: Access to cutting-edge AI technology
- **API-Based**: Requires Hugging Face token
- **Limits**: 800 words / 4,000 characters per request

### 🔍 OCR Capabilities

**Supported Languages:**
- English (`eng`) - Default
- Hindi (`hin`)
- French (`fra`)
- Spanish (`spa`)
- German (`deu`)
- [50+ additional languages supported](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)

**Input Formats:**
- Images: PNG, JPG, JPEG, BMP, TIFF
- Documents: PDF (with fallback OCR), TXT, MD

### 🧪 Intelligent Quiz Generation

**Features:**
- **Smart Question Selection**: Analyzes text for optimal question candidates
- **Distractor Generation**: Creates plausible wrong answers
- **Multiple Choice Format**: Professional MCQ structure
- **Customizable Count**: 1-20 questions per session
- **Answer Keys**: Included in all output formats

## 📦 Distribution

### 📱 Executable Creation
```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executables
pyinstaller --onefile --windowed main.py      # CLI version
pyinstaller --onefile --windowed gui.py       # GUI version
```

### 🚀 Deployment Options

<details>
<summary><strong>Streamlit Cloud Deployment</strong></summary>

1. Fork this repository
2. Connect to [Streamlit Cloud](https://share.streamlit.io/)
3. Deploy with one click
4. Configure secrets for API keys
</details>

<details>
<summary><strong>Docker Deployment</strong></summary>

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y tesseract-ocr
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```
</details>

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines:

### 🔧 Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/Sahaj33-op/StudySage-Offline-Online-AI-Note-Assistant.git
cd StudySage-Offline-Online-AI-Note-Assistant

# Install development dependencies
pip install -r requirements.txt
pip install black pytest flake8  # Development tools
```

### 📝 Contribution Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 🐛 Issue Reporting
- Use GitHub Issues for bug reports
- Include system information and error logs
- Provide minimal reproducible examples

## 📄 API Documentation

### Core Functions

#### `process_file(file_path, mode, api_key, min_length, max_length, lang)`
Process any supported file and return AI-generated summary.

**Parameters:**
- `file_path` (str): Path to input file
- `mode` (str): Processing mode ("online" or "offline")
- `api_key` (str): Hugging Face API token (for online mode)
- `min_length` (int): Minimum summary length in words
- `max_length` (int): Maximum summary length in words
- `lang` (str): OCR language code (default: "eng")

**Returns:**
- `str`: Generated summary text

#### `generate_questions(summary, num_questions)`
Generate multiple-choice questions from text summary.

**Parameters:**
- `summary` (str): Input text for question generation
- `num_questions` (int): Number of questions to generate (1-20)

**Returns:**
- `list`: Array of question objects with options and answers

## 🛡️ Privacy & Security

### 🔒 Data Handling
- **Offline Mode**: All processing happens locally, no data transmission
- **Online Mode**: Text sent to Hugging Face API, check their privacy policy
- **File Storage**: Temporary files auto-deleted after processing
- **Configuration**: Sensitive data excluded from version control

### 🔐 Best Practices
- Use offline mode for sensitive documents
- API keys stored locally, never committed to repository
- Regular security updates through dependency management

## 📊 Performance Benchmarks

| Operation | Offline Mode | Online Mode |
|-----------|-------------|-------------|
| **Text Summarization** (500 words) | ~10-15 seconds | ~3-5 seconds |
| **Quiz Generation** (5 questions) | ~2-3 seconds | ~2-3 seconds |
| **OCR Processing** (standard image) | ~3-8 seconds | ~3-8 seconds |
| **PDF Export** | ~1-2 seconds | ~1-2 seconds |

*Benchmarks measured on standard hardware with Intel i5 processor*

## 🆘 Troubleshooting

<details>
<summary><strong>Common Issues & Solutions</strong></summary>

**OCR Not Working**
- Ensure Tesseract is properly installed and in PATH
- Verify image quality and text clarity
- Check language pack installation

**Model Download Fails**
- Check internet connection
- Verify sufficient disk space (2GB+ recommended)
- Clear cache: `rm -rf models/` and retry

**API Errors**
- Verify Hugging Face token validity
- Check API rate limits
- Ensure proper token permissions

**Memory Issues**
- Reduce document size or split into smaller files
- Close other applications to free RAM
- Use offline mode for large documents

</details>

## 🏆 Acknowledgments

### 🔧 Technologies Used
- **[Hugging Face Transformers](https://huggingface.co/transformers/)** - AI model infrastructure
- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern desktop GUI
- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** - Optical character recognition
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** - PDF processing
- **[ReportLab](https://www.reportlab.com/)** - PDF generation
- **[NLTK](https://www.nltk.org/)** - Natural language processing

### 🎨 Design Credits
- ASCII art generation with custom styling
- UI/UX inspired by modern design principles
- Logo and branding by StudySage team

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2025 Sahaj
Permission is hereby granted, free of charge, to any person obtaining a copy...
```

## 👨‍💻 Author & Contact

<div align="center">

**Created with ❤️ by [Sahaj33](https://github.com/Sahaj33-op)**

**⭐ Star this repository if you find it helpful!**

</div>

***

<div align="center">

### 🚀 Ready to transform your learning experience?

**[Try StudySage Now](https://studysage-sahaj33.streamlit.app/) -  [Download Latest Release](https://github.com/Sahaj33-op/StudySage-Offline-Online-AI-Note-Assistant/releases) -  [Report Issues](https://github.com/Sahaj33-op/StudySage-Offline-Online-AI-Note-Assistant/issues)**

*Making AI-powered learning accessible to everyone* 🌟

</div>

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/87031716/4c42774d-430f-4b77-b82a-9a4e907fb0d6/StudySage-GitToDoc.txt)
