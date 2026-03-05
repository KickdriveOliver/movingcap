"""Stub/interface du module time/utime pour les variateurs servo MovingCap fullmo / CODE / Micropython

Le module `utime` (alternativement : `time`) fournit un sous-ensemble du module `time` de MicroPython ou CPython.

Il s'agit d'une implémentation limitée pour la plateforme MovingCap qui fournit des fonctions de temporisation et de délai.
La fonctionnalité complète de date/heure (localtime, mktime, time) n'est pas prise en charge sur MovingCap.

Pour la documentation complète du module time standard de MicroPython, voir :
https://docs.micropython.org/en/v1.9.4/pyboard/library/utime.html

Fonctions disponibles :
    - sleep(seconds) - Dormir pendant le nombre de secondes spécifié
    - sleep_ms(ms) - Dormir pendant le nombre de millisecondes spécifié
    - sleep_us(us) - Dormir pendant le nombre de microsecondes spécifié
    - ticks_ms() - Obtenir la valeur du compteur de millisecondes
    - ticks_us() - Obtenir la valeur du compteur de microsecondes
    - ticks_add(ticks, delta) - Ajouter delta à une valeur de ticks
    - ticks_diff(ticks1, ticks2) - Calculer la différence entre les valeurs de ticks

Non disponible sur MovingCap :
    - localtime() - Non pris en charge (pas de RTC)
    - mktime() - Non pris en charge (pas de RTC)
    - time() - Non pris en charge (pas de RTC)
    - ticks_cpu() - Non pris en charge

Fonctions Ticks - Notes Importantes :
    Les fonctions ticks_ms() et ticks_us() retournent des valeurs dans une plage définie
    par l'implémentation. Sur la plateforme MovingCap CODE actuelle, les valeurs bouclent
    dans une plage positive plus petite que la plage entière 32 bits complète.
    
    NE faites PAS d'hypothèses sur la plage de valeurs spécifique et n'effectuez pas
    d'opérations arithmétiques directes sur les valeurs de ticks. La plage peut changer
    dans les implémentations futures.
    
    Utilisez TOUJOURS ces fonctions d'aide pour l'arithmétique des ticks :
        - ticks_diff(ticks1, ticks2) - Calculer la différence entre deux valeurs de ticks
        - ticks_add(ticks, delta) - Ajouter/soustraire un décalage à une valeur de ticks
    
    Ces fonctions gèrent correctement le bouclage quelle que soit la plage de valeurs sous-jacente.

Notes d'utilisation :
    - Utiliser ce module pour les délais, les mesures de temps et les implémentations de temporisation
    - Pour une temporisation précise, préférer ticks_us() à ticks_ms()

Exemple d'utilisation :
    import time  # ou : import utime
    
    # Délais simples
    time.sleep(1)  # Dormir 1 seconde
    time.sleep_ms(100)  # Dormir 100 millisecondes
    time.sleep_us(50)  # Dormir 50 microsecondes
    
    # Mesure de temps
    start = time.ticks_ms()
    # ... faire quelque chose ...
    elapsed = time.ticks_diff(time.ticks_ms(), start)
    print("Écoulé :", elapsed, "ms")
    
    # Implémentation de temporisation
    timeout = 5000  # Temporisation de 5 secondes
    start = time.ticks_ms()
    condition = True
    while condition:
        if time.ticks_diff(time.ticks_ms(), start) > timeout:
            print("Temporisation !")
            break
        # ... faire du travail ...
"""
__author__ =  "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.10.xx"
__date__ = "2026-01-19"

def sleep(seconds: int):
    """Dormir pendant le nombre de secondes spécifié.
    
    Suspend l'exécution pendant au moins le nombre de secondes donné.
    Le temps de sommeil réel peut être plus long en raison de la planification du système.

    REMARQUE : MovingCap MicroPython ne prend actuellement pas en charge les flottants. "seconds" ne peut pas être un nombre fractionnaire.
    
    :param seconds: Nombre de secondes à dormir.
    :type seconds: int
    
    Exemple :
        time.sleep(2)  # Dormir pendant 2 secondes
        time.sleep(1)  # Dormir pendant 1 seconde
    """
    pass

def sleep_ms(ms: int):
    """Dormir pendant le nombre de millisecondes spécifié.
    
    Suspend l'exécution pendant au moins le nombre de millisecondes donné.
    Plus précis que sleep() pour les courts délais.
    
    :param ms: Nombre de millisecondes à dormir.
    :type ms: int
    
    Exemple :
        time.sleep_ms(500)  # Dormir pendant 500 millisecondes
        time.sleep_ms(10)   # Dormir pendant 10 millisecondes
    """
    pass

def sleep_us(us: int):
    """Dormir pendant le nombre de microsecondes spécifié.
    
    Suspend l'exécution pendant au moins le nombre de microsecondes donné.
    Fonction de délai la plus précise disponible. Pour les très courts délais, utiliser avec prudence
    car la surcharge système peut affecter la précision.
    
    :param us: Nombre de microsecondes à dormir.
    :type us: int
    
    Exemple :
        time.sleep_us(1000)  # Dormir pendant 1000 microsecondes (1 ms)
        time.sleep_us(50)    # Dormir pendant 50 microsecondes
    """
    pass

def ticks_ms() -> int:
    """Obtenir la valeur actuelle du compteur de millisecondes.
    
    Retourne un compteur de millisecondes croissant de façon monotone avec un point de référence arbitraire.
    Le compteur boucle après avoir atteint une valeur maximale définie par l'implémentation.
    
    La plage de valeurs spécifique dépend de l'implémentation et peut changer dans les versions futures.
    Ne vous fiez JAMAIS à une plage particulière et n'effectuez pas d'arithmétique directe sur les valeurs de ticks.
    
    Utilisez TOUJOURS ticks_diff() pour calculer les différences de temps et ticks_add() pour
    décaler les valeurs de ticks - ces fonctions gèrent correctement le bouclage.
    
    :return: Comptage de ticks en millisecondes actuel (plage définie par l'implémentation).
    :rtype: int
    
    Exemple :
        start = time.ticks_ms()
        # ... faire quelque chose ...
        duration = time.ticks_diff(time.ticks_ms(), start)  # CORRECT
        # duration = time.ticks_ms() - start  # INCORRECT - ne pas utiliser !
    """
    pass

def ticks_us() -> int:
    """Obtenir la valeur actuelle du compteur de microsecondes.
    
    Retourne un compteur de microsecondes croissant de façon monotone avec un point de référence arbitraire.
    Le compteur boucle après avoir atteint une valeur maximale définie par l'implémentation.
    Fournit une résolution plus élevée que ticks_ms() pour une temporisation précise.
    
    La plage de valeurs spécifique dépend de l'implémentation et peut changer dans les versions futures.
    Ne vous fiez JAMAIS à une plage particulière et n'effectuez pas d'arithmétique directe sur les valeurs de ticks.
    
    Utilisez TOUJOURS ticks_diff() pour calculer les différences de temps et ticks_add() pour
    décaler les valeurs de ticks - ces fonctions gèrent correctement le bouclage.
    
    :return: Comptage de ticks en microsecondes actuel (plage définie par l'implémentation).
    :rtype: int
    
    Exemple :
        start = time.ticks_us()
        # ... opération précise ...
        duration_us = time.ticks_diff(time.ticks_us(), start)  # CORRECT
    """
    pass

def ticks_add(ticks: int, delta: int) -> int:
    """Ajouter un delta à une valeur de ticks avec gestion correcte du bouclage.
    
    C'est la méthode correcte pour ajouter ou soustraire d'une valeur de ticks.
    Effectue une addition tout en gérant correctement le bouclage du compteur.
    
    :param ticks: Valeur de ticks de base (de ticks_ms() ou ticks_us()).
    :type ticks: int
    :param delta: Valeur à ajouter (positive) ou soustraire (négative).
    :type delta: int
    :return: Nouvelle valeur de ticks avec gestion correcte du bouclage.
    :rtype: int
    
    Exemple :
        # Calculer une échéance dans 5 secondes
        deadline = time.ticks_add(time.ticks_ms(), 5000)
        
        # Vérifier si l'échéance est passée
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            # Encore avant l'échéance
            pass
    """
    pass

def ticks_diff(ticks1: int, ticks2: int) -> int:
    """Calculer la différence signée entre deux valeurs de ticks.
    
    C'est la méthode correcte pour comparer ou trouver la différence entre les valeurs de ticks.
    Calcule (ticks1 - ticks2) avec gestion appropriée du bouclage du compteur.
    
    Le résultat est un entier signé :
        - Positif si ticks1 est "après" ticks2
        - Négatif si ticks1 est "avant" ticks2
        - Zéro s'ils sont égaux
    
    Le résultat est valide tant que la différence de temps réelle ne dépasse pas la moitié
    de la période des ticks (environ 149 heures pour ticks_ms dans l'implémentation actuelle).
    
    :param ticks1: Première valeur de ticks, typiquement le temps "ultérieur" ou "final".
    :type ticks1: int
    :param ticks2: Deuxième valeur de ticks, typiquement le temps "antérieur" ou "initial".
    :type ticks2: int
    :return: Différence signée (ticks1 - ticks2).
    :rtype: int
    
    Exemple :
        # Mesurer le temps écoulé
        start = time.ticks_ms()
        # ... opération ...
        elapsed = time.ticks_diff(time.ticks_ms(), start)
        
        # Temporisation basée sur échéance
        deadline = time.ticks_add(time.ticks_ms(), 1000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            pass  # Attendre jusqu'à l'échéance
        
        # Vérifier si la temporisation est dépassée
        if time.ticks_diff(time.ticks_ms(), start) > 1000:
            print("Plus d'1 seconde écoulée")
    """
    pass