"""Modulo sys stub/interfaccia per i servoazionamenti fullmo MovingCap / CODE / Micropython

Il modulo `sys` fornisce parametri e funzioni specifici del sistema per MovingCap MicroPython.

Questo modulo include:
- Funzioni del modulo sys standard MicroPython/CPython (sottoinsieme di v1.9.4)
- Estensioni specifiche MovingCap per applicazioni di controllo in tempo reale
- Funzioni di compatibilità per i vecchi azionamenti CANopen MovingCap con pymite/Python-On-A-Chip

Funzioni Standard:
    - version - Stringa di versione Python
    - version_info - Tupla di versione Python (major, minor, patch)
    - implementation - Dettagli di implementazione (name, version, platform, platver)
    - platform - Stringa di identificazione della piattaforma
    - byteorder - Ordine dei byte nativo ('little' o 'big')
    - exit([retval]) - Uscire dal programma
    - print_exception(exc, [file]) - Stampare traccia dell'eccezione
    - exc_info() - Ottenere informazioni sull'eccezione corrente come tupla

Estensioni MovingCap:
    - cycle_time_ms(period) - Helper per cicli a tempo di ciclo fisso
    - time() - Compatibilità: Ottenere timer in millisecondi (usare time.ticks_ms() nel nuovo codice)
    - wait(ms) - Compatibilità: Ritardo in millisecondi (usare time.sleep_ms() nel nuovo codice)

Per la documentazione completa del modulo sys di MicroPython, vedere:
https://docs.micropython.org/en/v1.9.4/pyboard/library/sys.html

Esempio di Utilizzo:
  import sys
  import time

  def do_control_task():
      dummy = 2000
      for runs in range((time.ticks_ms() % 100) + 10):
          dummy = dummy - 20
          dummy2 = dummy + 10

  # Verificare la versione Python
  print("sys.version (python) = %s" % sys.version)
  # Verificare i dettagli di implementazione
  print("sys.implementation = %s" % repr(sys.implementation))

  # Ciclo di controllo a tempo di ciclo fisso
  sys.cycle_time_ms(0)  # Resettare il timer di ciclo
  for cycle in range(20):
      # Eseguire operazioni di controllo
      do_control_task()
      remaining = sys.cycle_time_ms(10)  # Assicurare tempo di ciclo di 10ms
      print ("Ciclo di 10 msec, giro = %d, tempo rimanente = %d" % (cycle, remaining)) 

  # Gestione delle eccezioni
  try:
      risky_operation()
  except Exception as e:
      sys.print_exception(e)
      sys.exit(1)
"""
__author__ =  "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.10.xx"
__date__ = "2026-01-19"

# Attributi del modulo
version: str
"""Stringa di versione del linguaggio Python (es., "3.4.0")."""

version_info: tuple
"""Versione del linguaggio Python come tupla (major, minor, patch)."""

class _Implementation:
    """Oggetto informazioni di implementazione."""
    name: str
    """Nome implementazione ("micropython")."""
    version: tuple
    """Tupla di versione MicroPython (major, minor, micro)."""
    platform: str
    """Nome piattaforma ("movingcap")."""
    platver: tuple
    """Tupla di versione MovingCap (dev_type, major, minor, revision)."""

implementation: _Implementation
"""Dettagli di implementazione includendo versioni MicroPython e MovingCap."""

platform: str
"""Stringa di identificazione della piattaforma."""

byteorder: str
"""Ordine dei byte nativo: 'little' o 'big'."""

stdin: object
"""Flusso di input standard."""

stdout: object
"""Flusso di output standard."""

stderr: object
"""Flusso di errore standard."""

def exit(retval: int = 0):
    """Uscire dal programma sollevando un'eccezione SystemExit.
    
    :param retval: Codice di uscita (0 per successo, diverso da zero per errore). Predefinito è 0.
    :type retval: int
    :raises SystemExit: Sempre sollevata per terminare il programma.
    
    Esempio:
        if error_condition:
            sys.exit(1)  # Uscire con codice di errore 1
    """
    pass

def print_exception(exc, file=None):
    """Stampare traccia dell'eccezione su un file o stdout.
    
    Stampa il tipo di eccezione, il messaggio e la traccia in formato leggibile.
    Se nessun file è specificato, stampa su stdout.
    
    :param exc: Oggetto eccezione da stampare.
    :type exc: Exception
    :param file: Flusso file opzionale su cui scrivere. Se None, usa stdout.
    :type file: oggetto tipo file o None
    
    Esempio:
        try:
            risky_operation()
        except Exception as e:
            sys.print_exception(e)
            # o scrivere su file:
            # with open('error.log', 'w') as f:
            #     sys.print_exception(e, f)
    """
    pass

def exc_info() -> tuple:
    """Ottenere informazioni sull'eccezione corrente.
    
    Restituisce una tupla contenente (tipo, valore, traccia) dell'eccezione corrente.
    Se nessuna eccezione è in gestione, restituisce (None, None, None).
    
    :return: Tupla di (exception_type, exception_value, traceback).
    :rtype: tuple
    
    Esempio:
        try:
            1 / 0
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(exc_type)  # <class 'ZeroDivisionError'>
    """
    pass


def cycle_time_ms(period: int) -> int:
    """Helper per cicli a tempo di ciclo fisso per applicazioni di controllo in tempo reale.
    
    Questa funzione garantisce che un ciclo di controllo venga eseguito con un tempo di ciclo fisso e preciso,
    compensando i tempi di esecuzione variabili del corpo del ciclo. Mantiene il timing
    ritardando secondo necessità per raggiungere il periodo target.
    
    Schema di utilizzo:
    1. Chiamare con valore negativo (es., -1) per resettare/inizializzare il timer di ciclo
    2. Chiamare con il periodo desiderato (ms) alla fine di ogni iterazione del ciclo
    
    La funzione calcola il tempo rimanente fino a quando il prossimo ciclo dovrebbe iniziare e ritarda
    di conseguenza. Se il corpo del ciclo impiega più tempo del periodo, la funzione ritorna
    immediatamente (nessun ritardo) e il valore di ritorno sarà negativo o zero.
    
    :param period: Tempo di ciclo target in millisecondi. Usare valore negativo per resettare il timer.
    :type period: int
    :return: Tempo rimanente in millisecondi prima del completamento del ciclo. Negativo se in eccesso.
    :rtype: int
    
    Esempio:
        import sys
        
        # Inizializzare il timer di ciclo
        sys.cycle_time_ms(-1)
        
        while True:
            # Eseguire compiti di controllo (tempo di esecuzione variabile)
            read_sensors()
            calculate_control()
            update_outputs()
            
            # Assicurare tempo di ciclo fisso di 10ms
            remaining = sys.cycle_time_ms(10)
            if remaining < 0:
                print("Avviso: Superamento ciclo di", -remaining, "ms")
    
    Nota:
        Per cicli di controllo in tempo reale ad alta precisione dove il timing coerente è critico.
        Il tempo di ciclo effettivo può avere piccole variazioni dovute alla pianificazione del sistema.
    """
    pass

def time() -> int:
    """Ottenere il tempo di sistema corrente in millisecondi.
    
    Restituisce il valore del contatore in millisecondi. Questa è una funzione di compatibilità per
    i vecchi azionamenti CANopen MovingCap con pymite/Python-On-A-Chip.
    
    **Deprecato:** Usare `time.ticks_ms()` dal modulo `time` per nuove applicazioni.
    
    :return: Tempo corrente in millisecondi dall'avvio del sistema. (Micropython small int, intero con segno a 30 bit nell'implementazione attuale).
    :rtype: int
    
    Esempio:
        start = sys.time()
        # ... fare qualcosa ...
        elapsed = sys.time() - start
        print(f"L'operazione ha richiesto {elapsed} ms")
    
    Vedere anche:
        time.ticks_ms() - Funzione preferita per nuovo codice
    """
    pass

def wait(ms: int):
    """Attendere i millisecondi specificati.
    
    Ritarda l'esecuzione per il numero dato di millisecondi. Questa è una funzione di compatibilità
    per i vecchi azionamenti CANopen MovingCap con pymite/Python-On-A-Chip.
    
    **Deprecato:** Usare `time.sleep_ms()` dal modulo `time` per nuove applicazioni.
    
    :param ms: Numero di millisecondi da attendere.
    :type ms: int
    
    Esempio:
        sys.wait(100)  # Attendere 100 millisecondi
    
    Vedere anche:
        time.sleep_ms() - Funzione preferita per nuovo codice
    """
    pass
