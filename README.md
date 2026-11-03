# PrepPilot AI

An AI-powered placement practice companion for students.

## Current MVP

* Generate beginner, intermediate, and advanced interview questions.
* Submit an answer and receive structured AI feedback.
* Uses BharatCode's OpenAI-compatible Chat Completions API.

## Requirements

* Python 3.10+
* A BharatCode API key with eligible API access.

## Run Locally (Windows PowerShell)

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your private API key:

   ```text
   BHARATCODE_API_KEY=your_real_key_here
   ```

4. Start the application:

   ```powershell
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

## Security

Never share your API key or commit `.env` to GitHub. The `.gitignore` file excludes it.
