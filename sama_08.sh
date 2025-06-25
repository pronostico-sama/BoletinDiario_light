#!/usr/bin/bash
source /home/sgiraldoc4/.bashrc

#  sama_08.sh:
#   ejecuta todos los scripts necesarios para producir los mapas que se usan en el boletín de la mañana.
#
#  Created by Santiago Giraldo Cárdenas on 7/22/23.


###
# export SAMA=/home/jdmantillaq/Documents/SAMA/Boletin_Diario
# export path_cdo=/usr/bin/cdo
# export path_wget=/usr/bin/wget
# export path_convert=/usr/bin/convert


echo "aqui vamos"

cd $SAMA/icon/08/

echo "icon melo?"
bash icon.sh
echo "Sisas"


cd $SAMA/gem/08/

echo "gem melo?"
bash gem_prec.sh
echo "Sisas sisas"


cd $SAMA/gfs/08/

echo "gfs melo?"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 down_gfs_3hr.py
echo "Sisas sisas"


cd $SAMA/winds/08/

echo "vientos melo?"
bash winds.sh
echo "Sisas"


cd $SAMA/scripts/ejecutables/

echo "A producir las graficas maestro"

echo "ICON"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 icon-08.py
echo "melo"

echo "GEM"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 gem-08.py
echo "melo"

echo "GFS 3hr"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 gfs-3hr-08.py
echo "melo"


echo "Vamos por el ensemble"

cd $SAMA/ens/08/

# Este no funcionó bien
echo "listo el ensemble?"
bash operacional.sh
echo "Melo"

cd $SAMA/scripts/ejecutables/

echo "Graficas ENS"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 ens-08.py
echo "Melo"

echo "listo panel pronostico?"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 panel-08.py
echo "Melo"


echo "Ahora el GOES papi, ya casi"

echo "GOES listo?"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 goes-08.py
echo "melo"




echo "Estamos melos"
echo "Sisas"

echo "Actualicemos el sitio web mor..."

cd $SAMA/gem/08/

echo "temperatura gem?"
bash gem_temp.sh
echo "mela"


cd $SAMA/website/08/

echo "pronostico website"
bash website.sh
echo "melo"


echo "Estamos melos"
echo "Sisas sisas"


# Limpiar archivos txt para el boletín
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 $SAMA/report_lab/code/clean_txt_files_am.py

# Generar boletín
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 $SAMA/report_lab/code/0.boletin_diario_am.py

# Play AZ
echo "Vamos con AZ"
/home/sgiraldoc4/miniconda3/envs/sama/bin/python3 $SAMA/report_lab/code/play_AZ.py