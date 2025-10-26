# 1. Usar uma imagem base oficial do Python
FROM python:3.11-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 3. Instalar o 'uv' na imagem
RUN pip install uv

# 4. Copiar o arquivo de dependências
COPY requirements.txt .

# 5. Instalar as dependências usando uv
# Usamos --system para instalar globalmente no container (não precisamos de venv aqui)
RUN uv pip install --system --no-cache -r requirements.txt

# 6. Copiar o resto do código da aplicação
COPY . .

# 7. Expor a porta que o Uvicorn usará
EXPOSE 8000

# 8. Comando para iniciar a aplicação
# Note que não usamos --reload em produção
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]