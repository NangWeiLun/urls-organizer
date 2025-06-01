# Personal Notes: Why I Created This Repository

As a heavy researcher, I often open many browser tabs with articles and resources I don't have time to read or organize. Over the past two years, this habit has led to a huge backlog of unread URLs. Traditionally, organizing these links required reading them first, which was time-consuming and often impossible given my schedule.

With the advent of AI tools like NotebookLM, I realized that I may no longer need to read everything myself—AI can help summarize and organize information for me. However, to take full advantage of this, I first needed to organize the backlog of URLs I had collected. This project was created to automate the summarization and grouping of those URLs, making it easier to manage and leverage them with modern AI tools.

> I will also try Google Jules in the future as part of my workflow improvements.

## Personal Experiments with GitHub Copilot

I also created this repository to test writing all the code using GitHub Copilot in VS Code. I completed the entire codebase in about 2 hours without manually writing any code—most of my time was spent researching libraries and thinking about the design. This project serves as a testament to how AI-assisted coding can accelerate development and experimentation.

## Next Steps for Using URLs with NotebookLM

- Currently, NotebookLM does not support browsing or fetching the content of URLs from a .txt file. It only ingests the file contents as text.
- There are three possible approaches for using your URLs with NotebookLM:
  1. **Wait for NotebookLM to support adding a list of URLs as sources.** This would allow you to upload your URLs.txt and have NotebookLM fetch and process the content automatically (feature not available as of June 2025).
  2. **Add each URL manually as a source in NotebookLM.** This is time-consuming and not practical for large lists.
  3. **Process the URLs locally:**
     - Write a script to read each URL, fetch its web content, and save each page as a text or PDF file.
     - Upload these files to NotebookLM as sources for summarization and research.
     - (At this point, most of the value of NotebookLM is replaced by your local processing, since you can summarize and organize content before uploading.)

Choose the approach that best fits your workflow and the current capabilities of NotebookLM.
