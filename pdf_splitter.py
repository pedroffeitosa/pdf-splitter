from PyPDF2 import PdfReader, PdfWriter
import math
import os

def split_pdf(input_path: str, parts: int = 5, output_dir: str = None, rotation: int = 0, compress: bool = False):
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    # Calcula a divisão exata
    base_pages = total_pages // parts
    extra_pages = total_pages % parts

    print(f"Total pages: {total_pages}")
    print(f"Splitting into {parts} parts...")

    # Se não for especificada uma pasta de saída, usa a mesma do arquivo de entrada
    if output_dir is None:
        output_dir = os.path.dirname(input_path)

    current_page = 0
    for i in range(parts):
        # Calcula quantas páginas esta parte terá
        pages_in_part = base_pages + (1 if i < extra_pages else 0)
        end_page = current_page + pages_in_part

        writer = PdfWriter()
        for j in range(current_page, end_page):
            page = reader.pages[j]
            if rotation != 0:
                page.rotate(rotation)
            writer.add_page(page)

        output_filename = os.path.join(output_dir, f"volume_{i + 1}.pdf")
        
        # Configurações de compressão
        if compress:
            writer.add_metadata(reader.metadata)
            with open(output_filename, "wb") as output_file:
                writer.write(output_file, compress=True)
        else:
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)

        print(f"Created: {output_filename} (pages {current_page + 1} to {end_page})")
        current_page = end_page

# Example usage:
# split_pdf("your_file.pdf", parts=5)
