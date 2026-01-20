from docx import Document
import streamlit as st
import re


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


# --- Streamlit app ---
st.title("📄 Separador Automático de artigos")
st.write("Faça upload do documentoWord (.docx) para separar automaticamente artigos separados por 3 linhas brancas")

uploaded_file = st.file_uploader("Escolha um documento .docx", type="docx")

if uploaded_file:
    text = extract_text_from_word(uploaded_file)
    articles = article_split(text)

    st.success(f"✅ encontrados {len(articles)} artigos.")
    for i, article in enumerate(articles, 1):
        st.subheader(f"Artigo {i}")
        st.text_area(f"Conteudo {i}", article, height=200)
else:
    st.info("Escolha um documento .docx para começar.")
