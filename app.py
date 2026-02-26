import streamlit as st
import json
from pathlib import Path

# Import your modules
from parsers.resume_parser import parse_resume
from parsers.jd_parser import parse_job_description
from extractors.keyword_extractor import extract_features
from matcher.scorer import compute_score

# Load weights safely
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "data" / "config.json"

with open(CONFIG_PATH) as f:
    weights = json.load(f)

st.title("CV Scanner")

# --- INPUTS ---
jd_text = st.text_area("Paste the job description here:", height=300)

uploaded_files = st.file_uploader(
    "Upload resume files:",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# --- PROCESSING ---
if st.button("Screen Resumes", type="primary"):

    if not jd_text:
        st.error("Please paste a job description.")
        st.stop()

    if not uploaded_files:
        st.error("Please upload at least one resume.")
        st.stop()

    with st.spinner("Processing resumes..."):

        try:
            job_requirements = parse_job_description(jd_text)
            results = []

            for file in uploaded_files:
                resume_text = parse_resume(file)
                resume_features = extract_features(resume_text, job_requirements)

                score = compute_score(
                    resume_features,
                    job_requirements,
                    weights
                )

                results.append({
                    "name": file.name,
                    "score": score
                })

            # Sort by best match
            results.sort(key=lambda x: x["score"], reverse=True)

            st.success("Screening complete")

            for candidate in results:
                st.write(
                    f"**{candidate['name']}** — Score: {candidate['score']:.2f}"
                )

        except Exception as e:
            st.error(f"Processing failed: {e}")
