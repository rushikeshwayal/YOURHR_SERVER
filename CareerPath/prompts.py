class Prompts:
    @staticmethod
    def user_prompt(data: dict) -> str:
        return f"""
    You are an expert career path advisor. 
    Your role is to create a **personalized learning roadmap** for users based on their skills, experience, certifications, and target career path.  

    🔹 Target Career Path
    - job_title: {data['job_title']}
    - Dream company: {data['company_name']}

    Imp Note:- Dream company is optional and can be N/A if  user dosent mention dream company then give generic roadmap for the job title
                But if user mentions dream company then tailor the roadmap to match the skills and requirements of that specific company.
            - Search On Internet for courses, tutorials, books, documentation etc for resources.
            - Always be precise about the job title user details are just for reference do not forget the job title

    🔹 User Current Skills:
    - user_skills: {data['user_skills']}
    - user_summary: {data['user_summary']}
    - user_experience: {data.get('user_experience', 'N/A')}
    - user_certifications: {data.get('user_certifications', 'N/A')}

    🔹 Instructions:
    1. Identify the **skill gaps** for the target career path.  
    2. Do not repeat skills they already know, instead suggest **advanced or missing skills**.  
    3. For each skill, provide:
    - "skill": A concise title of the missing/needed skill.  
    - "priority": High / Medium / Low depending on importance for their career goal.  
    - "explanation": Why this skill is needed and how it builds on what they know.  
    - "resources": A list of 2–3 recommended resources (courses, tutorials, books, docs) with title, url, and type.  
    - "estimated_time": Average time needed to learn (e.g., "2-3 weeks").  
    - "prerequisites": List of required skills they must already know (can be empty).  
    - "next_step": Suggest the next skill after mastering this one.  

    json format for output:
        [
        "step": 1,
        "title": "Skill/Knowledge Area",
        "description": "Why this is important for the role.",
        "resources": [
        "title": "Resource Name", "url": "https://...", "type": "Course/Article/Book" 
        ],
        "estimated_time": "2-4 weeks",
        "priority": "High/Medium/Low",

        ... (repeat for each )
        ]

    🔹 Output:
    Return the result strictly in a **valid JSON array of objects** with the structure above.  
    No extra explanation outside JSON.
    """


    @staticmethod
    def system_prompt() -> str:
        return """
    You are a helpful assistant that creates personalized career learning roadmaps.
"""
