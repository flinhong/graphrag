import pymupdf4llm
from pathlib import Path
from markdown import markdown
from bs4 import BeautifulSoup
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Get the current script's directory
script_directory = Path(__file__).parent

# define paths
file_name = "10.1088@1361-6463@ac9066.pdf"
pdf_path = script_directory.parent / "passivation/pdf" / file_name
pdf_ocr_path = script_directory.parent / "passivation/pdf_ocr" / file_name.replace('.pdf', '.txt')
markdown_path = script_directory.parent / "passivation/markdown" / file_name.replace('.pdf', '.md')
text_path = script_directory.parent / "passivation/input" / file_name.replace('.pdf', '.txt')


# Convert PDF pages to images then extract text
def extract_text_from_pdf(pdf_path, output_text_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # List to hold text from each page
    text_list = []

    # Iterate over each page in the PDF
    for page_number in range(len(pdf_document)):
        # Load the page
        page = pdf_document.load_page(page_number)
        
        # Render the page as an image
        pix = page.get_pixmap()
        
        # Convert the image to bytes
        img_bytes = pix.tobytes()
        
        # Create a PIL image from bytes
        img = Image.open(io.BytesIO(img_bytes))
        
        # Perform OCR on the image
        text = pytesseract.image_to_string(img)
        
        # Append the extracted text to the list
        text_list.append(f"--- Page {page_number + 1} ---\n{text}\n")

    # Combine all text into one string
    full_text = "\n".join(text_list)

    # Save the extracted text to a file
    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write(full_text)

    print("Text extraction complete. Check the output file.")

# extract_text_from_pdf(pdf_path, pdf_ocr_path)


# extract to markdown file
md_text = pymupdf4llm.to_markdown(pdf_path)
Path(markdown_path).write_bytes(md_text.encode())


# Define a regex pattern to find the "References" section and everything after it
# This pattern assumes the "References" section is located on a single line
# pattern = r'(?i)^References\s*$[\s\S]*'  # Case-insensitive match for "References", "references", "REFERENCES", etc.
pattern = r'^(?:\*\*References\*\*|References).*'

# Remove unwanted sections using regex
# Replace the "References" section and everything after it with an empty string
cleaned_content = re.sub(pattern, '', md_text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)

# Convert Markdown to HTML
html_content = markdown(cleaned_content)

# Use BeautifulSoup to extract plain text
soup = BeautifulSoup(html_content, 'html.parser')
plain_text = soup.get_text()

Path(text_path).write_bytes(plain_text.encode())
