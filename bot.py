from telethon import TelegramClient, events
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = TelegramClient('cover_letter_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

user_states = {}

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Welcome! Use /set_profile to set up your profile.\n\nCommands:\n/start - Start the bot\n/setup_profile - Set up your profile\n/help - Show this help message\n/generate job_descripition - Generate a cover letter")

@bot.on(events.NewMessage(pattern='/setup_profile'))
async def setup_profile(event):
    user_id = event.sender_id
    form_link = f"https://cover-letter-writer-bot.onrender.com/profile_form?user_id={user_id}"
    await event.respond(f"Please set up your profile using this form: {form_link}")

@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond("Commands:\n/start - Start the bot\n/setup_profile - Set up your profile\n/help - Show this help message\n/generate job_descripition - Generate a cover letter")

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

    await event.respond("Generating cover letter...")
    # Send the job description to the API
    response = requests.post("https://cover-letter-writer-bot.onrender.com/generate_cover_letter", json=user_data)

    if response.status_code == 200:
        cover_letter = response.json().get("cover_letter", "Error generating cover letter.")
        
        # Respond with a copyable text block
        await event.respond(f"```{cover_letter}```", parse_mode="markdown")
    else:
        await event.respond("Failed to generate cover letter. Please try again later.")


print("Bot is running...")
bot.run_until_disconnected()