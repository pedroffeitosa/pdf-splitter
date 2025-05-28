import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from pdf_splitter import split_pdf
import os
from PyPDF2 import PdfReader

class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")
        self.root.geometry("600x600")  # Aumentei a altura para acomodar os novos controles
        
        # Variáveis
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.num_parts = tk.IntVar(value=5)
        self.total_pages = tk.IntVar(value=0)
        self.rotation = tk.IntVar(value=0)
        self.compress = tk.BooleanVar(value=False)
        
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
        
        # Pasta de saída
        output_frame = ttk.LabelFrame(main_frame, text="Pasta de Saída", padding="10")
        output_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, width=50)
        output_entry.grid(row=0, column=0, padx=5)
        
        output_button = ttk.Button(
            output_frame,
            text="Escolher",
            command=self.browse_output_dir
        )
        output_button.grid(row=0, column=1, padx=5)
        
        # Configurações
        parts_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        parts_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Número de partes
        ttk.Label(parts_frame, text="Número de partes:").grid(row=0, column=0, padx=5)
        parts_spinbox = ttk.Spinbox(
            parts_frame,
            from_=2,
            to=100,
            textvariable=self.num_parts,
            width=10,
            command=self.update_pages_per_part
        )
        parts_spinbox.grid(row=0, column=1, padx=5)
        
        # Rotação
        ttk.Label(parts_frame, text="Rotação:").grid(row=1, column=0, padx=5, pady=5)
        rotation_frame = ttk.Frame(parts_frame)
        rotation_frame.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Radiobutton(
            rotation_frame,
            text="0°",
            variable=self.rotation,
            value=0
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            rotation_frame,
            text="90°",
            variable=self.rotation,
            value=90
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            rotation_frame,
            text="180°",
            variable=self.rotation,
            value=180
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            rotation_frame,
            text="270°",
            variable=self.rotation,
            value=270
        ).pack(side=tk.LEFT, padx=5)
        
        # Compressão
        ttk.Checkbutton(
            parts_frame,
            text="Comprimir PDF",
            variable=self.compress
        ).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Informações do PDF
        info_frame = ttk.LabelFrame(main_frame, text="Informações do PDF", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.pages_label = ttk.Label(info_frame, text="Total de páginas: 0")
        self.pages_label.grid(row=0, column=0, padx=5)
        
        self.pages_per_part_label = ttk.Label(info_frame, text="Páginas por parte: 0")
        self.pages_per_part_label.grid(row=0, column=1, padx=5)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Botão de processamento
        process_button = ttk.Button(
            main_frame,
            text="Dividir PDF",
            command=self.process_pdf
        )
        process_button.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Status
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=("Helvetica", 10)
        )
        self.status_label.grid(row=7, column=0, columnspan=2)
        
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.input_file.set(filename)
            self.update_pdf_info()
            # Define a pasta de saída como a mesma do arquivo de entrada
            self.output_dir.set(os.path.dirname(filename))
            
    def browse_output_dir(self):
        dirname = filedialog.askdirectory(
            title="Selecione a pasta de saída"
        )
        if dirname:
            self.output_dir.set(dirname)
            
    def update_pdf_info(self):
        try:
            reader = PdfReader(self.input_file.get())
            self.total_pages.set(len(reader.pages))
            self.pages_label.config(text=f"Total de páginas: {self.total_pages.get()}")
            self.update_pages_per_part()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o PDF: {str(e)}")
            
    def update_pages_per_part(self, *args):
        if self.total_pages.get() > 0:
            parts = self.num_parts.get()
            pages_per_part = (self.total_pages.get() + parts - 1) // parts
            self.pages_per_part_label.config(
                text=f"Páginas por parte: {pages_per_part}"
            )
            
    def process_pdf(self):
        input_file = self.input_file.get()
        output_dir = self.output_dir.get()
        
        if not input_file:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF.")
            return
            
        if not os.path.exists(input_file):
            messagebox.showerror("Erro", "O arquivo selecionado não existe.")
            return
            
        if not output_dir:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de saída.")
            return
            
        try:
            self.status_label.config(text="Processando...")
            self.progress["value"] = 0
            self.root.update()
            
            # Atualiza a função split_pdf para usar as novas opções
            split_pdf(
                input_file,
                self.num_parts.get(),
                output_dir,
                self.rotation.get(),
                self.compress.get()
            )
            
            self.progress["value"] = 100
            self.status_label.config(text="PDF dividido com sucesso!")
            messagebox.showinfo("Sucesso", "O PDF foi dividido com sucesso!")
        except Exception as e:
            self.status_label.config(text="")
            self.progress["value"] = 0
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def main():
    root = ThemedTk(theme="arc")
    app = PDFSplitterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 