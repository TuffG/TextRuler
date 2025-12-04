"""Global hotkey manager using pynput."""
from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal


class HotkeyManager(QObject):
    """Manages global hotkeys."""
    
    # Signals
    toggle_ruler = pyqtSignal()
    toggle_overlay = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.listener = None
        
        # Define hotkey combinations
        self.hotkeys = {
            'toggle_ruler': {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.Key.f12},
            'toggle_overlay': {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.Key.f11}
        }
        
        # Track currently pressed keys
        self.current_keys = set()
    
    def start(self):
        """Start listening for hotkeys."""
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
    
    def stop(self):
        """Stop listening for hotkeys."""
        if self.listener:
            self.listener.stop()
    
    def on_press(self, key):
        """Handle key press."""
        # Normalize the key
        try:
            # For special keys like Ctrl, Alt, etc.
            normalized_key = key
        except AttributeError:
            # For regular character keys
            normalized_key = key
        
        # Add to current keys
        self.current_keys.add(normalized_key)
        
        # Check if any hotkey combination is pressed
        self.check_hotkeys()
    
    def on_release(self, key):
        """Handle key release."""
        # Remove from current keys
        if key in self.current_keys:
            self.current_keys.remove(key)
    
    def check_hotkeys(self):
        """Check if current key combination matches any hotkey."""
        # Check for toggle ruler (Ctrl+Alt+F12)
        if self.is_hotkey_pressed('toggle_ruler'):
            self.toggle_ruler.emit()
            self.current_keys.clear()  # Clear to avoid repeated triggers
        
        # Check for toggle overlay (Ctrl+Alt+F11)
        elif self.is_hotkey_pressed('toggle_overlay'):
            self.toggle_overlay.emit()
            self.current_keys.clear()
    
    def is_hotkey_pressed(self, hotkey_name):
        """Check if a specific hotkey is currently pressed."""
        target_keys = self.hotkeys.get(hotkey_name, set())
        if not target_keys:
            return False
        
        # Check if all target keys are in current keys
        # We need more flexible matching for modifier keys
        has_ctrl = any(k in self.current_keys for k in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl])
        has_alt = any(k in self.current_keys for k in [keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt])
        has_f12 = keyboard.Key.f12 in self.current_keys
        has_f11 = keyboard.Key.f11 in self.current_keys
        
        if hotkey_name == 'toggle_ruler':
            return has_ctrl and has_alt and has_f12
        elif hotkey_name == 'toggle_overlay':
            return has_ctrl and has_alt and has_f11
        
        return False
