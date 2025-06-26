# Boletín Diario - Generación de Reportes Meteorológicos

Este proyecto genera boletines meteorológicos diarios en formato PDF y PNG utilizando datos de entrada, gráficos y plantillas predefinidas. Los boletines incluyen información sobre condiciones observadas y pronósticos para diferentes jornadas del día.

## Descripción de los scripts principales

* `0.download_am.py` / `1.download_pm.py`: Descargan las imágenes necesarias desde Google Drive usando la librería gdown.
* `0.clean_txt_files_am.py` / `1.clean_txt_files_pm.`py`: Limpian y preparan los archivos .txt donde se debe ingresar la información del boletín.
* `0.boletin_diario_am.py` / `1.boletin_diario_pm.py`: Generan el boletín final (PDF y PNG) usando la información de los .txt y las imágenes descargadas.
* `plantillas_boletines.py`: Contiene las funciones para la generación y diseño de los boletines.
* `utilities.py`: Funciones auxiliares para manejo de archivos y directorios.

## Edición y generación del boletín final

Una vez ejecutado los bash y generado el informe preliminar recuerde completar la información de los archivos `.txt` (ubicados en [`report_lab/txt_boletin/08/`](txt_boletin/08) o [`report_lab/txt_boletin/16/`](txt_boletin/16)).


Ejecute el script Python correspondiente para generar el boletín completo:
* Para la mañana:
    ```bash
    python report_lab/code/0.boletin_diario_am.py
    ```
* Para la tarde:
    ```bash
    python report_lab/code/1.boletin_diario_pm.py
    ```


Los archivos generados de los boletines, tanto preliminares como finales, quedan almacenados en el directorio [boletines](boletines), dentro de la carpeta correspondiente a cada horario (08 para la mañana y 16 para la tarde).
