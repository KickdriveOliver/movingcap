---
description: "MovingCap Support - Intelligente Kompakantriebe von 12V bis 72V mit EtherCAT, TCP/IP oder CANopen"
---
# Willkommen beim Fullmo MovingCap Service-Portal!

Hier finden Sie Informationen, technische Dokumentation, Software und Unterstützung zu [Fullmo](https://fullmo.de/) MovingCap - Intelligente Kompaktantriebe mit Web & Python für Industrie-, Agrar- und Spezialanwendungen. Motoren mit integrierter Steuerung für 12V DC, 24V DC, 48V DC, 72V DC oder kundenspezifische Versorgungsspannungen. Kommunikation über EtherCAT, CANopen, Ethernet TCP/IP oder digitale I/O. MovingCap ermöglichen schaltschranklose, kompakte und dezentrale 24V-Automatisierung für Produktionsmaschinen, Zuführsysteme, teil-automatisierte Arbeitsplätze und viele andere Einsatzgebiete. Überall, wo es um Drehen, Linearbewegung, Verstellen, präzises Positionieren oder kraftgesteuerten Andruck geht.

![Fullmo MovingCap Familie](images/logo.png){ align=right width=50% }
 
- MovingCap turnTRACK CanOPEN (MC349 CAN, MC563 CAN, MC632/634/636 CAN) 
- MovingCap turnTRACK Ethernet TCP/IP (MC349 ETH, MC632/634/636 ETH, MCN23 ETH) 
- MovingCap shortTRACK EtherCAT und TCP/IP (MCSHORT ETH, shortTRACK 046) 
- MovingCap flatTRACK EtherCAT und TCP/IP (MCFLAT ETH, flatTRACK 100-650, FATtrack 200)
- MovingCap pushTRACK Kurzhubzylinder, Ethernet und TCP/IP (pushTRACK 45S100 - 115S240)
- MovingCap maxTRACK MovingCap Kompaktantriebe in Verbindung mit präziser Zahnriemenachse, Ethernet TCP/IP und CANopen

Frisch aus der Industrieregion Bodensee - MovingCaps werden 
entwickelt und produziert in Deutschland bei der **[Fullmo GmbH](https://fullmo.de/)** in 88677 Markdorf.

## MovingCap Ethernet Antriebe - Handbücher

- [MovingCap Ethernet Softwarehandbuch (Web, de)](https://movingcap.de/webmanuals/mc-eth-sw-manual)
- [MovingCap Ethernet Softwarehandbuch (PDF, de)](https://movingcap.de/user/MovingCap-AnwenderDoku/2-MovingCap_ETH_Ethernet/MovingCap-ETH-Software-Manual-de.pdf)
- [MovingCap Ethernet Software Manual (PDF, en)](https://movingcap.de/user/MovingCap-AnwenderDoku/2-MovingCap_ETH_Ethernet/MovingCap-ETH-Software-Manual-en.pdf)

## Weitere Anwenderdokumentation und Beispiele
[PDF-Handbücher, Datenblätter, technische Dokumentation und Beispiele](MovingCap-AnwenderDoku.md)

## Downloads: Softwareupdates, XDD-Dateien und PC-Software
[Softwareupdates für Antriebe, XDD-Dateien (Electronic Data Sheet) und PC-Software](MovingCap-Software.md)

## Frag den Roboter
Mit dem **[MovingCap Support Bot](https://movingcap.de/bot/)** steht Ihnen ein externer docsbot-Assistent zur Verfügung, der mit den Dokumenten dieser Webseite trainiert wurde. Bitte beachten Sie die dort beschriebenen Nutzungsbedingungen.

## Fragen Sie uns 
Für erste Informationen und Beratung wenden Sie sich an **[unsere Mitarbeiter](https://fullmo.de/ueber-uns)**, z.B. unter **[info@drives.fullmo.de](mailto:info@drives.fullmo.de)**.

## Ihre MovingCap-Vorteile

MovingCaps kennen Ihre Absolutposition, können EtherCAT, TCP/IP Sockets, CANopen, CiA 402, und verstehen Ihre Anwendungskoordinaten. Sie machen flexible I/O gesteuerte Bewegungen möglich, und können über Webseite, [Python](https://micropython.org) und [Kickdrive](https://kickdrive.de) mit eigenen Abläufen programmiert werden. Ganz ohne Mastersteuerung. 

- **Schnelle Inbetriebnahme**: Die MovingCap-Antriebe sind so konzipiert, dass sie schnell und einfach in Betrieb genommen werden können. Über Weboberfläche und Inbetriebnahmesoftware können Sie die Antriebe ohne großen Aufwand testen, einstellen und einsetzen. Für typische Bewegungsabläufe wie "wenn Eingang 1 kommt, immer 180° vorwärts drehen" gibt es Beispielprojekte, die über [Kickdrive](https://kickdrive.de) in den Antrieb geladen werden können. 

- **Immer wissen, wo man steht**: MovingCaps verwenden Absolut-Längenmessysteme oder Multiturn-Positionsencoder, und sind so direkt nach dem Einschalten fahrbereit, ohne Referenzfahrt. Über die Webseite können Sie in wenigen Schritten Ihren MovingCap so einrichten, dass Sie alle Positionen in Anwendungskoordinaten vorgeben können (z.B. "Winkelposition des Drehtellers"). Getriebeübersetzungen werden berüchsichtigt, zusammen mit rotierenden Koordinaten gemäß DS402 und Endlos-Vorwärts/Rückwärts-Anwendungen mit Überlauf. 

- **Kommunikationsfreudig**: MovingCap-Antriebe bieten eine Vielzahl von Kommunikationsmöglichkeiten von EtherCAT, CANopen bis zu digitalen I/O-Signalen und TCP/IP Textprotokolle. Dies ermöglicht eine flexible Integration in verschiedene Steuerungssysteme und einfache Kommunikation mit anderen Geräten.

- **Servoantriebe nach CiA 402 und CiA 301**: MovingCap-Antriebe bieten die im Geräteprofil CiA 402 definierten Bewegungsarten, Einstellmöglichkeiten und Rückmeldungen. Unabhängig davon, ob Sie über EtherCAT, Ethernet TCP/IP Socket-Verbindungen, CAN-Bus, die Webseite oder digitale Ein/Ausgänge kommunizieren. MovingCaps ermöglichen so z.B. präzise Positionierungen bis in den Mikrometerbereich, den Antrieb von Transportbändern mit variablen Geschwindigkeiten, kraftbegrenzte Bewegungen, oder das Ausführen von Referenzfahrten.

- **Micropython eingebaut**: Eigenständige Fahrprogramme ohne SPS - MovingCap-Ethernet-Antriebe unterstützen [MicroPython](https://micropython.org) und bieten eine eigene drive-Bibliothek. Damit können Sie kleine Python-Programme direkt im Antrieb hinterlegen und ausführen, ohne übergeordnete klassische SPS. Dies ermöglicht kostengünstige, flexible und einfach kombinierbare Applikationen ohne teure Spezialisierung auf einen Feldbushersteller.