from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
from matcher import analyze
from db import save, history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    resume: str
    jd: str

@app.post("/analyze")
def analyze_api(data: AnalyzeRequest):
    result = analyze(data.resume, data.jd)
    save(result)
    return result

@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...), jd: str = Form(...)):
    with pdfplumber.open(file.file) as pdf:
        resume = " ".join(page.extract_text() or "" for page in pdf.pages)
    result = analyze(resume, jd)
    save(result)
    return result

@app.get("/history")
def history_api():
    return history()