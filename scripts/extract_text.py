import os
from PyPDF2 import PdfReader

# Directory paths
INPUT_DIR = "F:/IIT-K-H/new/Data/All_papers"  # Folder containing PDF files
OUTPUT_DIR = "F:/IIT-K-H/new/Data/extracted_text"  # Folder to save extracted text

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: Extracted text.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

def save_text_to_file(text, output_path):
    """
    Saves extracted text to a file.
    Args:
        text (str): Text to save.
        output_path (str): Path to save the text file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Process each PDF in the input directory
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file_name)
            output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_name)[0]}.txt")

            print(f"Processing file: {file_name}")
            text = extract_text_from_pdf(pdf_path)

            if text:
                save_text_to_file(text, output_path)
                print(f"Extracted text saved to: {output_path}")
            else:
                print(f"Failed to extract text from: {file_name}")

if __name__ == "__main__":
    main()
