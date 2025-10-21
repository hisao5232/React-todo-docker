FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPIアプリをコピー（ここが重要）
COPY ./app ./app

# パッケージとして認識されるように
WORKDIR /app

# FastAPIを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
