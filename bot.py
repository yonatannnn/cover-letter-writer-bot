from telethon import TelegramClient, events
import requests
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create client without starting it immediately
bot = TelegramClient('cover_letter_bot', API_ID, API_HASH)

user_states = {}

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Welcome!\n\nCommands:\n/start - Start the bot\n/setup_profile - Set up your profile\n/help - Show this help message\n/generate job_descripition - Generate a cover letter")

@bot.on(events.NewMessage(pattern='/setup_profile'))
async def setup_profile(event):
    user_id = event.sender_id
    form_link = f"https://cover-letter-writer-bot-production.up.railway.app/profile_form?user_id={user_id}"
    await event.respond(f"Please set up your profile using this form: {form_link}")

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

    await event.respond("Generating cover letter...")
    # Send the job description to the API
    response = requests.post("https://cover-letter-writer-bot-production.up.railway.app/generate_cover_letter", json=user_data)

    if response.status_code == 200:
        cover_letter = response.json().get("cover_letter", "Error generating cover letter.")
        
        # Respond with a copyable text block
        await event.respond(f"```{cover_letter}```", parse_mode="markdown")
    elif response.status_code == 404:
        await event.respond("Please set up your profile first using /setup_profile.")
    else:
        await event.respond("Failed to generate cover letter. Please try again later.")

async def main():
    """Main function to run the bot"""
    print("Starting bot...")
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())