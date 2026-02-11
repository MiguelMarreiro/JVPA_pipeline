from docx import Document
import streamlit as st
import re
import pandas as pd
from io import StringIO
import os
from odf.opendocument import load
from odf.text import P, H, LineBreak


#Global definition of article delimiters and field identifiers
ARTICLE_START = "==Artigo_inicio=="
METADATA_FIELDS = ["Titulo", "SubTitulo", "Autor", "Data", "Tag", "Pag", "Numero", "Imagens"]



def extract_text_from_word(file, file_extension):
    """Extract all text from a Word document."""
    if file_extension == ".docx":
        doc = Document(file)
        text = [paragraph_to_html(p).removeprefix("<p>").removesuffix("</p>") for p in doc.paragraphs]
        return '\n'.join(text)
    elif file_extension == ".odt":
        """
        Extract text from ODT. Collects <text:p> text nodes in document order.
        """
        doc = load(file)
        lines = []
        paragraphs = doc.getElementsByType(P)
        for paragraph in paragraphs:
            text_str = "".join(getattr(n, "data", "") for n in paragraph.childNodes).strip()
            if text_str:
                lines.append(text_str)


    return "\n".join(lines)

def article_split(text):
    """Split articles and extract body and metadata."""
    raw_articles = text.split(ARTICLE_START)
    articles = []

    # loops articles
    for raw_article in raw_articles:
        raw_article = raw_article.strip()
        if not raw_article:
            continue #skip empty articles

        lines = [line.strip() for line in raw_article.splitlines() if line.strip()]
        
        metadata = {}
        body_lines = []

        # loops lines to find metadata fields to add them to the metadat dictionary
        for line in lines:
            # print(line)
            if any(line.startswith(f"#{field}:") for field in METADATA_FIELDS):
                key, value = line.split(":", 1)
                
                field = key.lstrip("#").rstrip()
                metadata[field] = value.strip()
                
            # everything else appends to body
            else:
                body_lines.append(line)
        try:
            (metadata["BODY"], metadata["Rodape"]) = ("\n".join(body_lines).strip()).split("#Rodape:", 1)
        except:
            metadata["BODY"] = "\n".join(body_lines).strip()

        # Fill missing metadata keys with empty string
        for field in METADATA_FIELDS:
            if field not in metadata:
                metadata[field] = ""

        articles.append(metadata)

    return articles


def paragraph_to_html(paragraph):
    html = ""
    for run in paragraph.runs:
        text = run.text
        if run.bold:
            text = f"<b>{text}</b>"
        if run.italic:
            text = f"<i>{text}</i>"
        if run.underline:
            text = f"<u>{text}</u>"
        html += text
    return f"<p>{html}</p>"

# def data_extract(articles):
#     csv = []
#     for article in articles:
#         [title, body] = re.split(r'(?:\n\s*){3,}', article)
#         csv.append({"Title": title, "Body": body})
#     return csv 



if __name__ == "__main__":
    # --- Streamlit app ---
    st.title("📄 Separador Automático de artigos")
    st.write("Faça upload do documento.docx ou .odt para separar automaticamente artigos separados por 3 linhas brancas")

    uploaded_file = st.file_uploader("Escolha um documento .docx", type=["docx", "odt"])
    

    if uploaded_file:
        filename, file_extension = os.path.splitext(uploaded_file.name)

        text = extract_text_from_word(uploaded_file, file_extension)
        articles = article_split(text)

        # data = data_extract(articles)

        df = pd.DataFrame(articles)

        #Display the DataFrame as a CSV table
        st.success(f"✅ encontrados {len(articles)} artigos.")
        st.dataframe(df)
        
        #Generate CSV for download
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="💾 Download CSV",
            data=csv_data,
            file_name="articles.csv",
            mime="text/csv"
        )

    
        for i, article in enumerate(articles, 1):
            st.subheader(f"Artigo {i}")
            st.text_area(f"{article["Titulo"]}", article["BODY"], height=200)
            if "Rodape" in article.keys():
                st.text_area("Rodapé", article["Rodape"], height=60)


    else:
        st.info("Escolha um documento .docx para começar.")
