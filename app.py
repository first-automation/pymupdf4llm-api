import tempfile

import pymupdf4llm
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

import os
API_TOKEN = os.getenv("API_TOKEN") # If not set, protection is disabled

class ConvertResponse(BaseModel):
    text: str | None = None


class ConvertPagesResponse(BaseModel):
    texts: list[str] = []


app = FastAPI()

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Checks if the token matches the API token.
    If API_TOKEN is not set, access is allowed without verification.
    """
    if API_TOKEN and credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def optional_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Enables token verification only if API_TOKEN is set.
    """
    if API_TOKEN:
        verify_token(credentials)

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
