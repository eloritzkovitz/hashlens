from fastapi import FastAPI, UploadFile, Form
import json
from .classify import init_db, add_signature, classify_file, extract_features
from .fingerprint import compute_fingerprint

app = FastAPI()
init_db()

# ---------- API Endpoints ----------
@app.post("/fingerprint")
async def fingerprint(file: UploadFile):
    data = json.load(file.file)
    temp_path = "tmp.json"
    with open(temp_path, "w") as f:
        json.dump(data, f)
    features = extract_features(temp_path)
    fp = compute_fingerprint(temp_path)
    return {
        "features": dict(features),
        "hash": fp.get("hash", "")
    }

@app.post("/add")
async def add(file: UploadFile, department: str = Form(...)):
    data = json.load(file.file)
    temp_path = "tmp.json"
    with open(temp_path, "w") as f:
        json.dump(data, f)
    add_signature(temp_path, department)
    fp = compute_fingerprint(temp_path)
    return {
        "status": "added",
        "department": department,
        "hash": fp.get("hash", "")
    }

@app.post("/classify")
async def classify(file: UploadFile):
    data = json.load(file.file)
    temp_path = "tmp.json"
    with open(temp_path, "w") as f:
        json.dump(data, f)
    result = classify_file(temp_path)
    fp = compute_fingerprint(temp_path)
    return {
        "result": result,
        "hash": fp.get("hash", "")
    }