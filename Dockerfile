# Usar uma imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt requirements.txt

# Instalar as dependências diretamente no ambiente do contêiner
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Expor a porta 8501 para o Streamlit
EXPOSE 8501

# Comando para rodar o aplicativo
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
