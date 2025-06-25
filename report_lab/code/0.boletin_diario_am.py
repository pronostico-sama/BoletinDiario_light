# %%

from plantillas_boletines import *
from playsound import playsound

import warnings
# Mute all warnings
warnings.filterwarnings("ignore")

# Set the current date (can be replaced with the current timestamp if needed)
date_now = pd.to_datetime(pd.Timestamp.today())
# date_now = pd.to_datetime('2025-04-04')

# Calculate the index (idx) as the number of days passed since the reference date
idx = (date_now - DATE_REF).days
# DATE_REF it is set to be '2025-03-31'

report = '08'
dir_figures = f'{dir_sama}/graficas/{report}/'
path_out = f'{dir_sama}/report_lab/boletines/{report}/'

report_horizontal_am(date_now, idx, report, dir_report_lab, dir_sama,
                     dir_figures, path_out)

report_vertical_am(date_now, idx, report, dir_report_lab, dir_sama,
                   dir_figures, path_out)


playsound(f'{dir_sama}/report_lab/sound/level-up.mp3')
# %%


# %%
