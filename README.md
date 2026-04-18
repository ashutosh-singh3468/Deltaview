# Document Comparator Web App

Simple Django app to compare two documents (`pdf`, `docx`, `txt`) and show highlighted differences.

## Features
- Upload two files (left and right)
- Extract text from PDF, DOCX, TXT
- Show word, sentence, and character counts
- Highlight differences:
  - Added text (green)
  - Removed text (red)
  - Changed text (yellow)
- Similarity percentage
- Split-screen comparison UI using Bootstrap
- Save file names and summary in SQLite

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000/
