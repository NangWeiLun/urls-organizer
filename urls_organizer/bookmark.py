import csv
import os

def grouped_csv_to_bookmark_html(csv_path, html_path):
    """
    Convert grouped_summaries.csv to a Netscape bookmark HTML file.
    Each group becomes a folder, each URL a bookmark with its summary as the description.
    Assumes grouped_summaries.csv columns: group,url,summary (no header).
    """
    groups = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            group = row[0] if row[0] else 'Ungrouped'
            url = row[1]
            summary = row[2] if len(row) > 2 else ''
            if not url:
                continue
            groups.setdefault(group, []).append((url, summary))

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
        f.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
        f.write('<TITLE>Bookmarks</TITLE>\n')
        f.write('<H1>Bookmarks</H1>\n')
        f.write('<DL><p>\n')
        for group, bookmarks in groups.items():
            f.write(f'    <DT><H3>{group}</H3>\n')
            f.write('    <DL><p>\n')
            for url, summary in bookmarks:
                f.write(f'        <DT><A HREF="{url}">{url}</A>\n')
                if summary:
                    f.write(f'        <DD>{summary}\n')
            f.write('    </DL><p>\n')
        f.write('</DL><p>\n')

if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), '../output/grouped_summaries.csv')
    html_path = os.path.join(os.path.dirname(__file__), '../output/bookmarks.html')
    grouped_csv_to_bookmark_html(csv_path, html_path)
    print(f"Bookmark HTML exported to {html_path}")