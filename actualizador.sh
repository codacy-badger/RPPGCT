#!/bin/bash

# Title         : actualizador.sh
# Description   : Actualiza los scripts sin alterar la configuración de inicio automático
# Author        : Veltys
# Date          : 01-07-2017
# Version       : 1.1.0
# Usage         : sudo bash actualizador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
  echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
  directorio='/opt/RPPGCT'

  echo 'Recuerde revisar ./Python/config.py.sample por si la configuración ha cambiado'

  /etc/init.d/temperaturas stop
  rm $directorio/pid.py
  rm $directorio/temperaturas.py
  rm /etc/init.d/temperaturas
  install ./Python/pid.py $directorio/
  install ./Python/temperaturas.py $directorio/
  install ./init/temperaturas.sh /etc/init.d/temperaturas

  /etc/init.d/cpu stop
  rm $directorio/cpu.py
  rm /etc/init.d/cpu
  install ./Python/cpu.py $directorio/
  install ./init/cpu.sh /etc/init.d/cpu

  /etc/init.d/reiniciar_router stop
  rm $directorio/internet.py
  rm $directorio/reiniciar_router.py
  rm /etc/init.d/reiniciar_router
  install ./Python/internet.py $directorio/
  install ./Python/reiniciar_router.py $directorio/
  install ./init/reiniciar_router.sh /etc/init.d/reiniciar_router
fi