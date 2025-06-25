# Boletín Diario - Generación de Reportes Meteorológicos

Este proyecto genera boletines meteorológicos diarios en formato PDF y PNG utilizando datos de entrada, gráficos y plantillas predefinidas. Los boletines incluyen información sobre condiciones observadas y pronósticos para diferentes jornadas del día.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
BoletinDiario_light/
├── report_lab/
│   ├── code/
│   │   ├── plantillas_boletines.py
│   │   ├── 0.boletin_diario_am.py
│   │   ├── 1.boletin_diario_pm.py
│   ├── fonts/
│   ├── txt_boletin/
│   ├── boletines/
├── graficas/
```

`Boletin_diario` corresponde al `basedir = os.getenv("SAMA")`

### Archivos principales

- **`plantillas_boletines.py`**: Contiene las funciones principales para generar boletines, incluyendo el manejo de plantillas, estilos de texto, y la integración de imágenes y texto.
- **`0.boletin_diario_am.py`**: Script para generar boletines de la jornada de la mañana.
- **`1.boletin_diario_pm.py`**: Script para generar boletines de la jornada de la tarde.

### Archivos necesarios
* Plantillas PDF: Las plantillas base para los boletines deben estar en la carpeta `report_lab/plantillas/`.
* Fuentes: Las fuentes necesarias deben estar en la carpeta `report_lab/fonts/`.
* Gráficos: Los gráficos diarios deben estar en la carpeta `graficas/{report}/`.
* Archivos de texto: Los textos de entrada deben estar en la carpeta `report_lab/txt_boletin/{report}/`.


## Requiriments
```
numpy==1.26.4
pandas==2.2.3
reportlab==4.3.1
Pillow==11.1.0
pypdf==5.4.0
markdown2==2.5.3
```

# Uso

Generar boletines
1. Configura las rutas de entrada y salida en los scripts `0.boletin_diario_am.py` y `1.boletin_diario_pm.py`.
2. Ejecuta el script correspondiente para generar los boletines:

    * Para la jornada de la **mañana**:
        ```
        python 0.boletin_diario_am.py
        ```
    * Para la jornada de la **tarde**:
        ```
        python 1.boletin_diario_pm.py
        ```
3. Los boletines generados se guardarán en la carpeta `report_lab/boletines/{report}/` en formato PDF y PNG.