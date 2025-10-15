import sys
from pathlib import Path

# Ensure repo root is on sys.path before core imports
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime
import os

# Import configuration
try:
    from config import OUTPUT_DIR
except ImportError:
    OUTPUT_DIR = "output"

from core.summarize import summarize_text
from core.ocr_reader import extract_text_from_image
from core.export_pdf import export_summary_to_pdf
from core.io import load_text_from_file

OUTPUT_PATH = Path(OUTPUT_DIR)
OUTPUT_PATH.mkdir(exist_ok=True)


class StudySageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StudySage – Offline AI Note Assistant")
        self.geometry("900x600")
        self.file_path = ""
        self.text_data = ""

        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="📘 StudySage – Offline AI Note Assistant", font=("Arial", 20)).pack(pady=15)

        ctk.CTkButton(self, text="📂 Choose File", command=self.load_file).pack()
        self.textbox = ctk.CTkTextbox(self, width=800, height=300)
        self.textbox.pack(pady=10)

        ctk.CTkButton(self, text="🧠 Generate Summary", command=self.do_summary).pack(pady=4)
        ctk.CTkButton(self, text="🖼 OCR (Image to Text)", command=self.do_ocr).pack(pady=4)
        ctk.CTkButton(self, text="📄 Export as PDF", command=self.export_pdf).pack(pady=4)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All Supported", "*.pdf *.txt *.png *.jpg *.jpeg"),
                ("PDF files", "*.pdf"),
                ("Text files", "*.txt"),
                ("Image files", "*.png *.jpg *.jpeg")
            ]
        )
        if not file_path:
            return

        self.file_path = file_path
        try:
            self.text_data = load_text_from_file(file_path)
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", self.text_data)
            messagebox.showinfo("✅ Success", "File loaded successfully!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to load file: {str(e)}")

    def do_summary(self):
        if not self.text_data:
            messagebox.showwarning("⚠️ No text", "Please load a file first.")
            return

        try:
            # Simple config for offline mode
            config = {"mode": "offline", "api_key": ""}
            summary = summarize_text(self.text_data, 30, 150, config)
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", summary)
            self.text_data = summary
            messagebox.showinfo("✅ Done", "Summary generated!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to generate summary: {str(e)}")

    def do_ocr(self):
        if not self.file_path:
            messagebox.showwarning("⚠️ No file", "Please load an image file first.")
            return

        try:
            ocr_text = extract_text_from_image(self.file_path)
            if not ocr_text.strip():
                messagebox.showwarning("⚠️ No text", "No text found in the image.")
                return

            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", ocr_text)
            self.text_data = ocr_text
            messagebox.showinfo("✅ Done", "OCR completed!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"OCR failed: {str(e)}")

    def export_pdf(self):
        if not self.text_data:
            messagebox.showwarning("⚠️ No text", "Nothing to export.")
            return
        try:
            name = OUTPUT_PATH / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            export_summary_to_pdf(self.text_data)
            messagebox.showinfo("✅ Done", f"Saved PDF to {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")

    def save_txt(self):
        if not self.text_data:
            messagebox.showwarning("⚠️ No text", "Nothing to save.")
            return
        try:
            name = OUTPUT_PATH / f"text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(name, 'w', encoding='utf-8') as f:
                f.write(self.text_data)
            messagebox.showinfo("✅ Done", f"Saved .txt to {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text: {str(e)}")

if __name__ == "__main__":
    app = StudySageApp()
    app.mainloop()