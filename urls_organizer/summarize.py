"""
# This script reads URLs from a file and summarizes each URL using aistudio.google.com's API.
1. read urls.txt line by line
2. each line represents a URL
3. send this url to aistudio.google.com and ask for a summary
4. the url and summary is saved in a file named summaries.csv
5. if the URL is invalid or request fails, save this URL in a file named errors.txt
"""

import csv
import time
import os
import google.generativeai as genai
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def summarize_url_content(url, api_key=None):
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google Gemini API key not set. Set GOOGLE_API_KEY env variable or pass api_key param.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(os.getenv("GOOGLE_MODEL_NAME"))
    prompt = f"Summarize the content of this URL in 2-3 sentences: {url}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # If quota or API error, stop the whole program
        logging.critical(f'Gemini API error: {e}')
        raise

def process_urls(input_file=None, summary_file=None, error_file=None):
    # Set default paths to use sample/urls.txt and output folder
    if input_file is None:
        input_file = os.path.join(os.path.dirname(__file__), '../sample/urls.txt')
    if summary_file is None:
        summary_file = os.path.join(os.path.dirname(__file__), '../output/summaries.csv')
    if error_file is None:
        error_file = os.path.join(os.path.dirname(__file__), '../output/errors.txt')

    # Load already processed URLs to support resume
    processed_urls = set()
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as sumfile:
            reader = csv.reader(sumfile)
            for row in reader:
                if row:
                    processed_urls.add(row[0])
    if os.path.exists(error_file):
        with open(error_file, 'r', encoding='utf-8') as errfile:
            for line in errfile:
                if line.strip():
                    processed_urls.add(line.strip())

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(summary_file, 'a', newline='', encoding='utf-8') as sumfile, \
         open(error_file, 'a', encoding='utf-8') as errfile:
        writer = csv.writer(sumfile)
        urls = [line.strip() for line in infile if line.strip()]
        for url in tqdm(urls, desc='Processing URLs'):
            if url in processed_urls:
                continue
            # Use tqdm.write to avoid interfering with the progress bar
            tqdm.write(f'Processing URL: {url}')
            try:
                summary = summarize_url_content(url)
                writer.writerow([url, summary])
                sumfile.flush()  # Ensure the row is written immediately
                tqdm.write(f'Success: {url}')
            except Exception as e:
                errfile.write(url + '\n')
                errfile.flush()
                tqdm.write(f'Exception for {url}: {e}')
                raise  # Stop the program on any error
            time.sleep(1)  # avoid rate limits

if __name__ == "__main__":
    process_urls()
