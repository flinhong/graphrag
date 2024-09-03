import pymupdf4llm
from pathlib import Path
from markdown import markdown
from bs4 import BeautifulSoup
import re


# Get the current script's directory
script_directory = Path(__file__).parent

# define paths
file_name = "10.1088@1361-6463@ac9066.pdf"
pdf_path = script_directory.parent / "passivation/pdf" / file_name
pdf_ocr_path = script_directory.parent / "passivation/pdf_ocr" / file_name.replace('.pdf', '.txt')
markdown_path = script_directory.parent / "passivation/markdown" / file_name.replace('.pdf', '.md')
text_path = script_directory.parent / "passivation/input" / file_name.replace('.pdf', '.txt')


# extract to markdown file
md_text = pymupdf4llm.to_markdown(pdf_path)
Path(markdown_path).write_bytes(md_text.encode())


# Define a regex pattern to find the "References" section and everything after it
# This pattern assumes the "References" section is located on a single line
# pattern = r'(?i)^References\s*$[\s\S]*'  # Case-insensitive match for "References", "references", "REFERENCES", etc.
pattern = r'^(?:\*\*References\*\*|References).*'

# Find all matches with their positions
matches = list(re.finditer(pattern, md_text, flags=re.MULTILINE | re.IGNORECASE))

# # Remove unwanted sections using regex
# # Replace the "References" section and everything after it with an empty string
# # have multiple matches, just deal with the last match
if (matches):
        # Get the position of the last match
    last_match = matches[-1]
    start, end = last_match.span()
    
    # Step 2: Replace the last match using slicing
    cleaned_content = md_text[:start] + ""

# # single match case
# cleaned_content = re.sub(pattern, '', md_text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)

# Convert Markdown to HTML
html_content = markdown(cleaned_content)

# Use BeautifulSoup to extract plain text
soup = BeautifulSoup(html_content, 'html.parser')
plain_text = soup.get_text()

Path(text_path).write_bytes(cleaned_content.encode())
