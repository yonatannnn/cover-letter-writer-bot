import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(user_data, job_description):
    portfolio = user_data.get("portfolio", "No portfolio provided")
    github = user_data.get("github", "No GitHub link provided")
    experience = user_data.get("experience", "No experience provided")
    first_name = user_data.get("first_name", "[Name]")
    last_name = user_data.get("last_name", "")
    preferences = user_data.get("preferences", "No preferences provided")
    additional_info = user_data.get("additional_info", "No additional information provided")

    prompt = f"""
    Write a professional and concise cover letter for the following job description. The cover letter should:
    - Be tailored to the job description, highlighting only relevant skills and experiences for this job description.
    - Avoid overused phrases like "excited," "eager," "proficient." "honed," etc.
    - Sound human-written, not AI-generated.
    - Include links to the candidate's portfolio and GitHub at the end if any.
    - Start with a strong, professional opening that avoids clichés like "I am excited to apply for...".

    Job Description:
    {job_description}

    Candidate Information:
    - Experience: {experience}
    - First Name: {first_name}
    - Last Name: {last_name}
    - Additional Information: {additional_info}
    - Preferences: {preferences}
    - Portfolio: {portfolio}
    - GitHub: {github}

    Structure the cover letter as follows:
    1. A professional opening that introduces the candidate and mentions the role.
    2. A brief paragraph highlighting relevant skills and experiences that match the job description.
    3. A closing paragraph expressing interest in discussing the role further.
    4. Links to the portfolio and GitHub at the end but if links are not given dont even talk about the link.

    Ensure the tone is professional, concise, and free of AI-like language.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert at writing professional and human-like cover letters."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

