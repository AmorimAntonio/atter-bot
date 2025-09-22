FROM python:3.12-slim

# evitando prompts interativos e tirando o buffer dos logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Diretório da app
WORKDIR /app

# Instala dependências de sistema (opcional, mas útil p/ debug/healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copia só requirements primeiro (melhor cache de build)
COPY requirements.txt .

# Instala dependências do Python
RUN pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Se você mantiver o keep_alive/Flask, abra a porta 8080 (não é obrigatório para bot)
EXPOSE 8080

# (Opcional) healthcheck pingando o Flask interno
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8080/ || exit 1

# Rode seu bot
# Troque "main.py" pelo nome correto do arquivo principal (parece que é "main")
CMD ["python", "-u", "main.py"]