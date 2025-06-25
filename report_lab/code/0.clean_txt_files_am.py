#%%
from plantillas_boletines import clean_txt_files
import os

# Directorios de entrada y de salida
dir_sama = os.getenv("NODO")


if dir_sama is None:
    # Set the environment variable DIR to the desired path
    os.environ['NODO'] = '/home/sgiraldoc4/BoletinDiario_light'
    dir_sama = os.environ.get("NODO")
    
report = '08'
clean_txt_files(report)


#%%
    

