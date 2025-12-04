"""
TextRuler - Main Application

A text ruler overlay application to help focus on specific lines of text.
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from settings import AppSettings
from ruler_window import RulerWindow
from overlay_window import OverlayWindow
from hotkey_manager import HotkeyManager
from tray_icon import TrayIcon


class TextRulerApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)  # Keep running when windows are hidden
        
        # Initialize settings
        self.settings = AppSettings()
        
        # Create windows
        self.ruler_window = RulerWindow(self.settings)
        self.overlay_window = OverlayWindow(self.settings, self.ruler_window)
        
        # Connect ruler to overlay
        self.ruler_window.set_overlay_window(self.overlay_window)
        
        # Create hotkey manager
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.toggle_ruler.connect(self.toggle_ruler)
        self.hotkey_manager.toggle_overlay.connect(self.toggle_overlay)
        self.hotkey_manager.start()
        
        # Create system tray icon
        self.tray_icon = TrayIcon(self.settings)
        self.tray_icon.create_tray_icon()
        
        # Connect tray icon signals
        self.tray_icon.toggle_ruler_requested.connect(self.toggle_ruler)
        self.tray_icon.toggle_overlay_requested.connect(self.toggle_overlay)
        self.tray_icon.exit_requested.connect(self.exit_app)
        self.tray_icon.ruler_color_changed.connect(self.on_ruler_color_changed)
        self.tray_icon.overlay_color_changed.connect(self.on_overlay_color_changed)
    
    def toggle_ruler(self):
        """Toggle ruler visibility."""
        self.ruler_window.toggle_visibility()
        self.tray_icon.update_ruler_state(self.ruler_window.isVisible())
        
        # Update overlay if visible
        if self.overlay_window.isVisible():
            self.overlay_window.update()
    
    def toggle_overlay(self):
        """Toggle overlay visibility."""
        self.overlay_window.toggle_visibility()
        self.tray_icon.update_overlay_state(self.overlay_window.isVisible())
    
    def on_ruler_color_changed(self, color):
        """Handle ruler color change."""
        self.settings.set_ruler_color(color)
        self.ruler_window.update()
        self.tray_icon.update_ruler_color(color)
    
    def on_overlay_color_changed(self, color):
        """Handle overlay color change."""
        self.settings.set_overlay_color(color)
        self.overlay_window.update()
        self.tray_icon.update_overlay_color(color)
    
    def exit_app(self):
        """Exit the application."""
        self.hotkey_manager.stop()
        self.app.quit()
    
    def run(self):
        """Run the application."""
        return self.app.exec_()


def main():
    """Application entry point."""
    app = TextRulerApp()
    sys.exit(app.run())


if __name__ == '__main__':
    main()
