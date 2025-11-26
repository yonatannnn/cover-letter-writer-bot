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
    form_link = f"https://writer-microservice-production.up.railway.app/profile_form?user_id={user_id}"
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
    Write a concise, project-driven application note (NOT a traditional cover letter) strictly following these guidelines:
    
    1. FORMAT & LENGTH:
    -   
    - Omit traditional elements like date, address, and formal salutations. Start directly with content.
    - Use a brief, bulleted list for the main experience/project section (2-3 items).
    
    2. CONTENT FOCUS:
    - Opening: A single, brief sentence introducing the candidate and expressing direct interest in the role.
    - Body (Bulleted): List 2-3 of the candidate's MOST RELEVANT projects or concrete achievements that directly address the job requirements.
        - Each bullet point MUST integrate a direct link (e.g., [Project Name](link_to_github_or_portfolio)) as verifiable proof of work. Prioritize this link integration.
        - Focus on the *impact*, *scale*, or *specific technology* that matches the job description.
    - Closing: A single, professional sentence inviting immediate review of the linked projects.
    
    3. TONE & CLICHÉ AVOIDANCE:
    - Must be extremely direct, scannable, and professional.
    - Avoid ALL fluff, generic skills, and narrative prose. The entire goal is to point the reader to the proof of work.
    - Absolutely NO phrases like: "excited", "eager", "passionate", "proficient", "honed", "leveraged", "seamlessly", or any AI clichés.
    
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
        model="gpt-4", # gpt-4 is generally better for complex prompt adherence
        messages=[
            {"role": "system", "content": "You are a professional technical recruiter writing an ultra-concise application note. Your sole purpose is to quickly highlight verified work that directly matches the job requirements."},
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
    response = requests.post("https://writer-microservice-production.up.railway.app/generate_cover_letter", json=user_data)

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