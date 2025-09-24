import sqlite3
import json
from collections import Counter

DB_FILE = "hashlens.db"

# ---------- DB Init ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            features TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------- Feature extraction ----------
def extract_features(file_path: str) -> Counter:
    """Flatten JSON and return feature counter"""
    with open(file_path, "r") as f:
        data = json.load(f)
    
    features = Counter()
    
    def flatten(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                flatten(v, prefix + k + ".")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                flatten(v, prefix + f"{i}.")
        else:
            features[prefix + str(type(obj).__name__)] += 1
            if isinstance(obj, str):
                # optional: add tokenized words
                for token in obj.lower().split():
                    features[token] += 1
    
    flatten(data)
    return features

# ---------- DB Functions ----------
def add_signature(file_path: str, department: str):
    features = extract_features(file_path)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO signatures (department, features) VALUES (?, ?)",
        (department, json.dumps(features))
    )
    conn.commit()
    conn.close()
    return "added"

# ---------- Similarity ----------
def cosine_similarity(counter1: Counter, counter2: Counter) -> float:
    """Compute cosine similarity between two feature Counters"""
    intersection = set(counter1.keys()) & set(counter2.keys())
    numerator = sum(counter1[x] * counter2[x] for x in intersection)
    sum1 = sum(v**2 for v in counter1.values())
    sum2 = sum(v**2 for v in counter2.values())
    denominator = (sum1**0.5) * (sum2**0.5)
    if not denominator:
        return 0.0
    return numerator / denominator

def classify_file(file_path: str):
    features_new = extract_features(file_path)
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT department, features FROM signatures")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return "No known signatures. Add training data first."

    # Compute similarity per department
    dept_scores = {}
    for dept, feat_str in rows:
        feat_stored = Counter(json.loads(feat_str))
        score = cosine_similarity(features_new, feat_stored)
        if dept not in dept_scores:
            dept_scores[dept] = []
        dept_scores[dept].append(score)
    
    # Average score per department
    avg_scores = {dept: sum(scores)/len(scores) for dept, scores in dept_scores.items()}
    best_dept = max(avg_scores, key=avg_scores.get)
    best_score = avg_scores[best_dept]

    return f"Closest department: {best_dept} (similarity: {best_score:.2f})"
