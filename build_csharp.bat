@echo off
echo Building CursorAutoRegister C# Application...

echo Installing Python dependencies...
pip install -r requirements.txt

echo Building C# application...
dotnet restore
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o ./publish

echo Copying Python backend...
copy automation_backend.py ./publish/

echo Build complete! 
echo Executable: ./publish/CursorAutoRegister.exe
echo.
echo The application includes:
echo - Beautiful C# WPF interface with animations
echo - Python automation backend
echo - All dependencies bundled
echo.
pause