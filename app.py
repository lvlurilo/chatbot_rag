import streamlit as st
from io import StringIO 
import service as Service

FORMATO_ARQUIVO = "txt"

st.title("Chatbot")
tab_chatbot, tab_upload_arquivo = st.tabs(["Chatbot", "Upload de arquivo"])

with tab_chatbot:
    st.header("Chatbot")
    
    consulta = st.text_input("Faça uma pergunta:")
    
    if consulta:
        documentos_relevantes = Service.buscar_documentos(consulta)
        
        if documentos_relevantes:
            resposta = Service.gerar_resposta(consulta, documentos_relevantes)
            st.write(resposta)
        else:
            st.write("Nenhum informação relevante encontrada.")

with tab_upload_arquivo:
    st.header("Upload de arquivo")
    
    arquivo = st.file_uploader(f"Escolha um arquivo de texto no formato {FORMATO_ARQUIVO}", type=[FORMATO_ARQUIVO])
    
    if arquivo is not None:
        stringio = StringIO(arquivo.getvalue().decode("utf-8"))
        texto = stringio.read()
        
        st.text_area("Conteúdo do arquivo", texto, height=50)
        
        if st.button("Indexar no Pinecone"):
            id_documento = arquivo.name
            Service.indexar_documento(id_documento, texto)
            st.success(f"Arquivo '{arquivo.name}' indexado com sucesso!")


