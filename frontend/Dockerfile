# React Frontend 用 Dockerfile
FROM node:20-alpine

# 作業ディレクトリ
WORKDIR /app

# 依存関係ファイルを先にコピー
COPY package*.json ./

# 開発用に依存関係をインストール
RUN npm install

# 残りのソースをコピー
COPY . .

# Vite 開発サーバーを公開（--host で外部アクセス許可）
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
