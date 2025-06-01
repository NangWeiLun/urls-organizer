from summarize import process_urls
from group import process_groups
from dotenv import load_dotenv
from bookmark import grouped_csv_to_bookmark_html
import os

if __name__ == "__main__":
    load_dotenv()
    process_urls()
    process_groups()
    csv_path = os.path.join(os.path.dirname(__file__), '../output/grouped_summaries.csv')
    html_path = os.path.join(os.path.dirname(__file__), '../output/bookmarks.html')
    grouped_csv_to_bookmark_html(csv_path, html_path)
    print(f"Bookmark HTML exported to {html_path}")