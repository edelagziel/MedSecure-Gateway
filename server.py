from fastapi import FastAPI
from fastapi import UploadFile, File, Header
from services.pipeline import process_file

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    checksum: str = Header(None)
):
    result = process_file(file, checksum)
    return result
