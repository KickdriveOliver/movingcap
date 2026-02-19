"""Module mcdrive stub/interface pour les servovariateurs fullmo MovingCap / CODE / Micropython

Le module/bibliothèque Python mcdrive permet d'accéder aux fonctions du servovariateur MovingCap et
au dictionnaire d'objets CiA402.

* WriteObject et ReadObject fournissent un accès général à tous les objets disponibles du
dictionnaire de variateur MovingCap. Si vous êtes familier avec les objets standard CiA 402 / CANopen / CoE EtherCAT
et les objets spécifiques au fabricant documentés dans le manuel utilisateur MovingCap, c'est
tout ce dont vous avez besoin pour écrire une application maître complète du variateur.

* Des fonctions supplémentaires sont fournies comme raccourci et moyen plus rapide d'écrire vos applications.
Elles effectuent essentiellement plusieurs opérations d'écriture/lecture sur les objets CiA 402 pour obtenir le même
résultat.

Veuillez vous référer à nos exemples pour voir comment faire bouger votre moteur avec seulement quelques lignes de code.
"""
__author__ =  "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.10.xx"
__date__ = "2025-11-04"

def WriteObject(index : int, subindex : int, value : int) -> int:
    """Écrire valeur d'objet CANopen (numérique uniquement)

    :param index: Index CANopen [unsigned16], ex. 0x607A pour "position cible"
    :type index: int
    :param subindex: Sous-index CANopen [unsigned8], ex. 0
    :type subindex: int
    :param value: Nouvelle valeur pour cet objet [integer32]
    :type value: int
    :return: 0 si réussi, ou le code d'erreur interne de la pile CANopen.
        Vous pouvez généralement ignorer cette valeur. Vérifiez uniquement lorsque vous n'êtes pas sûr
        si l'index/sous-index est un objet valide pour l'accès en écriture.
    :rtype: int
    """
    ret =  0
    return ret

def ReadObject(index : int, subindex : int) -> int:
    """Lire valeur d'objet CANopen (numérique uniquement)

    :param index: Index CANopen [unsigned16], ex. 0x6064 pour "valeur position réelle"
    :type index: int
    :param subindex: Sous-index CANopen [unsigned8], ex. 0
    :type subindex: int
    :return: Valeur d'objet actuelle [integer32]. Si l'objet n'est pas un objet valide pour l'accès en lecture,
        une valeur d'erreur interne de la pile CANopen est retournée. Notez que la valeur de retour est toujours integer32,
        même si l'entrée du dictionnaire d'objets a un type de données CANopen différent.
    :rtype: int
    """
    value = 0
    return value

def WriteControl(control : int):
    """Écrire le mot de contrôle CiA 402 (objet CANopen 6040h.0h)

    :param control: Nouvelle valeur [unsigned16]
    :type control: int
    """
    pass


def EnableDrive():
    """Préparer pour le fonctionnement.
    
    Cette fonction bascule à travers les états requis de la machine d'état CiA 402,
    jusqu'à ce que "operation enabled" soit atteint.
    
    Ceci est équivalent à vérifier le mot d'état du variateur
    via `ReadStatusword` et commander les changements d'état requis en utilisant 
    `WriteControl`. La séquence est :

    * Si le variateur est en état d'erreur : WriteControl(0x80) réinitialisation défaut -> nouvel état "switch on disabled"
    * WriteControl(0x6) shutdown -> nouvel état "ready to switch on"
    * WriteControl(0x7) switch on -> nouvel état "switched on"
    * WriteControl(0xf) enable operation -> nouvel état "operation enabled"
    
    Seules les transitions requises sont effectuées. Si le variateur est déjà en état "operation enabled"
    (ReadStatusword est 0x27), la fonction retourne immédiatement.

    Voir aussi `PowerQuit`

    :return: 1 si le passage à "operation enabled" réussit. 0 si échec.
    :rtype: int
    """
    value = 0
    return value

def StopMotion():
    """Entre dans l'état 'Quick Stop',
    après avoir défini le paramètre 605Ah.0h Quick stop option code = 6 : "Ralentir sur rampe quick stop et rester en quick stop actif".
    Utilise l'objet 6085h.0h Quick Stop deceleration value.
    
    Voir aussi `ContinueMotion` pour reprendre le fonctionnement après un Quick Stop.
    """
    pass

def ContinueMotion():
    """Reprendre le mouvement.
    
    Cette fonction continue le mouvement après être entré dans un état Quick Stop (par ex. en utilisant `StopMotion`).
    """
    pass

def PowerQuit():
    """Réinitialise le mode de fonctionnement à zéro (voir `SetOpMode`),
    puis bascule la machine d'état CiA 402 vers "switch on disabled".

    Cela éteint en toute sécurité le variateur tout en maintenant la connexion.
    
    Voir aussi `EnableDrive`
    """
    pass

def StorePermanent():
    """Stocker les paramètres actuels en mémoire non volatile.
    
    Enregistre la configuration actuelle du variateur (paramètres) dans EEPROM/Flash afin qu'ils
    persistent après le cycle d'alimentation. Cela inclut les paramètres de mouvement, les paramètres E/S,
    et d'autres valeurs de configuration qui ont été modifiées par rapport aux valeurs par défaut.
    
    Note : L'utilisation excessive de cette fonction peut user la mémoire non volatile.
    N'appelez que lorsque nécessaire pour sauvegarder les modifications de configuration.

    Note : Bien qu'il soit possible d'appeler StorePermanent() au milieu d'un mouvement, vous pouvez subir des
    glitches/saccades mineurs dans les mouvements de trajectoire à haute vitesse car l'accès EEPROM nécessite le gel
    d'autres tâches pendant un court laps de temps.
    """
    pass

def GoPosAbs(targetPos : int):
    """Démarrer un nouveau mouvement vers une position absolue.

    * Si nécessaire, basculer vers le mode de fonctionnement 1 - mode de positionnement profil (SetOpMode(1))
    * Définir la nouvelle cible (voir `SetTargetPos`)
    * Démarrer le positionnement en utilisant le mode CiA 402 "single setpoint" : la nouvelle position cible est traitée immédiatement.

    Le contrôle de positionnement utilise "6083h.0h profile acceleration" (`SetAcc`) et
    "6084h.0h profile deceleration" (`SetDec`) pour le mouvement.

    Utilisez `ChkReady` et `ChkError` pour attendre la fin du positionnement et détecter les erreurs pendant l'exécution.

    Voir aussi 'GoPosRel'

    :param targetPos: Nouvelle position cible absolue [integer32]
    :type targetPos: int
    """
    pass

def GoPosRel(relativePos : int):
    """Démarrer un nouveau mouvement vers une position relative.

    Identique à `GoPosAbs`, mais spécifiez une position relative.

    Par défaut "relative" signifie "relative à la position cible précédente utilisée",
    mais l'objet "60F2h.0h positioning option code" peut spécifier une signification différente,
    par ex. "relative à la position réelle actuelle".

    :param relativePos: Nouvelle position cible relative [integer32]
    :type relativePos: int
    """
    pass

def GoVel(targetVelocity : int):
    """Démarrer un nouveau fonctionnement à vitesse constante.

    * Si nécessaire, basculer vers le mode de fonctionnement 3 - mode de vitesse profil (SetOpMode(3))
    * Définir la nouvelle vitesse cible et 
    
    Les changements de vitesse sont appliqués en utilisant l'objet "6083h.0h profile acceleration" (voir `SetAcc`).
    Si la direction est changée (par ex. de vitesse positive à négative), l'objet
    "6085h.0h quickstop deceleration" est utilisé jusqu'à ce que la vitesse soit zéro,
    puis 6083h.0h est appliqué pour accélérer dans la direction opposée.
    
    Le paramètre de décélération n'a aucune influence.

    :param targetVelocity: Nouvelle vitesse cible [integer32]
    :type targetVelocity: int
    """
    pass

def SetTargetPos(targetPos : int):
    """Raccourci pour écrire l'objet "607Ah.0h target position"

    :param targetPos: Nouvelle position cible [integer32]
    :type targetPos: int
    """
    pass

def SetPosVel(profileVelocity : int):
    """Raccourci pour écrire l'objet "6081h.0h profile velocity"

    :param profileVelocity: Nouvelle vitesse de profil [unsigned32]
    :type profileVelocity: int
    """
    pass

def SetAcc(profileAcceleration : int):
    """Raccourci pour écrire l'objet "6083h.0h profile acceleration"

    :param profileAcceleration: Nouvelle accélération de profil [unsigned32]
    :type profileAcceleration: int
    """
    pass

def SetDec(profileDeceleration : int):
    """Raccourci pour écrire l'objet "6084h.0h profile deceleration"

    :param profileDeceleration: Nouvelle décélération de profil [unsigned32]
    :type profileDeceleration: int
    """
    pass

def GoHome(method : int, velocity : int, acceleration : int, offset : int):
    """Démarrer la course de référence/homing CiA 402

    * Basculer vers le mode de fonctionnement 6 - mode de vitesse profil (SetOpMode(3))
    * Définir les objets 6098h.0h homing method, 6099h.1h homing speed, 609Ah.0h homing acceleration et 607Ch.0h homing offset
    * Démarrer le mouvement
    
    Valeurs `method` courantes pour MovingCap sont :
    * 37 ou 35 = ne pas bouger. Définir la position réelle actuelle comme nouvelle position zéro.
    * -18 = course de référence bloc en direction positive
    * -19 = course de référence bloc en direction négative
    
    Utilisez `ChkReady` et `ChkError` pour attendre la fin de la course de homing et détecter les erreurs pendant l'exécution.

    :param method: Méthode de homing CiA 402 [unsigned8]
    :type method: int
    :param velocity: Vitesse de homing [unsigned32]
    :type velocity: int
    :param acceleration: Accélération de homing [unsigned32]
    :type acceleration: int
    :param offset: Position d'offset de homing [integer32]. Après une opération de homing réussie, faire de cette valeur
        de position la nouvelle position réelle.
    :type offset: int
    """
    pass

def SetOpMode(opMode: int):
    """Raccourci pour écrire l'objet "6060h.0h modes of operation"

    :param opMode: Nouveau mode de fonctionnement [unsigned8] : 0 - pas de mode. 1 - mode de position profil. 3 - mode de vitesse profil. 6 - mode homing.
    :type opMode: int
    """
    pass

def GetOpMode() -> int:
    """Raccourci pour lire l'objet "6060h.0h modes of operation"

    :return: Mode de fonctionnement [unsigned8], voir `SetOpMode`
    :rtype: int
    """
    opMode = 0
    return opMode

def SetTorque(torque : int):
    """Raccourci pour écrire l'objet "6073h.0h max current"

    :param torque: Nouvelle valeur de courant max. [unsigned16], qui est directement en relation avec le couple maximum pendant le fonctionnement.
        L'unité de valeur est 0,1%, c'est-à-dire torque = 100 signifie "10% couple" et torque = 1000 signifie "100% couple" (par défaut).
    :type torque: int
    """
    pass

def ChkIn(inNo : int) -> int:
    """Vérifier l'entrée numérique

    :param inNo: N° d'entrée de 1..10 (selon le modèle MovingCap)
    :type inNo: int
    :return: 0 si bas. 1 si haut (actif)
    :rtype: int
    """
    pass

def SetOut(outNo : int):
    """Activer la sortie numérique

    :param outNo: N° de sortie de 1..4 (selon le modèle MovingCap)
    :type outNo: int
    """
    pass

def ClearOut(outNo : int):
    """Désactiver la sortie numérique

    :param outNo: N° de sortie de 1..4 (selon le modèle MovingCap)
    :type outNo: int
    """
    pass

def GetActualPos() -> int:
    """Raccourci pour lire l'objet "6064h.0h position actual value"

    :return: position actuelle [integer32]
    :rtype: int
    """
    actualPos = 0
    return actualPos

def ReadStatusword() -> int:
    """Raccourci pour lire l'objet "6041h.0h statusword"

    :return: valeur du mot d'état CiA 402 [unsigned16]
    :rtype: int
    """
    statusWord = 0
    return statusWord


def ChkReady() -> int:
    """Vérifier si le variateur a terminé le mouvement en cours (bit "target reached" du mot d'état activé), 
    ou si une erreur s'est produite (bit "error" activé).

    Utiliser après un nouvel appel `GoPosAbs`, `GoPosRel` ou `GoHome`. 

    :return: 1 si prêt. 0 si pas encore prêt.
    :rtype: int
    """
    isReady = 0
    return isReady

def ChkEnabled() -> int:
    """Vérifier si le variateur est dans l'état "operation enabled".
    
    Vérifie le mot d'état CiA 402 pour déterminer si le variateur est prêt pour des commandes de mouvement.
    Retourne la même valeur que `ChkReady` - vérifie à la fois l'atteinte de la cible et l'état activé.
    
    :return: 1 si activé et prêt. 0 si non activé ou pas prêt.
    :rtype: int
    """
    isEnabled = 0
    return isEnabled

def ChkMoving() -> int:
    """Vérifier si le variateur exécute actuellement un mouvement.
    
    Surveille l'état du variateur pour déterminer si un mouvement est en cours.
    Utile pour détecter si le variateur est en mouvement ou à l'arrêt.
    
    :return: 1 si en mouvement. 0 si à l'arrêt.
    :rtype: int
    """
    isMoving = 0
    return isMoving

def ChkError() -> int:
    """Vérifier si le bit "error" du mot d'état est activé.

    :return: 1 si erreur. 0 si pas d'erreur.
    :rtype: int
    """   
    isError = 0
    return isError

def ChkMfrStatus(bitIndex : int) -> int:
    """Vérifier un bit spécifique du registre d'état fabricant objet 1002h.0h.

    Bits d'erreur disponibles MovingCap Ethernet :
    0 Erreur surtension (Uzk)
    1 Erreur sous-tension (Uzk)
    2 Erreur Ack
    3 Erreur surchauffe
    4 Erreur I2T / Réduction de puissance
    5 Interruption connexion
    6 Erreur course
    7 Erreur communication
    8 Erreur capteur
    9 Erreur activation matérielle
    11 Erreur surintensité
    12 Erreur force / couple externe

    :param bitIndex: le numéro de bit de 0..15
    :type bitIndex: int
    :return: 1 si erreur. 0 si pas d'erreur.
    :rtype: int
    """
    isError = 0
    return isError

def SendEmcyMsg(errorNumber: int, errorRegister: int = 0, errorCode: int = 0x509b) -> None:
    """Envoyer un message d'urgence (EMCY).
    
    Cette fonction envoie un message d'urgence CANopen (EMCY) avec des informations d'erreur personnalisées.
    Les messages EMCY sont utilisés pour signaler des conditions d'erreur au maître du réseau ou aux systèmes de surveillance.
    
    La fonction prend en charge deux conventions d'appel pour la compatibilité ascendante :
    - Forme complète : SendEmcyMsg(errorNumber, errorRegister, errorCode)
    - Forme courte : SendEmcyMsg(errorNumber) - utilise errorRegister=0x00 et errorCode=0x509b par défaut
    
    :param errorNumber: Numéro d'erreur spécifique au fabricant [unsigned32]. 
        Il s'agit généralement d'un code d'erreur personnalisé défini par l'application.
    :type errorNumber: int
    :param errorRegister: Valeur du registre d'erreur CANopen [unsigned8], par défaut 0x00.
        Registre codé en bits selon la spéc. CANopen (erreur générique, courant, tension, température, etc.)
    :type errorRegister: int
    :param errorCode: Code d'erreur d'urgence CANopen [unsigned16], par défaut 0x509b.
        Code d'erreur standard ou spécifique au fabricant selon la spécification CANopen.
    :type errorCode: int
    
    Exemple :
        SendEmcyMsg(0x12345678)  # Forme simple
        SendEmcyMsg(0x12345678, 0x01, 0x5000)  # Forme complète avec tous les paramètres
    """
    pass
