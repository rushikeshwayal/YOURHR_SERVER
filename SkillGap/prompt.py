# InterviewQus/prompts.py
class Prompts:
    @staticmethod
    def user_prompt(data: dict) -> str:
        return f"""
You are an expert skill gap analyzer. 
You take the user's skill set and job description as input
and show the skill gap and give explanation for each skill gap.

job_title: {data['job_title']}
company_name: {data['company_name']}
job_description: {data['job_description']}
skills_required: {data['skills_required']}
experience_required: {data['experience_required']}
user_skills: {data['user_skills']}
user_summary: {data['user_summary']}
user_experience: {data.get('user_experience', 'N/A')}
user_certifications: {data.get('user_certifications', 'N/A')}

Give the output strictly in JSON array format as mentioned below:
[
    
    "skill_gap": "skill gap 1",
    "explanation": "Sample explanation for skill gap 1"
    ,
    ...
]
add 
Percentage skill gap for all skill gaps: 'percentage_skill_gap'
"""

    @staticmethod
    def system_prompt() -> str:
        return """
You are a helpful assistant that analyzes skill gaps based on job descriptions and user skills.
"""
