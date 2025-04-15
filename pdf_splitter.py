from PyPDF2 import PdfReader, PdfWriter
import math

def split_pdf(input_path: str, parts: int = 5):
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    pages_per_part = math.ceil(total_pages / parts)

    print(f"Total pages: {total_pages}")
    print(f"Splitting into {parts} parts with up to {pages_per_part} pages each...")

    for i in range(parts):
        start = i * pages_per_part
        end = min((i + 1) * pages_per_part, total_pages)

        writer = PdfWriter()
        for j in range(start, end):
            writer.add_page(reader.pages[j])

        output_filename = f"volume_{i + 1}.pdf"
        with open(output_filename, "wb") as output_file:
            writer.write(output_file)

        print(f"Created: {output_filename} (pages {start + 1} to {end})")

# Example usage:
# split_pdf("your_file.pdf", parts=5)
