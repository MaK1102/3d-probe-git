import serial
import time
import threading
import schiefe_ebene


class BackgroundTasks(threading.Thread):
    def run(self, *args):
        self.stop = False  # wird benöting um es zu stoppen
        self.exit = False
        self.verbindung = False
        self.s_value = []  # gibt die Messdaten für andere Programme frei
        self.boot(3, 4)  # start die verbindung mit dem arduino
        self.n = 0
        while self.stop == False:  # wiederholt solange bis stop == True
            self.n +=1
            try:
                data = str(self.arduino.readline()).strip("\ brn'")  # entfernt unötige zeichen
            except:
                self.verbindung = False
                self.run()
            data = data.split(":")  # zerlegt den Datensatz in Sensornummer und wert
            # print(self.s_value)
            try:
                try:
                    schiefe_ebene.p.s[int(data[0])].posz = float(data[1]) / 100 # aktualisiert den Sensor wert
                except:
                    if len(data) == 1:
                        print("keine Daten")
                    else:
                        print("daten konnten nicht gespeichert werden.")
            except IndexError:  # Falls der arduino keine daten sendent (ist für die ersten zyklen zu erwarten)
                print("keine Daten")
                None
        while self.stop == True:
            if self.exit == True:
                break
            time.sleep(0.1)
        if self.exit == True:
            return
        self.run()

    def write(self, command):
        match command:
            case "touch":
                x = 1
        self.arduino.write(bytes(str(x), 'utf-8'))

    def boot(self, *com, trys=5):
        self.verbindung = 2
        for n in range(trys):
            if self.stop == True:
                break
            for num in com:
                try:
                    port = f"COM{num}"
                    self.arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)  # setzt die arduino verbindung
                    self.verbindung = True
                    print(f"Verbingung mit Port {port} hergestellt")
                    return
                except:
                    print(f"Error: Verbindung mit {port} konnte nicht Hergestellt werden \n Versuch Nummer {n + 1}")
            if n + 1 != trys:
                print(" Neu versuch in 5s")
                time.sleep(1)
        print(f"Die Anzahl der versuche wurde Überschritten, Es gab {n + 1} versuche")
        self.verbindung = False
        self.stop = True


t = BackgroundTasks()
t.start()


def stop():
    t.stop = True


def go():
    t.stop = False


def exit():
    t.exit = True
