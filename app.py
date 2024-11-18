import tempfile

import pymupdf4llm
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel


class ConvertResponse(BaseModel):
    text: str | None = None


class ConvertPagesResponse(BaseModel):
    texts: list[str] = []


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/convert")
async def convert(file: UploadFile = File(...)) -> ConvertResponse:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_file.flush()
        result = pymupdf4llm.to_markdown(temp_file.name)
    return ConvertResponse(text=result)


@app.post("/convert_pages")
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
