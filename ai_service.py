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
    Write a short, ultra-clear Upwork proposal strictly following these rules:

1. FORMAT:
   - No greetings like “Hi” or “Dear Client.”
   - Start immediately with one sentence that matches the client’s main need.
   - Keep the total proposal under 130 words.

2. CONTENT RULES:
   - Focus ONLY on what the client asked for — no generic skills, no filler.
   - Include 2–3 bullet points showing directly relevant experience or projects.
   - Each bullet must reference real past work. If a link is provided, include the RAW URL only (no markdown, no parentheses, no brackets).
   - Do NOT make up achievements or fabricate links.

3. TONE:
   - Direct, confident, solution-oriented.
   - No clichés: avoid “passionate,” “eager,” “excited,” “skilled,” “expert,” etc.
   - No storytelling — only facts that prove capability.

4. CLOSING:
   - End with one short sentence offering to start immediately or clarify requirements.

5. LINK RULES (IMPORTANT):
   - All links must be printed ONLY as plain URLs (example: https://example.com).
   - Never use markdown formats like [ ] or ( ).

Here is the job description (analyze carefully and extract the core needs):
{job_description}

Candidate Information (use ONLY what's relevant to the job, prioritize projects and links):
    - Name: {first_name} {last_name}
    - Experience: {experience}
    - Additional Info: {additional_info}
    - Preferences: {preferences}
    - Portfolio Link: {portfolio}
    - GitHub Link: {github}

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