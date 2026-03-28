@echo off
python -u "C:\Users\WelCome\AndroidStudioProjects\CPASongs\check_bible_verses.py" > "C:\Users\WelCome\AndroidStudioProjects\CPASongs\bible_check_results.txt" 2>&1
echo Done. Exit code: %ERRORLEVEL%

