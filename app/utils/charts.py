#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilidades para crear y actualizar gráficos.
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from .theme import Theme

class ChartManager:
    """Clase para gestionar gráficos de matplotlib."""
    
    def __init__(self, parent, figsize=(5, 3), dpi=100):
        """
        Inicializa un gestor de gráficos.
        
        Args:
            parent: Widget padre donde se mostrará el gráfico
            figsize: Tamaño de la figura
            dpi: Resolución de la figura
        """
        self.fig = Figure(figsize=figsize, dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        
        # Configuración inicial
        self.update_theme()
    
    def update_theme(self):
        """Actualiza el tema del gráfico según el tema actual."""
        bg_color = Theme.get_chart_bg_color()
        text_color = Theme.get_text_color()
        grid_color = Theme.get_grid_color()
        
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)
        
        # Actualizar colores de texto
        self.ax.tick_params(colors=text_color, which='both')
        self.ax.xaxis.label.set_color(text_color)
        self.ax.yaxis.label.set_color(text_color)
        self.ax.title.set_color(text_color)
        
        # Actualizar colores de ejes y cuadrícula
        for spine in self.ax.spines.values():
            spine.set_color(grid_color)
        
        self.ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)
        
        # Redibujar
        self.canvas.draw()
    
    def plot_line(self, data, label=None, color=None, clear=True):
        """
        Dibuja una línea en el gráfico.
        
        Args:
            data: Lista o array con los datos a graficar
            label: Etiqueta para la leyenda
            color: Color de la línea
            clear: Si se debe limpiar el gráfico antes de dibujar
        """
        if clear:
            self.ax.clear()
            self.update_theme()
        
        if not data:
            return
        
        x = list(range(len(data)))
        self.ax.plot(x, data, label=label, color=color)
        
        if label:
            self.ax.legend(loc='upper right')
        
        self.canvas.draw()
    
    def plot_multi_line(self, data_dict, clear=True):
        """
        Dibuja múltiples líneas en el gráfico.
        
        Args:
            data_dict: Diccionario con {nombre: [datos], ...}
            clear: Si se debe limpiar el gráfico antes de dibujar
        """
        if clear:
            self.ax.clear()
            self.update_theme()
        
        chart_colors = Theme.get_chart_colors()
        
        for name, data in data_dict.items():
            if not data:
                continue
                
            x = list(range(len(data)))
            color = chart_colors.get(name, None)
            self.ax.plot(x, data, label=name, color=color)
        
        self.ax.legend(loc='upper right')
        self.canvas.draw()
    
    def set_title(self, title):
        """Establece el título del gráfico."""
        self.ax.set_title(title)
        self.canvas.draw()
    
    def set_labels(self, xlabel=None, ylabel=None):
        """Establece las etiquetas de los ejes."""
        if xlabel:
            self.ax.set_xlabel(xlabel)
        if ylabel:
            self.ax.set_ylabel(ylabel)
        self.canvas.draw()
    
    def get_widget(self):
        """Retorna el widget del canvas para colocarlo en la interfaz."""
        return self.canvas_widget
        
    def configure_chart(self, ax, xlabel, ylabel, title):
        """Configura un gráfico con etiquetas y título."""
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Aplicar tema
        bg_color = Theme.get_chart_bg_color()
        text_color = Theme.get_text_color()
        grid_color = Theme.get_grid_color()
        
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=text_color, which='both')
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)
        
        for spine in ax.spines.values():
            spine.set_color(grid_color)