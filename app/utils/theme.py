#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para gestionar el tema y apariencia de la aplicación.
"""

class Theme:
    """Clase para gestionar el tema de la aplicación."""
    
    # Colores principales
    DARK_BG = "#1E1E2E"
    LIGHT_BG = "#F0F0F5"
    
    DARK_SECONDARY = "#2D2D3F"
    LIGHT_SECONDARY = "#E0E0E8"
    
    DARK_TEXT = "#FFFFFF"
    LIGHT_TEXT = "#333333"
    
    ACCENT_BLUE = "#7B68EE"
    ACCENT_GREEN = "#50C878"
    ACCENT_RED = "#FF5252"
    ACCENT_YELLOW = "#FFD700"
    
    # Estado actual
    _dark_mode = True
    
    @classmethod
    def toggle_theme(cls):
        """Alterna entre tema claro y oscuro."""
        cls._dark_mode = not cls._dark_mode
        return cls._dark_mode
    
    @classmethod
    def is_dark_mode(cls):
        """Retorna si el tema actual es oscuro."""
        return cls._dark_mode
        
    @classmethod
    def is_light_mode(cls):
        """Retorna si el tema actual es claro."""
        return not cls._dark_mode
    
    @classmethod
    def get_bg_color(cls):
        """Obtiene el color de fondo según el tema actual."""
        return cls.DARK_BG if cls._dark_mode else cls.LIGHT_BG
    
    @classmethod
    def get_secondary_color(cls):
        """Obtiene el color secundario según el tema actual."""
        return cls.DARK_SECONDARY if cls._dark_mode else cls.LIGHT_SECONDARY
    
    @classmethod
    def get_text_color(cls):
        """Obtiene el color de texto según el tema actual."""
        return cls.DARK_TEXT if cls._dark_mode else cls.LIGHT_TEXT
    
    @classmethod
    def get_chart_colors(cls):
        """Obtiene los colores para gráficos."""
        return {
            "cpu": cls.ACCENT_BLUE,
            "ram": cls.ACCENT_GREEN,
            "disk": cls.ACCENT_YELLOW,
            "net_recv": "#9370DB",  # Púrpura medio
            "net_sent": "#20B2AA",  # Verde azulado claro
            "fps": "#FF8C00",       # Naranja oscuro
            "alert": cls.ACCENT_RED
        }
    
    @classmethod
    def get_chart_bg_color(cls):
        """Obtiene el color de fondo para gráficos."""
        return "#2A2A3A" if cls._dark_mode else "#F8F8FA"
    
    @classmethod
    def get_grid_color(cls):
        """Obtiene el color de la cuadrícula para gráficos."""
        return "#3F3F5F" if cls._dark_mode else "#DDDDDD"
        
    @classmethod
    def get_color(cls, name):
        """Obtiene un color específico según el nombre y el tema actual."""
        colors = {
            "bg": cls.get_bg_color(),
            "secondary": cls.get_secondary_color(),
            "text": cls.get_text_color(),
            "chart_bg": cls.get_chart_bg_color(),
            "grid": cls.get_grid_color(),
            "cpu": cls.ACCENT_BLUE,
            "ram": cls.ACCENT_GREEN,
            "disk": cls.ACCENT_YELLOW,
            "net": "#9370DB",
            "alert": cls.ACCENT_RED,
            "success": cls.ACCENT_GREEN,
            "warning": cls.ACCENT_YELLOW,
            "error": cls.ACCENT_RED
        }
        return colors.get(name, "#FFFFFF")