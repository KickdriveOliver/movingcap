"""Módulo time/utime stub/interfaz para servocontroladores fullmo MovingCap / CODE / Micropython

El módulo `utime` (alternativamente: `time`) proporciona un subconjunto del módulo `time` de MicroPython o CPython.

Esta es una implementación limitada para la plataforma MovingCap que proporciona funciones de temporización y retardo.
La funcionalidad completa de fecha/hora (localtime, mktime, time) no está soportada en MovingCap.

Para documentación completa sobre el módulo time estándar de MicroPython, consulte:
https://docs.micropython.org/en/v1.9.4/pyboard/library/utime.html

Funciones Disponibles:
    - sleep(seconds) - Dormir durante el número especificado de segundos
    - sleep_ms(ms) - Dormir durante el número especificado de milisegundos
    - sleep_us(us) - Dormir durante el número especificado de microsegundos
    - ticks_ms() - Obtener valor del contador de milisegundos
    - ticks_us() - Obtener valor del contador de microsegundos
    - ticks_add(ticks, delta) - Agregar delta a un valor ticks
    - ticks_diff(ticks1, ticks2) - Calcular diferencia entre valores ticks

No Disponible en MovingCap:
    - localtime() - No soportado (sin RTC)
    - mktime() - No soportado (sin RTC)
    - time() - No soportado (sin RTC)
    - ticks_cpu() - No soportado

Funciones Ticks - Notas Importantes:
    Las funciones ticks_ms() y ticks_us() devuelven valores en un rango definido por
    la implementación. En la plataforma MovingCap CODE actual, los valores se reinician
    dentro de un rango positivo más pequeño que el rango completo de enteros de 32 bits.
    
    NO haga suposiciones sobre el rango de valores específico ni realice operaciones
    aritméticas directas sobre valores ticks. El rango puede cambiar en implementaciones futuras.
    
    SIEMPRE use estas funciones auxiliares para la aritmética de ticks:
        - ticks_diff(ticks1, ticks2) - Calcular la diferencia entre dos valores ticks
        - ticks_add(ticks, delta) - Agregar/restar un desplazamiento a un valor ticks
    
    Estas funciones manejan correctamente el desbordamiento independientemente del rango
    de valores subyacente.

Notas de Uso:
    - Use este módulo para retardos, mediciones de tiempo e implementaciones de timeout
    - Para temporización precisa, prefiera ticks_us() sobre ticks_ms()

Ejemplo de Uso:
    import time  # o: import utime
    
    # Retardos simples
    time.sleep(1)  # Dormir 1 segundo
    time.sleep_ms(100)  # Dormir 100 milisegundos
    time.sleep_us(50)  # Dormir 50 microsegundos
    
    # Medición de tiempo
    start = time.ticks_ms()
    # ... hacer algo ...
    elapsed = time.ticks_diff(time.ticks_ms(), start)
    print("Transcurrido:", elapsed, "ms")
    
    # Implementación de timeout
    timeout = 5000  # Timeout de 5 segundos
    start = time.ticks_ms()
    condition = True
    while condition:
        if time.ticks_diff(time.ticks_ms(), start) > timeout:
            print("¡Timeout!")
            break
        # ... hacer trabajo ...
"""
__author__ =  "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.10.xx"
__date__ = "2026-01-19"

def sleep(seconds: int):
    """Dormir durante el número especificado de segundos.
    
    Suspende la ejecución durante al menos el número dado de segundos.
    El tiempo de suspensión real puede ser mayor debido a la programación del sistema.

    NOTA: MovingCap MicroPython actualmente no soporta flotantes. "seconds" no puede ser un número fraccionario.
    
    :param seconds: Número de segundos para dormir.
    :type seconds: int
    
    Ejemplo:
        time.sleep(2)  # Dormir durante 2 segundos
        time.sleep(1)  # Dormir durante 1 segundo
    """
    pass

def sleep_ms(ms: int):
    """Dormir durante el número especificado de milisegundos.
    
    Suspende la ejecución durante al menos el número dado de milisegundos.
    Más preciso que sleep() para retardos cortos.
    
    :param ms: Número de milisegundos para dormir.
    :type ms: int
    
    Ejemplo:
        time.sleep_ms(500)  # Dormir durante 500 milisegundos
        time.sleep_ms(10)   # Dormir durante 10 milisegundos
    """
    pass

def sleep_us(us: int):
    """Dormir durante el número especificado de microsegundos.
    
    Suspende la ejecución durante al menos el número dado de microsegundos.
    Función de retardo más precisa disponible. Para retardos muy cortos, use con precaución
    ya que la sobrecarga del sistema puede afectar la precisión.
    
    :param us: Número de microsegundos para dormir.
    :type us: int
    
    Ejemplo:
        time.sleep_us(1000)  # Dormir durante 1000 microsegundos (1 ms)
        time.sleep_us(50)    # Dormir durante 50 microsegundos
    """
    pass

def ticks_ms() -> int:
    """Obtener el valor actual del contador de milisegundos.
    
    Devuelve un contador de milisegundos monotónicamente creciente con punto de referencia arbitrario.
    El contador se reinicia después de alcanzar un valor máximo definido por la implementación.
    
    El rango de valores específico depende de la implementación y puede cambiar en versiones futuras.
    NUNCA confíe en un rango particular ni realice aritmética directa sobre valores ticks.
    
    SIEMPRE use ticks_diff() para calcular diferencias de tiempo y ticks_add() para
    desplazar valores ticks - estas funciones manejan correctamente el desbordamiento.
    
    :return: Conteo actual de ticks de milisegundos (rango definido por la implementación).
    :rtype: int
    
    Ejemplo:
        start = time.ticks_ms()
        # ... hacer algo ...
        duration = time.ticks_diff(time.ticks_ms(), start)  # CORRECTO
        # duration = time.ticks_ms() - start  # INCORRECTO - ¡no usar!
    """
    pass

def ticks_us() -> int:
    """Obtener el valor actual del contador de microsegundos.
    
    Devuelve un contador de microsegundos monotónicamente creciente con punto de referencia arbitrario.
    El contador se reinicia después de alcanzar un valor máximo definido por la implementación.
    Proporciona mayor resolución que ticks_ms() para temporización precisa.
    
    El rango de valores específico depende de la implementación y puede cambiar en versiones futuras.
    NUNCA confíe en un rango particular ni realice aritmética directa sobre valores ticks.
    
    SIEMPRE use ticks_diff() para calcular diferencias de tiempo y ticks_add() para
    desplazar valores ticks - estas funciones manejan correctamente el desbordamiento.
    
    :return: Conteo actual de ticks de microsegundos (rango definido por la implementación).
    :rtype: int
    
    Ejemplo:
        start = time.ticks_us()
        # ... operación precisa ...
        duration_us = time.ticks_diff(time.ticks_us(), start)  # CORRECTO
    """
    pass

def ticks_add(ticks: int, delta: int) -> int:
    """Agregar un delta a un valor ticks con manejo correcto de desbordamiento.
    
    Esta es la forma correcta de agregar o restar de un valor ticks.
    Realiza suma mientras maneja correctamente el desbordamiento del contador.
    
    :param ticks: Valor ticks base (de ticks_ms() o ticks_us()).
    :type ticks: int
    :param delta: Valor a agregar (positivo) o restar (negativo).
    :type delta: int
    :return: Nuevo valor ticks con manejo correcto de desbordamiento.
    :rtype: int
    
    Ejemplo:
        # Calcular una fecha límite 5 segundos en el futuro
        deadline = time.ticks_add(time.ticks_ms(), 5000)
        
        # Verificar si la fecha límite ha pasado
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            # Todavía antes de la fecha límite
            pass
    """
    pass

def ticks_diff(ticks1: int, ticks2: int) -> int:
    """Calcular la diferencia con signo entre dos valores ticks.
    
    Esta es la forma correcta de comparar o encontrar la diferencia entre valores ticks.
    Calcula (ticks1 - ticks2) con manejo apropiado del desbordamiento del contador.
    
    El resultado es un entero con signo:
        - Positivo si ticks1 es "después" de ticks2
        - Negativo si ticks1 es "antes" de ticks2
        - Cero si son iguales
    
    El resultado es válido siempre que la diferencia de tiempo real no exceda la mitad
    del período de ticks (aproximadamente 149 horas para ticks_ms en la implementación actual).
    
    :param ticks1: Primer valor ticks, típicamente el tiempo "posterior" o "final".
    :type ticks1: int
    :param ticks2: Segundo valor ticks, típicamente el tiempo "anterior" o "inicial".
    :type ticks2: int
    :return: Diferencia con signo (ticks1 - ticks2).
    :rtype: int
    
    Ejemplo:
        # Medir tiempo transcurrido
        start = time.ticks_ms()
        # ... operación ...
        elapsed = time.ticks_diff(time.ticks_ms(), start)
        
        # Timeout basado en fecha límite
        deadline = time.ticks_add(time.ticks_ms(), 1000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            pass  # Esperar hasta la fecha límite
        
        # Verificar si el timeout fue excedido
        if time.ticks_diff(time.ticks_ms(), start) > 1000:
            print("Más de 1 segundo transcurrido")
    """
    pass