FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY . .
RUN uv pip install --system .

# 시스템에 설치되어 있으니 바로 실행
CMD ["char-index-mcp"]