# FastAPI Backend 用 Dockerfile
FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係を先にコピー（キャッシュ効率化）
COPY requirements.txt .

# netcat-openbsd をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# アプリケーションソースをコピー
COPY ./app /app
COPY ./wait-for-db.sh /wait-for-db.sh

# スクリプトを実行可能に
RUN chmod +x /wait-for-db.sh

# FastAPI 開発サーバー起動（--reloadでホットリロード）
CMD ["/wait-for-db.sh", "db", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
