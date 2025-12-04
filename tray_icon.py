"""System tray icon and menu."""
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal
import os


class TrayIcon(QObject):
    """System tray icon with context menu."""
    
    # Signals
    toggle_ruler_requested = pyqtSignal()
    toggle_overlay_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    ruler_color_changed = pyqtSignal(str)
    overlay_color_changed = pyqtSignal(str)
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.tray_icon = None
        self.menu = None
        
        self.ruler_color_actions = {}
        self.overlay_color_actions = {}
    
    def create_tray_icon(self):
        """Create and show the system tray icon."""
        # Create tray icon
        self.tray_icon = QSystemTrayIcon()
        
        # Try to load icon, use default if not found
        icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'icon.png')
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Use a default icon from Qt
            from PyQt5.QtWidgets import QStyle, QApplication
            style = QApplication.style()
            icon = style.standardIcon(QStyle.SP_ComputerIcon)
            self.tray_icon.setIcon(icon)
        
        # Create context menu
        self.create_menu()
        
        # Set tooltip
        self.tray_icon.setToolTip("TextRuler")
        
        # Show the tray icon
        self.tray_icon.show()
    
    def create_menu(self):
        """Create the context menu."""
        self.menu = QMenu()
        
        # Toggle Ruler
        self.toggle_ruler_action = QAction("Toggle Ruler (Ctrl+Alt+F12)", self.menu)
        self.toggle_ruler_action.setCheckable(True)
        self.toggle_ruler_action.setChecked(self.settings.get_ruler_visible())
        self.toggle_ruler_action.triggered.connect(self.toggle_ruler_requested.emit)
        self.menu.addAction(self.toggle_ruler_action)
        
        # Toggle Overlay
        self.toggle_overlay_action = QAction("Toggle Overlay (Ctrl+Alt+F11)", self.menu)
        self.toggle_overlay_action.setCheckable(True)
        self.toggle_overlay_action.setChecked(self.settings.get_overlay_visible())
        self.toggle_overlay_action.triggered.connect(self.toggle_overlay_requested.emit)
        self.menu.addAction(self.toggle_overlay_action)
        
        self.menu.addSeparator()
        
        # Ruler Color submenu
        ruler_color_menu = QMenu("Ruler Color", self.menu)
        colors = self.settings.get_color_list()
        current_ruler_color = self.settings.get_ruler_color()
        
        for color in colors:
            action = QAction(color, ruler_color_menu)
            action.setCheckable(True)
            action.setChecked(color == current_ruler_color)
            action.triggered.connect(lambda checked, c=color: self.on_ruler_color_changed(c))
            ruler_color_menu.addAction(action)
            self.ruler_color_actions[color] = action
        
        self.menu.addMenu(ruler_color_menu)
        
        # Overlay Color submenu
        overlay_color_menu = QMenu("Overlay Color", self.menu)
        current_overlay_color = self.settings.get_overlay_color()
        
        for color in colors:
            action = QAction(color, overlay_color_menu)
            action.setCheckable(True)
            action.setChecked(color == current_overlay_color)
            action.triggered.connect(lambda checked, c=color: self.on_overlay_color_changed(c))
            overlay_color_menu.addAction(action)
            self.overlay_color_actions[color] = action
        
        self.menu.addMenu(overlay_color_menu)
        
        self.menu.addSeparator()
        
        # Exit
        exit_action = QAction("Exit", self.menu)
        exit_action.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(exit_action)
        
        # Set the menu
        self.tray_icon.setContextMenu(self.menu)
    
    def on_ruler_color_changed(self, color):
        """Handle ruler color change from menu."""
        # Update checkmarks
        for c, action in self.ruler_color_actions.items():
            action.setChecked(c == color)
        
        self.ruler_color_changed.emit(color)
    
    def on_overlay_color_changed(self, color):
        """Handle overlay color change from menu."""
        # Update checkmarks
        for c, action in self.overlay_color_actions.items():
            action.setChecked(c == color)
        
        self.overlay_color_changed.emit(color)
    
    def update_ruler_state(self, visible):
        """Update ruler toggle state in menu."""
        if self.toggle_ruler_action:
            self.toggle_ruler_action.setChecked(visible)
    
    def update_overlay_state(self, visible):
        """Update overlay toggle state in menu."""
        if self.toggle_overlay_action:
            self.toggle_overlay_action.setChecked(visible)
    
    def update_ruler_color(self, color):
        """Update ruler color checkmarks."""
        for c, action in self.ruler_color_actions.items():
            action.setChecked(c == color)
    
    def update_overlay_color(self, color):
        """Update overlay color checkmarks."""
        for c, action in self.overlay_color_actions.items():
            action.setChecked(c == color)
