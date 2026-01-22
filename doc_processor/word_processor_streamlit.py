from docx import Document
import streamlit as st
import re
import pandas as pd
from io import StringIO

def extract_text_from_word(file):
    """Extract all text from a Word document."""
    try:
        doc = Document(file)
        text = [p.text for p in doc.paragraphs]
        return '\n'.join(text)
    except Exception as e:
        raise ValueError(f"Error reading Word document: {str(e)}")


def article_split(text):
    """Split text where there are 3 or more empty lines."""
    articles = re.split(r'(?:\n\s*){4,}', text)
    return [a.strip() for a in articles if a.strip()]


def data_extract(articles):
    csv = []
    for article in articles:
        [title, body] = re.split(r'(?:\n\s*){3,}', article)
        csv.append({"Title": title, "Body": body})
    return csv 

# --- Streamlit app ---
st.title("📄 Separador Automático de artigos")
st.write("Faça upload do documentoWord (.docx) para separar automaticamente artigos separados por 3 linhas brancas")

uploaded_file = st.file_uploader("Escolha um documento .docx", type="docx")

if uploaded_file:
    text = extract_text_from_word(uploaded_file)
    articles = article_split(text)

    data = data_extract(articles)

    df = pd.DataFrame(data)

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
        st.text_area(f"Conteudo {i}", article, height=200)


else:
    st.info("Escolha um documento .docx para começar.")
