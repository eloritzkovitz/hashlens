import streamlit as st
import requests
import json
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

st.title("HashLens Demo")

mode = st.radio("Mode", ["Add Signature", "Classify File", "Batch Classify"])

if mode in ["Add Signature", "Classify File"]:
    uploaded = st.file_uploader("Upload JSON file", type=["json"])
    if uploaded:
        data = json.load(uploaded)
        temp_path = "temp.json"
        with open(temp_path, "w") as f:
            json.dump(data, f)

        if mode == "Add Signature":
            dept = st.selectbox("Department", ["marketing", "engineering"])
            if st.button("Add"):
                with open(temp_path, "rb") as f:
                    response = requests.post(
                        f"{API_URL}/add",
                        files={"file": f},
                        data={"department": dept}
                    )
                if response.status_code == 200:
                    st.success(f"Added to {dept}")
                else:
                    st.error("Failed to add signature.")

        elif mode == "Classify File":
            if st.button("Classify"):
                with open(temp_path, "rb") as f:
                    response = requests.post(
                        f"{API_URL}/classify",
                        files={"file": f}
                    )
                if response.status_code == 200:
                    st.write(response.json())
                else:
                    st.error("Failed to classify file.")

        if st.checkbox("Show fingerprint"):
            with open(temp_path, "rb") as f:
                response = requests.post(
                    f"{API_URL}/fingerprint",
                    files={"file": f}
                )
            if response.status_code == 200:
                result = response.json()
                st.json(result)
                # Show hash if present
                hash_value = result.get("features", {}).get("hash") or result.get("hash")
                if hash_value:
                    st.write(f"**Hash:** `{hash_value}`")
            else:
                st.error("Failed to get fingerprint.")

# ---------------- Batch Classification ----------------
elif mode == "Batch Classify":
    uploaded_files = st.file_uploader("Upload multiple JSON files", type=["json"], accept_multiple_files=True)
    if uploaded_files and st.button("Classify All"):
        results = []
        for uploaded in uploaded_files:
            temp_path = f"temp_{uploaded.name}"
            data = json.load(uploaded)
            with open(temp_path, "w") as f:
                json.dump(data, f)
            with open(temp_path, "rb") as f:
                response = requests.post(
                    f"{API_URL}/classify",
                    files={"file": f}
                )
            if response.status_code == 200:
                result_text = response.json()['result']
            else:
                result_text = "Error"
            results.append({"file": uploaded.name, "classification": result_text})

        st.table(results)
