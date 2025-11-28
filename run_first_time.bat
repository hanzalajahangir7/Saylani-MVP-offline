@echo off
echo ============================================================
echo  SAYLANI AI DECISION SUPPORT SYSTEM - FIRST TIME SETUP
echo ============================================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Please ensure Python 3.8+ is installed
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo [3/5] Installing dependencies...
echo This may take a few minutes...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [4/5] Training AI engine on historical data...
echo This will take 3-5 minutes...
python train_engine.py
if errorlevel 1 (
    echo ERROR: Training failed
    pause
    exit /b 1
)
echo ✓ AI engine trained successfully
echo.

echo [5/5] Launching dashboard...
streamlit run dashboard/app.py
