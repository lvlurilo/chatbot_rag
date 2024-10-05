
# Chatbot RAG
Este projeto implementa um chatbot utilizando a arquitetura de RAG (Retrieval-Augmented Generation), com a integração de tecnologias como OpenAI GPT-3.5, Pinecone e Streamlit, visando permitir a busca e a geração de respostas com base em documentos indexados.

### Tecnologias Utilizadas
* Python: Linguagem de programação principal;
* OpenAI GPT-3.5: Utilizado para a geração de respostas baseadas em textos fornecidos;
* Pinecone: Serviço de busca vetorial usado para armazenar embeddings de documentos;
* Docker: Para empacotamento e execução do projeto em ambientes consistentes;
* Streamlit: Interface gráfica para interações com o chatbot.

### Pré-requisitos
* Docker  instalado;

* Indice Criado no Pinecone. Sugestão de configuração de Indice:
    name='chatbot-rag',
    dimension=1536,
    metric='cosine'
    region='us-east-1'

* Chaves de API para OpenAI e Pinecone:
    OpenAI API Key: Para gerar embeddings e respostas com ChatGPT.
    Pinecone API Key: Para armazenar e buscar embeddings de documentos.

* Arquivo **.env** contendo as variáveis de ambiente necessárias. Ajuste as variáveis conforme suas credenciais:
    OPENAI_API_KEY=seu_openai_api_key
    PINECONE_API_KEY=seu_pinecone_api_key
    PINECONE_INDEX_NAME=seu_pinecone_index_name
    AWS_REGION=aws_region_do_index_pinecone


### Execução do Projeto
Build e execute com Docker Compose:
Na raiz do projeto, execute o seguinte comando para construir e rodar o contêiner:
docker-compose up --build

Após a execução, acesse a aplicação em localhost:8501 do seu navegador

### Utilizando a aplicação
Para que o chatbot possa responder com base em documentos específicos, você deve fazer o upload de arquivos .txt através da interface no Streamlit.

**Upload de Documentos**
Acesse a aba "Upload de arquivo".
Selecione um arquivo de texto no formato .txt.
Clique em "Indexar no Pinecone".

**Consultas ao Chatbot**
Na aba "Chatbot", insira uma pergunta no campo de texto.
O chatbot buscará informações relevantes a partir dos documentos indexados no Pinecone e utilizará o GPT-3.5 para gerar uma resposta baseada no conteúdo disponível.
