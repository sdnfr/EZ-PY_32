# EZ-PY-32
Dieses Repository beinhaltet die Micropython-Implentierung der EZ-PY 32 Platine. Diese kann mit einem Uart-Programmiergerät, vorzugsweise CP2102 programmiert werden.

## Einrichtung
### Benötigte Software
* [esptool.py](https://github.com/espressif/esptool) 
* [ampy](https://github.com/scientifichackers/ampy)
* [micropython binaries](https://micropython.org/download/esp32/)

### Chip flashen
<br>
<code> esptool.py --chip esp32 --port PORT erase_flash </code>
<br>
<code> esptool.py --chip esp32 --port PORT write_flash -z 0x1000 MICROPYTHON.BIN </code>
<br>

### .py-Datein auf Chip kopieren

<br>
<code> ampy --port PORT put boot.py</code>
<br>
<code> ampy --port PORT put drivers </code>
<br>
<br>
<code> ampy --port PORT put model.py</code>
<br>
<code> ampy --port PORT put view.py</code>
<br>
<code> ampy --port PORT put controller.py</code>
<br>

Um sich mit dem WLAN verbinden zu können, muss noch eine Datei password.py erstellt werden, die pw und name essid (wlan name) wie folgt:

<code> essid = YOURWLANNAMESTRING </code>
<br>
<code> pw= YOURPASSWORDSTRING </code>
<br>

Zuletzt 
<br>
<code> ampy --port PORT put password.py</code>
<br>

Nun sollte das Board eingerichtet sein. Es können nun nach Belieben Dateien ergänzt oder verändert werden.
## Driver
### ILI9486 Display
Das Board enthält einen LCD Display mit ILI9486 IC, welcher mit einem 8Bit parallelem Datenbus arbeitet. Die Pins sind der Platine angepasst, können aber in drivers/ili9486py.py noch angepasst werden. Der Driver enthält bereits alle nötigen Helper-Funktionen, um auf dem Display etwas anzeigen zu können. Nach dem initialisieren können z.B. folgende Funktionen benutzt werden:

<br>
<code> import drivers/ili9486py as lcd</code>
<br>
<code> lcd.init()</code>
<br>
<code> lcd.fill_Screen(0xFFFF)</code>
<br>
<code> lcd.fill_Rect(x_=9,y_=0,w_=100,h_=200, c_=0xFFFF)</code>
<br>
<code> lcd.Draw_Pixe(x_=20,y_=45, c_=0xFFFF)</code>
<br>

Die Farben werden hier als 16 Bit Daten kodiert, wobei LSB Bit 0 bis Bit 4 für blau stehen(5 Bit), B5 bis B10 für grün (6 Bit) und B11 bis B15 MSB für rot (5 Bit). Also eine 5-6-5 RGB Farbkodierung.

Text kann mittels eines ASCII lcd-font-array ebenfalls ausgegeben werden wie folgt:

<br>
<code> lcd.Draw_Char(x_ = 20, y_ = 20, ch_ = 0x71, co_ = 0xFFFF, si_ = 2 )</code>
<br>
si_ ist hier die Textgröße. Es exisiteren auch zudem Higher-Level Funktionen die Texte mit Überschrift und Rahmen darstellen wie z.B.

<code> lcd.	display.Draw_Info_Box_Text(x=20,y=20,w=400,h=280,size = 2,heading="sample heading",body="sample body")</code>
<br>

### Drehencoder
Der Drehencoder benötigt bei Initialisierung 3 Callbacks, die jeweils per Interrupt ausgelöst werden, sobald der Encoder geklickt(OnClick), nach rechts im Uhrzeigersinn (onRight) oder nach links gegen Uhrzeigersinn (OnLeft) gedreht wird. 
<br>
<code> import drivers/encoder as enc</code>
<br>
<code> enc.init(onClick,onLeft,onRight)​</code>
<code>enc.setColorBin(0b101)​</code><br>
<code>enc.setColor(r=3,g=1,b=2)​</code><br>

<code>def onClick():​</code><br>
<code>[tab]   Pin.Toggle()</code><br>
<br>

Die Farbe des Drehencoders kann entweder binär bestimmt werden, als 3 Bit Farbe oder kann auch über PWM gesetzt werden. Hier hat jede Farbe 2 Bit, also insgesamt 6 Bit. Es muss aber dabei das Flag PWMEncoder auf True gesetzt werden, um diese Funktion zu aktivieren, da sich diese noch auf beta Stand befindet.

### ST7789 Display
Mit der SPI Schnittstelle kann zusätzlich ein Display bedient werden. Die Initialisierung erfolgt wie folgt:
<code>
    spi = machine.SPI(1, baudrate=27000000, polarity=1, sck = sck, mosi = mosi)
    display = st7789.ST7789(
        spi, 135, 240,
        reset=machine.Pin(23, machine.Pin.OUT),
        dc=machine.Pin(16, machine.Pin.OUT),
        cs=machine.Pin(5, machine.Pin.OUT)
    )</code>

Nun kann wie bei dem anderen Driver display.fill() oder display.fill_rect() aufgerufen werden.
## MVC Menü
Das Beispielprogramm ist nach dem üblichen MVC-Design-Pattern implementiert, welches es ermöglicht, modular zu arbeiten und neue Bildschirme und Funktionalitäten einfach zu ergänzen oder zu entfernen.
### Controller
Der Controller in controller.py ist das Herzstück des Beispielprogramms und verbindet die verschiedenen Bildschirme(Views) mit der Logik(Model). Im Hauptprogramm boot.py wird der Controller und die beiden Driver display und encoder initialisiert und dann in der while-Schleife führt der Controller ein update() durch. In diesem checkt er, ob die beiden Flags drawNewDisplay oder selectNewDisplay gesetzt wurden, welche in den callback-Funktionen des Encoders gesetzt werden. Wird der Encoder benutzt, ruft es die jeweilige callback-Funktion im Controller auf, der sich dann darum kümmert die entsprechenden Flags zu setzen. Abhängig von diesen kümmert sich dann der Controller, das die richtige View ausgegeben wird. Hierzu verwaltet der Controller die verschiedenen views als dictionary-Objekte. Über die zugewiesene print-Funktion kann dieser dann die view anzeigen lassen, und übergibt ihr die notwendigen Parameter die aus dem Model kommen.

### Model
Das Model hat die Aufgabe, die Logik der gewünschten Funktionen zu berechnen. Sobald der Controller die notwendigen Parameter braucht, ruft er hier die jeweiligen Funktionen auf, die bereits bei Initialisierung erstellt wurden. Optional ist es auch möglich, diese in einer refresh-Methode erneut zu berechnen. 

### View
Die View ist zuständig dafür, die von der Logik stammenden und vom Controller bereitgestellten Daten darzustellen. Diese Darstellung wird in einer print-Funktion ausgeführt, die vom Controller zum benötigten Zeitpunkt ausgewählt wird. Im Fall dass in der View auch noch Objekte ausgewählt werden können, benötigt der Controller Daten über diese Objekte welche in den getSelector-Funktionen bereitgestellt werden. 

## Common Workflows
### Neue Funktionalität hinzufügen
Hierfür müssen alle 3 Komponenten des MWC Patterns verändert werden:
* Dem Controller muss ein neues view-Objekt hinzugefügt werden, dass dem Hauptdisplay main als display zugeordnet werden muss. Anschließend muss eine draw(print) und getSelectors-Funktion aus dem zugehörigen view file zugeordnet werden. Falls Argumente berechnet werden müssen, werden diese über args bzw. einer refresh-Methode aus dem model ebenso zugewiesen.
* Im Model kann nun die Funktionalität der neuen Funktionen hinzugefügt werden. Wichtig ist dass diese im Controller aufgerufen wird. Um die verschiedenen Funktionen zur Übersichtlichkeit zu trennen, kann das model aufgeteilt werden in models/model_funktion1.py und models/model_funktion2.py. Der Controller kann dann das jeweilige Model für die jeweilige View auswählen. Momentan ist die WLAN Funktionalität im einzigen Model integriert.
* Das View file braucht nun eine print-Methode, die dem Controller zugeteilt wurde. Hier kann nun sich ausschließlich um die Darstellung der optionalen Argumente gekümmert werden. Ebenso ist es möglich, einzelne view-files anzulegen, falls die Darstellung komplexer wird. 
### Neue Driver hinzufügen
Ziel des EZ-PY 32 Boards ist es, dieses als Ergänzung zu eigenen Entwicklerboards/Sensoren/Aktoren zu benutzen. Das Github Repository sollte dazu genutzt werden, um weitere Driver für Boards zu ergänzen, um die Funktionalitäten zu erweitern. Hardware Driver können dann im drivers Ordner gerne via pull-request hinzugefügt werden. Damit kann dann der Driver in boot.py initialisiert werden, und im Model dann benutzt werden, und dessen Auswertung via Controller in der view auch ausgegeben werden können. Zusätzlich kann auch die Encoder-Farbe als view genutzt werden.

### Neue Bitmaps hinzufügen
Die Bitmaps müssen im data.json als eindimensionales Array mit 40x60 Byte insgesamt hinzugefügt werden. Momentan (Stand 06.01.2021) befindet sich die drawBitmap noch in der Display Driver Bibliothek, sollte aber in ein model_bitmap verschoben werden. 
## Disclaimer
Der Sourcecode ist ''subject to change'' und daher wird die Code-Dokumentation im github repository so weit wie möglich zu pflegen versucht. Dieses Readme dient nur als Quick Start Guide, und die Dokumentation soll im Code gepflegt werden.
