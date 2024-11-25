import os
import tempfile

import pymupdf4llm
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

API_TOKEN = os.getenv("API_TOKEN")  # If not set, protection is disabled


class ConvertResponse(BaseModel):
    text: str | None = None


class ConvertPagesResponse(BaseModel):
    texts: list[str] = []


app = FastAPI()

security = HTTPBearer()


def optional_auth(request: Request):
    if API_TOKEN:  # Only verify if API_TOKEN is set
        auth_header: str | None = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = auth_header.split(" ")[1]
        if token != API_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/convert", dependencies=[Depends(optional_auth)])
async def convert(file: UploadFile = File(...)) -> ConvertResponse:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_file.flush()
        result = pymupdf4llm.to_markdown(temp_file.name)
    return ConvertResponse(text=result)


@app.post("/convert_pages", dependencies=[Depends(optional_auth)])
async def convert_pages(file: UploadFile = File(...)) -> ConvertPagesResponse:
    results: list[str] = []
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_file.flush()
        count = 0
        while True:
            try:
                result = pymupdf4llm.to_markdown(temp_file.name, pages=[count])
            except IndexError:
                break
            results.append(result)
            count += 1
    return ConvertPagesResponse(texts=results)
