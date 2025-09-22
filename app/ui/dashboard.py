#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dashboard para el Monitor de Sistema Avanzado
--------------------------------------------
Interfaz gráfica que muestra información del sistema en tiempo real.
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time
import threading

from ..core.system_monitor import SystemMonitor
from ..utils.theme import Theme
from ..utils.charts import ChartManager

class Dashboard(ctk.CTkFrame):
    """Clase que maneja la interfaz gráfica del dashboard."""
    
    def __init__(self, parent, theme_manager):
        """
        Inicializa el dashboard.
        
        Args:
            parent: Widget padre (ventana principal)
            theme_manager: Instancia de Theme para manejar colores
        """
        super().__init__(parent)
        self.parent = parent
        self.theme = theme_manager
        self.system_monitor = SystemMonitor()
        
        # Crear frame para gráficos
        self.charts_frame = ctk.CTkFrame(self)
        self.charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.chart_manager = ChartManager(self.charts_frame, figsize=(5, 3), dpi=100)
        
        # Configurar actualización periódica
        self.update_interval = 1000  # ms
        self.history_length = 60  # puntos de datos para gráficos
        
        # Datos históricos
        self.cpu_history = [0] * self.history_length
        self.ram_history = [0] * self.history_length
        self.disk_history = [0] * self.history_length
        self.net_history = [0] * self.history_length
        self.fps_history = [0] * self.history_length
        
        # Configurar alertas
        self.alert_thresholds = {
            'cpu': 80,  # %
            'ram': 80,  # %
            'disk': 90,  # %
            'temp': 80  # °C
        }
        
        self.active_alerts = []
        
        # Crear widgets
        self.create_widgets()
        
        # Iniciar monitoreo
        self.start_monitoring()
    
    def create_widgets(self):
        """Crea todos los widgets del dashboard."""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Monitor de Sistema Avanzado",
            font=("Segoe UI", 24, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Frame superior para métricas principales
        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Métricas en tiempo real
        self.create_metrics_widgets()
        
        # Frame central para gráficos
        self.charts_frame = ctk.CTkFrame(self.main_frame)
        self.charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Crear gráficos
        self.create_charts()
        
        # Frame inferior para procesos y alertas
        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Tabla de procesos
        self.create_process_table()
        
        # Panel de alertas
        self.create_alerts_panel()
        
        # Barra de estado
        self.create_status_bar()
    
    def create_metrics_widgets(self):
        """Crea los widgets para mostrar métricas en tiempo real."""
        # Frame para métricas
        metrics_frame = ctk.CTkFrame(self.top_frame)
        metrics_frame.pack(fill=tk.X, pady=5)
        
        # Configurar grid
        for i in range(5):
            metrics_frame.columnconfigure(i, weight=1)
        
        # CPU
        cpu_frame = ctk.CTkFrame(metrics_frame)
        cpu_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(cpu_frame, text="CPU", font=("Segoe UI", 14, "bold")).pack(pady=2)
        self.cpu_label = ctk.CTkLabel(cpu_frame, text="0%", font=("Segoe UI", 20))
        self.cpu_label.pack(pady=2)
        self.cpu_temp_label = ctk.CTkLabel(cpu_frame, text="0°C", font=("Segoe UI", 12))
        self.cpu_temp_label.pack(pady=2)
        
        # RAM
        ram_frame = ctk.CTkFrame(metrics_frame)
        ram_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(ram_frame, text="RAM", font=("Segoe UI", 14, "bold")).pack(pady=2)
        self.ram_label = ctk.CTkLabel(ram_frame, text="0%", font=("Segoe UI", 20))
        self.ram_label.pack(pady=2)
        self.ram_used_label = ctk.CTkLabel(ram_frame, text="0 GB / 0 GB", font=("Segoe UI", 12))
        self.ram_used_label.pack(pady=2)
        
        # Disco
        disk_frame = ctk.CTkFrame(metrics_frame)
        disk_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(disk_frame, text="Disco", font=("Segoe UI", 14, "bold")).pack(pady=2)
        self.disk_label = ctk.CTkLabel(disk_frame, text="0%", font=("Segoe UI", 20))
        self.disk_label.pack(pady=2)
        self.disk_io_label = ctk.CTkLabel(disk_frame, text="0 MB/s", font=("Segoe UI", 12))
        self.disk_io_label.pack(pady=2)
        
        # Red
        net_frame = ctk.CTkFrame(metrics_frame)
        net_frame.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(net_frame, text="Red", font=("Segoe UI", 14, "bold")).pack(pady=2)
        self.net_label = ctk.CTkLabel(net_frame, text="↓ 0 KB/s", font=("Segoe UI", 20))
        self.net_label.pack(pady=2)
        self.net_up_label = ctk.CTkLabel(net_frame, text="↑ 0 KB/s", font=("Segoe UI", 12))
        self.net_up_label.pack(pady=2)
        
        # FPS
        fps_frame = ctk.CTkFrame(metrics_frame)
        fps_frame.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(fps_frame, text="FPS", font=("Segoe UI", 14, "bold")).pack(pady=2)
        self.fps_label = ctk.CTkLabel(fps_frame, text="0", font=("Segoe UI", 20))
        self.fps_label.pack(pady=2)
        self.fps_avg_label = ctk.CTkLabel(fps_frame, text="Prom: 0", font=("Segoe UI", 12))
        self.fps_avg_label.pack(pady=2)
    
    def create_charts(self):
        """Crea los gráficos para visualizar datos históricos."""
        # Configurar grid para gráficos
        self.charts_frame.columnconfigure(0, weight=1)
        self.charts_frame.columnconfigure(1, weight=1)
        self.charts_frame.rowconfigure(0, weight=1)
        self.charts_frame.rowconfigure(1, weight=1)
        
        # Gráfico de CPU
        self.cpu_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.cpu_chart_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.cpu_fig = Figure(figsize=(4, 3), dpi=100)
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        self.chart_manager.configure_chart(self.cpu_ax, "CPU (%)", "Tiempo (s)", "Uso de CPU")
        
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.cpu_chart_frame)
        self.cpu_canvas.draw()
        self.cpu_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de RAM
        self.ram_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.ram_chart_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.ram_fig = Figure(figsize=(4, 3), dpi=100)
        self.ram_ax = self.ram_fig.add_subplot(111)
        self.chart_manager.configure_chart(self.ram_ax, "RAM (%)", "Tiempo (s)", "Uso de RAM")
        
        self.ram_canvas = FigureCanvasTkAgg(self.ram_fig, master=self.ram_chart_frame)
        self.ram_canvas.draw()
        self.ram_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de Disco
        self.disk_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.disk_chart_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.disk_fig = Figure(figsize=(4, 3), dpi=100)
        self.disk_ax = self.disk_fig.add_subplot(111)
        self.chart_manager.configure_chart(self.disk_ax, "Disco (MB/s)", "Tiempo (s)", "Actividad de Disco")
        
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, master=self.disk_chart_frame)
        self.disk_canvas.draw()
        self.disk_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de FPS
        self.fps_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.fps_chart_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        self.fps_fig = Figure(figsize=(4, 3), dpi=100)
        self.fps_ax = self.fps_fig.add_subplot(111)
        self.chart_manager.configure_chart(self.fps_ax, "FPS", "Tiempo (s)", "Frames Por Segundo")
        
        self.fps_canvas = FigureCanvasTkAgg(self.fps_fig, master=self.fps_chart_frame)
        self.fps_canvas.draw()
        self.fps_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_process_table(self):
        """Crea la tabla de procesos."""
        # Frame para tabla de procesos
        process_frame = ctk.CTkFrame(self.bottom_frame)
        process_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Título
        ctk.CTkLabel(process_frame, text="Procesos", font=("Segoe UI", 14, "bold")).pack(pady=5)
        
        # Tabla
        columns = ("Nombre", "PID", "CPU %", "RAM %")
        self.process_tree = ttk.Treeview(process_frame, columns=columns, show="headings", height=5)
        
        # Configurar columnas
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)
        
        self.process_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(process_frame, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_alerts_panel(self):
        """Crea el panel de alertas."""
        # Frame para alertas
        alerts_frame = ctk.CTkFrame(self.bottom_frame)
        alerts_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Título
        ctk.CTkLabel(alerts_frame, text="Alertas", font=("Segoe UI", 14, "bold")).pack(pady=5)
        
        # Lista de alertas
        self.alerts_listbox = tk.Listbox(alerts_frame, bg=self.theme.get_color("bg"), 
                                        fg=self.theme.get_color("danger"),
                                        font=("Segoe UI", 10),
                                        height=5)
        self.alerts_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(alerts_frame, orient="vertical", command=self.alerts_listbox.yview)
        self.alerts_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón para limpiar alertas
        self.clear_alerts_btn = ctk.CTkButton(
            alerts_frame, 
            text="Limpiar Alertas",
            command=self.clear_alerts
        )
        self.clear_alerts_btn.pack(pady=5)
    
    def create_status_bar(self):
        """Crea la barra de estado."""
        self.status_bar = ctk.CTkFrame(self.main_frame, height=25)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(
            self.status_bar, 
            text="Monitor activo | Última actualización: Nunca",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Botón de configuración
        self.settings_btn = ctk.CTkButton(
            self.status_bar,
            text="⚙️ Configuración",
            width=120,
            command=self.show_settings
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=10)
        
        # Botón para alternar tema
        self.theme_btn = ctk.CTkButton(
            self.status_bar,
            text="🌙 Tema Oscuro" if self.theme.is_light_mode() else "☀️ Tema Claro",
            width=120,
            command=self.toggle_theme
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
    
    def start_monitoring(self):
        """Inicia el monitoreo del sistema."""
        # Configurar callbacks
        self.system_monitor.set_update_callback(self.update_dashboard)
        
        # Iniciar monitoreo en un hilo separado
        self.monitoring_thread = threading.Thread(target=self.system_monitor.start_monitoring, daemon=True)
        self.monitoring_thread.start()
        
        # Programar primera actualización
        self.parent.after(self.update_interval, self.update_dashboard)
    
    def update_dashboard(self):
        """Actualiza todos los elementos del dashboard."""
        try:
            # Obtener datos actuales
            cpu_percent = self.system_monitor.get_cpu_percent()
            cpu_temp = self.system_monitor.get_cpu_temp()
            ram_percent = self.system_monitor.get_ram_percent()
            ram_used, ram_total = self.system_monitor.get_ram_usage()
            disk_percent = self.system_monitor.get_disk_percent()
            disk_io = self.system_monitor.get_disk_io()
            net_down, net_up = self.system_monitor.get_network_speed()
            fps = self.system_monitor.get_fps()
            
            # Actualizar etiquetas
            self.cpu_label.configure(text=f"{cpu_percent:.1f}%")
            self.cpu_temp_label.configure(text=f"{cpu_temp:.1f}°C")
            
            self.ram_label.configure(text=f"{ram_percent:.1f}%")
            self.ram_used_label.configure(text=f"{ram_used:.1f} GB / {ram_total:.1f} GB")
            
            self.disk_label.configure(text=f"{disk_percent:.1f}%")
            read_io, write_io = disk_io
            self.disk_io_label.configure(text=f"R: {read_io:.1f} W: {write_io:.1f} MB/s")
            
            self.net_label.configure(text=f"↓ {self._format_network_speed(net_down)}")
            self.net_up_label.configure(text=f"↑ {self._format_network_speed(net_up)}")
            
            self.fps_label.configure(text=f"{fps} FPS")
            avg_fps = sum(self.fps_history) / len(self.fps_history) if any(self.fps_history) else 0
            self.fps_avg_label.configure(text=f"Prom: {avg_fps:.1f}")
            
            # Actualizar historiales
            self.cpu_history.append(cpu_percent)
            self.cpu_history.pop(0)
            
            self.ram_history.append(ram_percent)
            self.ram_history.pop(0)
            
            # Para disk_io, solo guardamos el primer valor (lectura)
            read_io, _ = disk_io
            self.disk_history.append(read_io)
            self.disk_history.pop(0)
            
            self.net_history.append(net_down)
            self.net_history.pop(0)
            
            self.fps_history.append(fps)
            self.fps_history.pop(0)
            
            # Actualizar gráficos
            self.update_charts()
            
            # Actualizar tabla de procesos
            self.update_process_table()
            
            # Verificar alertas
            self.check_alerts(cpu_percent, ram_percent, disk_percent, cpu_temp)
            
            # Actualizar barra de estado
            current_time = time.strftime("%H:%M:%S")
            self.status_label.configure(text=f"Monitor activo | Última actualización: {current_time}")
            
            # Programar siguiente actualización
            self.parent.after(self.update_interval, self.update_dashboard)
            
        except Exception as e:
            print(f"Error al actualizar dashboard: {e}")
            # Intentar recuperarse
            self.parent.after(self.update_interval * 2, self.update_dashboard)
    
    def update_charts(self):
        """Actualiza los gráficos con los datos más recientes."""
        # Eje X común (últimos N segundos)
        x_data = list(range(-len(self.cpu_history) + 1, 1))
        
        # Actualizar gráfico de CPU
        self.cpu_ax.clear()
        self.chart_manager.configure_chart(self.cpu_ax, "CPU (%)", "Tiempo (s)", "Uso de CPU")
        self.cpu_ax.plot(x_data, self.cpu_history, color=self.theme.get_color("primary"))
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_canvas.draw()
        
        # Actualizar gráfico de RAM
        self.ram_ax.clear()
        self.chart_manager.configure_chart(self.ram_ax, "RAM (%)", "Tiempo (s)", "Uso de RAM")
        self.ram_ax.plot(x_data, self.ram_history, color=self.theme.get_color("info"))
        self.ram_ax.set_ylim(0, 100)
        self.ram_canvas.draw()
        
        # Actualizar gráfico de Disco
        self.disk_ax.clear()
        self.chart_manager.configure_chart(self.disk_ax, "Disco (MB/s)", "Tiempo (s)", "Actividad de Disco")
        self.disk_ax.plot(x_data, self.disk_history, color=self.theme.get_color("success"))
        max_disk = max(self.disk_history) if max(self.disk_history) > 0 else 10
        self.disk_ax.set_ylim(0, max_disk * 1.2)
        self.disk_canvas.draw()
        
        # Actualizar gráfico de FPS
        self.fps_ax.clear()
        self.chart_manager.configure_chart(self.fps_ax, "FPS", "Tiempo (s)", "Frames Por Segundo")
        self.fps_ax.plot(x_data, self.fps_history, color=self.theme.get_color("warning"))
        max_fps = max(self.fps_history) if max(self.fps_history) > 0 else 60
        self.fps_ax.set_ylim(0, max_fps * 1.2)
        self.fps_canvas.draw()
    
    def update_process_table(self):
        """Actualiza la tabla de procesos."""
        # Limpiar tabla
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Obtener procesos
        processes = self.system_monitor.get_top_processes(10)
        
        # Agregar a la tabla
        for proc in processes:
            self.process_tree.insert("", tk.END, values=(
                proc['name'][:20],
                proc['pid'],
                f"{proc['cpu']:.1f}%",
                f"{proc['memory']:.1f}%"
            ))
    
    def check_alerts(self, cpu_percent, ram_percent, disk_percent, cpu_temp):
        """Verifica si hay alertas que mostrar."""
        current_time = time.strftime("%H:%M:%S")
        
        # Verificar CPU
        if cpu_percent > self.alert_thresholds['cpu']:
            alert_msg = f"{current_time} - ⚠️ Alerta: CPU al {cpu_percent:.1f}%"
            if alert_msg not in self.active_alerts:
                self.active_alerts.append(alert_msg)
                self.alerts_listbox.insert(tk.END, alert_msg)
                self.alerts_listbox.itemconfig(tk.END, {'bg': self.theme.get_color("danger_bg")})
        
        # Verificar RAM
        if ram_percent > self.alert_thresholds['ram']:
            alert_msg = f"{current_time} - ⚠️ Alerta: RAM al {ram_percent:.1f}%"
            if alert_msg not in self.active_alerts:
                self.active_alerts.append(alert_msg)
                self.alerts_listbox.insert(tk.END, alert_msg)
                self.alerts_listbox.itemconfig(tk.END, {'bg': self.theme.get_color("danger_bg")})
        
        # Verificar Disco
        if disk_percent > self.alert_thresholds['disk']:
            alert_msg = f"{current_time} - ⚠️ Alerta: Disco al {disk_percent:.1f}%"
            if alert_msg not in self.active_alerts:
                self.active_alerts.append(alert_msg)
                self.alerts_listbox.insert(tk.END, alert_msg)
                self.alerts_listbox.itemconfig(tk.END, {'bg': self.theme.get_color("danger_bg")})
        
        # Verificar Temperatura
        if cpu_temp > self.alert_thresholds['temp']:
            alert_msg = f"{current_time} - 🔥 Alerta: Temperatura CPU {cpu_temp:.1f}°C"
            if alert_msg not in self.active_alerts:
                self.active_alerts.append(alert_msg)
                self.alerts_listbox.insert(tk.END, alert_msg)
                self.alerts_listbox.itemconfig(tk.END, {'bg': self.theme.get_color("danger_bg")})
    
    def clear_alerts(self):
        """Limpia todas las alertas."""
        self.alerts_listbox.delete(0, tk.END)
        self.active_alerts = []
    
    def toggle_theme(self):
        """Alterna entre tema claro y oscuro."""
        self.theme.toggle_theme()
        
        # Actualizar botón de tema
        self.theme_btn.configure(
            text="🌙 Tema Oscuro" if self.theme.is_light_mode() else "☀️ Tema Claro"
        )
        
        # Actualizar gráficos
        self.update_charts()
        
        # Actualizar colores de widgets
        self.alerts_listbox.configure(
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("danger")
        )
    
    def show_settings(self):
        """Muestra la ventana de configuración."""
        # Crear ventana de configuración
        settings_window = ctk.CTkToplevel(self.parent)
        settings_window.title("Configuración")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # Título
        ctk.CTkLabel(
            settings_window, 
            text="Configuración",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)
        
        # Frame para configuraciones
        settings_frame = ctk.CTkFrame(settings_window)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Intervalo de actualización
        update_frame = ctk.CTkFrame(settings_frame)
        update_frame.pack(fill=tk.X, pady=5)
        
        ctk.CTkLabel(
            update_frame, 
            text="Intervalo de actualización (ms):",
            font=("Segoe UI", 12)
        ).pack(side=tk.LEFT, padx=10)
        
        update_entry = ctk.CTkEntry(update_frame, width=100)
        update_entry.insert(0, str(self.update_interval))
        update_entry.pack(side=tk.RIGHT, padx=10)
        
        # Umbrales de alerta
        alert_frame = ctk.CTkFrame(settings_frame)
        alert_frame.pack(fill=tk.X, pady=5)
        
        ctk.CTkLabel(
            alert_frame, 
            text="Umbrales de alerta:",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # CPU
        cpu_alert_frame = ctk.CTkFrame(settings_frame)
        cpu_alert_frame.pack(fill=tk.X, pady=2)
        
        ctk.CTkLabel(
            cpu_alert_frame, 
            text="CPU (%):",
            font=("Segoe UI", 12)
        ).pack(side=tk.LEFT, padx=10)
        
        cpu_alert_entry = ctk.CTkEntry(cpu_alert_frame, width=100)
        cpu_alert_entry.insert(0, str(self.alert_thresholds['cpu']))
        cpu_alert_entry.pack(side=tk.RIGHT, padx=10)
        
        # RAM
        ram_alert_frame = ctk.CTkFrame(settings_frame)
        ram_alert_frame.pack(fill=tk.X, pady=2)
        
        ctk.CTkLabel(
            ram_alert_frame, 
            text="RAM (%):",
            font=("Segoe UI", 12)
        ).pack(side=tk.LEFT, padx=10)
        
        ram_alert_entry = ctk.CTkEntry(ram_alert_frame, width=100)
        ram_alert_entry.insert(0, str(self.alert_thresholds['ram']))
        ram_alert_entry.pack(side=tk.RIGHT, padx=10)
        
        # Botones
        btn_frame = ctk.CTkFrame(settings_window)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Función para guardar configuración
        def save_settings():
            try:
                # Actualizar intervalo
                new_interval = int(update_entry.get())
                if new_interval >= 100:
                    self.update_interval = new_interval
                
                # Actualizar umbrales
                new_cpu = int(cpu_alert_entry.get())
                if 0 <= new_cpu <= 100:
                    self.alert_thresholds['cpu'] = new_cpu
                
                new_ram = int(ram_alert_entry.get())
                if 0 <= new_ram <= 100:
                    self.alert_thresholds['ram'] = new_ram
                
                settings_window.destroy()
            except ValueError:
                pass
        
        # Botón guardar
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Guardar",
            command=save_settings
        )
        save_btn.pack(side=tk.RIGHT, padx=10)
        
        # Botón cancelar
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=settings_window.destroy
        )
        cancel_btn.pack(side=tk.RIGHT, padx=10)
    
    def _format_network_speed(self, speed_bytes):
        """Formatea la velocidad de red en unidades legibles."""
        if speed_bytes < 1024:
            return f"{speed_bytes:.1f} B/s"
        elif speed_bytes < 1024 * 1024:
            return f"{speed_bytes / 1024:.1f} KB/s"
        else:
            return f"{speed_bytes / (1024 * 1024):.1f} MB/s"