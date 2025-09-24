# HashLens

HashLens is a tool for analyzing, fingerprinting, and classifying JSON files by department (e.g., marketing, engineering). It provides a FastAPI backend and a Streamlit frontend.

## Features

- **Fingerprint JSON files:** Analyze structure and content, generate a hash.
- **Add signatures:** Store fingerprints by department for future classification.
- **Classify files:** Predict department based on similarity to stored signatures.
- **Batch Classify:** Upload and classify multiple JSON files at once.

## Getting Started

### 1. Install dependencies

```sh
pip install -r requirements.txt
```

### 2. Run the backend API

```sh
uvicorn backend.api:app --reload
```

### 3. Run the frontend

```sh
streamlit run frontend/app.py
```

### 4. Usage

- **Add Signature:** Upload a JSON file and assign it to a department.
- **Classify File:** Upload a JSON file to predict its department.
- **Show Fingerprint:** View the fingerprint and hash of a JSON file.
- **Batch Classify:** Upload multiple JSON files and classify all at once. Results are shown in a table.

## Example JSON

See the `data/` folder for sample files.

## Project Structure

```
hashlens.db
requirements.txt
backend/
    api.py
    classify.py
    fingerprint.py
data/
    engineering_1.json
    engineering_2.json
    marketing_1.json
    marketing_2.json
frontend/
    app.py
```

