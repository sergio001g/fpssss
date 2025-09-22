#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para monitoreo de recursos del sistema.
"""

import psutil
import time
import threading
import numpy as np
from datetime import datetime

class SystemMonitor:
    """Clase principal para monitoreo de recursos del sistema."""
    
    def __init__(self, history_size=60):
        """
        Inicializa el monitor de sistema.
        
        Args:
            history_size (int): Tamaño del historial de datos a mantener.
        """
        self.history_size = history_size
        self.running = False
        self.update_interval = 1.0  # segundos
        self.update_callbacks = []
        
        # Historiales
        self.cpu_history = []
        self.ram_history = []
        self.disk_history = []
        self.net_recv_history = []
        self.net_sent_history = []
        self.fps_history = []
        
    def set_update_callback(self, callback):
        """
        Establece una función de callback para actualizar la interfaz.
        
        Args:
            callback: Función a llamar cuando se actualicen los datos
        """
        if callback not in self.update_callbacks:
            self.update_callbacks.append(callback)
            
    def start_monitoring(self):
        """Inicia el monitoreo de recursos en un bucle."""
        if self.running:
            return
            
        self.running = True
        
        while self.running:
            # Obtener datos actuales
            self.update_data()
            
            # Llamar a los callbacks registrados
            for callback in self.update_callbacks:
                try:
                    callback()
                except Exception as e:
                    print(f"Error en callback: {e}")
            
            # Esperar hasta la próxima actualización
            time.sleep(self.update_interval)
    
    def stop(self):
        """Detiene el monitoreo de recursos."""
        self.running = False
            
    def update_data(self):
        """Actualiza los datos del sistema."""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_history.append(cpu_percent)
        if len(self.cpu_history) > self.history_size:
            self.cpu_history = self.cpu_history[-self.history_size:]
            
        # RAM
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        self.ram_history.append(ram_percent)
        if len(self.ram_history) > self.history_size:
            self.ram_history = self.ram_history[-self.history_size:]
            
        # Disco
        try:
            disk = psutil.disk_usage('C:\\')  # Usar C:\ en Windows
            disk_percent = disk.percent
            self.disk_history.append(disk_percent)
            if len(self.disk_history) > self.history_size:
                self.disk_history = self.disk_history[-self.history_size:]
        except Exception as e:
            print(f"Error al obtener uso de disco: {e}")
            self.disk_history.append(0)
            
        # Red
        net = psutil.net_io_counters()
        self.net_recv_history.append(net.bytes_recv / 1024 / 1024)  # MB
        self.net_sent_history.append(net.bytes_sent / 1024 / 1024)  # MB
        if len(self.net_recv_history) > self.history_size:
            self.net_recv_history = self.net_recv_history[-self.history_size:]
        if len(self.net_sent_history) > self.history_size:
            self.net_sent_history = self.net_sent_history[-self.history_size:]
            
        # FPS (simulado para demostración)
        fps = np.random.randint(30, 120)
        self.fps_history.append(fps)
        if len(self.fps_history) > self.history_size:
            self.fps_history = self.fps_history[-self.history_size:]
    
    def get_cpu_percent(self):
        """Retorna el porcentaje actual de uso de CPU."""
        if not self.cpu_history:
            return 0
        return self.cpu_history[-1]
    
    def get_ram_percent(self):
        """Retorna el porcentaje actual de uso de RAM."""
        if not self.ram_history:
            return 0
        return self.ram_history[-1]
        
    def get_ram_usage(self):
        """Retorna la memoria RAM usada y total en GB."""
        ram = psutil.virtual_memory()
        used = ram.used / (1024 * 1024 * 1024)  # Convertir a GB
        total = ram.total / (1024 * 1024 * 1024)  # Convertir a GB
        return round(used, 2), round(total, 2)
    
    def get_disk_percent(self):
        """Retorna el porcentaje actual de uso de disco."""
        if not self.disk_history:
            return 0
        return self.disk_history[-1]
        
    def get_disk_io(self):
        """Retorna la actividad de lectura/escritura del disco en MB/s."""
        try:
            # Obtener estadísticas de E/S del disco
            disk_io = psutil.disk_io_counters()
            read_bytes = disk_io.read_bytes / (1024 * 1024)  # MB
            write_bytes = disk_io.write_bytes / (1024 * 1024)  # MB
            return round(read_bytes, 2), round(write_bytes, 2)
        except Exception as e:
            print(f"Error al obtener E/S de disco: {e}")
            return 0, 0
    
    def get_network_usage(self):
        """Retorna el uso actual de red (recibido, enviado) en MB."""
        recv = self.net_recv_history[-1] if self.net_recv_history else 0
        sent = self.net_sent_history[-1] if self.net_sent_history else 0
        return recv, sent
        
    def get_network_speed(self):
        """Retorna la velocidad actual de red (descarga, subida) en MB/s."""
        try:
            # Obtener estadísticas de red actuales
            net_io = psutil.net_io_counters()
            recv_bytes = net_io.bytes_recv / (1024 * 1024)  # MB
            sent_bytes = net_io.bytes_sent / (1024 * 1024)  # MB
            
            # Calcular velocidad (simulada para demostración)
            # En una implementación real, se calcularía la diferencia entre mediciones
            recv_speed = np.random.uniform(0.1, 10.0)  # Entre 0.1 y 10 MB/s
            sent_speed = np.random.uniform(0.05, 5.0)  # Entre 0.05 y 5 MB/s
            
            return round(recv_speed, 2), round(sent_speed, 2)
        except Exception as e:
            print(f"Error al obtener velocidad de red: {e}")
            return 0.0, 0.0
        
    def get_cpu_temp(self):
        """Retorna la temperatura de la CPU (simulada)."""
        # Simulamos temperatura entre 40-80°C
        return np.random.randint(40, 80)
        
    def get_fps(self):
        """Retorna el FPS actual."""
        if not self.fps_history:
            return 0
        return self.fps_history[-1]
    
    def get_process_list(self, limit=10):
        """
        Obtiene la lista de procesos ordenados por uso de CPU.
        
        Args:
            limit (int): Número máximo de procesos a retornar.
            
        Returns:
            list: Lista de diccionarios con información de procesos.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'cpu_percent': pinfo['cpu_percent'],
                    'memory_percent': pinfo['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Ordenar por uso de CPU
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return processes[:limit]
        
        # Valores actuales
        self.cpu_percent = 0
        self.ram_percent = 0
        self.disk_percent = 0
        self.net_recv = 0
        self.net_sent = 0
        self.fps = 0
        
        # Valores anteriores para cálculos
        self.last_time = time.time()
        self.last_frame_time = time.time()
        self.frame_count = 0
        
        # Callbacks
        self.update_callbacks = []
        
        # Información de red previa para cálculo de velocidad
        self.prev_net_io = psutil.net_io_counters()
        self.prev_net_time = time.time()
    
    def start(self):
        """Inicia el monitoreo en segundo plano."""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
    
    def stop(self):
        """Detiene el monitoreo."""
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=1.0)
    
    def register_update_callback(self, callback):
        """
        Registra una función de callback para notificar actualizaciones.
        
        Args:
            callback (callable): Función a llamar cuando hay nuevos datos.
        """
        if callable(callback) and callback not in self.update_callbacks:
            self.update_callbacks.append(callback)
    
    def unregister_update_callback(self, callback):
        """Elimina un callback registrado."""
        if callback in self.update_callbacks:
            self.update_callbacks.remove(callback)
    
    def _notify_update(self):
        """Notifica a todos los callbacks registrados."""
        for callback in self.update_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error en callback: {e}")
    
    def _monitor_loop(self):
        """Bucle principal de monitoreo."""
        while self.running:
            try:
                self._update_metrics()
                self._notify_update()
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Error en monitoreo: {e}")
    
    def _update_metrics(self):
        """Actualiza todas las métricas del sistema."""
        # CPU
        self.cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_history.append(self.cpu_percent)
        if len(self.cpu_history) > self.history_size:
            self.cpu_history.pop(0)
        
        # RAM
        mem = psutil.virtual_memory()
        self.ram_percent = mem.percent
        self.ram_history.append(self.ram_percent)
        if len(self.ram_history) > self.history_size:
            self.ram_history.pop(0)
        
        # Disco
        disk = psutil.disk_usage('/')
        self.disk_percent = disk.percent
        self.disk_history.append(self.disk_percent)
        if len(self.disk_history) > self.history_size:
            self.disk_history.pop(0)
        
        # Red
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.prev_net_time
        
        if time_diff > 0:
            self.net_recv = (current_net_io.bytes_recv - self.prev_net_io.bytes_recv) / time_diff
            self.net_sent = (current_net_io.bytes_sent - self.prev_net_io.bytes_sent) / time_diff
            
            self.net_recv_history.append(self.net_recv)
            self.net_sent_history.append(self.net_sent)
            
            if len(self.net_recv_history) > self.history_size:
                self.net_recv_history.pop(0)
            if len(self.net_sent_history) > self.history_size:
                self.net_sent_history.pop(0)
        
        self.prev_net_io = current_net_io
        self.prev_net_time = current_time
        
        # FPS del sistema
        self.frame_count += 1
        current_time = time.time()
        time_diff = current_time - self.last_frame_time
        
        if time_diff >= 1.0:  # Actualizar FPS cada segundo
            self.fps = self.frame_count / time_diff
            self.fps_history.append(self.fps)
            if len(self.fps_history) > self.history_size:
                self.fps_history.pop(0)
            
            self.frame_count = 0
            self.last_frame_time = current_time
    
    def get_cpu_info(self):
        """Obtiene información detallada de la CPU."""
        cpu_info = {
            'percent': self.cpu_percent,
            'count': psutil.cpu_count(logical=True),
            'physical_count': psutil.cpu_count(logical=False),
            'per_cpu': psutil.cpu_percent(percpu=True),
            'freq': psutil.cpu_freq() if hasattr(psutil, 'cpu_freq') else None,
            'history': self.cpu_history
        }
        return cpu_info
    
    def get_memory_info(self):
        """Obtiene información detallada de la memoria."""
        mem = psutil.virtual_memory()
        memory_info = {
            'percent': self.ram_percent,
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'history': self.ram_history
        }
        return memory_info
    
    def get_disk_info(self):
        """Obtiene información detallada del disco."""
        disk = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters() if hasattr(psutil, 'disk_io_counters') else None
        
        disk_info = {
            'percent': self.disk_percent,
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'io': disk_io,
            'history': self.disk_history
        }
        return disk_info
    
    def get_network_info(self):
        """Obtiene información detallada de la red."""
        net_info = {
            'recv_speed': self.net_recv,
            'sent_speed': self.net_sent,
            'recv_history': self.net_recv_history,
            'sent_history': self.net_sent_history,
            'connections': len(psutil.net_connections())
        }
        return net_info
    
    def get_fps_info(self):
        """Obtiene información de FPS del sistema."""
        fps_info = {
            'current': self.fps,
            'history': self.fps_history,
            'avg': np.mean(self.fps_history) if self.fps_history else 0,
            'min': min(self.fps_history) if self.fps_history else 0,
            'max': max(self.fps_history) if self.fps_history else 0
        }
        return fps_info
    
    def get_processes(self, sort_by='cpu', limit=10):
        """
        Obtiene lista de procesos ordenados por uso de recursos.
        
        Args:
            sort_by (str): Campo para ordenar ('cpu', 'memory')
            limit (int): Número máximo de procesos a retornar
            
        Returns:
            list: Lista de diccionarios con información de procesos
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'username': pinfo['username'],
                    'cpu_percent': pinfo['cpu_percent'],
                    'memory_percent': pinfo['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Ordenar y limitar
        if sort_by == 'memory':
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        else:
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return processes[:limit]