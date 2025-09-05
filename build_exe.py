import subprocess
import sys
import os

def build_exe():
    print("Building CursorAutoRegister executable...")
    
    try:
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed", 
            "--name", "CursorAutoRegister",
            "--add-data", "cursor_auto_register.py;.",
            "--hidden-import", "selenium",
            "--hidden-import", "webdriver_manager",
            "--hidden-import", "requests",
            "--hidden-import", "bs4",
            "cursor_auto_register.py"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            print("📁 Executable created: dist/CursorAutoRegister.exe")
        else:
            print("❌ Build failed:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    build_exe()