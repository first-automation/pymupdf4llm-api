# pymupdf4llm-api

API server for [pymupdf4llm](https://github.com/pymupdf/RAG/).

## Getting Started

```bash
git clone https://github.com/first-automation/pymupdf4llm-api.git
cd pymupdf4llm-api
docker compose up
# or
docker run ghcr.io/first-automation/pymupdf4llm-api/pymupdf4llm-api:latest
```

Invoke the API with curl:

```bash
curl -X POST http://localhost:8000/convert -H "Content-Type: multipart/form-data" -F "file=@path/to/your/file.pdf"
```
