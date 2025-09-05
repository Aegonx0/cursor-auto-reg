@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Building standalone executable...
pyinstaller --onefile --windowed --name "CursorAutoRegister" --icon=NONE cursor_auto_register.py

echo Build complete! Check the 'dist' folder for your executable.
pause