# TextRuler Build Script

## Build Instructions

### Prerequisites
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Build Executable
```bash
pyinstaller TextRuler.spec
```

The executable will be created in the `dist` folder.

### Alternative Simple Build
```bash
pyinstaller --name TextRuler --onefile --windowed --icon=resources/icon.png --add-data "resources;resources" main.py
```

## Distribution

The resulting `TextRuler.exe` in the `dist` folder is a standalone executable that can be distributed without requiring Python installation.
