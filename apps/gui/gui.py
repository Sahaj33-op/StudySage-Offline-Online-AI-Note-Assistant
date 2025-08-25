import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime
import os
from core.summarize import summarize_text, load_text_from_file
from core.ocr_reader import extract_text_from_image
from core.export_pdf import export_summary_to_pdf
from core.io import load_text_from_file

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

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
        ctk.CTkButton(self, text="💾 Save as .txt", command=self.save_txt).pack(pady=4)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Supported files", "*.txt *.md *.jpg *.jpeg *.png *.pdf")])
        if path:
            self.file_path = path
            ext = Path(path).suffix.lower()
            try:
                if ext in ['.txt', '.md']:
                    self.text_data = load_text_from_file(path)
                elif ext in ['.jpg', '.jpeg', '.png']:
                    self.text_data = extract_text_from_image(path)
                elif ext == '.pdf':
                    self.text_data = load_text_from_file(path)
                else:
                    messagebox.showerror("Error", "Unsupported file type.")
                    return
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", self.text_data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def do_summary(self):
        if not self.text_data:
            messagebox.showwarning("⚠️ No text", "Please load a file or run OCR first.")
            return
        try:
            summary = summarize_text(self.text_data, min_len=50, max_len=200, config={"mode": "offline"})
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", summary)
            self.text_data = summary
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate summary: {str(e)}")

    def do_ocr(self):
        if not self.file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            messagebox.showerror("Error", "Please select an image file for OCR.")
            return
        try:
            self.text_data = extract_text_from_image(self.file_path)
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", self.text_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to perform OCR: {str(e)}")

    def export_pdf(self):
        if not self.text_data:
            messagebox.showwarning("⚠️ No text", "Nothing to export.")
            return
        try:
            name = OUTPUT_DIR / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            export_summary_to_pdf(self.text_data)
            messagebox.showinfo("✅ Done", f"Saved PDF to {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")

    def save_txt(self):
        if not self.text_data:
            messagebox.showwarning("⚠️ No text", "Nothing to save.")
            return
        try:
            name = OUTPUT_DIR / f"text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(name, 'w', encoding='utf-8') as f:
                f.write(self.text_data)
            messagebox.showinfo("✅ Done", f"Saved .txt to {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text: {str(e)}")

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = StudySageApp()
    app.mainloop()