#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : cpu.py
# Description   : Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma"
# Author        : Veltys
# Date          : 10-08-2017
# Version       : 2.1.7
# Usage         : python3 cpu.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual simplemente apaga todos los leds hasta que esta misma señal sea recibida de nuevo


DEBUG = False
DEBUG_REMOTO = False


import errno                                                                    # Códigos de error
import os                                                                       # Funcionalidades varias del sistema operativo
import sys                                                                      # Funcionalidades varias del sistema

if DEBUG_REMOTO:
    import pydevd                                                               # Depuración remota

import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO

import comun                                                                    # Funciones comunes a varios sistemas

from time import sleep                                                          # Para hacer pausas

try:
    from psutil import cpu_percent                                              # Obtención del porcentaje de uso de la CPU

except ImportError:
    print('Error: Paquete "psutil" no encontrado' + os.linesep + 'Puede instalarlo con la orden "[sudo] pip3 install psutil"', file = sys.stderr)
    sys.exit(errno.ENOENT)

try:
    from config import cpu_config as config                                       # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


class cpu(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

    def bucle(self):
        try:
            alarma = 0

            while True:
                if self._modo_apagado:
                    for gpio, _, activacion, _ in self._config.GPIOS:
                        GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                else:
                    cpu = cpu_percent()

                    i = 0
                    for gpio, _, activacion, _ in self._config.GPIOS:
                        if i < len(self._config.GPIOS) - 1:
                            if cpu >= 100 / (len(self._config.GPIOS) - 1) * i:
                                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)
                            else:
                                GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                        elif cpu >= 95:
                            alarma = alarma + 1

                            if alarma >= 5:
                                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)

                        else:
                            alarma = 0
                            GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                        i = i + 1

                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            self.cerrar()
            return

    def __del__(self):
        super().__del__()


def main(argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    app = cpu(config, os.path.basename(argv[0]))
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
