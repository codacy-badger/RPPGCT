#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : config.py
# Description   : Módulo configurador para ser importado en el resto de módulos o sistemas que lo necesiten
# Author        : Veltys
# Date          : 18-11-2017
# Version       : 1.4.2
# Usage         : import config | from config import <clase>
# Notes         : A título ilustrativo, a se ofrece una configuración por defecto (la mía, para ser exactos)


class config_global:
    # Configuración común

    IP_DEP_REMOTA   = '0.0.0.0'                                                 # IP del servidor de depuración


class cpu_config(config_global):
    # Configuración del sistema de CPU

    GPIOS           = [(26, True,  True ),                                      # GPIOS contiene ternas de datos en formato lista:
                       (19, True,  True ),                                      # el primer elemento será el número (BCM) de puerto GPIO a manipular,
                       (13, True,  True ),                                      # el segundo, el modo (True para salida, False para entrada)
                       ( 6, True,  True ),                                      # y el tercero, la activación si es de salida (True si es activo a alto nivel o False si es a bajo nivel) o el estado si es de entrada (True si está bajado y False subido)
                       ( 5, True,  True ),
                      ]

    PAUSA           = 10                                                        # PAUSA contiene el tiempo que el bucle estará parado

    senyales        = {'SIGTERM': 'sig_cerrar',                                 # senyales (señales) contiene el tipo de señal y la función a la que ésta se asociará
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }


class domotica_cliente_config(config_global):
    puerto          = 4710                                                      # El puerto 4710 ha sido escogido arbitrariamente por estar libre, según la IANA:
                                                                                # https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=85


class domotica_servidor_config(domotica_cliente_config):
    GPIOS           = [(17, False, False),
                       (27, True , False),
                       (23, False, False),
                       (24, True , False),
                      ]

    PAUSA           = 0.20

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }


class internet_config(config_global):
    HOSTS           = ['google.es',                                             # HOSTS contiene los servidores a los cuales se les hará ping para comprobar si hay internet
                       '2001:4860:4860::8888',
                       '2001:4860:4860::8844',
                       '8.8.8.8',
                       '8.8.4.4',
                       'opendns.com',
                       '2620:0:ccc::2',
                       '2620:0:ccd::2',
                       '208.67.222.222',
                       '208.67.220.220',
                      ]


class reiniciar_router_config(config_global):
    GPIOS           = [( 4, True,  False),
                      ]

    PAUSA           = 15

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }


class temperaturas_config(config_global):
    COLORES         = [(0.0, 0.0, 1.0, 0.0),                                    # COLORES contiene una matriz de 4 x 4 que, por columnas, representa cada led y, por filas, la etapa de temperatura
                       (0.0, 1.0, 0.0, 0.0),
                       (1.0, 0.6, 0.0, 0.0),
                       (1.0, 0.0, 0.0, 1.0),
                      ]

    FRECUENCIA      = 60                                                        # FRECUENCIA contiene la frecuencia (en herzios) de refresco de los leds

    GPIOS           = [(16, True,  True ),
                       (20, True,  True ),
                       (21, True,  True ),
                       (12, True,  True ),
                      ]

    TEMPERATURAS    = [40, 45, 50]                                              # TEMPERATURAS contiene las temperaturas de activación de cada etapa

    PAUSA           = 60

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }