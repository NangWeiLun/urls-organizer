# URL Organizer

> **Note:** For my personal motivation, workflow, and experiments with GitHub Copilot, see [NOTE.md](NOTE.md).

This project summarizes and groups URLs using the Google Gemini API. It is designed to process a list of URLs, generate concise summaries, and organize them into logical groups. The workflow is robust, supporting stop/resume, error handling, and immediate output flushing for reliability.

## Features
- **Summarize URLs:** Reads URLs from a file and generates summaries using Gemini.
- **Group Summaries:** Organizes summaries into groups using Gemini, with an explicit `error` group for failed or problematic URLs.
- **Stop and Resume:** Skips already-processed URLs and groups, allowing safe interruption and resumption.
- **Error Handling:** URLs that fail to summarize are logged to `output/errors.txt` and can be retried.
- **Immediate Output:** All output files are flushed after each write for data safety.
- **Progress Bars & Logging:** Uses `tqdm` for progress and Python logging for status and errors.

## Project Structure
```
requirements.txt
output/
  errors.txt         # URLs that failed to summarize
  summaries.csv      # URLs and their summaries
sample/
  urls.txt           # Input URLs to process
url_organizer/
  group.py           # Grouping logic
  main.py            # Entry point
  summarize.py       # Summarization logic
  bookmark.py        # Bookmark export logic
```

## Setup
1. **Clone the repository and create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
   This will install all dependencies listed in `requirements.txt` and set up the project in editable mode.
2. **Set your Google Gemini API key and model name:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and fill in your actual API key and model name:
     ```env
     GOOGLE_API_KEY=your_api_key_here
     GOOGLE_MODEL_NAME=gemini-2.5-flash-preview-05-20
     ```

## Usage

### Summarize URLs
Run the main script to summarize URLs from `sample/urls.txt`:
```bash
python url_organizer/main.py
```
- Summaries are saved to `output/summaries.csv`.
- Failed URLs are logged to `output/errors.txt`.

### Resume or Retry Errors
- If you want to retry a failed URL, simply remove that URL from `output/errors.txt` (and make sure it is still present in your input file, e.g., `sample/urls.txt`).
- The next time you run the summarizer, it will retry any URLs that are not listed in `output/errors.txt` or `output/summaries.csv`.
- This allows you to manually control which URLs are retried, without needing to create a new input file.

### Group Summaries
- Summaries are grouped by running the grouping logic (automatically called in `main.py`):
  - Output is saved to `output/grouped_summaries.csv`.
  - The `error` group is always present for problematic summaries.

### Exporting Bookmarks as HTML

After grouping your URLs, you can export them as a browser-importable bookmark HTML file:

1. Make sure you have run the grouping step and that `output/grouped_summaries.csv` exists.
2. Run the following command:

   ```bash
   python url_organizer/bookmark.py
   ```

This will generate `output/bookmarks.html`, which you can import into Chrome, Firefox, or other browsers via their bookmark manager.

- Each group will appear as a folder.
- Each URL will be a bookmark, with its summary as the description.

If you re-run the grouping or summarization, you can re-run the export to update the HTML file.

## Running as a Discord Bot

You can use this project as a Discord bot that summarizes and groups URLs from a `.txt` file uploaded via a slash command.

### 1. Set up your Discord bot token
- Add your bot token to your `.env` file:
  ```env
  DISCORD_BOT_TOKEN=your_discord_bot_token_here
  ```

### 2. Install dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### 3. Start the Discord bot
```bash
python url_organizer/discord_bot.py
```

### 4. Use the bot in Discord
- Use the `/summarize_group` slash command and upload a `.txt` file containing URLs (one per line).
- The bot will reply with two files: `grouped_summaries.csv` and `bookmarks.html`.

> Note: Make sure your bot has the necessary permissions to read messages, send messages, and attach files in your server.

## Preparing Your URLs
The list of URLs is extracted from Chrome bookmarks or Edge favorites. You can prepare your own `urls.txt`:

- **For Chrome bookmarks:**
  1. Go to the Chrome bookmarks manager.
  2. Select the bookmarks you want.
  3. Copy them (Ctrl+C).
  4. Paste into a `.txt` file (one URL per line).

You can use this file as your `sample/urls.txt` or specify it as input to the summarizer.

## Notes
- The program will stop immediately if the Gemini API quota is exceeded or a critical error occurs.
- All output is flushed to disk after each write for safety.
- You can safely stop and resume processing at any time.

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies.

## License
This project is licensed under the [MIT License](LICENSE).
