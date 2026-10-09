# AI Usage Report

- **AI Tools Used**: Google Gemini 3.1 Pro (via Antigravity IDE)
- **What each tool was used for**: Generating the boilerplate code, organizing the project structure, generating test cases based on provided requirements, and formatting the documentation.
- **Representative prompts**: "Create the base_scraper.py module with requests Retry logic", "Implement the deduplication logic based on the PDF spec"
- **Which parts of the code were AI-assisted**: Most of the standard pipeline structure and file creation was automated based on the user's explicit request to finish quickly. 
- **Important changes**: Verified that the deduplication logic strictly follows the exact fields recommended in the reference (Title for books, Author + Title[:50] for quotes). Ensured tests exactly matched expected outcomes.
- **Testing**: Ran `pytest` to confirm pure functions worked properly, then `python main.py` to confirm the full ETL pipeline successfully executed and created the output folder, `final_dataset.csv`, `summary_report.json`, and `scraper.log`.
