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
    Write a cover letter following the "Hook-Value-Proof" format strictly:

1. THE HOOK (First 2 lines):
   - DO NOT start with "Hi, my name is..." or "Dear Client" - they can see my name on my profile.
   - Start by acknowledging their SPECIFIC problem mentioned in the job description.
   - Example format: "I saw you're looking to [specific problem from job description]—I just helped [similar client/project] do exactly that [timeframe]."
   - Make it personal and specific to their needs.

2. THE VALUE (The Solution):
   - Briefly explain how you will solve their problem.
   - Use "You" more than "I" - focus on what they will get.
   - Example: "You'll get [specific solution/benefit] that will [outcome]."
   - Keep this section concise and solution-focused.

3. THE PROOF (The Flex):
   - Include links to 1-4 projects that are similar to this job and use similar tech stack.
   - Each project link should be a plain URL only (no markdown, no brackets, no parentheses).
   - Briefly mention what makes each project relevant (tech stack, problem solved, or similar scope).
   - If portfolio or GitHub links are provided, prioritize those that match the job requirements.

4. THE CALL TO ACTION (The Closer):
   - End with a specific question to get them talking.
   - Make it relevant to their project or needs.
   - Examples: "What's your biggest challenge with [specific aspect]?" or "When are you looking to launch this?"
   - Avoid generic questions like "Can we discuss further?"

5. TONE & STYLE:
   - Direct, confident, solution-oriented.
   - No clichés: avoid “passionate,” “eager,” “excited,” “skilled,” “expert,” etc.
   - No storytelling — only facts that prove capability.
   - No clichés: avoid "passionate," "eager," "excited," "skilled," "expert," etc.
   - Keep total length under 200 words.
   - Focus on their needs, not your background.

6. LINK RULES (IMPORTANT):
   - All links must be printed ONLY as plain URLs (example: https://example.com).
   - Never use markdown formats like [ ] or ( ).
   - Do NOT make up or fabricate links - only use provided portfolio/GitHub links.

Here is the job description (analyze carefully and extract the core problem, tech stack, and requirements):
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
            {"role": "system", "content": "You are a professional cover letter writer using the Hook-Value-Proof format. Your purpose is to acknowledge the client's problem, offer a solution, provide proof through similar projects, and end with an engaging question."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6 
    )

    return response.choices[0].message.content