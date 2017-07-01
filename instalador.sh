#!/bin/bash

# Title		: instalador.sh
# Description	: Instala los scripts y los configura para iniciarse automáticamente
# Author	: Veltys
# Date		: 29-06-2017
# Version	: 1.1.0
# Usage		: sudo bash instalador.sh
# Notes		: Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
  echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
  directorio='/opt/RPPGCT'

  mkdir $directorio

  install ./Python/config.py.sample $directorio/
  echo "Recuerde editar ${directorio}/config.py.sample y guardarlo como config.py con los valores adecuados"

  install ./Python/pid.py $directorio/
  install ./Python/temperaturas.py $directorio/
  install ./init/temperaturas.sh /etc/init.d/temperaturas
  update-rc.d temperaturas defaults

  install ./Python/cpu.py $directorio/
  install ./init/cpu.sh /etc/init.d/cpu
  update-rc.d cpu defaults

  install ./Python/internet.py $directorio/
  install ./Python/reiniciar_router.py $directorio/
  install ./init/reiniciar_router.sh /etc/init.d/reiniciar_router
  update-rc.d reiniciar_router defaults
fi
