import json, hashlib
from collections import Counter

def compute_fingerprint(path: str, top_tokens: int = 50) -> dict:
    type_counts = Counter()
    token_counts = Counter()

    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                for token in k.lower().split("_"):
                    token_counts[token] += 1
                walk(v)
        elif isinstance(obj, list):
            type_counts["array"] += 1
            for v in obj:
                walk(v)
        elif isinstance(obj, str):
            type_counts["string"] += 1
        elif isinstance(obj, bool):
            type_counts["boolean"] += 1
        elif isinstance(obj, (int, float)):
            type_counts["number"] += 1
        elif obj is None:
            type_counts["null"] += 1

    with open(path, "r") as f:
        data = json.load(f)
    walk(data)

    profile = {
        "types": dict(type_counts),
        "tokens": dict(token_counts.most_common(top_tokens))
    }

    # stable JSON string → hash
    profile_str = json.dumps(profile, sort_keys=True)
    profile_hash = hashlib.sha256(profile_str.encode()).hexdigest()

    return {"profile": profile, "hash": profile_hash}
