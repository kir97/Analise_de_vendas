# Usa a imagem base do Python
FROM python:3.12

# Instala dependências de sistema necessárias
RUN apt-get update && apt-get install -y sqlite3 libfreetype6-dev libpng-dev

# Configuração do Streamlit
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

# Expondo a porta padrão do Streamlit
EXPOSE 8501

# Define a pasta de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos restantes
COPY . .

# Executa o dashboard
CMD ["streamlit", "run", "scripts/dashboard.py"]