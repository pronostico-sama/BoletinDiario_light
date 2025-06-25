#!/usr/bin/bash
source /home/sgiraldoc4/.bashrc

#  sama_16.sh:
#   ejecuta todos los scripts necesarios para producir los mapas que se usan en el boletín de la tarde.
#
#  Created by Santiago Giraldo Cárdenas on 2024/04/01.


###
# export SAMA=/home/jdmantillaq/Documents/SAMA/Boletin_Diario
# export path_cdo=/usr/bin/cdo
# export path_wget=/usr/bin/wget
# export path_convert=/usr/bin/convert


echo "aqui vamos"

cd $SAMA/icon/16/

echo "icon melo?"
bash icon.sh
echo "Sisas"


cd $SAMA/gem/16/

echo "gem melo?"
bash gem_prec.sh
echo "Sisas sisas"


cd $SAMA/gfs/16/

echo "gfs melo?"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 down_gfs_3hr.py
echo "Sisas sisas"


cd $SAMA/winds/16/

echo "vientos melo?"
bash winds.sh
echo "Sisas"


cd $SAMA/scripts/ejecutables/

echo "A producir las graficas maestro"

echo "ICON"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 icon-16.py
echo "melo"

echo "GEM"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 gem-16.py
echo "melo"

echo "GFS 3hr"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 gfs-3hr-16.py
echo "melo"


echo "Vamos por el ensemble"

cd $SAMA/ens/16/

echo "listo el ensemble?"
bash operacional.sh
echo "Melo"

cd $SAMA/scripts/ejecutables/

echo "Graficas ENS"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 ens-16.py
echo "Melo"

echo "listo panel pronostico?"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 panel-16.py
echo "Melo"


echo "Ahora el GOES papi, ya casi"

echo "GOES listo?"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 goes-16.py
echo "melo"


echo "Ahora el acumulado de GPM de ayer"

cd $SAMA/gpm/16/

echo "GPM"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 GPM_diario_BarraNueva.py
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 cat_gpm.py
echo "melo"

echo "Estamos melos"
echo "Sisas"


echo "Actualicemos el sitio web mor"

cd $SAMA/gem/16/

echo "temperatura gem?"
bash gem_temp.sh
echo "mela"


cd $SAMA/website/16/

echo "pronostico website"
bash website.sh
echo "melo"


echo "Estamos melos"
echo "Sisas sisas"

# Limpiar archivos txt para el boletín
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 $SAMA/report_lab/code/clean_txt_files_pm.py

# Generar boletín
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 $SAMA/report_lab/code/1.boletin_diario_pm.py

# Play AZ
echo "Vamos con AZ"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 $SAMA/report_lab/code/play_AZ.py
