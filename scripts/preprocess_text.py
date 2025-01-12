import os
import re

# Directory paths
INPUT_DIR = "F:/IIT-K-H/new/Data/extracted_text"  # Folder with extracted text files
OUTPUT_DIR = "F:/IIT-K-H/new/Data/preprocessed_text"  # Folder to save preprocessed text files

def preprocess_text(raw_text):
    """
    Preprocess and structure the raw text into sections.
    Args:
        raw_text (str): Raw text extracted from a PDF.
    Returns:
        dict: A dictionary containing structured sections.
    """
    # Remove extra whitespaces
    text = re.sub(r"\s+", " ", raw_text)

    # Define sections to extract
    sections = {
        "Abstract": "",
        "Introduction": "",
        "Methodology": "",
        "Results": "",
        "Discussion": "",
        "Conclusion": ""
    }

    # Use regex to identify sections
    for section in sections.keys():
        match = re.search(rf"(?i){section}[:\s]*(.*?)(?=\n[A-Z][a-z]|\Z)", text, re.DOTALL)
        if match:
            sections[section] = match.group(1).strip()

    return sections

def save_preprocessed_text(sections, output_path):
    """
    Save the structured sections to a file.
    Args:
        sections (dict): Dictionary of structured sections.
        output_path (str): Path to save the preprocessed text.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for section, content in sections.items():
            f.write(f"{section}:\n{content}\n\n")

def main():
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Process each extracted text file in the input directory
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".txt"):
            input_path = os.path.join(INPUT_DIR, file_name)
            output_path = os.path.join(OUTPUT_DIR, file_name)

            print(f"Processing file: {file_name}")
            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            # Preprocess the text
            structured_sections = preprocess_text(raw_text)

            # Save the preprocessed text
            save_preprocessed_text(structured_sections, output_path)
            print(f"Preprocessed text saved to: {output_path}")

if __name__ == "__main__":
    main()
