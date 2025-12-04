"""Ruler overlay window."""
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QTimer, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QCursor
import sys


class RulerWindow(QWidget):
    """Transparent ruler overlay window."""
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.dragging = False
        self.drag_start_pos = QPoint(0, 0)
        self.overlay_window = None  # Will be set by main app
        
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize the window."""
        # Make window frameless and always on top
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # Enable transparency
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        
        # Set cursor
        self.setCursor(Qt.SizeAllCursor)  # Changed to allow both horizontal and vertical dragging
        
        # Initial geometry will be set in load_settings()
    
    def load_settings(self):
        """Load settings and apply them."""
        height = self.settings.get_ruler_height()
        x_pos = self.settings.get_ruler_x()
        y_pos = self.settings.get_ruler_y()
        
        # Find screen for the saved position and adjust width
        screen_geometry = self.get_screen_geometry_at(x_pos, y_pos)
        if screen_geometry:
            self.setGeometry(screen_geometry.x(), y_pos, screen_geometry.width(), height)
            # Ensure X position is within screen bounds
            if x_pos < screen_geometry.x():
                x_pos = screen_geometry.x()
            elif x_pos > screen_geometry.x() + screen_geometry.width():
                x_pos = screen_geometry.x()
            self.move(x_pos, y_pos)
        else:
            # Fallback to primary screen
            screen = QApplication.primaryScreen().geometry()
            self.setGeometry(screen.x(), y_pos, screen.width(), height)
            self.move(x_pos if x_pos >= screen.x() else screen.x(), y_pos)
        
        if self.settings.get_ruler_visible():
            self.show()
        else:
            self.hide()
    
    def paintEvent(self, event):
        """Paint the ruler."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get color and opacity
        color_name = self.settings.get_ruler_color()
        color_hex = self.settings.get_color_hex(color_name)
        opacity = self.settings.get_ruler_opacity(color_name)
        
        # Parse hex color
        color = QColor(color_hex)
        color.setAlphaF(opacity)
        
        # Draw filled rectangle
        painter.fillRect(self.rect(), color)
    
    def get_screen_geometry_at(self, x, y):
        """Get the geometry of the screen containing the given point."""
        desktop = QApplication.desktop()
        if desktop:
            for i in range(desktop.screenCount()):
                screen_geometry = desktop.screenGeometry(i)
                if screen_geometry.contains(x, y):
                    return screen_geometry
        # Fallback to primary screen
        return QApplication.primaryScreen().geometry()
    
    def adjust_to_current_screen(self):
        """Adjust ruler width to match the current screen."""
        current_x = self.x()
        current_y = self.y()
        screen_geometry = self.get_screen_geometry_at(current_x, current_y)
        
        if screen_geometry:
            # Adjust width to match screen
            new_x = max(screen_geometry.x(), min(current_x, screen_geometry.x() + screen_geometry.width() - 100))
            self.setGeometry(new_x, current_y, screen_geometry.width(), self.height())
            self.move(new_x, current_y)
    
    def mousePressEvent(self, event):
        """Handle mouse press - start dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_pos = QPoint(
                event.globalX() - self.x(),
                event.globalY() - self.y()
            )
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - stop dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            # Adjust to current screen and save position
            self.adjust_to_current_screen()
            self.settings.set_ruler_x(self.x())
            self.settings.set_ruler_y(self.y())
    
    def mouseMoveEvent(self, event):
        """Handle mouse move - update ruler position."""
        if self.dragging:
            new_x = event.globalX() - self.drag_start_pos.x()
            new_y = event.globalY() - self.drag_start_pos.y()
            
            # Move ruler
            self.move(new_x, new_y)
            
            # Check if we moved to a different screen and adjust width
            screen_geometry = self.get_screen_geometry_at(new_x, new_y)
            if screen_geometry and self.width() != screen_geometry.width():
                # Adjust width to match new screen
                adjusted_x = max(screen_geometry.x(), min(new_x, screen_geometry.x() + screen_geometry.width() - 100))
                self.setGeometry(adjusted_x, new_y, screen_geometry.width(), self.height())
                self.move(adjusted_x, new_y)
            
            # Update overlay if it exists
            if self.overlay_window:
                self.overlay_window.update_ruler_position()
    
    def wheelEvent(self, event):
        """Handle mouse wheel - adjust height or change color."""
        from PyQt5.QtCore import Qt as QtCore_Qt
        
        modifiers = event.modifiers()
        
        if modifiers & Qt.ShiftModifier:
            # Shift + Wheel: Change color
            self.cycle_color(event.angleDelta().y() > 0)
        else:
            # Normal wheel: Adjust height
            delta = event.angleDelta().y()
            if delta > 0:
                new_height = min(self.height() + 5, 500)
            else:
                new_height = max(self.height() - 5, 20)
            
            self.resize(self.width(), new_height)
            self.settings.set_ruler_height(new_height)
            
            # Update overlay
            if self.overlay_window:
                self.overlay_window.update_ruler_position()
            
            self.update()
    
    def cycle_color(self, forward=True):
        """Cycle through available colors."""
        colors = self.settings.get_color_list()
        current = self.settings.get_ruler_color()
        
        try:
            current_index = colors.index(current)
        except ValueError:
            current_index = 0
        
        if forward:
            new_index = (current_index + 1) % len(colors)
        else:
            new_index = (current_index - 1) % len(colors)
        
        new_color = colors[new_index]
        self.settings.set_ruler_color(new_color)
        self.update()
    
    def toggle_visibility(self):
        """Toggle ruler visibility."""
        if self.isVisible():
            self.hide()
            self.settings.set_ruler_visible(False)
        else:
            self.show()
            self.settings.set_ruler_visible(True)
    
    def set_overlay_window(self, overlay_window):
        """Set reference to overlay window."""
        self.overlay_window = overlay_window
