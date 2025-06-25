from playsound import playsound
import os
# Directorios de entrada y de salida
dir_sama = os.getenv("SAMA")

if dir_sama is None:
    # Set the environment variable DIR to the desired path
    os.environ['SAMA'] = '/home/jdmantillaq/Documents/SAMA/Boletin_Diario'

    dir_sama = os.environ.get("SAMA")

playsound(f'{dir_sama}/report_lab/sound/AZ.mp3')