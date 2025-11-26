import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(user_data, job_description):
    portfolio = user_data.get("portfolio", "")
    github = user_data.get("github", "")
    experience = user_data.get("experience", "")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    preferences = user_data.get("preferences", "")
    additional_info = user_data.get("additional_info", "")
    
    # We omit the opening_phrase and links_section builder since the new format integrates links directly into the body.

    prompt = f"""
    Write a concise, project-driven application note (NOT a traditional cover letter) strictly following these guidelines:
    
    1. FORMAT & LENGTH:
    - Total output must be 100-150 words MAXIMUM.
    - Omit traditional elements like date, address, and formal salutations (e.g., "Dear Hiring Manager"). Start directly with content.
    - Use a brief, bulleted list for the main experience/project section.
    
    2. CONTENT FOCUS:
    - Opening: A single, brief sentence introducing the candidate and expressing direct interest in the role.
    - Body (Bulleted): List 2-3 of the candidate's MOST RELEVANT projects or concrete achievements that directly address the job requirements.
        - Each bullet point MUST integrate a direct link (Portfolio or GitHub) as verifiable proof of work. Prioritize this link integration.
        - Focus on the *impact*, *scale*, or *specific technology* that matches the job description.
    - Closing: A single, professional sentence inviting immediate review of the linked projects.
    
    3. TONE & CLICHÉ AVOIDANCE:
    - Must be extremely direct, scannable, and professional.
    - Avoid ALL fluff, generic skills, and narrative prose. The entire goal is to point the reader to the proof of work.
    - Absolutely NO phrases like: "excited", "eager", "passionate", "proficient", "honed", "leveraged", or any AI clichés.

    4. choose projects that are most relevant to the job description.
    5. if the client writes anything specific about the cover letter, you should follow that. i.e if he writes start by saying "bla bla bla" you should start by saying "bla bla bla"
    
    Job Description (analyze carefully for specific technical requirements):
    {job_description}
    
    Candidate Information (use ONLY what's relevant to the job, prioritize projects and links):
    - Name: {first_name} {last_name}
    - Experience: {experience}
    - Additional Info: {additional_info}
    - Preferences: {preferences}
    - Portfolio Link: {portfolio}
    - GitHub Link: {github}

    
    Important: The final output must be a direct, scannable text that immediately highlights related, verifiable work.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional technical recruiter writing an ultra-concise application note. Your sole purpose is to quickly highlight verified work that directly matches the job requirements."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6 # Slightly lower temperature for more direct, structured output
    )

    return response.choices[0].message.content