# pymupdf4llm-api

API server for [pymupdf4llm](https://github.com/pymupdf/RAG/).

## Getting Started

```bash
git clone https://github.com/first-automation/pymupdf4llm-api.git
cd pymupdf4llm-api
docker compose up
```
or
```bash
docker run -d \
  --name pymupdf4llm-service \
  -p 5000:5000 \
  -e API_TOKEN=your_secure_token \
  ghcr.io/first-automation/pymupdf4llm-api/pymupdf4llm-api:latest
```
or in a docker-compose.yaml file

```yaml
services:
  pymupdf4llm:
    image: devpartitech/pymupdf4llm-api:latest
    container_name: pymupdf4llm-service
    ports:
      - "60002:8000" # Expose port 60002 to access the API
    environment:
      - API_TOKEN=578910
```

### Invoke the API with curl:
- Without token:
```bash
curl -X POST http://localhost:8000/convert -H "Content-Type: multipart/form-data" -F "file=@path/to/your/file.pdf"
```

- With token:
```bash
curl -X POST http://localhost:8000/convert -H "Authorization: Bearer your_secure_token" -H "Content-Type: multipart/form-data" -F "file=@path/to/your/file.pdf"
```







