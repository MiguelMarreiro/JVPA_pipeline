# Auto Pipeline — Document Processor

A small document processing pipeline to split articles and extraxt data from a structured source file


## Source file structure
ARTICLE_START = "==Artigo_inicio=="
METADATA_FIELDS = ["Titulo", "SubTitulo", "Autor", "Data", "Tag", "Pag", "Numero", "Imagens"]

There cannot be new lines in the content of any metadata field
Rodape must be the last field of the article, after the body 


## Features
- Simple word extraction and processing utilities.
- Streamlit web UI for interactive processing (word_processor_streamlit.py, word_processor_streamlit_multi.py).
- CSV output

## Requirements
- Python 3.8+
- See `doc_processor/requirements.txt` for Python dependencies.

## Setup
1. Create and activate a virtual environment:

   - Windows (PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r doc_processor/requirements.txt
   ```

   - Windows (cmd):

   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate.bat
   pip install -r doc_processor/requirements.txt
   ```

## Running the Streamlit app
Launch the interactive app (multi-file Streamlit UI):

```bash
streamlit run doc_processor/word_processor_streamlit_multi.py
```

Or run the single-file Streamlit app:

```bash
streamlit run doc_processor/word_processor_streamlit.py
```

## Quick CLI usage
- Run example/test script(s):

```bash
python doc_processor/test.py
python doc_processor/test2.py
```

## Project layout
- `doc_processor/` — core processing scripts and Streamlit UIs..
  - `word_processor_streamlit.py` — Streamlit docx UI.
  - `word_processor_streamlit_multi.py` — Streamlit docx and odt UI.
  - `requirements.txt` — Python deps for the doc processor.



## Notes & Next steps
- The Streamlit apps are the quickest way to try the pipeline interactively.
- If you want, I can add a short CONTRIBUTING guide, CI test commands, or package the processor.

---
Created for the document processing pipeline in this repository.
