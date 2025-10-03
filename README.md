# YouNote AI 

YouNote is your AI-powered companion for effortless learning. Instantly generate clear, concise notes from any YouTube video. Just paste the link and let YouNote do the rest! All your notes are saved for easy access, so you can revisit key insights and the original videos anytime.
Start noting smarter and learning faster with YouNote today!

Deployed: https://younote-q32b.onrender.com

## Stack
- Backend: Python, Django
- DataBase:  PosgresSQL
- Frontend: HTML, CSS, Javascript

- Deployed via Render

## Example
![YouNote Example (1)](https://github.com/user-attachments/assets/fea4306a-d07c-4f0a-9a20-c39379698678)

![YouNote Example2 (1)](https://github.com/user-attachments/assets/5f0b62b8-62d6-437f-8903-fbb16134a4ae)


## Features
- User authentication (signup, login)
- Generates Notes based on Youtube link input by user
- Downloads audio from a YouTube link via oytubefix
- Transcribes audio via AssemblyAI
- Generates study-style notes using OpenAI
- Stores generated notes per user in the database
- Allows user to edit and delete saved notes



## Requirements
- Python 3.11+ 
- Django 4+
- pytubefix 
- assemblyai (for transcription)
- openai (for text generation)
- Other deps in requirements.txt (all required deps are in this file)

## Environment variables
Create a `.env` or configure environment variables:

```
ASSEMBLYAI_KEY=your_assemblyai_key
OPENAI_KEY=your_openai_key
DJANGO_SECRET_KEY=your_secret_key
```

(Names correspond to keys referenced with python-decouple `config()` in views.)

## Install (Windows)
1. Create and activate virtualenv:
   powershell:
   ```
   python -m venv myenv
   .\myenv\Scripts\Activate.ps1
   ```
   cmd:
   ```
   python -m venv myenv
   myenv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add env vars (or use a `.env` file).

## Run (development)
```
python manage.py migrate
python manage.py runserver
```



