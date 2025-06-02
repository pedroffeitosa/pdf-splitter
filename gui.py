import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from pdf_splitter import split_pdf, estimate_processing_time
import os
from PyPDF2 import PdfReader
import threading
import time

class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")
        
        # Theme configuration
        self.current_theme = tk.StringVar(value="arc")  # Default light theme
        self.root.set_theme(self.current_theme.get())
        
        # Configuração inicial para tela cheia
        self.root.attributes('-zoomed', True)  # Para Linux
        self.root.minsize(800, 600)  # Tamanho mínimo da janela
        
        # Variáveis
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.num_parts = tk.IntVar(value=5)
        self.total_pages = tk.IntVar(value=0)
        self.rotation = tk.IntVar(value=0)
        self.compress = tk.BooleanVar(value=False)
        self.is_fullscreen = tk.BooleanVar(value=True)
        self.processing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar o grid para expandir
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Barra de título personalizada
        title_bar = ttk.Frame(main_frame)
        title_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Título
        title_label = ttk.Label(
            title_bar,
            text="PDF Splitter",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Theme toggle button
        self.theme_button = ttk.Button(
            title_bar,
            text="🌙",  # Moon symbol for dark mode
            width=3,
            command=self.toggle_theme
        )
        self.theme_button.pack(side=tk.RIGHT, padx=5)
        
        # Botão de tela cheia
        fullscreen_button = ttk.Button(
            title_bar,
            text="⛶",  # Símbolo de tela cheia
            width=3,
            command=self.toggle_fullscreen
        )
        fullscreen_button.pack(side=tk.RIGHT)
        
        # Seleção de arquivo
        file_frame = ttk.LabelFrame(main_frame, text="Arquivo PDF", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        file_frame.grid_columnconfigure(0, weight=1)
        
        file_entry = ttk.Entry(file_frame, textvariable=self.input_file)
        file_entry.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        
        browse_button = ttk.Button(
            file_frame,
            text="Procurar",
            command=self.browse_file
        )
        browse_button.grid(row=0, column=1, padx=5)
        
        # Pasta de saída
        output_frame = ttk.LabelFrame(main_frame, text="Pasta de Saída", padding="10")
        output_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        output_frame.grid_columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir)
        output_entry.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        
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
        
        # Frame para detalhes da divisão
        division_frame = ttk.Frame(info_frame)
        division_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.division_label = ttk.Label(division_frame, text="")
        self.division_label.pack()
        
        # Barra de progresso
        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            mode="determinate"
        )
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Status e tempo estimado
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="",
            font=("Helvetica", 10)
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.estimated_time_label = ttk.Label(
            self.status_frame,
            text="",
            font=("Helvetica", 10)
        )
        self.estimated_time_label.pack(side=tk.RIGHT)
        
        # Botão de processamento
        self.process_button = ttk.Button(
            main_frame,
            text="Dividir PDF",
            command=self.process_pdf
        )
        self.process_button.grid(row=7, column=0, columnspan=2, pady=20)
        
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_theme.get() == "arc":
            self.current_theme.set("equilux")  # Dark theme
            self.theme_button.configure(text="☀️")  # Sun symbol for light mode
        else:
            self.current_theme.set("arc")  # Light theme
            self.theme_button.configure(text="🌙")  # Moon symbol for dark mode
        
        # Apply the new theme
        self.root.set_theme(self.current_theme.get())
        
        # Update widget styles for better dark mode compatibility
        if self.current_theme.get() == "equilux":
            style = ttk.Style()
            style.configure("TLabel", foreground="white")
            style.configure("TButton", foreground="white")
            style.configure("TCheckbutton", foreground="white")
            style.configure("TRadiobutton", foreground="white")
        else:
            style = ttk.Style()
            style.configure("TLabel", foreground="black")
            style.configure("TButton", foreground="black")
            style.configure("TCheckbutton", foreground="black")
            style.configure("TRadiobutton", foreground="black")
        
    def toggle_fullscreen(self):
        if self.is_fullscreen.get():
            self.root.attributes('-zoomed', False)
            self.is_fullscreen.set(False)
        else:
            self.root.attributes('-zoomed', True)
            self.is_fullscreen.set(True)
        
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
            
            # Update estimated time
            file_size_mb = os.path.getsize(self.input_file.get()) / (1024 * 1024)
            self.update_estimated_time(file_size_mb, self.total_pages.get())
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o PDF: {str(e)}")
            
    def update_pages_per_part(self, *args):
        if self.total_pages.get() > 0:
            total = self.total_pages.get()
            parts = self.num_parts.get()
            
            # Calcula a divisão exata
            base_pages = total // parts
            extra_pages = total % parts
            
            # Cria a mensagem detalhada
            message = "Divisão das páginas:\n"
            current_page = 1
            
            for i in range(parts):
                pages_in_part = base_pages + (1 if i < extra_pages else 0)
                end_page = current_page + pages_in_part - 1
                message += f"Parte {i+1}: páginas {current_page} a {end_page} ({pages_in_part} páginas)\n"
                current_page = end_page + 1
            
            self.division_label.config(text=message)
            
    def update_progress(self, progress: float, message: str):
        """Update progress bar and status message."""
        if progress < 0:  # Error occurred
            self.status_label.config(text=f"Erro: {message}")
            self.progress["value"] = 0
            self.process_button.config(state="normal")
            self.processing = False
            return
            
        self.progress["value"] = progress
        self.status_label.config(text=message)
        
        if progress >= 100:
            self.status_label.config(text="PDF dividido com sucesso!")
            self.process_button.config(state="normal")
            self.processing = False
            messagebox.showinfo("Sucesso", "O PDF foi dividido com sucesso!")
    
    def update_estimated_time(self, file_size_mb: float, total_pages: int):
        """Update estimated processing time display."""
        estimated_seconds = estimate_processing_time(file_size_mb, total_pages)
        minutes = int(estimated_seconds // 60)
        seconds = int(estimated_seconds % 60)
        self.estimated_time_label.config(
            text=f"Tempo estimado: {minutes} min {seconds} seg"
        )
    
    def process_pdf(self):
        if self.processing:
            return
            
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
            self.processing = True
            self.process_button.config(state="disabled")
            self.status_label.config(text="Processando...")
            self.progress["value"] = 0
            self.root.update()
            
            # Calculate file size in MB
            file_size_mb = os.path.getsize(input_file) / (1024 * 1024)
            self.update_estimated_time(file_size_mb, self.total_pages.get())
            
            # Start processing in a separate thread
            thread = threading.Thread(
                target=split_pdf,
                args=(
                    input_file,
                    self.num_parts.get(),
                    output_dir,
                    self.rotation.get(),
                    self.compress.get(),
                    self.update_progress
                )
            )
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.status_label.config(text="")
            self.progress["value"] = 0
            self.process_button.config(state="normal")
            self.processing = False
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def main():
    root = ThemedTk(theme="arc")  # Start with light theme
    app = PDFSplitterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 