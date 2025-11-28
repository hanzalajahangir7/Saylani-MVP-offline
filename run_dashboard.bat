@echo off
echo ============================================================
echo  SAYLANI AI DECISION SUPPORT SYSTEM - DASHBOARD
echo ============================================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Launching dashboard...
streamlit run dashboard/app.py
