# MCP server (char-index-mcp) Docker image
FROM python:3.14-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY pyproject.toml .
COPY char_index_mcp/ char_index_mcp/
RUN uv pip install --system .

CMD ["char-index-mcp"]
