"""Stub/interface du module sys pour les variateurs servo MovingCap fullmo / CODE / Micropython

Le module `sys` fournit des paramètres et fonctions spécifiques au système pour MovingCap MicroPython.

Ce module comprend :
- Fonctions du module sys standard MicroPython/CPython (sous-ensemble de v1.9.4)
- Extensions spécifiques MovingCap pour applications de contrôle en temps réel
- Fonctions de compatibilité pour les variateurs CANopen MovingCap hérités avec pymite/Python-On-A-Chip

Fonctions Standard :
    - version - Chaîne de version Python
    - version_info - Tuple de version Python (major, minor, patch)
    - implementation - Détails d'implémentation (name, version, platform, platver)
    - platform - Chaîne d'identification de plateforme
    - byteorder - Ordre des octets natif ('little' ou 'big')
    - exit([retval]) - Quitter le programme
    - print_exception(exc, [file]) - Afficher la trace de l'exception
    - exc_info() - Obtenir les informations sur l'exception actuelle sous forme de tuple

Extensions MovingCap :
    - cycle_time_ms(period) - Aide pour boucles à temps de cycle fixe
    - time() - Compatibilité : Obtenir le minuteur en millisecondes (utilisez time.ticks_ms() dans nouveau code)
    - wait(ms) - Compatibilité : Délai en millisecondes (utilisez time.sleep_ms() dans nouveau code)

Pour la documentation complète du module sys de MicroPython, voir :
https://docs.micropython.org/en/v1.9.4/pyboard/library/sys.html

Exemple d'Utilisation :
  import sys
  import time

  def do_control_task():
      dummy = 2000
      for runs in range((time.ticks_ms() % 100) + 10):
          dummy = dummy - 20
          dummy2 = dummy + 10

  # Vérifier la version Python
  print("sys.version (python) = %s" % sys.version)
  # Vérifier les détails d'implémentation
  print("sys.implementation = %s" % repr(sys.implementation))

  # Boucle de contrôle à temps de cycle fixe
  sys.cycle_time_ms(0)  # Réinitialiser le minuteur de cycle
  for cycle in range(20):
      # Effectuer les opérations de contrôle
      do_control_task()
      remaining = sys.cycle_time_ms(10)  # Assurer un temps de cycle de 10ms
      print ("Cycle de 10 msec, tour = %d, temps restant = %d" % (cycle, remaining)) 

  # Gestion des exceptions
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

# Attributs du module
version: str
"""Chaîne de version du langage Python (p.ex., "3.4.0")."""

version_info: tuple
"""Version du langage Python sous forme de tuple (major, minor, patch)."""

class _Implementation:
    """Objet d'information sur l'implémentation."""
    name: str
    """Nom de l'implémentation ("micropython")."""
    version: tuple
    """Tuple de version MicroPython (major, minor, micro)."""
    platform: str
    """Nom de la plateforme ("movingcap")."""
    platver: tuple
    """Tuple de version MovingCap (dev_type, major, minor, revision)."""

implementation: _Implementation
"""Détails d'implémentation incluant les versions MicroPython et MovingCap."""

platform: str
"""Chaîne d'identification de plateforme."""

byteorder: str
"""Ordre des octets natif : 'little' ou 'big'."""

stdin: object
"""Flux d'entrée standard."""

stdout: object
"""Flux de sortie standard."""

stderr: object
"""Flux d'erreur standard."""

def exit(retval: int = 0):
    """Quitter le programme en levant une exception SystemExit.
    
    :param retval: Code de sortie (0 pour succès, non-zéro pour erreur). Par défaut 0.
    :type retval: int
    :raises SystemExit: Toujours levée pour terminer le programme.
    
    Exemple :
        if error_condition:
            sys.exit(1)  # Quitter avec code d'erreur 1
    """
    pass

def print_exception(exc, file=None):
    """Afficher la trace de l'exception dans un fichier ou stdout.
    
    Affiche le type d'exception, le message et la trace dans un format lisible.
    Si aucun fichier n'est spécifié, affiche sur stdout.
    
    :param exc: Objet exception à afficher.
    :type exc: Exception
    :param file: Flux de fichier optionnel où écrire. Si None, utilise stdout.
    :type file: objet de type fichier ou None
    
    Exemple :
        try:
            risky_operation()
        except Exception as e:
            sys.print_exception(e)
            # ou écrire dans un fichier :
            # with open('error.log', 'w') as f:
            #     sys.print_exception(e, f)
    """
    pass

def exc_info() -> tuple:
    """Obtenir des informations sur l'exception actuelle.
    
    Renvoie un tuple contenant (type, valeur, trace) de l'exception actuelle.
    Si aucune exception n'est en cours de traitement, renvoie (None, None, None).
    
    :return: Tuple de (exception_type, exception_value, traceback).
    :rtype: tuple
    
    Exemple :
        try:
            1 / 0
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(exc_type)  # <class 'ZeroDivisionError'>
    """
    pass


def cycle_time_ms(period: int) -> int:
    """Aide pour boucles à temps de cycle fixe pour applications de contrôle en temps réel.
    
    Cette fonction garantit qu'une boucle de contrôle s'exécute avec un temps de cycle fixe et précis,
    compensant les temps d'exécution variables du corps de la boucle. Elle maintient le timing
    en retardant selon les besoins pour atteindre la période cible.
    
    Modèle d'utilisation :
    1. Appeler avec valeur négative (p.ex., -1) pour réinitialiser/initialiser le minuteur de cycle
    2. Appeler avec la période souhaitée (ms) à la fin de chaque itération de boucle
    
    La fonction calcule le temps restant jusqu'à ce que le prochain cycle devrait commencer et retarde
    en conséquence. Si le corps de la boucle prend plus longtemps que la période, la fonction retourne
    immédiatement (pas de retard) et la valeur de retour sera négative ou nulle.
    
    :param period: Temps de cycle cible en millisecondes. Utiliser valeur négative pour réinitialiser le minuteur.
    :type period: int
    :return: Temps restant en millisecondes avant la fin du cycle. Négatif en cas de dépassement.
    :rtype: int
    
    Exemple :
        import sys
        
        # Initialiser le minuteur de cycle
        sys.cycle_time_ms(-1)
        
        while True:
            # Effectuer les tâches de contrôle (temps d'exécution variable)
            read_sensors()
            calculate_control()
            update_outputs()
            
            # Assurer un temps de cycle fixe de 10ms
            remaining = sys.cycle_time_ms(10)
            if remaining < 0:
                print("Avertissement : Dépassement de cycle de", -remaining, "ms")
    
    Note :
        Pour les boucles de contrôle en temps réel de haute précision où le timing cohérent est critique.
        Le temps de cycle réel peut présenter de petites variations dues à la planification du système.
    """
    pass

def time() -> int:
    """Obtenir l'heure système actuelle en millisecondes.
    
    Renvoie la valeur du compteur en millisecondes. C'est une fonction de compatibilité pour
    les variateurs CANopen MovingCap hérités avec pymite/Python-On-A-Chip.
    
    **Obsolète :** Utilisez `time.ticks_ms()` du module `time` pour les nouvelles applications.
    
    :return: Temps actuel en millisecondes depuis le démarrage du système. (Micropython small int, entier signé sur 30 bits dans l'implémentation actuelle).
    :rtype: int
    
    Exemple :
        start = sys.time()
        # ... faire quelque chose ...
        elapsed = sys.time() - start
        print(f"L'opération a pris {elapsed} ms")
    
    Voir aussi :
        time.ticks_ms() - Fonction préférée pour nouveau code
    """
    pass

def wait(ms: int):
    """Attendre les millisecondes spécifiées.
    
    Retarde l'exécution pendant le nombre donné de millisecondes. C'est une fonction de compatibilité
    pour les variateurs CANopen MovingCap hérités avec pymite/Python-On-A-Chip.
    
    **Obsolète :** Utilisez `time.sleep_ms()` du module `time` pour les nouvelles applications.
    
    :param ms: Nombre de millisecondes à attendre.
    :type ms: int
    
    Exemple :
        sys.wait(100)  # Attendre 100 millisecondes
    
    Voir aussi :
        time.sleep_ms() - Fonction préférée pour nouveau code
    """
    pass
