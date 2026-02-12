from telethon import TelegramClient, events
import requests
import os
from dotenv import load_dotenv
import asyncio
import openai # Added for the generation function definition

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Ensure this is loaded if used locally

# Create client without starting it immediately
bot = TelegramClient('cover_letter_bot', API_ID, API_HASH)

user_states = {}

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Welcome!\n\nCommands:\n/start - Start the bot\n/setup_profile - Set up your profile\n/help - Show this help message\n/generate job_descripition - Generate a cover letter")

@bot.on(events.NewMessage(pattern='/setup_profile'))
async def setup_profile(event):
    user_id = event.sender_id
    # Ensure this link points to your external service where profile data is managed
    form_link = f"https://web-production-ec6c45.up.railway.app/profile_form?user_id={user_id}"
    await event.respond(f"Please set up your profile using this form: {form_link}")

# --- UPDATED GENERATION LOGIC ---
# This function is the new, concise, project-focused core.
# NOTE: You MUST update this function on your external server
# (https://web-production-ec6c45.up.railway.app) for this logic to run there.

def generate_application_note(user_data, job_description):
    portfolio = user_data.get("portfolio", "")
    github = user_data.get("github", "")
    experience = user_data.get("experience", "")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    preferences = user_data.get("preferences", "")
    additional_info = user_data.get("additional_info", "")
    
    # We remove 'opening_phrase' as the new format is ultra-concise and direct.

    prompt = f"""
    Write a cover letter following the "Hook-Value-Proof" format strictly:
    
    1. CLIENT INSTRUCTIONS:
    - Scan the job description for explicit phrasing requirements and repeat them verbatim in the requested spot before writing anything else if the client do not write anything do not write it.
    
    2. THE HOOK (First 2 lines):
    - DO NOT start with "Hi, my name is..." or "Dear Client" - they can see your name on your profile.
    - Start by acknowledging their SPECIFIC problem mentioned in the job description.
    - Example format: "I saw you're looking to [specific problem from job description]—I just helped [similar client/project] do exactly that [timeframe]."
    - Make it personal and specific to their needs.
    
    3. THE VALUE (The Solution):
    - Briefly explain how you will solve their problem.
    - Use "You" more than "I" - focus on what they will get.
    - Example: "You'll get [specific solution/benefit] that will [outcome]."
    - Keep this section concise and solution-focused.
    
    4. THE PROOF (The Flex):
    - Include links to 1-2 projects that are similar to this job and use similar tech stack.
    - Each project link should be a plain URL only (no markdown, no brackets, no parentheses).
    - Briefly mention what makes each project relevant (tech stack, problem solved, or similar scope).
    - Format: "Similar project using [tech stack]: [URL]"
    - If portfolio or GitHub links are provided, prioritize those that match the job requirements.
    - Do NOT make up or fabricate links - only use provided portfolio/GitHub links.
    
    5. THE CALL TO ACTION (The Closer):
    - End with a specific question to get them talking.
    - Make it relevant to their project or needs.
    - Examples: "What's your biggest challenge with [specific aspect]?" or "When are you looking to launch this?"
    - Avoid generic questions like "Can we discuss further?"
    
    6. TONE & CLICHÉ AVOIDANCE:
    - Must be extremely direct, scannable, and professional.
    - Avoid ALL fluff, generic skills, and narrative prose.
    - Absolutely NO phrases like: "excited", "eager", "passionate", "proficient", "honed", "leveraged", or any AI clichés.
    - Keep total length under 200 words.
    
    7. DATA HYGIENE:
    - Never output placeholder tokens such as [name] or [company]. If data is missing, omit that detail rather than leaving blanks.

    8. LINK FORMAT (VERY IMPORTANT):
    - All links must be printed ONLY as plain URLs, with no additional formatting.
    - Do NOT wrap links in brackets, parentheses, quotes, markdown, or text labels.
    - Output links exactly like: http://example.com

    
    Job Description (analyze carefully for specific problem, tech stack, and requirements):
    {job_description}
    
    Candidate Information (use ONLY what's relevant to the job, prioritize projects and links):
    - Name: {first_name} {last_name}
    - Experience: {experience}
    - Additional Info: {additional_info}
    - Preferences: {preferences}
    - Portfolio Link: {portfolio}
    - GitHub Link: {github}

    
    Important: The final output must follow the Hook-Value-Proof format and immediately highlight related, verifiable work.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4", # gpt-4 is generally better for complex prompt adherence
        messages=[
            {"role": "system", "content": "You are a professional cover letter writer using the Hook-Value-Proof format. Your purpose is to acknowledge the client's problem, offer a solution, provide proof through similar projects, and end with an engaging question."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6 # Lowered temperature for more structure
    )

    return response.choices[0].message.content

# --- END OF UPDATED GENERATION LOGIC ---

@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond("Commands:\n/setup_profile - Set up your profile\n/generate job_descripition - Generate a cover letter")

@bot.on(events.NewMessage(pattern=r'(?s)/generate\s*(.*)'))  
async def handle_job_description(event):
    job_description = event.pattern_match.group(1).strip()
    
    if not job_description:
        await event.respond("Please provide a job description after the /generate command.")
        return

    user_data = {
        "user_id": event.sender_id,
        "job_description": job_description
    }

    await event.respond("Generating application note...")
    
    # Send the job description to the API on your external server
    response = requests.post("https://web-production-ec6c45.up.railway.app/generate_cover_letter", json=user_data)

    if response.status_code == 200:
        cover_letter = response.json().get("cover_letter", "Error generating cover letter.")
        
        # Respond with a copyable text block
        await event.respond(f"```{cover_letter}```", parse_mode="markdown")
    elif response.status_code == 404:
        await event.respond("Please set up your profile first using /setup_profile.")
    else:
        # Get error details from response
        try:
            error_details = response.json()
            error_message = error_details.get('error', 'Unknown error')
        except:
            error_message = f"HTTP {response.status_code}: {response.text}"
        
        await event.respond(f"Failed to generate cover letter. Error: {error_message}")

async def main():
    """Main function to run the bot"""
    print("Starting bot...")
    # Using 'await bot.start(BOT_TOKEN)' for bot login
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())