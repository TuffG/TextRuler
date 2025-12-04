"""Screen overlay window with ruler cutout."""
import ctypes
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QPainter, QColor, QRegion, QPainterPath

# Windows constants for click-through
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED = 0x00080000
GWL_EXSTYLE = -20


class OverlayWindow(QWidget):
    """Full-screen overlay with cutout for ruler."""
    
    def __init__(self, settings, ruler_window):
        super().__init__()
        self.settings = settings
        self.ruler_window = ruler_window
        
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize the overlay window."""
        # Make window frameless and always on top (but below ruler)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowTransparentForInput  # Qt's way of saying click-through
        )
        
        # Enable transparency
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        # Make window cover all screens
        desktop = QApplication.desktop()
        if desktop:
            # Get geometry spanning all screens
            screen_geometry = QRect()
            for i in range(desktop.screenCount()):
                screen_geometry = screen_geometry.united(desktop.screenGeometry(i))
            self.setGeometry(screen_geometry)
        else:
            self.setGeometry(0, 0, 3840, 2160)  # Fallback
            
        # Ensure click-through on Windows
        self.set_click_through()
    
    def set_click_through(self):
        """Set Windows specific flags for click-through."""
        try:
            hwnd = self.winId()
            style = ctypes.windll.user32.GetWindowLongW(int(hwnd), GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(int(hwnd), GWL_EXSTYLE, style | WS_EX_TRANSPARENT | WS_EX_LAYERED)
        except Exception as e:
            print(f"Error setting click-through: {e}")

    def load_settings(self):
        """Load and apply settings."""
        if self.settings.get_overlay_visible():
            self.show()
            self.set_click_through()  # Re-apply when showing
        else:
            self.hide()
    
    def paintEvent(self, event):
        """Paint the overlay with cutout."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get color and opacity
        color_name = self.settings.get_overlay_color()
        color_hex = self.settings.get_color_hex(color_name)
        opacity = self.settings.get_overlay_opacity(color_name)
        
        color = QColor(color_hex)
        color.setAlphaF(opacity)
        
        # Create a path for the entire window
        full_path = QPainterPath()
        full_path.addRect(QRectF(self.rect()))
        
        # Create cutout path for ruler area
        if self.ruler_window and self.ruler_window.isVisible():
            ruler_rect = self.ruler_window.geometry()
            cutout_path = QPainterPath()
            cutout_path.addRect(
                ruler_rect.x(),
                ruler_rect.y(),
                ruler_rect.width(),
                ruler_rect.height()
            )
            
            # Subtract cutout from full path
            final_path = full_path.subtracted(cutout_path)
            painter.fillPath(final_path, color)
        else:
            # No cutout needed if ruler is hidden
            painter.fillPath(full_path, color)
    
    def update_ruler_position(self):
        """Called when ruler moves or resizes."""
        self.update()
    
    def toggle_visibility(self):
        """Toggle overlay visibility."""
        if self.isVisible():
            self.hide()
            self.settings.set_overlay_visible(False)
        else:
            self.show()
            self.settings.set_overlay_visible(True)
            self.set_click_through()
            self.update()
    
    # Note: wheelEvent removed as it won't work with click-through enabled
