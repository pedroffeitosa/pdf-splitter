import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from pdf_splitter import split_pdf
import os

class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")
        self.root.geometry("600x400")
        
        # Variáveis
        self.input_file = tk.StringVar()
        self.num_parts = tk.IntVar(value=5)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="PDF Splitter",
            font=("Helvetica", 24, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Seleção de arquivo
        file_frame = ttk.LabelFrame(main_frame, text="Arquivo PDF", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        file_entry = ttk.Entry(file_frame, textvariable=self.input_file, width=50)
        file_entry.grid(row=0, column=0, padx=5)
        
        browse_button = ttk.Button(
            file_frame,
            text="Procurar",
            command=self.browse_file
        )
        browse_button.grid(row=0, column=1, padx=5)
        
        # Número de partes
        parts_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        parts_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(parts_frame, text="Número de partes:").grid(row=0, column=0, padx=5)
        parts_spinbox = ttk.Spinbox(
            parts_frame,
            from_=2,
            to=100,
            textvariable=self.num_parts,
            width=10
        )
        parts_spinbox.grid(row=0, column=1, padx=5)
        
        # Botão de processamento
        process_button = ttk.Button(
            main_frame,
            text="Dividir PDF",
            command=self.process_pdf,
            style="Accent.TButton"
        )
        process_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Status
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=("Helvetica", 10)
        )
        self.status_label.grid(row=4, column=0, columnspan=2)
        
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.input_file.set(filename)
            
    def process_pdf(self):
        input_file = self.input_file.get()
        if not input_file:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF.")
            return
            
        if not os.path.exists(input_file):
            messagebox.showerror("Erro", "O arquivo selecionado não existe.")
            return
            
        try:
            self.status_label.config(text="Processando...")
            self.root.update()
            
            split_pdf(input_file, self.num_parts.get())
            
            self.status_label.config(text="PDF dividido com sucesso!")
            messagebox.showinfo("Sucesso", "O PDF foi dividido com sucesso!")
        except Exception as e:
            self.status_label.config(text="")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def main():
    root = ThemedTk(theme="arc")
    app = PDFSplitterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 