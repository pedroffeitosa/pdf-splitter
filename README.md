# PDF Splitter

A simple Python script to split large PDF files into smaller parts.

## Features

- Split any PDF into multiple volumes.
- Automatically calculates how many pages go into each part.
- No file size limit — runs locally on your machine.

## Requirements

- Python 3.7+
- `PyPDF2` library

## Setup Instructions

### 1. Clone this repository

```
git clone https://github.com/yourusername/pdf-splitter.git
cd pdf-splitter
```

### 2. Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Add your PDF file

Place the PDF you want to split in the same folder as the script. Rename it to `documento_grande.pdf` or edit the script to match your file name.

### 5. Run the script

```
python pdf_splitter.py
```

## Customization

To split the PDF into a different number of parts, edit the last line of the script:

```python
split_pdf_into_parts("documento_grande.pdf", parts=5)
```

## License

This project is licensed under the MIT License.