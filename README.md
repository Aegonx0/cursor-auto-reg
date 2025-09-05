# CursorAutoRegister

Automated Cursor account registration tool with stunning modern interfaces available in both C# WPF and Python versions.

## 🎨 Two Beautiful Interfaces

### 🔥 C# WPF Version (Recommended)
- **Ultra-Modern Design**: Material Design with glass morphism effects
- **Animated Particles**: Dynamic background with floating particles
- **Gradient Animations**: Smooth color transitions and hover effects
- **Professional Layout**: Card-based design with shadows and blur effects
- **Real-time Progress**: Animated progress bars with gradient colors

### 🐍 Python Tkinter Version
- **GitHub Dark Theme**: Professional dark interface
- **Custom Components**: Hand-crafted buttons and progress bars
- **Smooth Animations**: Flowing progress indicators
- **Clean Typography**: Modern fonts with proper hierarchy

## ✨ Features

- **Automated Browser Control**: Chrome in incognito mode with stealth settings
- **Smart Name Generation**: Realistic random names for human-like accounts
- **Temporary Email Integration**: Seamless temp-mail.org integration
- **Automatic Verification**: Extracts and enters 6-digit codes automatically
- **Real-time Logging**: Beautiful activity logs with timestamps
- **Human-like Behavior**: Random delays and natural interactions

## 🚀 Quick Start

### C# WPF Version (Best Experience)
```bash
# Build the stunning C# interface
build_csharp.bat
```

### Python Version (Cross-platform)
```bash
# Build the Python version
build.bat
```

## 📋 Requirements

- **Windows 10/11** (for C# version)
- **Chrome Browser** installed
- **.NET 6.0** (for C# version)
- **Python 3.7+** (for Python version)
- **Internet Connection**

## 🛠️ Build Options

### C# WPF Application
```bash
# Install dependencies and build
dotnet restore
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true

# Or use the batch file
build_csharp.bat
```

### Python Application
```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
pyinstaller --onefile --windowed cursor_auto_register.py
```

### GitHub Actions
Both versions are built automatically:
- **C# Version**: `CursorAutoRegister.exe`
- **Python Version**: `CursorAutoRegister-Python.exe`

## 🎯 How It Works

1. **🚀 Browser Launch**: Opens Chrome in incognito mode with anti-detection
2. **🌐 Navigation**: Goes to Cursor sign-up page
3. **👤 Identity Generation**: Creates realistic random names
4. **📧 Email Setup**: Gets temporary email from temp-mail.org
5. **📝 Form Filling**: Enters all registration details
6. **🔐 Password Creation**: Generates secure, memorable passwords
7. **📬 Email Verification**: Waits for and extracts verification codes
8. **✅ Completion**: Finalizes account creation

## 🎨 Interface Highlights

### C# WPF Features
- **Glass Morphism Cards**: Translucent panels with blur effects
- **Particle System**: 50+ animated background particles
- **Gradient Buttons**: Multi-color hover animations
- **Smooth Transitions**: Fade and scale animations
- **Modern Typography**: Segoe UI with perfect spacing

### Python Features
- **GitHub Dark Theme**: Professional developer-style colors
- **Custom Animations**: Hand-coded progress and pulse effects
- **Rounded Components**: Modern button and card designs
- **Gradient Backgrounds**: Smooth color transitions

## 📁 File Structure

```
CursorAutoRegister/
├── 🎨 C# WPF Version
│   ├── MainWindow.xaml          # Beautiful UI layout
│   ├── MainWindow.xaml.cs       # UI logic and animations
│   ├── App.xaml                 # Application resources
│   └── CursorAutoRegister.csproj # Project configuration
├── 🐍 Python Version
│   ├── cursor_auto_register.py  # Main application
│   └── build_exe.py            # Build script
├── 🔧 Backend
│   ├── automation_backend.py    # Selenium automation
│   └── requirements.txt        # Python dependencies
└── 🚀 Build Scripts
    ├── build_csharp.bat        # C# build script
    └── build.bat               # Python build script
```

## 🎯 Why Choose Each Version?

### C# WPF Version
- ✅ **Stunning Visuals**: Material Design with animations
- ✅ **Better Performance**: Native Windows application
- ✅ **Modern UI**: Glass effects and particle animations
- ✅ **Professional Feel**: Enterprise-grade interface

### Python Version
- ✅ **Cross-platform**: Works on Windows, Mac, Linux
- ✅ **Lightweight**: Smaller file size
- ✅ **Familiar**: Standard Python development
- ✅ **Customizable**: Easy to modify and extend

Both versions provide the same powerful automation capabilities with beautiful, modern interfaces!