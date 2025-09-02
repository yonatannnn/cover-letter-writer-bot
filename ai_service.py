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
    opening_phrase = user_data.get("opening_phrase", "")  # New field for custom opening
    
    # Build links section only if provided
    links_section = ""
    if portfolio or github:
        links_section = "\n\nRelevant Links:\n"
        if portfolio: links_section += f"Portfolio: {portfolio}\n"
        if github: links_section += f"GitHub: {github}"

    prompt = f"""
    Write a professional cover letter strictly following these guidelines:
    
    1. STRUCTURE:
    - Opening: {f"Use this exact opening phrase if provided: '{opening_phrase}'" if opening_phrase else "Start with a strong, unique professional opening"}
    - Body: 1-2 paragraphs MAXIMUM showing ONLY the most relevant experience/skills from the candidate that match the job
    - Closing: Brief professional closing with invitation to discuss further
    - Links: {links_section if links_section else "Omit links section entirely if no links provided"}
    
    2. TONE REQUIREMENTS:
    - Must sound human-written (vary sentence structure, avoid perfect grammar occasionally)
    - Absolutely NO phrases like: "excited", "eager", "passionate", "proficient", "honed", "leveraged", "seamlessly", "
    - No AI clichés like "In a world where...", "As a [job title] with X years..."
    - More concrete achievements than generic skills
    
    3. CONTENT RULES:
    - Only include experience/skills that DIRECTLY match job requirements
    - For each skill/experience mentioned, show HOW it applies to this specific job
    - If no relevant experience matches, be honest but highlight transferable skills
    - Never make up qualifications
    
    Job Description (analyze carefully for requirements):
    {job_description}
    
    Candidate Information (use ONLY what's relevant to the job):
    - Name: {first_name} {last_name}
    - Experience: {experience}
    - Additional Info: {additional_info}
    - Preferences: {preferences}
    
    Important: The cover letter must be:
    - 200-300 words maximum
    - Focused solely on job requirements
    - Professional but not robotic
    - Completely original phrasing
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional resume writer who creates human-sounding, job-specific cover letters that avoid all AI clichés."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content