import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import tempfile
from discord import app_commands

from urls_organizer.summarize import process_urls
from urls_organizer.group import process_groups
from urls_organizer.bookmark import grouped_csv_to_bookmark_html

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient(intents=intents)

@client.tree.command(name="summarize_group", description="Upload a .txt file of URLs to summarize, group, and get results.")
@app_commands.describe(urls_file="A .txt file containing URLs, one per line.")
async def summarize_group(interaction: discord.Interaction, urls_file: discord.Attachment):
    await interaction.response.defer(thinking=True)
    # Save uploaded file to a temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "urls.txt")
        output_dir = os.path.join(tmpdir, "output")
        os.makedirs(output_dir, exist_ok=True)
        summaries_path = os.path.join(output_dir, "summaries.csv")
        grouped_path = os.path.join(output_dir, "grouped_summaries.csv")
        bookmarks_path = os.path.join(output_dir, "bookmarks.html")
        await urls_file.save(input_path)
        # Summarize
        process_urls(input_file=input_path, summary_file=summaries_path, error_file=os.path.join(output_dir, "errors.txt"))
        process_groups(input_file=summaries_path, output_file=grouped_path)
        grouped_csv_to_bookmark_html(grouped_path, bookmarks_path)
        # Send results
        await interaction.followup.send(content="Here are your grouped summaries and bookmarks:",
            files=[discord.File(grouped_path, filename="grouped_summaries.csv"),
                   discord.File(bookmarks_path, filename="bookmarks.html")])

@client.tree.command(name="testtest", description="Test if the bot is working.")
async def testtest(interaction: discord.Interaction):
    await interaction.response.send_message("Bot is alive and responding to slash commands!")

if __name__ == '__main__':
    if not TOKEN:
        print('Please set DISCORD_BOT_TOKEN in your .env file.')
    else:
        client.run(TOKEN)
