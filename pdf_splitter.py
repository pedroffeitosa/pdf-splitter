from PyPDF2 import PdfReader, PdfWriter
import math
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Optional
import psutil
import time

def get_optimal_thread_count() -> int:
    """Calculate optimal number of threads based on CPU cores and available memory."""
    cpu_count = os.cpu_count() or 4
    available_memory = psutil.virtual_memory().available
    # Use at most 75% of available CPU cores to leave resources for other processes
    return max(1, min(cpu_count - 1, int(cpu_count * 0.75)))

def process_pdf_part(args: tuple) -> tuple:
    """Process a single part of the PDF in a separate thread."""
    reader, start_page, end_page, output_filename, rotation, compress, metadata = args
    writer = PdfWriter()
    
    for j in range(start_page, end_page):
        page = reader.pages[j]
        if rotation != 0:
            page.rotate(rotation)
        writer.add_page(page)
    
    if compress:
        writer.add_metadata(metadata)
        with open(output_filename, "wb") as output_file:
            writer.write(output_file, compress=True)
    else:
        with open(output_filename, "wb") as output_file:
            writer.write(output_file)
    
    return (output_filename, start_page + 1, end_page)

def split_pdf(
    input_path: str,
    parts: int = 5,
    output_dir: str = None,
    rotation: int = 0,
    compress: bool = False,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> None:
    """
    Split a PDF file into multiple parts using multi-threading.
    
    Args:
        input_path: Path to the input PDF file
        parts: Number of parts to split the PDF into
        output_dir: Directory to save the output files
        rotation: Rotation angle for pages (0, 90, 180, 270)
        compress: Whether to compress the output PDFs
        progress_callback: Optional callback function to report progress
    """
    # Initialize PDF reader
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    metadata = reader.metadata
    
    # Calculate optimal thread count
    thread_count = min(get_optimal_thread_count(), parts)
    
    # Calculate pages per part
    base_pages = total_pages // parts
    extra_pages = total_pages % parts
    
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    
    # Prepare arguments for each part
    tasks = []
    current_page = 0
    for i in range(parts):
        pages_in_part = base_pages + (1 if i < extra_pages else 0)
        end_page = current_page + pages_in_part
        output_filename = os.path.join(output_dir, f"volume_{i + 1}.pdf")
        
        tasks.append((
            reader,
            current_page,
            end_page,
            output_filename,
            rotation,
            compress,
            metadata
        ))
        current_page = end_page
    
    # Process parts using thread pool
    completed_parts = 0
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(process_pdf_part, task) for task in tasks]
        
        for future in as_completed(futures):
            try:
                output_filename, start_page, end_page = future.result()
                completed_parts += 1
                if progress_callback:
                    progress = (completed_parts / parts) * 100
                    progress_callback(progress, f"Processed {output_filename} (pages {start_page} to {end_page})")
            except Exception as e:
                if progress_callback:
                    progress_callback(-1, f"Error processing part: {str(e)}")
                raise e

def estimate_processing_time(file_size_mb: float, total_pages: int) -> float:
    """
    Estimate processing time based on file size and number of pages.
    Returns estimated time in seconds.
    """
    # Rough estimation: 1 second per 10MB + 0.1 second per page
    return (file_size_mb / 10) + (total_pages * 0.1)

# Example usage:
# split_pdf("your_file.pdf", parts=5)
