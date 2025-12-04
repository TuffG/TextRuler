# TextRuler

A Windows text ruler application to help focus on specific lines of text with optional screen overlay.

![TextRuler](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Ruler Overlay**: Horizontal ruler that can be positioned anywhere on screen
- **Screen Fade/Overlay**: Dims the entire screen except the ruler area for better focus
- **Color Customization**: 8 colors (Red, Blue, Green, Yellow, Purple, Orange, Black, White) with per-color opacity memory
- **Global Hotkeys**: 
  - `Ctrl+Alt+F12`: Toggle ruler
  - `Ctrl+Alt+F11`: Toggle overlay
  - Mouse wheel: Adjust height/opacity
  - `Shift+Mouse wheel`: Change colors
- **Settings Persistence**: All settings automatically saved between sessions
- **System Tray Integration**: Convenient tray icon with context menu
- **Multi-Monitor Support**: Works seamlessly across multiple screens

## Screenshots

*Add screenshots here to showcase the application*

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10/11

### From Source

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/TextRuler.git
cd TextRuler
```

> **Note**: Replace `YOUR_USERNAME` with your GitHub username when cloning.

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

The application starts minimized in the system tray. Right-click the tray icon to access the menu.

### Keyboard Shortcuts

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
- **Toggle Ruler** - Turn ruler on/off
- **Toggle Overlay** - Turn overlay on/off
- **Ruler Color** - Choose color for ruler
- **Overlay Color** - Choose color for overlay
- **Exit** - Quit application

For detailed usage instructions, see [QUICKSTART.md](QUICKSTART.md).

## Building Executable

To create a standalone `.exe` file:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller TextRuler.spec
```

The executable will be created in the `dist` folder and can be distributed without requiring Python installation.

For more build options, see [BUILD.md](BUILD.md).

## Project Structure

```
TextRuler/
├── main.py              # Application entry point
├── ruler_window.py      # Ruler overlay window
├── overlay_window.py    # Screen overlay with cutout
├── tray_icon.py         # System tray icon and menu
├── settings.py          # Settings management
├── hotkey_manager.py    # Global hotkey handling
├── requirements.txt     # Python dependencies
├── TextRuler.spec      # PyInstaller configuration
├── README.md           # This file
├── QUICKSTART.md       # Quick start guide
├── BUILD.md            # Build instructions
└── LICENSE             # MIT License
```

## Configuration

Settings are stored in `~/.text_ruler_settings.json` and include:
- Ruler position, height, color, and visibility
- Overlay color and visibility
- Per-color opacity settings
- Hotkey configurations

To reset settings, delete the settings file.

## Troubleshooting

- **Hotkeys not working**: Run the application as administrator
- **Ruler not visible**: Press `Ctrl+Alt+F12` or use the tray menu
- **Icon missing**: A default icon will be used if the icon file is not found

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Global hotkeys powered by [pynput](https://github.com/moses-palmer/pynput)

## Author

**Gebhard Schrader**

- GitHub: [@TuffG](https://github.com/TuffG)

---

If you find this project useful, please consider giving it a ⭐ on GitHub!
