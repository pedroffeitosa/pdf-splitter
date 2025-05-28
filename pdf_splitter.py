from PyPDF2 import PdfReader, PdfWriter
import math
import os

def split_pdf(input_path: str, parts: int = 5, output_dir: str = None):
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    pages_per_part = math.ceil(total_pages / parts)

    print(f"Total pages: {total_pages}")
    print(f"Splitting into {parts} parts with up to {pages_per_part} pages each...")

    # Se não for especificada uma pasta de saída, usa a mesma do arquivo de entrada
    if output_dir is None:
        output_dir = os.path.dirname(input_path)

    for i in range(parts):
        start = i * pages_per_part
        end = min((i + 1) * pages_per_part, total_pages)

        writer = PdfWriter()
        for j in range(start, end):
            writer.add_page(reader.pages[j])

        output_filename = os.path.join(output_dir, f"volume_{i + 1}.pdf")
        with open(output_filename, "wb") as output_file:
            writer.write(output_file)

        print(f"Created: {output_filename} (pages {start + 1} to {end})")

# Example usage:
# split_pdf("your_file.pdf", parts=5)
