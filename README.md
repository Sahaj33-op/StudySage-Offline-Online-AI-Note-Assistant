
## 🧠 StudySage – Offline & Online AI Note Assistant

```

               ░██████╗████████╗██╗░░░██╗██████╗░██╗░░░██╗  ░██████╗░█████╗░░██████╗░███████╗
               ██╔════╝╚══██╔══╝██║░░░██║██╔══██╗╚██╗░██╔╝  ██╔════╝██╔══██╗██╔════╝░██╔════╝
               ╚█████╗░░░░██║░░░██║░░░██║██║░░██║░╚████╔╝░  ╚█████╗░███████║██║░░██╗░█████╗░░
               ░╚═══██╗░░░██║░░░██║░░░██║██║░░██║░░╚██╔╝░░  ░╚═══██╗██╔══██║██║░░╚██╗██╔══╝░░
               ██████╔╝░░░██║░░░╚██████╔╝██████╔╝░░░██║░░░  ██████╔╝██║░░██║╚██████╔╝███████╗
               ╚═════╝░░░░╚═╝░░░░╚═════╝░╚═════╝░░░░╚═╝░░░  ╚═════╝░╚═╝░░╚═╝░╚═════╝░╚══════╝

                           StudySage – Offline AI Note Assistant by Sahaj33
```

> AI-powered summary & quiz generator with OCR, PDF export, offline/online modes, and Streamlit/GUI/CLI support.

<a href="https://studysage-sahaj33.streamlit.app/" target="blank">
    <img src="https://img.shields.io/badge/Deployed%20on-Streamlit-ff4b4b?logo=streamlit" alt="Streamlit Deploy">
  
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Offline AI](https://img.shields.io/badge/Offline%20AI-Yes-green)]()
[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)

<p align="center">
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-key-features">✨ Key Features</a> •
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-project-structure">📂 Project Structure</a> •
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-online-vs-offline-mode">🧠 Online vs Offline Mode</a> •
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-quickstart">🚀 Quickstart</a> •
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-gui-customtkinter">🖼 GUI (CustomTkinter)</a>
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#%EF%B8%8F-setup-instructions">⚙️ Setup Instructions</a>
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-credits">🧠 Credits</a>
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-license">📜 License</a>
  <a href="https://github.com/Sahaj33-op/StudySage-Offline-AI-Note-Assistant?tab=readme-ov-file#-author">🙌 Author</a>
</p>
---

## ✨ Key Features

| Feature                     | Description                                                    |
| --------------------------- | -------------------------------------------------------------- |
| 📝 Summary Generation       | Summarize text files, markdown, PDFs, or OCR'd images using AI |
| 🧪 Quiz Question Generator  | Create MCQs from summaries with distractors                    |
| 🖼 OCR from Images          | Extract text from `.jpg/.png` via Tesseract                    |
| 📄 PDF Export (Manual)      | Export summary/quiz to PDF with user confirmation              |
| 💾 Save to Text File        | Save generated content to `.txt`                               |
| 🔄 Online & Offline Mode    | Choose between offline summarizer or Hugging Face API          |
| 🌐 Streamlit Web UI         | Sleek, scrollable web interface with PDF download buttons      |
| 🖥 Desktop GUI              | CustomTkinter GUI version for local use                        |
| 🧪 Smart CLI Interface      | Modular feature selection, input flow control, minimal logs    |
| 🧠 Hugging Face API Support | Uses `sshleifer/distilbart-cnn-12-6` offline or via token      |

---

## 📂 Project Structure

```
StudySage/
├── app.py                  # Streamlit Web UI
├── main.py                 # CLI mode entry
├── gui.py                  # Desktop GUI
├── export_pdf.py           # PDF generation
├── quiz_gen.py             # Quiz generator logic
├── summarize_text.py       # Summary generator logic
├── ocr_reader.py           # OCR image text reader
├── requirements.txt        # Python dependencies
├── README.md               # Project overview
├── LICENSE                 # MIT License
├── output/                 # (gitignored) Generated files
├── assets/                 # Logo, banner, optional GUI images
└── .gitignore              # Clean repo config
```

---

## 🧠 Online vs Offline Mode

| Mode    | Summary Engine                    | Quiz Engine | OCR | Requires Internet |
| ------- | --------------------------------- | ----------- | --- | ----------------- |
| Offline | Local model (DistilBART)          | Local NLTK  | Yes | ❌                 |
| Online  | HuggingFace API (faster & better) | Local NLTK  | Yes | ✅ (API key)       |

To use online mode, generate a Hugging Face token: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## 🚀 Quickstart

### 🖥 CLI Mode

```bash
python main.py
```

* Choose Offline or Online
* Enter note file (`.txt`, `.pdf`, `.md`, `.jpg`, `.png`)
* Set summary word range (optional)
* Generate summary
* Prompt: Want to generate quiz? (y/n)
* Prompt: Save summary/quiz as PDF? (y/n)
* Output shown in clean format

---

### 🌐 Streamlit Web App

```bash
streamlit run app.py
```

* Upload file
* Choose features: Summary, Quiz
* Customize summary range
* Click **Process**
* Auto-scrolls to output
* Buttons to download PDF

> 🧠 Supports session memory — doesn’t lose results after button clicks!

---

### 🖼 GUI (CustomTkinter)

```bash
python gui.py
```

* Pick file with **Choose File**
* Click buttons:

  * Generate Summary
  * OCR (Image)
  * Export PDF
  * Save as .txt

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

* Python 3.10+
* pip
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

  * Windows: Add to PATH or set `tesseract_cmd` in code
  * Linux: `sudo apt install tesseract-ocr`
  * macOS: `brew install tesseract`

---

### 🧪 Create a Virtual Environment (Optional but Recommended)

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

---

### 📦 Install Requirements

```bash
pip install -r requirements.txt
```

If using HuggingFace online mode, download tokenizer models on first use.

---

## 📥 Packaging as Executable (.exe)

You can package this into a standalone `.exe` for easy Windows sharing:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py      # For CLI exe
pyinstaller --onefile --windowed gui.py       # For GUI exe
```

> Result will appear in `/dist`. These are excluded from Git tracking via `.gitignore`.

---

## 🔐 Clean GitHub Repo (.gitignore)

Git ignores:

* `output/` PDFs and temporary files
* `models/`, `__pycache__/`, `.DS_Store`
* PyInstaller build files (`build/`, `dist/`, `main.spec`)
* `config.json` (contains sensitive keys)

✅ Run:

```bash
git add .
git commit -m "Clean project, add new features"
git push origin main
```

---

## 🧠 Credits

* Hugging Face (`transformers`)
* `sshleifer/distilbart-cnn-12-6` model
* Streamlit
* PyMuPDF, ReportLab, Pillow
* Tesseract OCR

---

## 📜 License

Licensed under the [MIT License](LICENSE)

---

## 🙌 Author

Made with ❤️ by **[Sahaj33](https://github.com/Sahaj33-op)**
Let’s empower learning with AI!

---
