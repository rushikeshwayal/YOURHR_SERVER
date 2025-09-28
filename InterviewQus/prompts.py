class Prompts:
    @staticmethod
    def user_prompt(job_title, company_name, job_description,
                    skills_required, experience_required):
        return f"""
You are an expert interview question generator. ...
job_title: {job_title}
company_name: {company_name}
job_description: {job_description}
skills_required: {skills_required}
experience_required: {experience_required}

Give the output in json format as mentioned below:
[
    
        "question": "Question 1",
        "answer": "Sample answer for question 1"
    ,
    ...
]
"""
    @staticmethod
    def system_prompt():
        return """
You are a helpful assistant that generates interview questions...
"""
