---
description: "Einführung in CANopen, CoE (CANopen over EtherCAT) und CiA 402"
---
# Einführung in CANopen, CoE (CANopen over EtherCAT) und CiA 402

2025-06-01 / www.kickdrive.de / www.fullmo.de

CANopen over EtherCAT (CoE) ist eine Software-Schnittstelle, die das CiA 402-Geräteprofil-Framework von CANopen in EtherCAT-Netzwerke integriert. Innerhalb von CoE spielt das CiA-402-Geräteprofil, definiert nach IEC 61800-7-201:2015, eine zentrale Rolle. CiA 402 definiert standarddisierte Nur-Lese oder Lese/Schreib-Parameterobjekte, zusammen mit einer CiA 402 Standard-Objektnummer (Index und Subindex). CiA 402 definiert Geräteverhalten sowie Standard-Betriebsmodi, die speziell für drehzahlveränderbare elektrische Antriebssysteme entwickelt wurden. 

CiA 301 definiert die Kommunikation zwischen Steuerungen (Master) und Geräten (Devices/Slaves) durch klar definierte Interaktionsmuster zum Konfigurieren, Steuern und Überwachen von Geräten auf Feld-Ebene. CANopen definiert unter anderem Kommunikationsparadigmen wie die Service Data Objects / SDO, bei dem der Controller aktiv Informationen an verbundene Geräte sendet ("SDO Download") oder von diesen anfordert ("SDO Upload"). 

## CANopen CiA 301 Übersicht des Kommunikationsprofils

### Einleitung
CiA 301 definiert die CANopen-Anwendungsschicht und das Kommunikationsprofil. Es legt Datentypen, Kodierungsregeln, das Objektverzeichnis (Object Dictionary) sowie alle Kommunikationsdienste und -protokolle fest – insbesondere NMT, SDO, PDO, SYNC, TIME und EMCY.

In typischen CANopen-Netzen steuert **NMT** das Hochfahren der Knoten, Zustandsübergänge und Fehlerüberwachung, während **SDO** einen Peer-to-Peer-Zugang zu Parametern im Objektverzeichnis bereitstellt.

### Network Management (NMT)

#### Controller–Device-Modell
Das CANopen-NMT folgt einem Controller–Device-Modell. Ein Knoten fungiert als **NMT-Controller**, bis zu 127 Knoten (Node-IDs 1–127) agieren als **NMT-Devices**. Durch das Senden unbestätigter NMT-Dienstnachrichten auf COB-ID 0x000 kann der Controller einzelne oder alle Devices initialisieren, starten, stoppen oder zurücksetzen.

### Node-Control-Dienste

Diese unbestätigten NMT-Dienste ermöglichen die direkte Steuerung der Geräte:

- **Start Remote Node:** `01h` → Gerät auf Operational setzen
- **Stop Remote Node:** `02h` → Gerät auf Stopped setzen
- **Enter Pre-operational:** `80h` → Gerät auf Pre-operational setzen
- **Reset Node:** `81h` → Anwendungs-Reset durchführen
- **Reset Communication:** `82h` → Kommunikations-Reset durchführen

#### Beispiele:
- `COB-ID=0h, Size=2, Data=81 00` → NMT Reset Node (alle Nodes)
- `COB-ID=0h, Size=2, Data=01 05` → NMT Start für Node-ID 5

#### Fehlerkontrolldienste
Es gibt zwei Fehlerüberwachungsmechanismen – **Node Guarding** und **Heartbeat** – von denen pro Device nur einer verwendet werden darf. 

Im **Node Guarding**-Modus muss das Device innerhalb eines vorgegebenen Timeouts auf den **Guarding Request** des Controllers antworten. 

Im **Heartbeat**-Modus sendet jedes Device periodisch einen Ein-Byte-Status (0 = Boot-up, 4 = Stopped, 5 = Operational, 127 = Pre-operational) über COB-ID 0x700 + Node-ID; der Controller überwacht Timeouts zur Fehlererkennung.

#### Boot-up-Dienst
Unmittelbar nach dem Unterzustand **Reset Communication** sendet ein Device eine Ein-Byte-**Boot-up**-Nachricht (0x00) auf **COB-ID 0x700 + Node-ID**, um seine Konfigurationsbereitschaft zu signalisieren.

#### NMT-Zustandsmaschine
Die NMT-Zustandsmaschine umfasst vier Hauptzustände mit drei Initialisierungs-Unterzuständen:

1. **Initialization** (automatisch nach Power-on, unterteilt in:  
   a. *Initializing* – Grundinitialisierung  
   b. *Reset Application* – Rücksetzen anwendungsbezogener Parameter  
   c. *Reset Communication* – Rücksetzen kommunikationsbezogener Parameter)  
2. **Pre-operational** – nur SDO-Zugriff, PDOs inaktiv  
3. **Operational** – alle Kommunikationsobjekte (PDO, SYNC, TIME, EMCY, SDO) aktiv  
4. **Stopped** – Kommunikation gestoppt, bis auf Fehlerkontrolle  


Übergänge erfolgen über NMT-Dienste, Hardware-Resets oder lokale Steuerung.

##### Zustands–Objekt-Beziehung
| NMT-Zustand     | PDO | SDO | SYNC | TIME | EMCY | Node-Control/Fehlerkontrolle |
|:---------------:|:---:|:---:|:----:|:----:|:----:|:---------------------------:|
| Pre-operational |     | ✓   | ✓   | ✓   | ✓   | ✓                         |
| Operational     | ✓   | ✓   | ✓   | ✓   | ✓   | ✓                         |
| Stopped         |     |     |     |     | ✓   | ✓                         |

Damit ist eine Parametrierung per SDO in **Pre-operational** möglich, während PDO‑Echtzeitübertragung erst in **Operational** stattfindet.

### Service Data Objects (SDO)

#### Client–Server-Modell
SDO implementiert ein bestätigtes Client–Server-Protokoll zum Zugriff auf beliebige Einträge im Objektverzeichnis. 

Für den Standard-SDO Kanal gilt: Client-Anfragen (i.d.R durch den Controller gesendet) erfolgen auf COB-ID 0x600 + NodeID; Server/Device-Antworten auf 0x580 + NodeID.

#### SDO-Dienste
SDO gliedert sich in:
1. **SDO Download** (Client→Server): Schreibzugriff  
   - **Initiate** (expedited): bis zu 4 Byte Daten in einem Frame  
   - **Segment**: Toggle-Bit-Protokoll für >4 Byte  
2. **SDO Upload** (Server→Client): Lesezugriff  
   - **Initiate** (expedited): liefert ≤4 Byte  
   - **Segment**: mehrteilige Übertragung für >4 Byte  
3. **SDO Abort Transfer**: Abbruch bei Fehler  
4. **(Optional) Block Download/Upload**: optimierte Blockübertragung mit CRC und Sequenznummern

Alle SDO-Dienste sind **bestätigt**; Antworten enthalten einen Return-Code für Erfolg oder Fehler.

#### Expedited vs. Segmented vs. Block
- **Expedited** (≤4 B): ein Frame, keine Segmentierung.  
- **Segmented** (>4 B): mehrere Frames à 7 Daten-Byte mit Toggle-Bit.  
- **Block** (optional): nummerierte Blöcke, Client bestätigt Blöcke, CRC möglich.

#### Protokolldetails
- **Download Initiate**: Client sendet `cs=0x20–0x23` in Byte 0, Index in Bytes 1–2, Sub-Index Byte 3, Daten in Bytes 4–7.  
- **Upload Initiate**: Client sendet `cs=0x40`, Server antwortet mit `cs=0x43` (expedited) oder `cs=0x41` (segmented) plus Länge.  
- **Segmente**: Client/Server verwenden `cs=0x00/0x01` für Download-Segmente; `cs=0x60/0x61` für Upload.  
- **Block**: `cs=0xA0…0xA4` für Block-Download; `cs=0xC0…0xC2` für Block-Upload.

### Zusammenfassung
Das Kommunikationsprofil CiA 301 gewährleistet, dass CANopen-Geräte standardisiert konfiguriert, überwacht und gesteuert werden können. **NMT** übernimmt den gesamten Gerätelebenszyklus – Boot-up, Parametrierung (via SDO in *Pre-operational*) und Echtzeitkommunikation (*Operational*). **SDO** bietet den flexiblen Client–Server-Zugriff auf beliebige Objektverzeichniseinträge, von Einzelparametern bis zu 4 Bytes Länge (expedited transfer) bis hin zu ganzen Datensätzen (segmented oder block transfer).

In Kombination mit PDO für zyklische Prozessdaten, SYNC für netzweite Synchronisation und EMCY für schnelle Fehleralarmierung bildet CiA 301 die Grundlage für interoperable, leistungsfähige Kommunikation in Automatisierungsnetzwerken.

## CiA 402 - Allgemeine Übersicht

### Einführung

CiA 402, alternativ auch als DS 402 / Device Standard 402 bezeichnet, ist ein Geräteprofil für Antriebe und Bewegungssteuerung, das von der CAN in Automation (CiA)-Organisation definiert wurde. Es spezifiziert ein universelles Interface und standardisiertes Verhalten zur Steuerung elektrischer Antriebe — wie Servoantriebe, Servorregler, Frequenzumrichter und ähnliche Geräte. Es ist als "CANopen Device Profile" Bestandteil des CANopen-Protokolls, findet jedoch auch in EtherCAT, POWERLINK- und anderen Applikationsprotokollen wie TCP/IP zum Einsatz. Das CiA 402 Geräteprofil ist in der Norm IEC61800-7-201 spezifiziert als Profil Typ 1 - CiA402 Drive Profile for power drive systems (PDS). 

Dieser Abschnitt bietet einen Überblick über die zentralen Aspekte von CiA 402, mit Fokus auf die Antriebszustände / "State Machine", das Haupt-**Controlword (6040h)** und **Statusword (6041h)**, gängige **Modes of Operation (6060h)** sowie eine Zusammenfassung weiterer wesentlicher Standardobjekte des Objektverzeichnisses / Object Dictionary.

### Die CiA 402 State Machine

Im Zentrum des CiA 402 Profils steht die **State Machine (PDS FSA, Power Drive System - Finite State Automat)**, welche die zulässigen Zustände und Übergänge eines Antriebs definiert. Die State Machine sorgt durch die Definition erlaubter Aktionen und erforderlicher Reaktionen in verschiedenen Betriebszuständen für eine sichere und vorhersehbare Steuerung von Bewegungsachsen.

#### Hauptzustände

- **Not Ready to Switch On**: Anfangszustand nach dem Einschalten. Der Antrieb ist nicht bereit, um Bewegungen auszuführen.
- **Switch On Disabled**: Antrieb darf nicht freigeschaltet werden (z.B. nach Fehler oder während Initialisierung).
- **Ready to Switch On**: Interne Prüfungen abgeschlossen; Antrieb kann freigeschaltet werden.
- **Switched On**: Antrieb ist bereit für Enable-Befehl.
- **Operation Enabled**: Der Antrieb kann Bewegungsbefehle ausführen.
- **Quick Stop Active**: Quick Stop ist aktiviert, der Antrieb stoppt so schnell wie möglich.
- **Fault Reaction Active**: Der Antrieb reagiert auf einen erkannten Fehler—er führt entsprechende Sicherheitsmaßnahmen durch.
- **Fault**: Ein Fehlerzustand wurde erkannt; der Antrieb muss zurückgesetzt werden.

#### Übergänge

Zustandsübergänge werden von Bits im **Controlword (6040h)** gesteuert, das vom Master an das Gerät gesendet wird. Der Antrieb meldet seinen aktuellen Zustand über das **Statusword (6041h)** zurück.

Ein vereinfachtes Diagramm:

![MovingCap CiA 402 State Machine](images/mc_cia402_web.svg)

Übersicht der Zustandsübergänge

|Nr. |Aktueller Zustand      | Nächster Zustand        |  Beschreibung                    | Steuerwort Bits (15...0)        | Statuswort nach Übergang (15...0)   |
|--|------------------------|-------------------------|--------------------------------------|---------------------------------|--------------------------------------|
|1| Not ready to switch on | Switch on disabled      | Automatisch nach Initialisierung     | xxxxxxxxxxxxxxxx (kein ext. Befehl)| xxxxxxxx x1xx0000                 |
|2| Switch on disabled     | Ready to switch on      | Shutdown                             | xxxxxxxxxx000110 (0x0006)       | xxxxxxxx x01x0001                   |
|3| Ready to switch on     | Switched on             | Switch On                            | xxxxxxxxxx000111 (0x0007)       | xxxxxxxx x01x0011                   |
|4| Switched on            | Operation enabled       | Enable Operation                     | xxxxxxxxxx001111 (0x000F)       | xxxxxxxx x01x0111                   |
|6| Switched on            | Ready to switch on      | Shutdown                             | xxxxxxxxxx000110 (0x0006)       | xxxxxxxx x01x0001                   |
|5| Operation enabled      | Switched on             | Disable Operation                    | xxxxxxxxxx000111 (0x0007)       | xxxxxxxx x01x0011                   |
|11| Operation enabled      | Quick stop active       | Quick Stop                           | xxxxxxxxxx000010 (0x0002)       | xxxxxxxx x00x0111                   |
|12| Quick stop active      | Switch on disabled      | Disable Voltage                      | xxxxxxxxxx000000 (0x0000)       | xxxxxxxx x1xx0000                   |
|10| Switched on            | Switch on disabled      | Disable Voltage                      | xxxxxxxxxx000000 (0x0000)       | xxxxxxxx x1xx0000                   |
|7| Ready to switch on     | Switch on disabled      | Disable Voltage                      | xxxxxxxxxx000000 (0x0000)       | xxxxxxxx x1xx0000                   |
|13| Operation enabled      | Fault reaction active   | Fehler erkannt (int. Übergang)       | Automatisch (kein Steuerwort)   | xxxxxxxx x0xx1111                   |
|14| Fault reaction active  | Fault                   | Intern nach Fehlerreaktion           | Automatisch (kein Steuerwort)   | xxxxxxxx x0xx1000                   |
|15| Fault                  | Switch on disabled      | Fault Reset                          | xxxxxxxx1xxxxxxx (0x0080)       | xxxxxxxx x1xx0000                   |
|(16)| Quick stop active      | Operation enabled      | Enable Operation (1)                  | xxxxxxxxxx001111 (0x000F)       | xxxxxxxx x01x0111                   |

Eine detaillierte Beschreibung ist in der CiA 402 Spezifikation enthalten.

**Hinweis:** 
(1) Die CiA 402 Spezifikation empfiehlt, Übergang 16 *nicht* zu implementieren.

### Controlword (6040h Objekt)

Das Controlword (Index 6040h) ist das zentrale Steuerobjekt, mit dem der Master den Zustand und das Verhalten des Antriebs steuert. Es handelt sich um ein 16-Bit-Wort, wobei jedes Bit (bzw. Bitgruppen) bestimmte Aktionen oder Anforderungen am Antrieb auslösen, wie Zustandswechsel oder Bewegungsbefehle.

#### Wichtige Bit-Funktionen

| Bit   | Name                    | Beschreibung                                  |
|-------|-------------------------|-----------------------------------------------|
| 0     | Switch On               | Fordert das Einschalten des Antriebs an       |
| 1     | Enable Voltage          | Schaltet die interne Spannungsversorgung frei |
| 2     | Quick Stop              | Fordert schnelles Stoppen der Bewegung an     |
| 3     | Enable Operation        | Vollständige Freischaltung der Achse          |
| 7     | Fault Reset             | Fehler quittieren/zurücksetzen                |
| 8     | Halt                    | Bewegung anhalten ohne den Antrieb zu deaktivieren |
| 9     | Operation Mode Specific | Wird in bestimmten Betriebsmodi verwendet     |
| 10    | Reserved                | -                                             |
| 11-15 | Hersteller-spezifisch   | -                                             |

Die Kombination und zeitliche Abfolge dieser Bits bestimmen exakt, wie die State Machine zwischen Zuständen wechselt. Zum Beispiel: Für den Wechsel von **Switch On Disabled** zu **Operation Enabled** müssen die Bits 0, 1 und 2 gesetzt werden, anschließend Bit 3. Vgl. hierzu auch das obige Diagramm und die Tabelle der Zustandsübergänge. 

### Statusword (6041h Objekt)

Das Statusword (Index 6041h) ist ein 16-Bit-Wort, das vom Antrieb an den Master gesendet wird und den aktuellen Status signalisiert. Durch das Auslesen des Statuswords erkennt der Master den aktuellen Zustand des Antriebs in der CiA 402 State Machine.

#### Repräsentative Bit-Bedeutungen

| Bit   | Name                    | Beschreibung                                    |
|-------|-------------------------|-------------------------------------------------|
| 0     | Ready to Switch On      | Antrieb ist bereit zum Freischalten             |
| 1     | Switched On             | Antrieb ist freigeschaltet                      |
| 2     | Operation Enabled       | Antrieb ist für Bewegungen freigegeben          |
| 3     | Fault                   | Fehler liegt vor                                |
| 4     | Voltage Enabled         | Power / Spannung für Antriebs-Endstufe liegt an                        |
| 5     | Quick Stop              | Reaktion auf Quick Stop Funktion ist aktiv                   |
| 6     | Switch On Disabled      | Antrieb ist deaktiviert                         |
| 7     | Warning                 | Warnung liegt vor (kein Fehler)                 |
| 8     | Manufacturer Specific   | (1)                                             |
| 9     | remote                  |   (2)   |
| 10    | target reached          | Position ist innerhalb der Ziel-Toleranz        |
| 11    | internal limit active   | Grenze laut 607D Objekten erreicht              |
| 12,13 | Operation Mode specific | -                                               |
| 14,15 | Manufacturer Specific    | -                                               |


**Hinweise:** 
(1) MovingCap und Festo-Antriebe nutzen dieses Bit für den Zustand **Drive Moving**.

(2) Das remote Bit hat bei MovingCap-Antrieben keine Bedeutung bzw. wird nicht gesetzt. Das Controlword wird auch bei remote = 0 ausgewertet. 

### Betriebsarten

Modes of Operation (Index 6060h) bestimmt den Betriebsmodus, in dem der Antrieb arbeitet. Jeder Modus unterstützt ein anderes Steuerparadigma (z.B. Positionsregelung, Geschwindigkeitsregelung, Drehmomentregelung).

#### 6060h Modes of Operation

| Wert (Dezimal)   | Mode Name                  | Anwendung                                               |
|------------------|---------------------------|---------------------------------------------------------|
| -128 bis -1      | Manufacturer Specific      | Hersteller-spezifisch                                   |
| 0                | Kein Modus zugeordnet      | -                                                       |
| 1                | Profile Position Mode      | Fährt Position mit definierten Profil                   |
| 2                | Velocity Mode              | (veraltet, meist nicht unterstützt, siehe Mode 3)       |
| 3                | Profile Velocity Mode      | Fährt Geschwindigkeit mit Profilbeschleunigung          |
| 4                | Profile Torque Mode        | Steuert Drehmoment gemäß Profil                         |
| 6                | Homing Mode                | Referenzfahrt ("Home"-Position anfahren)                |
| 7                | Interpolated Position Mode | Fährt nach interpolierten Positionpunkten               |
| 8                | Cyclic Synchronous Position| Synchrone Positionsregelung (Echtzeit)                  |
| 9                | Cyclic Synchronous Velocity| Synchrone Drehzahlregelung (Echtzeit)                   |
| 10               | Cyclic Synchronous Torque  | Synchrones Drehmoment (Echtzeit)                        |

Ein Servoantrieb unterstützt in der Regel nur einige der Betriebsmodi gemäß CiA 402. Häufig verwendete Modi sind
- 1 = Profile Position Mode,
- 3 = Profile Velocity Mode,
- 6 = Homing Mode,
- 8 = Cyclic Synchronous Position Mode.

Der aktuelle Modus kann mit **Modes of operation display** (6061h) ausgelesen werden.

### Profile Position Mode

**Profile Position Mode** (PPM,  6060h = 1) ist einer der grundlegenden Positionsregelungsmodi im CiA 402. In diesem Modus bewegt der Antrieb seine Last zu einer Zielposition entlang eines Bewegungsprofils. Dabei können Parameter wie Geschwindigkeit, Beschleunigung und Verzögerung eingestellt werden, was sanfte und kontrollierte Bewegungen ermöglicht. Der Modus eignet sich für Punkt-zu-Punkt-Positionierung, Ablaufbewegungen oder Indizierungsaufgaben.

#### Ablauf

1. **Modes of Operation** (6060h) auf 1 setzen (Profile Position Mode).
2. **Target position** (607Ah) und gewünschte Profilparameter setzen.
3. **Profile velocity** (6081h), **profile acceleration** (6083h) und **profile deceleration** (6084h) konfigurieren.
4. Mit dem **Controlword** (6040h) die Bewegung starten (z.B. durch Setzen des New Set-point Bits gemäß CiA 402).
5. **Statusword** (6041h) und **Position actual value** (6064h) überwachen, um die Abwicklung zu bestätigen.

#### Wichtige Objekte für Profile Positioning

| Index | Name                  | Beschreibung                                              |
|-------|----------------------|----------------------------------------------------------|
| 6060h | Modes of Operation    | Auf 1 setzen für Profile Position Mode                   |
| 607Ah | Target Position       | Zielposition                                             |
| 6081h | Profile Velocity      | Maximal zulässige Geschwindigkeit                       |
| 6083h | Profile Acceleration  | Beschleunigungsrate                                      |
| 6084h | Profile Deceleration  | Verzögerungsrate                                         |
| 6064h | Position Actual Value | Ist-Position                                             |
| 6040h | Controlword           | Bewegt auslösen und Status verwalten                     |
| 6041h | Statusword            | Rückmeldung zum Zustand                                 |

Optional/zusätzliche Objekte:
- 60F2h: Positioning Option Code (z.B. "relative" oder "absolute")
- 6073h: Max Current – Max. Strom/Drehmoment/Kraft für den Antrieb
- 607Dh.01h/607Dh.02h: Software Position Limit – Software-Endschalter

### Profile Velocity Mode

**Profile Velocity Mode** (PVM, 6060h = 3) ermöglicht es, die Achsgeschwindigkeit direkt vorzugeben, wobei profilierte Beschleunigungs- und Verzögerungsrampen eingehalten werden können. Typische Anwendungen finden sich beispielsweise bei Förderbändern, Lüftern oder anderen Systemen, in denen eine konstante Geschwindigkeit gefordert ist.

#### Ablauf

1. **Modes of Operation** (6060h) auf 3 setzen (Profile Velocity Mode).
2. **Target velocity** (60FFh) sowie gewünschte **profile acceleration/deceleration** (6083h/6084h) setzen.
3. **Controlword** (6040h) verwenden, um Start, Stop oder Geschwindigkeitsänderungen auszulösen.
4. **Velocity actual value** (606Ch) und **Statusword** (6041h) zur Überwachung auslesen.

#### Wichtige Objekte für Profile Velocity

| Index | Name                     | Beschreibung                                   |
|-------|--------------------------|-----------------------------------------------|
| 6060h | Modes of Operation       | Auf 3 setzen für Profile Velocity Mode         |
| 60FFh | Target Velocity          | Soll-Geschwindigkeit                           |
| 6083h | Profile Acceleration     | Beschleunigungsrampe                           |
| 6084h | Profile Deceleration     | Verzögerungsrampe                              |
| 606Ch | Velocity Actual Value    | Ist-Geschwindigkeit                            |
| 6040h | Controlword              | Steuerung Start/Stop/Halt                      |
| 6041h | Statusword               | Feedback und Zustandsüberwachung               |

### Wichtige Object Dictionary Einträge

Die folgende Tabelle enthält einige wichtige Einträge gemäß CiA 402 Device Profile, die für Antriebssteuerung und -überwachung zentral sind.

| Index  | Name                       | Beschreibung                                         | Typ        |
|--------|----------------------------|------------------------------------------------------|------------|
| 6040h  | Controlword                | Steuer- und Zustandswechsel (Master → Antrieb)       | unsigned16 |
| 6041h  | Statusword                 | Statusrückmeldung (Antrieb → Master)                 | unsigned16 |
| 6060h  | Modes of Operation         | Setzt Betriebsmodus des Antriebs                     | integer8   |
| 6061h  | Modes of Operation Display | Aktueller Betriebsmodus                              | integer8   |
| 607Ah  | Target Position            | Zielposition für Profile Position Mode               | integer32  |
| 6064h  | Position Actual Value      | Positionsrückmeldung                                 | integer32  |
| 606Ch  | Velocity Actual Value      | Geschwindigkeit (Istwert)                            | integer32  |
| 6081h  | Profile Velocity           | Max. Geschwindigkeit bei Profile Position Mode       | unsigned32 |
| 6083h  | Profile Acceleration       | Beschleunigungsrampe                                 | unsigned32 |
| 6084h  | Profile Deceleration       | Verzögerungsrampe                                    | unsigned32 |
| 60FFh  | Target Velocity            | Soll-Geschwindigkeit im Profile Velocity Mode        | integer32  |
| 6098h  | Homing Method              | Auswahl Homing-Strategie                             | integer8   |
| 607Dh.01h | Min position limit      | Software-Endschalter Minimum                         | integer32  |
| 607Dh.02h | Max position limit      | Software-Endschalter Maximum                         | integer32  |
| 6073h  | Max Current                | Max. Strom/Drehmoment/Kraft                          | unsigned16 |
| 6075h  | Motor Rated Current        | Nennstrom für Antrieb/Motor                          | unsigned32 |
| 6078h  | Current Actual Value       | Aktueller Motorstrom                                 | integer16  |

### Positionsskalierung / User-Defined Units

Positionsskalierung in CiA 402 kombiniert konfigurierbare Skalierungsparameter mit festen Motor-/Encoder-Eigenschaften, um interne Positionseinheiten (Inkremente) in anwenderspezifische/technische Einheiten umzuwandeln.

#### Motor-/Encoder-Systemeigenschaften (608Fh)

- **608Fh: Position Encoder Resolution**
  - `608Fh.01 encoder_increments`: Inkremente je Motordrehung
  - `608Fh.02 motor_revolutions`: Motordrehungen pro Encoderumdrehung
  - Beispiel: Bei einem 16-bit Inkremental-Encoder: `608Fh.01 = 65.536`, `608Fh.02 = 1` (üblicherweise 1, außer bei nicht 1:1-Getriebe zwischen Motor und Encoder)

**Hinweis:**  
Diese Werte spiegeln Hardware-Eigenschaften wider und sollten nur bei Hardwarewechsel verändert werden.

#### Konfigurierbare Skalierung (6091h und 6092h)

- **6091h: Gear Ratio**
  - `6091h.01h motor_revolutions`: Anzahl Motordrehungen
  - `6091h.02h shaft_revolutions` Anzahl Abtriebsumdrehungen
  - Beispiel: 5 Motordrehungen pro 2 Abtriebsumdrehungen → `6091h.01h = 5`, `6091h.02h = 2`

- **6092h: Feed Constant**
  - `6092h.01h feed`: Technische Einheit pro Abtriebsumdrehung (z.B. mm, μm)
  - `6092h.02h shaft_revolutions`: Anzahl Abtriebsumdrehungen
  - Beispiel: Zahnriemenachse mit 100 mm pro Umdrehung, Skala μm: `6092h.01h feed = 100.000`, `6092h.02h = 1`


#### Formeln zur Positionsskalierung

| Größe                                      | Formel (sprachlich)                                                    | Formel (mit CiA 402-Objekten)                                                                                                      |
|--------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Encoder resolution                         | Encoder_resolution = encoder_increments / motor_rev                      | 608Fh.01h / 608Fh.02h                                                                                                              |
| Gear ratio                                 | Gear_ratio = motor_revolutions / shaft_revolutions                       | 6091h.01h / 6091h.02h                                                                                                              |
| Feed constant                              | Feed_constant = feed  / shaft_revolutions                                | 6092h.01h / 6092h.02h                                                                                                              |
| Interne Positionseinheit                   | Pos_internal = Pos_user × Encoder_resolution × Gear_ratio / Feed_constant| Pos_user × (608Fh.01h / 608Fh.02h) × (6091h.01h / 6091h.02h) / (6092h.01h / 6092h.02h)                                             |
|                                            |                                                                          | oder: Pos_user × (608Fh.01h × 6091h.01h × 6092h.02h) / (608Fh.02h × 6091h.02h × 6092h.01h)                                        |
| Position als Anwendergröße                 | Pos_user = Pos_internal × Feed_constant / (Encoder_resolution × Gear_ratio) | Pos_internal × (6092h.01h / 6092h.02h) / [ (608Fh.01h / 608Fh.02h) × (6091h.01h / 6091h.02h) ]                                     |
|                                            |                                                                          | oder: Pos_internal × (608Fh.02h × 6091h.02h × 6092h.01h) / (608Fh.01h × 6091h.01h × 6092h.02h)                                    |

#### Beispiel

Gegeben:
- Motor-Encoder = 65.536 Inkremente je Motordrehung (`608Fh.01h = 65536`, `608Fh.02h = 1`)
- Gear ratio: 1 Abtriebsumdrehung pro 5 Motordrehungen (`6091h.01h = 5`, `6091h.02h = 1`)
- Feed constant: 100 mm pro Abtriebsumdrehung (`6092h.01h = 100`, `6092h.02h = 1`)

Gerechnet:

Anwendereinheit / user-defined unit pro internen Encoder-Inkrement 
= (Feed constant) / (Gear ratio × Encoder resolution) 
= (100 mm/U) / (5 × 65.536 Inkremente/U) 
= 0,00030517578125 [mm / Inkrement]

Beispiel: Position steht bei 80.000 interne Inkremente
Pos_user = 80.000 × 0.00030517578125 ≈ 24,41 mm

**Hinweis:**  
- Die Werte in 608Fh spiegeln Hardwareeigenschaften wider und sollten nur bei Hardwareänderung angepasst werden.
- Die Skalierungsparameter (6091h, 6092h) müssen zur Applikation und gewünschten Einheit passen.
- Die Einheit der feed constant (z.B. μm, mm, Grad) bestimmt die technische Größe für alle Positionswerte, die über die CiA 402-Objekte ausgetauscht werden.


### Glossar

| Begriff                       | Beschreibung                                                                                        |
|-------------------------------|-----------------------------------------------------------------------------------------------------|
| **CiA 301**                   | Kommunikationsprofil, definiert von CAN in Automation (CiA), das wesentliche CANopen-Anwendungsschichtdienste, -protokolle und -kommunikationsobjekte spezifiziert (u.a. NMT, PDO, SDO, SYNC, EMCY). Ursprünglich für CAN-basierte eingebettete Systeme entwickelt, bildet CiA 301 die Basis zahlreicher Geräteprofile, einschließlich CiA 402. Es findet auch Verwendung in weiteren Kommunikationstechnologien, insbesondere als \"CANopen over EtherCAT\" (CoE) von Beckhoff in EtherCAT-Systemen. Festgelegt in EN 50325-4.|
| **CiA 402 (DS 402)**          | Geräteprofil für elektrische Antriebe definiert von CAN in Automation (CiA). Es bietet ein universelles Interface und standardisiertes Verhalten zur Steuerung unterschiedlicher elektrischer Antriebe (z.B. Servoantriebe, Frequenzumrichter). Ursprünglich Bestandteil des CANopen-Protokolls als "CANopen Device Profile", es wird heute aber auch häufig eingesetzt für EtherCAT, POWERLINK, TCP/IP. Definiert in IEC61800-7-201 als standardisiertes Profil für elektrische Antriebssysteme (PDS).|
| **CAN (Controller Area Network)** | Robustes Kommunikationsbussystem Feldbus im Fahrzeugbereich und Automatisierung. |
| **CANopen**                       | Kommunikationsprotokoll und Gerätespezifikation für Automatisierung.    |
| **CiA (CAN in Automation)**       | Internationale Nutzer- und Herstellervereinigung für Entwicklung und Unterstützung CAN-basierter Protokolle.|
| **Objektverzeichnis (OD)**        | Standardisierte Tabelle für Organisation von Kommunikations- und Geräteparametern eines CANopen-Geräts.|
| **SDO (Service Data Object)**     | Protokoll für Peer-to-Peer-Kommunikation und Parameterzugriff in CANopen-Netzwerken.  |
| **PDO (Process Data Object)**     | Zeitkritisches Objekt zur Datenübertragung von Prozessdaten in Echtzeit.             |
| **NMT (Network Management)**      | Protokoll zur Verwaltung von Zuständen (Initialisierung, Pre-Operational, Operational, Stopped) in CANopen.|
| **SYNC-Objekt**                   | Synchronisationsobjekt für Knotenaktionen im Netzwerk.                          |
| **EMCY (Emergency Message)**      | Objekt zur sofortigen Meldung von Fehlern/Störungen an eine Steuerung.                 |
| **Antriebs-Zustandsautomat**      | Standardisierter Zustandsautomat (CiA 402) für Steuerung von Antriebszuständen und Übergängen.  |
| **Betriebsarten (Modes of Operation)**  | Betriebsarten für Bewegungssteuerung (Position, Geschwindigkeit, Homing).|
| **TPDO/RPDO (Transmit/Receive PDO)**  | Richtungsbezogenes PDO für Senden/Empfangen von Daten (TPDO/RPDO).                     |
| **Heartbeat/Node Guarding**       | Mechanismen zur Knotenüberwachung und Fehlererkennung im Netzwerk.                     |
| **Controller**                    | Netzwerk steuernder Knoten, z.B. Maschinensteuerung. Steuert andere Knoten; fungiert als NMT-Controller und SDO-Client. |
| **Device**                 | Gesteuerter Knoten, z.B. ein Servoantrieb. Vom Controller gesteuert; fungiert als NMT-Device und SDO-Server. |
| **SDO Client**            | Dienste anfragender Knoten / Controller. Fragt Daten vom SDO Server an. |
| **SDO Server**            | Dienste bereitstellender Knoten / Device. Antwortet auf Anfragen vom SDO Client. |

**Beispiel zur Verdeutlichung**:  
Eine CANopen PC-Software wie Kickdrive fungiert als NMT-Controller und SDO-Client, während ein CANopen-Knoten, z.B. ein Servoantrieb, als NMT-Device und SDO-Server agiert.
