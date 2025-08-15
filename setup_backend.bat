@echo off
echo Setting up AI-Powered Menu Intelligence Widget Backend...
echo.

echo Installing pipenv...
pip install pipenv

echo.
echo Installing backend dependencies...
cd backend
pipenv install --dev
cd ..

echo.
echo Backend setup complete!
echo.
echo Next steps:
echo 1. Copy backend/env.example to backend/.env
echo 2. Add your OpenAI API key to backend/.env
echo 3. Run start_backend.bat to start the server
echo.
pause
