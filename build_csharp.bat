@echo off
echo Building CursorAutoRegister C# Application...

echo Building C# application...
dotnet restore
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o ./publish

echo Build complete! 
echo Executable: ./publish/CursorAutoRegister.exe
echo.
echo The application includes:
echo - Stunning C# WPF interface with animations and particles
echo - Complete automation logic built-in C#
echo - Selenium WebDriver with automatic ChromeDriver management
echo - All dependencies bundled in single EXE
echo - No Python required!
echo.
pause