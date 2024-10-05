import openai
import os
from pinecone import Pinecone

AWS_REGION = os.getenv('AWS_REGION')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
SCORE_THRESHOLD = 0.4
CHUNK_MAX_TOKENS = 100
CHATGPT_CHAT_MODELO = 'gpt-3.5-turbo'
PINECONE_MAX_IDX_RETORNO = 2
CHATGPT_EMBEDDING_MODELO = 'text-embedding-3-small'

# Inicializando Pinecone e OpenAI
pc = Pinecone(api_key=PINECONE_API_KEY) 
index = pc.Index(PINECONE_INDEX_NAME)
openai.api_key = OPENAI_API_KEY

def gerar_embedding(texto):
    """
    Gera o embedding para um texto usando o modelo OpenAI.

    Parâmetros:
        texto (str): O texto a ser convertido em embedding.

    Retorno:
        list: O embedding do texto, representado como uma lista de floats.
    """
    response = openai.Embedding.create(
        input=[texto],
        model=CHATGPT_EMBEDDING_MODELO        
    )
    return response['data'][0]['embedding']

def indexar_documento(id_documento, texto):
    """
    Indexa um documento no Pinecone dividindo-o em chunks e gerando embeddings para cada parte.

    Parâmetros:
        id_documento (str): O identificador único do documento.
        texto (str): O conteúdo do documento a ser indexado.
    """
    partes_texto = gerar_chunk_texto(texto)

    for idx, parte in enumerate(partes_texto):
        vetor = gerar_embedding(parte)
        id_documento_sem_extensao = os.path.splitext(id_documento)[0]
        metadata = {"id_parte": f"{id_documento_sem_extensao}_{idx}", "parte_texto": parte}
        index.upsert(vectors=[(f"{id_documento_sem_extensao}_{idx}", vetor, metadata)])

def buscar_documentos(consulta):
    """
    Busca documentos relevantes no Pinecone com base em uma consulta.

    Parâmetros:
        consulta (str): A consulta de busca a ser comparada com os documentos.

    Retorno:
        list: Uma lista de correspondências relevantes, incluindo os metadados dos documentos.
    """
    vetor_consulta = gerar_embedding(consulta)
    resultado_busca = index.query(vector=vetor_consulta, top_k=PINECONE_MAX_IDX_RETORNO, include_metadata=True)
    return resultado_busca['matches']

def filtrar_documentos_por_relevancia(documentos):
    """
    Filtra os documentos com base no score de relevância.

    Parâmetros:
        documentos (list): A lista de documentos retornados pela busca.

    Retorno:
        list: Os documentos cujo score é maior ou igual ao SCORE_THRESHOLD.
    """
    return [doc for doc in documentos if doc['score'] >= SCORE_THRESHOLD]

def gerar_resposta(consulta, documentos):
    """
    Gera uma resposta com base na consulta e nos documentos relevantes filtrados.

    Parâmetros:
        consulta (str): A consulta de entrada para gerar uma resposta.
        documentos (list): A lista de documentos relevantes para gerar a resposta.

    Retorno:
        str: A resposta gerada pelo GPT, baseada apenas nos documentos fornecidos.
    """
    documentos_relevantes = filtrar_documentos_por_relevancia(documentos)

    if not documentos_relevantes:
        return "Nenhum documento relevante foi encontrado para essa consulta."

    contexto = "\n".join([doc['metadata'].get('parte_texto', '') for doc in documentos_relevantes])
    
    prompt = f"""
    conteúdo fornecido: {contexto}.
    Use apenas o conteúdo fornecido para responder à pergunta:{consulta}
    """
    
    response = openai.ChatCompletion.create(
        model=CHATGPT_CHAT_MODELO,
        messages=[
            {"role": "system", "content": "Você é um assistente útil que responde perguntas baseado somente no conteúdo fornecido."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content']


def gerar_chunk_texto(texto): 
    """
    Divide um texto em chunks menores, garantindo que cada chunk respeite o limite de tokens.

    Parâmetros:
        texto (str): O texto a ser dividido em chunks.

    Retorno:
        list: Uma lista de chunks de texto.
    """    
    chunks = []
    chunk_atual = []
    tamanho_atual = 0

    partes_texto = texto.split('.')
    
    for parte in partes_texto:
        tamanho_parte = len(parte.split())

        if tamanho_atual + tamanho_parte > CHUNK_MAX_TOKENS:
            chunks.append(' '.join(chunk_atual))
            chunk_atual = []
            tamanho_atual = 0
        
        chunk_atual.append(f"{parte}.")
        tamanho_atual += tamanho_parte
           
    if chunk_atual:
        chunks.append(' '.join(chunk_atual))
    
    return chunks



