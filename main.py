#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Monitor de Sistema Avanzado
---------------------------
Dashboard que monitorea CPU, RAM, disco, red, procesos.
Incluye alertas, gráficos históricos y predicciones.
"""

import os
import sys
from app.gui import App

if __name__ == "__main__":
    # Iniciar la aplicación
    app = App()
    app.mainloop()