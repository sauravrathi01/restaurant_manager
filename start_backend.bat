@echo off
echo Starting AI-Powered Menu Intelligence Widget Backend...
echo.
echo Make sure you have:
echo 1. Python 3.8+ installed
echo 2. pipenv installed: pip install pipenv
echo 3. Dependencies installed: pipenv install --dev
echo 4. backend/.env file configured with your OpenAI API key
echo.
cd backend
pipenv run python main.py
pause
