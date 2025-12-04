"""Settings management for TextRuler application."""
import json
import os
from typing import Dict, Any
from PyQt5.QtCore import QSettings


class AppSettings:
    """Manages application settings with persistence."""
    
    # Default color palette
    COLORS = {
        'Red': '#FF6B6B',
        'Blue': '#4ECDC4',
        'Green': '#95E1D3',
        'Yellow': '#FFE66D',
        'Purple': '#A78BFA',
        'Orange': '#FFA500',
        'Black': '#2D3436',
        'White': '#F5F5F5'
    }
    
    def __init__(self):
        """Initialize settings manager."""
        self.settings_file = os.path.join(
            os.path.expanduser('~'),
            '.text_ruler_settings.json'
        )
        self.settings = self._load_settings()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            'ruler': {
                'height': 50,
                'x_position': 0,
                'y_position': 300,
                'color': 'Blue',
                'visible': False,
                'opacity_by_color': {color: 0.7 for color in self.COLORS.keys()}
            },
            'overlay': {
                'color': 'Black',
                'visible': False,
                'opacity_by_color': {color: 0.5 for color in self.COLORS.keys()}
            },
            'hotkeys': {
                'toggle_ruler': 'ctrl+alt+f12',
                'toggle_overlay': 'ctrl+alt+f11'
            }
        }
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle new settings
                    defaults = self._get_defaults()
                    self._merge_dicts(defaults, loaded)
                    return defaults
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self._get_defaults()
        return self._get_defaults()
    
    def _merge_dicts(self, base: Dict, updates: Dict) -> None:
        """Recursively merge updates into base dictionary."""
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dicts(base[key], value)
            else:
                base[key] = value
    
    def save(self) -> None:
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    # Ruler settings
    def get_ruler_height(self) -> int:
        return self.settings['ruler']['height']
    
    def set_ruler_height(self, height: int) -> None:
        self.settings['ruler']['height'] = height
        self.save()
    
    def get_ruler_x(self) -> int:
        return self.settings['ruler'].get('x_position', 0)
    
    def set_ruler_x(self, x: int) -> None:
        self.settings['ruler']['x_position'] = x
        self.save()
    
    def get_ruler_y(self) -> int:
        return self.settings['ruler']['y_position']
    
    def set_ruler_y(self, y: int) -> None:
        self.settings['ruler']['y_position'] = y
        self.save()
    
    def get_ruler_color(self) -> str:
        return self.settings['ruler']['color']
    
    def set_ruler_color(self, color: str) -> None:
        self.settings['ruler']['color'] = color
        self.save()
    
    def get_ruler_visible(self) -> bool:
        return self.settings['ruler']['visible']
    
    def set_ruler_visible(self, visible: bool) -> None:
        self.settings['ruler']['visible'] = visible
        self.save()
    
    def get_ruler_opacity(self, color: str = None) -> float:
        if color is None:
            color = self.get_ruler_color()
        return self.settings['ruler']['opacity_by_color'].get(color, 0.7)
    
    def set_ruler_opacity(self, opacity: float, color: str = None) -> None:
        if color is None:
            color = self.get_ruler_color()
        self.settings['ruler']['opacity_by_color'][color] = opacity
        self.save()
    
    # Overlay settings
    def get_overlay_color(self) -> str:
        return self.settings['overlay']['color']
    
    def set_overlay_color(self, color: str) -> None:
        self.settings['overlay']['color'] = color
        self.save()
    
    def get_overlay_visible(self) -> bool:
        return self.settings['overlay']['visible']
    
    def set_overlay_visible(self, visible: bool) -> None:
        self.settings['overlay']['visible'] = visible
        self.save()
    
    def get_overlay_opacity(self, color: str = None) -> float:
        if color is None:
            color = self.get_overlay_color()
        return self.settings['overlay']['opacity_by_color'].get(color, 0.5)
    
    def set_overlay_opacity(self, opacity: float, color: str = None) -> None:
        if color is None:
            color = self.get_overlay_color()
        self.settings['overlay']['opacity_by_color'][color] = opacity
        self.save()
    
    def get_color_list(self):
        """Return list of available color names."""
        return list(self.COLORS.keys())
    
    def get_color_hex(self, color_name: str) -> str:
        """Get hex color code for a color name."""
        return self.COLORS.get(color_name, '#4ECDC4')
