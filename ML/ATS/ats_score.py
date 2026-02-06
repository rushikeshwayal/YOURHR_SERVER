from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def text_similarity(resume_text: str, job_text: str) -> float:
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_df=0.85,
        sublinear_tf=True
    )
    vectors = vectorizer.fit_transform([resume_text, job_text])
    return cosine_similarity(vectors[0], vectors[1])[0][0]


def skill_similarity(resume_data: dict, job_skills: str) -> float:
    resume_skills = set(
        s.lower() for s in resume_data.get("skills", [])
    )

    if not job_skills:
        return 0.0

    job_skills = set(
        s.strip().lower()
        for s in job_skills.split(",")
    )

    if not job_skills:
        return 0.0

    return len(resume_skills & job_skills) / len(job_skills)


def calculate_ats_score(resume_text, job_text, resume_data, job):
    text_score = text_similarity(resume_text, job_text)
    skill_score = skill_similarity(resume_data, job.skills_required)

    ats_score = (0.7 * skill_score + 0.3 * text_score) * 100
    return round(ats_score, 2)
