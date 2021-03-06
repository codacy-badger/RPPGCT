#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : reiniciar_router.py
# Description   : Sistema que comprueba si hay acceso a Internet. Si no, manda una señal en un puerto GPIO determinado
# Author        : Veltys
# Date          : 30-11-2017
# Version       : 2.2.0
# Usage         : python3 reiniciar_router.py
# Notes         : La idea es conectar un relé a este GPIO y al mismo la alimentación del sistema de acceso a Internet
#                 Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual simplemente apaga todos los leds hasta que esta misma señal sea recibida de nuevo


DEBUG        = False
DEBUG_REMOTO = False


import errno                                                                                # Códigos de error
import os                                                                                   # Funcionalidades varias del sistema operativo
import socket                                                                               # Tratamiento de sockets
import sys                                                                                  # Funcionalidades varias del sistema

import comun                                                                                # Funciones comunes a varios sistemas

if DEBUG_REMOTO:
    import pydevd                                                                           # Depuración remota

from time import sleep                                                                      # Gestión de pausas

try:
    from config import reiniciar_router_config as config                                    # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from internet import hay_internet                                                           # Módulo propio de comprobación de Internet


class reiniciar_router(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def bucle(self):
        try:
            if self._conectar('conectar ' + self._config.servidor, False):
                for GPIO in self._config.GPIO:
                    self._enviar_y_recibir('apagar ' + str(GPIO[0]))

                self._desconectar()

            sleep(self._config.PAUSA * 4)                                                   # Es necesario una pausa adicional, ya que al arrancar es posible que este script se ejecute antes de que haya red y no queremos que se reinicie el router "porque sí"

            while True:
                if hay_internet():                                                          # Si hay Internet, simplemente se esperará para hacer la próxima comprobación
                    sleep(self._config.PAUSA * 60)

                else:                                                                       # En caso contrario, se mandará la orden de apagado durante el tiempo mínimo establecido y después se restablecerá
                    if self._conectar('conectar ' + self._config.servidor, False):
                        for GPIO in self._config.GPIO:
                            self._enviar_y_recibir('encender ' + str(GPIO[0]))

                        sleep(self._config.PAUSA)

                        for GPIO in self._config.GPIO:
                            self._enviar_y_recibir('apagar ' + str(GPIO[0]))

                        self._desconectar()

                    sleep(self._config.PAUSA * 12)                                          # Al acabar, se esperará a que se haya levantado la conexión y se volverá a comprobar

        except KeyboardInterrupt:
            self.cerrar()
            return


    def __del__(self):
        super().__del__()


def main(argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    app = reiniciar_router(config, os.path.basename(argv[0]))
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
