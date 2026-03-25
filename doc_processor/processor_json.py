import json
import csv
import pandas as pd
import streamlit as st

def process_json(input_json):
    """
    Process the JSON input and return the extracted data and CSV content.
    """
    # Load JSON data
    data = json.loads(input_json)

    # Extract fields
    edition_title = data.get("edition_title", "")
    edition_date = data.get("edition_date", "")
    edition_number = data.get("edition_number", "")
    ficha_tecnica = data.get("ficha_tecnica", "")
    editorial = data.get("editorial", {})
    articles = data.get("articles", [])

    # Prepare CSV data
    csv_data = []
    for article in articles:
        csv_data.append({
            "edition_title": edition_title,
            "edition_date": edition_date,
            "edition_number": edition_number,
            "titulo": article.get("titulo", ""),
            "subtitulo": article.get("subtitulo", ""),
            "autor": article.get("autor", ""),
            "paginas": article.get("paginas", ""),
            "num_imagens": article.get("num_imagens", 0),
            "tags": ", ".join(article.get("tags", [])),
            "corpo": article.get("corpo", "")
        })

    return edition_title, edition_number, edition_date, ficha_tecnica, editorial, articles, csv_data

def generate_csv(csv_data):
    """
    Generate a CSV file from the given data and return it as a string.
    """
    csv_file = "articles_output.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "edition_title", "edition_date", "edition_number", "titulo", "subtitulo", "autor",
            "paginas", "num_imagens", "tags", "corpo"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    return csv_file

# --- Streamlit app ---
if __name__ == "__main__":
    st.title("📄 Separador Automático de artigos")
    st.write("Faça upload do documento JSON para processar os artigos")

    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

    if uploaded_file is not None:
        # Read and process the uploaded JSON file
        input_json = uploaded_file.read().decode("utf-8")
        edition_title, edition_number, edition_date, ficha_tecnica, editorial, articles, csv_data = process_json(input_json)

        # Display edition information
        st.subheader("Informações da Edição")
        st.write(f"Título da Edição: {edition_title}")
        st.write(f"Data da Edição: {edition_date}")
        st.write(f"Número da Edição: {edition_number}")

        # Generate CSV file for download
        csv_file = generate_csv(csv_data)
        with open(csv_file, "rb") as f:
            st.download_button(
                label="Download CSV",
                data=f,
                file_name="articles_output.csv",
                mime="text/csv"
            )

        
        # Display ficha tecnica and editorial
        st.subheader("Ficha Técnica")
        st.write(ficha_tecnica)

        st.subheader("Editorial")
        st.write(f"Autor: {editorial.get('autor', '')}")
        st.write(f"Corpo: {editorial.get('corpo', '')}")

        # Display CSV preview
        st.subheader("CSV Preview")
        df = pd.DataFrame(csv_data)
        st.dataframe(df)


        # Display article bodies
        st.subheader("Artigos")
        for i, article in enumerate(articles):
            with st.expander(f"Artigo {i + 1}: {article.get('titulo', 'Sem Título')}"):
                st.write(article.get("corpo", ""))