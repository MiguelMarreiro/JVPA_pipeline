from docx import Document
from pathlib import Path
from tkinter import Tk, filedialog
import re

def select_word_file() -> str:
    """
    Open a file dialog to select a Word document.
    
    Returns:
        str: Full path to the selected .docx file, or empty string if cancelled
    """
    root = Tk()
    root.withdraw()  # Hide the root window
    
    file_path = filedialog.askopenfilename(
        title="Select a Word Document",
        filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
    )
    
    root.destroy()
    return file_path


def extract_text_from_word(file_path):
    try:
        #load word document
        doc = Document(file_path)

        #extract all text
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        
        return '\n'.join(text)
    except Exception as e:
        raise ValueError(f"Error reading Word document: {str(e)}")


def article_split(text):
    # Split where there are 3 or more empty lines (any number of \n)
    articles = re.split(r'(?:\n\s*){4,}', text)

    for article in articles:
        print("-----Artigo -----")
        print(article.strip())


if __name__ == '__main__':
    # Simple GUI workflow
    selected_file = select_word_file()
    if selected_file:
        # print(f"Selected file: {selected_file}")
        text = extract_text_from_word(selected_file)
        # print("\nExtracted text:")
        # print(text)
        article_split(text)
    else:
        print("No file selected.")

    