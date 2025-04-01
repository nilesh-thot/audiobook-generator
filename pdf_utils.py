from PyPDF2 import PdfReader

def extract_specific_pages(pdf_path,pages=None):
    reader=PdfReader(pdf_path)
    if pages is None:
        pages=range(1,len(reader.pages)+1)
    max_page=len(reader.pages)
    valid_pages=[p for p in pages if p<=max_page]
    extracted_text=""
    for page_num in valid_pages:
        page=reader.pages[page_num-1]
        extracted_text+=page.extract_text()
    return extracted_text

def preprocess_text(text):
    text=text.replace("\n"," ")
    text=text.replace(".","\n")
    return text