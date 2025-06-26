#%%
import gdown
import os


# Dictionary mapping report IDs to Google Drive folder URLs
url_dic = {
    '08': 'https://drive.google.com/drive/folders/1kJTdYEIT_N5BU-wzbnb5ltINTjGlyyju',
    '16': 'https://drive.google.com/drive/folders/1Zb1eebvLpc3GMsvl87FOcxTWuOc84xRO'
}

# Report identifier (used to select the correct Google Drive folder)
report = '08'

# Get the input/output directory from the environment variable "NODO"
dir_sama = os.getenv("NODO")

if dir_sama is None:
    # If the environment variable is not set, set it to a default path
    os.environ['NODO'] = '/home/sgiraldoc4/BoletinDiario_light'
    dir_sama = os.environ.get("NODO")


# Path where the downloaded figures will be saved
path_figures = os.path.join(dir_sama, 'graficas', '')

print('\t\033[94mDescargando las gráficas...\033[0m')

# Download the entire folder from Google Drive using gdown and save it to path_figures
result = gdown.download_folder(
    url_dic[report],
    output=path_figures,
    quiet=True,
    use_cookies=True,
)

if result:
    print('\t\t\033[92mDescarga completada: ok\033[0m')
else:
    print('\t\t\033[91mDescarga fallida\033[0m')