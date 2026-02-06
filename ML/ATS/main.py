from preprocess import clean_text
from ats_score import calculate_ats_score

if __name__ == "__main__":
    resume_text = """
    Python developer with experience in machine learning,
    NLP, FastAPI, SQL, and Git.
    """

    jd_text = """
    Looking for a Python engineer skilled in machine learning,
    NLP, AWS, Docker, and FastAPI.
    """

    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    ats_score = calculate_ats_score(resume_clean, jd_clean)

    print(f"ATS Score: {ats_score}%")
