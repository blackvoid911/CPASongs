@echo off
python -u "C:\Users\WelCome\AndroidStudioProjects\CPASongs\verify_urdu_bible.py" > "C:\Users\WelCome\AndroidStudioProjects\CPASongs\urdu_verification.txt" 2>&1
echo Done. Exit code: %ERRORLEVEL%
type "C:\Users\WelCome\AndroidStudioProjects\CPASongs\urdu_verification.txt"

