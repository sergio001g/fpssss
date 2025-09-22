#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo principal de la interfaz gráfica.
"""

import customtkinter as ctk
from .ui.dashboard import Dashboard
from .utils.theme import Theme

class App(ctk.CTk):
    """Clase principal de la aplicación."""
    
    def __init__(self):
        """Inicializa la aplicación."""
        super().__init__()
        
        # Configuración de la ventana
        self.title("Monitor de Sistema Avanzado")
        self.geometry("1200x700")
        self.minsize(900, 600)
        
        # Configuración de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear gestor de tema
        self.theme_manager = Theme()
        
        # Crear dashboard
        self.dashboard = Dashboard(self, self.theme_manager)
        self.dashboard.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar cierre de la aplicación
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        """Maneja el cierre de la aplicación."""
        # Detener el monitoreo antes de cerrar
        if hasattr(self.dashboard, 'system_monitor'):
            self.dashboard.system_monitor.stop()
        
        # Cerrar la aplicación
        self.destroy()