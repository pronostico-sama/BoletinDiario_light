#!/bin/sh

#  sama_08.sh:
#   ejecuta todos los scripts necesarios para producir los mapas que se usan
#   en el boletín de la mañana.
#
#  Created by Santiago Giraldo Cárdenas on 7/22/23.

# Se descargan las figuras de google drive
python3 $NODO/report_lab/code/0.download_am.py


# Limpiar archivos txt para el boletín
python3 $NODO/report_lab/code/0.clean_txt_files_am.py


# Generar boletín
python3 $NODO/report_lab/code/0.boletin_diario_am.py