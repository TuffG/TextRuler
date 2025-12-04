# TextRuler - Quick Start

## Installation

```bash
# Install dependencies
pip install PyQt5 pynput
```

## Starting the Application

```bash
python main.py
```

The application starts minimized in the system tray (taskbar).

## Usage

### Keyboard Shortcuts (Global)

| Shortcut | Function |
|----------|----------|
| `Ctrl+Alt+F12` | Toggle ruler on/off |
| `Ctrl+Alt+F11` | Toggle overlay on/off |

### Mouse Controls

**On the Ruler:**
- **Drag**: Move ruler vertically
- **Mouse wheel**: Adjust height (20-500px)
- **Shift+Mouse wheel**: Change color

**On the Overlay:**
- **Mouse wheel**: Adjust transparency
- **Shift+Mouse wheel**: Change color

### System Tray Menu

Right-click on the tray icon:
- Toggle Ruler - Turn ruler on/off
- Toggle Overlay - Turn overlay on/off
- Ruler Color - Choose color for ruler
- Overlay Color - Choose color for overlay
- Exit - Quit application

## Features

✅ **8 Colors**: Red, Blue, Green, Yellow, Purple, Orange, Black, White  
✅ **Transparency Memory**: Each color remembers its transparency  
✅ **Settings**: All settings are automatically saved  
✅ **Multi-Monitor**: Works on multiple screens  

## Creating Executable

To create a `.exe` file:

```bash
pip install pyinstaller
pyinstaller TextRuler.spec
```

The `.exe` will be created in the `dist/` folder and can be run without Python installation.

## Troubleshooting

- **Hotkeys not working**: Run as administrator
- **Ruler not visible**: Press `Ctrl+Alt+F12` or use tray menu
- **Icon missing**: Icon will be automatically generated on first start

## Reset Settings

Delete the file: `C:\Users\YourName\.text_ruler_settings.json`
