# Mini ATS System

The Mini ATS System is a lightweight applicant tracking simulator that evaluates how well a resume matches a given job description. It extracts skills from both the resume and the job posting, categorizes them (hard skills, tools, soft skills), calculates match scores, and provides suggestions to improve the resume. The frontend is built with Streamlit and the skill library is stored in a SQLite database.

## Features

* Upload a resume (PDF or DOCX)
* Paste any job description
* Extract skills using a database-backed keyword list
* Categorize skills into hard skills, tools, and soft skills
* Compute category-level match scores and overall fit score
* Display matched, missing, and extra skills
* Generate suggestions for improving the resume

## Installation

1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
```

3. Activate the virtual environment
```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Initialize the skills database
```bash
python dbpop.py
```

This will create or update the skills.db file in the project root.

## Running the Application

Start the Streamlit app from the project root:
```bash
streamlit run src/app.py
```

The application will be available at:
```
http://localhost:8501
```

## Project Structure
```
src/
  app.py
  parsers.py
  keyword_extractor.py
  scoring.py
  suggestions.py
  text_cleaning.py
  visuals.py
dbpop.py
skills.db
requirements.txt
README.md
```

## Notes

* To modify or expand the skill database, edit dbpop.py and run it again.
* This project is intended for demonstration and portfolio use rather than production deployment.
