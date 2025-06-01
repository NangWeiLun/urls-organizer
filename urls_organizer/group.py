"""
1. Read url and content from a file named `summaries.csv`.
2. Each line in the file contains a URL and its corresponding summary.
3. Read the first 20 summarys from the file, send them to aistudio.google.com's API to generate a group summary.
    - start with 0 group.
    - keep the index of the summary, use the index for grouping.
    - ask OpenAI to group the index of the summarys, give the group a name
    - if none of the existing group suitable then create a new group
    - example: 
        - input: 
            ```
            Current groups = finance, technology, health
            Summaries = Summary 1, Summary 2, Summary 3, .... Summary 20
            ```
        - output:
            ```
            finance: [0, 1]
            technology: [2, 3]
            health: [4, 5]
            new_group: [6, 7, 8, 9, 10, 11]
            ```
4. Save the grouped summaries in a file named `grouped_summaries.csv`.
5. Repeat the process for the next 20 summaries until all summaries are processed.
"""

import csv
import os
import google.generativeai as genai
from tqdm import tqdm
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def group_summaries_api(summaries, current_groups=None, api_key=None):
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google Gemini API key not set. Set GOOGLE_API_KEY env variable or pass api_key param.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(os.getenv("GOOGLE_MODEL_NAME"))
    group_list = ", ".join(current_groups) if current_groups else "error"
    summaries_text = "\n".join([f"{i}: {s}" for i, s in enumerate(summaries)])
    prompt = (
        f"Current groups: {group_list}\n"
        f"Summaries:\n{summaries_text}\n"
        "Group the summaries by their content. For each group, provide a group name and the list of summary indices. "
        "If a summary does not fit any existing group, create a new group. "
        "If a summary is an error or could not be summarized, put it in the 'error' group. "
        "Respond in this format:\n"
        "group_name: [indices]\n"
        "..."
    )
    response = model.generate_content(prompt)
    time.sleep(1)  # avoid rate limits between API calls
    # Parse the response into a dict
    group_result = {}
    for line in response.text.strip().splitlines():
        if ':' in line:
            group, indices = line.split(':', 1)
            indices = [int(i) for i in indices.strip(" []\n").split(',') if i.strip().isdigit()]
            group_result[group.strip()] = indices
    return group_result

def process_groups(input_file=None, output_file=None, batch_size=20):
    # Set default paths to use output folder
    if input_file is None:
        input_file = os.path.join(os.path.dirname(__file__), '../output/summaries.csv')
    if output_file is None:
        output_file = os.path.join(os.path.dirname(__file__), '../output/grouped_summaries.csv')
    groups = {"error": []}  # Always include 'error' group
    processed_batches = set()
    # Support resume: read already processed groupings and reconstruct groups
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as outfile:
            reader = csv.reader(outfile)
            for row in reader:
                if row and len(row) > 2:
                    group_name, url, summary = row[0], row[1], row[2]
                    processed_batches.add((url, summary))
                    if group_name not in groups:
                        groups[group_name] = []
                    groups[group_name].append((url, summary))
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'a', newline='', encoding='utf-8') as outfile:
        reader = list(csv.reader(infile))
        writer = csv.writer(outfile)
        for i in tqdm(range(0, len(reader), batch_size), desc='Grouping Summaries'):
            batch = reader[i:i+batch_size]
            # Skip batch if all summaries in this batch are already grouped
            if all((row[0], row[1]) in processed_batches for row in batch):
                continue
            summaries = [row[1] for row in batch]
            current_groups = list(groups.keys())
            logging.info(f'Processing batch {i//batch_size+1}: {len(batch)} summaries')
            group_result = group_summaries_api(summaries, current_groups)
            for group_name, indices in group_result.items():
                if group_name not in groups:
                    groups[group_name] = []
                for idx in indices:
                    abs_idx = i + idx
                    groups[group_name].append((reader[abs_idx][0], reader[abs_idx][1]))
                    writer.writerow([group_name, reader[abs_idx][0], reader[abs_idx][1]])
                    outfile.flush()  # Ensure the row is written immediately
    logging.info('Grouping complete.')
    return groups

if __name__ == "__main__":
    process_groups()