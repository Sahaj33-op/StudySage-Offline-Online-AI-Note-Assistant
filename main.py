import os
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from pathlib import Path
from quiz_gen import generate_questions
from export_pdf import export_summary_to_pdf, export_quiz_to_pdf
from ocr_reader import extract_text_from_image
from pyfiglet import Figlet
from colorama import Fore, Style, init
from datetime import datetime
import requests
import json
import torch
import re
import platform
import sys
from PIL import Image
import fitz  # PyMuPDF
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")
MODELS_DIR = Path("models")
OUTPUT_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Constants for mode limits
ONLINE_MODE_MAX_CHARS = 4000
ONLINE_MODE_MAX_WORDS = 800
OFFLINE_MODE_MAX_CHARS = 100000
OFFLINE_MODE_MAX_WORDS = 20000

init(autoreset=True)

CONFIG_FILE = Path("config.json")

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"mode": "offline", "api_key": ""}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def download_model():
    print(Fore.BLUE + "[+] Downloading model...")
    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    model_path = MODELS_DIR / model_name.split('/')[-1]
    tokenizer.save_pretrained(model_path)
    model.save_pretrained(model_path)
    print(Fore.GREEN + "[+] Model downloaded.")
    return model_path

def get_model_path():
    model_name = "sshleifer/distilbart-cnn-12-6"
    model_path = MODELS_DIR / model_name.split('/')[-1]
    if not model_path.exists():
        return download_model()
    return model_path

def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_logo():
    clear_terminal()
    f = Figlet(font='slant')
    print(Fore.CYAN + f.renderText("StudySage"))
    print(Fore.YELLOW + "🧠 StudySage – AI Note Assistant by Sahaj33\n")

def print_mode_banner(mode):
    clear_terminal()
    f = Figlet(font='slant')
    print(Fore.CYAN + f.renderText("StudySage"))
    mode_text = "OFFLINE MODE" if mode == "offline" else "ONLINE MODE"
    mode_color = Fore.GREEN if mode == "offline" else Fore.BLUE
    print(mode_color + "=" * 50)
    print(mode_color + f"🎯 {mode_text} ACTIVATED")
    print(mode_color + "=" * 50 + "\n")
    print(Fore.YELLOW + "🧠 StudySage – AI Note Assistant by Sahaj33\n")

def load_text_from_file(file_path: str, lang: str = 'eng') -> str:
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    logger.info(f"Processing file: {file_path} (extension: {ext})")
    
    try:
        if ext in ['.txt', '.md', '.py', '.json', '.csv']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            logger.info(f"Text file extracted: {len(text)} characters")
            return text

        elif ext == '.pdf':
            text = ""
            try:
                doc = fitz.open(file_path)
                logger.info(f"PDF opened with {len(doc)} pages")
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    # First, try to extract text directly
                    page_text = page.get_text("text")
                    if page_text.strip():
                        text += page_text + "\n"
                        logger.info(f"Page {page_num + 1}: Extracted text directly ({len(page_text)} characters)")
                    else:
                        logger.info(f"Page {page_num + 1}: No text extracted directly, falling back to OCR")
                        # Fallback to OCR if no text is extracted
                        pix = page.get_pixmap(dpi=300)
                        img_path = os.path.join("output", f"temp_page_{page_num}.png")
                        pix.save(img_path)
                        ocr_text = extract_text_from_image(img_path, lang)
                        if ocr_text and ocr_text.strip():
                            text += ocr_text + "\n"
                            logger.info(f"Page {page_num + 1}: OCR extracted {len(ocr_text)} characters")
                        else:
                            logger.warning(f"Page {page_num + 1}: OCR extracted no text")
                        os.remove(img_path)
                doc.close()
            except Exception as e:
                logger.error(f"Error extracting text from PDF: {str(e)}")
                raise Exception(f"Error extracting text from PDF: {str(e)}")
            final_text = text.strip()
            logger.info(f"Final PDF text: {len(final_text)} characters")
            return final_text

        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            ocr_text = extract_text_from_image(file_path, lang)
            logger.info(f"Image OCR extracted: {len(ocr_text)} characters")
            return ocr_text

        else:
            logger.error(f"Unsupported file format: {ext}")
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        logger.error(f"Error loading file: {str(e)}")
        raise Exception(f"Error loading file: {str(e)}")

def chunk_text(text, max_length=1024):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def count_words(text):
    return len(text.split())

def count_chars(text):
    return len(text)

def check_text_limits(text, mode):
    words = count_words(text)
    chars = count_chars(text)
    
    if mode == "online":
        if words > ONLINE_MODE_MAX_WORDS or chars > ONLINE_MODE_MAX_CHARS:
            return False, f"Text exceeds online mode limits (max {ONLINE_MODE_MAX_WORDS} words or {ONLINE_MODE_MAX_CHARS} chars)."
    else:
        if words > OFFLINE_MODE_MAX_WORDS or chars > OFFLINE_MODE_MAX_CHARS:
            return False, f"Text exceeds offline mode limits (max {OFFLINE_MODE_MAX_WORDS} words or {OFFLINE_MODE_MAX_CHARS} chars)."
    
    return True, ""

def summarize_text(text, min_len, max_len, config, cli_mode=True):
    within_limits, limit_message = check_text_limits(text, config["mode"])
    if not within_limits:
        if config["mode"] == "online":
            if cli_mode:
                print(Fore.YELLOW + f"\n[!] {limit_message}")
                print(Fore.YELLOW + "Switching to offline mode...")
            config["mode"] = "offline"
            if not (MODELS_DIR / "distilbart-cnn-12-6").exists():
                if cli_mode:
                    download_model()
                else:
                    raise ValueError("Offline model not available. Please download the model or use online mode.")
        else:
            raise ValueError(limit_message)

    if config["mode"] == "offline":
        if cli_mode:
            print(Fore.BLUE + "[+] Using offline model...")
        model_path = get_model_path()
        summarizer = pipeline("summarization", model=str(model_path))
        chunks = chunk_text(text)
        summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        return " ".join(summaries)
    else:
        if cli_mode:
            print(Fore.BLUE + "[+] Using online API...")
        if not config["api_key"]:
            raise ValueError("API key not set for online mode.")
        
        headers = {"Authorization": f"Bearer {config['api_key']}"}
        API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        
        chunks = chunk_text(text)
        summaries = []
        for chunk in chunks:
            response = requests.post(API_URL, headers=headers, json={
                "inputs": chunk,
                "parameters": {
                    "max_length": max_len,
                    "min_length": min_len,
                    "do_sample": False
                }
            })
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.text}")
            
            summaries.append(response.json()[0]['summary_text'])
        
        return " ".join(summaries)

def display_results(summary, questions=None):
    clear_terminal()
    print(Fore.GREEN + "\n📝 Summary:")
    print(Fore.WHITE + summary + "\n")
    
    if questions:
        print(Fore.GREEN + "📝 Quiz Questions:")
        for i, q in enumerate(questions, 1):
            print(Fore.CYAN + f"\nQuestion {i}: {q['question']}")
            print(Fore.YELLOW + "Options:")
            for j, option in enumerate(q["options"], 1):
                print(f"{j}. {option}")
            print(Fore.GREEN + f"Correct Answer: {q['answer']}")

def run_features(choice, text, min_len, max_len, config, last_summary=None):
    summary = last_summary
    questions = None
    
    if choice == "1":  # Summary
        summary = summarize_text(text, min_len, max_len, config)
        display_results(summary)
        
        save_pdf = input(Fore.CYAN + "\n💾 Save summary as PDF? (y/n): ").strip().lower()
        if save_pdf == 'y':
            pdf_path = export_summary_to_pdf(summary)
            print(Fore.GREEN + "✅ Summary PDF saved.")
        
        return summary, None
    
    elif choice == "2":  # Quiz
        if not summary:
            summary = summarize_text(text, min_len, max_len, config)
        num_questions = input(Fore.YELLOW + "Enter number of questions (1-20): ")
        try:
            num_questions = max(1, min(20, int(num_questions)))
        except ValueError:
            num_questions = 5  # Default
            print(Fore.YELLOW + "Invalid input. Using 5 questions.")
        
        print(Fore.BLUE + "[+] Generating quiz...")
        questions = generate_questions(summary, num_questions)
        display_results(summary, questions)
        
        save_pdf = input(Fore.CYAN + "\n💾 Save quiz as PDF? (y/n): ").strip().lower()
        if save_pdf == 'y':
            pdf_path = export_quiz_to_pdf(questions)
            print(Fore.GREEN + "✅ Quiz PDF saved.")
        
        return summary, questions

def setup_mode():
    config = load_config()
    
    while True:
        print(Fore.YELLOW + "\nSelect processing mode:")
        print("1. Offline (slower, no API key)")
        print("2. Online (faster, requires API key)")
        print("3. Exit")
        
        choice = input(Fore.CYAN + "\nEnter choice (1-3): ")
        
        if choice == "1":
            config["mode"] = "offline"
            save_config(config)
            print_mode_banner("offline")
            return config
        
        elif choice == "2":
            api_key = input(Fore.YELLOW + "Enter Hugging Face API key: ").strip()
            if not api_key:
                print(Fore.RED + "❌ API key required for online mode.")
                continue
            
            config["mode"] = "online"
            config["api_key"] = api_key
            save_config(config)
            print_mode_banner("online")
            return config
        
        elif choice == "3":
            print(Fore.YELLOW + "Goodbye!")
            sys.exit(0)
        
        else:
            print(Fore.RED + "❌ Invalid choice.")

def process_file(file_path, mode="online", api_key=None, min_length=30, max_length=200, lang='eng'):
    config = {"mode": mode, "api_key": api_key or ""}
    text = load_text_from_file(file_path, lang=lang)
    if not text:
        return "No text could be extracted from the file. The file may be empty, contain no recognizable text, or OCR may have failed."
    summary = summarize_text(text, min_length, max_length, config, cli_mode=False)
    return summary

def main():
    print_logo()
    config = setup_mode()
    
    last_file_path = None
    last_text = None
    last_summary = None
    last_questions = None
    
    while True:
        print(Fore.YELLOW + "\n📝 Customize Summary Length:")
        length_input = input("Enter min,max (or press Enter for default [30,200]) or type 0 to exit: ")
        
        if length_input == "0":
            print(Fore.YELLOW + "Goodbye!")
            break
        
        try:
            if length_input:
                min_len, max_len = map(int, length_input.split(','))
            else:
                min_len, max_len = 30, 200
        except ValueError:
            print(Fore.RED + "❌ Invalid input. Using default values.")
            min_len, max_len = 30, 200
        
        if not last_file_path:
            print(Fore.YELLOW + "\n📂 Enter note file path (.txt, .md, .pdf, .png/.jpg): ")
            file_path = input().strip()
            
            if not file_path:
                print(Fore.RED + "❌ No file path provided.")
                continue
            
            try:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(Fore.BLUE + "\n🌐 Available OCR languages: https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html")
                    print(Fore.YELLOW + "\n🌐 NOTE: Use high-quality images for best results.")
                    lang = input(Fore.BLUE + "\n🌐 Enter OCR language code (Enter for 'eng'): ").strip() or 'eng'
                    text = load_text_from_file(file_path, lang)
                else:
                    text = load_text_from_file(file_path)
                
                last_file_path = file_path
                last_text = text
                last_summary = None
                last_questions = None
            except Exception as e:
                print(Fore.RED + f"\n❌ Error: {str(e)}")
                input(Fore.YELLOW + "\nPress Enter to continue...")
                continue
        
        print(Fore.YELLOW + "\nSelect feature:")
        print("1. Generate Summary")
        print("2. Generate Quiz")
        print("3. Change File")
        print("4. Back to Mode Selection")
        
        feature_choice = input(Fore.CYAN + "\nEnter choice (1-4): ")
        
        try:
            if feature_choice == "1":
                last_summary, last_questions = run_features("1", last_text, min_len, max_len, config)
                quiz_choice = input(Fore.CYAN + "\nGenerate quiz questions? (y/n): ").strip().lower()
                if quiz_choice == 'y':
                    last_summary, last_questions = run_features("2", last_text, min_len, max_len, config, last_summary)
            
            elif feature_choice == "2":
                last_summary, last_questions = run_features("2", last_text, min_len, max_len, config, last_summary)
            
            elif feature_choice == "3":
                last_file_path = None
                last_text = None
                last_summary = None
                last_questions = None
                continue
            
            elif feature_choice == "4":
                config = setup_mode()
                last_file_path = None
                last_text = None
                last_summary = None
                last_questions = None
                continue
            
            else:
                print(Fore.RED + "❌ Invalid choice.")
            
            input(Fore.GREEN + "\n✅ Press Enter to continue...")
        
        except Exception as e:
            print(Fore.RED + f"\n❌ Error: {str(e)}")
            input(Fore.YELLOW + "\nPress Enter to continue...")

if __name__ == "__main__":
    main()
