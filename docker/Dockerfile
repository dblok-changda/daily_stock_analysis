# ===================================
# Anote - Docker note
# ===================================
# note：note + note

FROM node:20-slim AS web-builder

WORKDIR /app/apps/dsa-web

COPY apps/dsa-web/package.json apps/dsa-web/package-lock.json ./
RUN npm ci

COPY apps/dsa-web/ ./
RUN npm run build

# Pin to bookworm: wkhtmltopdf was removed from Debian testing (2025)
FROM python:3.11-slim-bookworm

# notedirectories
WORKDIR /app

# note
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# note（wkhtmltopdf note wkhtmltoimage，for Markdown note Issue #289）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    git \
    gosu \
    wkhtmltopdf \
    fontconfig \
    libjpeg62-turbo \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# note root note (UID 1000)
RUN groupadd -g 1000 dsa && \
    useradd -u 1000 -g dsa -m dsa

# notefiles
COPY requirements.txt .

# note Python note
RUN pip install --no-cache-dir -r requirements.txt

# note
COPY *.py ./
COPY api/ ./api/
COPY data_provider/ ./data_provider/
COPY bot/ ./bot/
COPY src/ ./src/
COPY strategies/ ./strategies/
COPY --from=web-builder /app/static ./static/
COPY docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Verify the bundled AlphaSift adapter from requirements.
RUN python -c "import alphasift.dsa_adapter"

# notedatadirectoriesnote non-root note
RUN mkdir -p /app/data /app/logs /app/reports && \
    chown -R dsa:dsa /app && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

# efinance notecache（search-cache.json）note data directories，
# notedirectoriesdefaultnote root note；note root note dsa note PermissionError，
# note efinance datanote A notedatanote。notedirectoriesnote dsa note。
# note，note Python notedirectories。
RUN EF_DATA_DIR="$(python -c 'import efinance, pathlib; print(pathlib.Path(efinance.__file__).parent / "data")')" && \
    mkdir -p "$EF_DATA_DIR" && \
    chown -R dsa:dsa "$EF_DATA_DIR"

# notedefaultnote
ENV PYTHONUNBUFFERED=1
ENV LOG_DIR=/app/logs
ENV DATABASE_PATH=/app/data/stock_analysis.db
# Web/API service
ENV WEBUI_HOST=0.0.0.0
ENV API_PORT=8000

# note API note
EXPOSE 8000

# datanote（notedata）
VOLUME ["/app/data", "/app/logs", "/app/reports"]

# note（FastAPI note）
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || curl -f http://localhost:8000/health \
    || python -c "import sys; sys.exit(0)"

# note bind mount directoriesnote，note dsa note；
# note docker-compose exec note -u dsa，note root-owned files。
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# defaultnote（note）
CMD ["python", "main.py", "--schedule"]
