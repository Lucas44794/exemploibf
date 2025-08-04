# Usa a imagem base com suporte multiplataforma
FROM --platform=$BUILDPLATFORM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Atualiza pip e instala dependências
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn==20.1.0

# Expõe a porta padrão do Flask/Gunicorn
EXPOSE 5000

# Comando para iniciar o app com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]