from transformers import pipeline
from pathlib import Path
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def load_text_from_file(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError("File not found.")
    return path.read_text(encoding='utf-8')

def summarize_text(text, min_len=30, max_len=200):
    print(Fore.BLUE + "[+] Loading summarization model (offline)...")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    summary_text = summary[0]['summary_text']

    print(Fore.YELLOW + "\n📄 Summary:\n")
    print(summary_text)

    save = input(Fore.CYAN + "\n💾 Save summary to file? (y/n): ").strip().lower()
    if save == 'y':
        filename = OUTPUT_DIR / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        print(Fore.GREEN + f"✅ Saved to {filename}")

    return summary_text

def main():
    print("🧠 Welcome to StudySage - Offline Note Summarizer")
    file_path = input("Enter the path to your .txt or .md note file: ")

    try:
        text = load_text_from_file(file_path)
        print("[✓] Text loaded. Summarizing...\n")
        summarize_text(text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
