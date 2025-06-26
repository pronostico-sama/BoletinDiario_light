#!/bin/sh

#  sama_16.sh:
#   ejecuta todos los scripts necesarios para producir los mapas que se usan en el boletín de la tarde.
#
#  Created by Santiago Giraldo Cárdenas on 2024/04/01.

# Se descargan las figuras de google drive
python3 $NODO/report_lab/code/1.download_pm.py


# Limpiar archivos txt para el boletín
python3 $NODO/report_lab/code/1.clean_txt_files_pm.py


# Generar boletín
python3 $NODO/report_lab/code/1.boletin_diario_pm.py