#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from serial.tools import list_ports
import serial
import time

import sys
from PyQt4 import QtCore, QtGui, QtSql

class sync(QtGui.QWidget):
    def __init__(self):
        super(sync, self).__init__()

        self.button = QtGui.QPushButton("Synchroniser")
        self.button.clicked.connect(self._syncRoutine)

        self.label = QtGui.QLabel("")

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)

        self.disconnectUsbTimer = QtCore.QTimer(self)
        self.disconnectUsbTimer.timeout.connect(self._disconnectUsb)
        self.arduinoUsbTimer = QtCore.QTimer(self)
        self.arduinoUsbTimer.timeout.connect(self._arduinoUsb)

    """Routine de détection du port usb de l'arduino et de synchronisation"""
    def _syncRoutine(self):
        #Stop les timer qui étaient en cours
        self.disconnectUsbTimer.stop()
        self.arduinoUsbTimer.stop()
        self.label.setText("Veuillez deconnecter l'Arduino...")
        self._disconnectUsb()
        time.sleep(5)
        self._arduinoUsb()

    def _disconnectUsb(self):
        "Récupère une liste des usb (sans l'arduino)"
        self.disconnectedlistUSB = set(self._list_serial_ports()) #Liste des usb
        self.label.setText("Veuillez connecter l'Arduino...")

    def _arduinoUsb(self):
        print "ha"
        """Fait la différence avec la liste avec l'arduino connecté pour trouver le port utilisé"""
        arduinoUSB = [x for x in self._list_serial_ports() if x not in self.disconnectedlistUSB] #différence listes ubs

        """Si il n'y a eu qu'un changement on a trouvé l'arduino :)"""
        if len(arduinoUSB) == 1:
            self._synchro(arduinoUSB[0])
            self.label.setText("Synchronisation completee avec succes")
        else:
            self.label.setText("Probleme de detection de l'Arduino\nVeuillez reessayer")


    """Liste tous les ports usb"""
    def _list_serial_ports(self):
        # Windows
        if os.name == 'nt':
            # Scan for available ports.
            available = []
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    available.append('COM'+str(i + 1))
                    s.close()
                except serial.SerialException:
                    pass
            return available
        else:
            # Mac / Linux
            return [port[0] for port in list_ports.comports()]

    """Lit une valeur dans le serial, retourne un int"""
    def _readValue(self, ser):
        received = False
        while not received:
            try:
                value = ser.read(1).__repr__()
            except serial.SerialException:
                received = False
            else:
                if len(value) == 6:
                    value = int(value[3:4])
                    received = True
        return value

    """Synchronisation avec l'arduino"""
    def _synchro(self, usb):
        ser = serial.Serial(usb, 9600, timeout = 0.5) #Initialize connection
        """Collecte données"""
        value = 1
        mesures = []
        #Code de commencement de communication
        ser.write(chr(255))
        while value != 0:
            value = self._readValue(ser)
            mesures.append(value)

        mesures.pop() #Enlève le dernier 0

        """Sauve données dans db"""
        query = QtSql.QSqlQuery()
        for i in range(0, len(mesures)/10):

            """Transforme un nb <10 en espace+digit"""
            if len(mesures[(i*10)+6]) == 1:
                mesures[(i*10)+7] = "0" + mesures[(i*10)+6]
            if len(mesures[(i*10)+7]) == 1:
                mesures[(i*10)+6] = "0" + mesures[(i*10)+6]

            """Id de new User"""
            if mesures[(i*10)] == 255:
                mesures[(i*10)] = 0

            query.exec_("INSERT INTO mesures (utilisateur, poids, taille, temperature, frequence, time) mesures("+mesures[(i*10)]+", "+mesures[(i*10) + 2]+", "+mesures[(i*10)+1]+", "+str((float(mesures[(i*10)+3])/10)+ 35)+", "+mesures[(i*10)+4]+", DATETIME('20"+mesures[(i*10)+5]+"-"+mesures[(i*10)+6]+"-"+mesures[(i*10)+7]+" "+mesures[(i*10)+8]+":"+mesures[(i*10)+9]+":01'))")

        """Envois liste des utilisateurs"""
        query.exec_("SELECT id, nom, prenom FROM utilisateurs")
        while query.next():

            curId = query.value(0).toInt()[0] #Id utilisateur
            lastName = query.value(1).toString() #Nom
            firstName = query.value(2).toString() #Prénom

            for i in range(len(firstName), 5):
                firstName += " "

            ser.write(chr(curId))
            ser.write(str(lastName[0]))
            for i in range(0, 5):
                 ser.write(str(firstName[i]))

        ser.write(chr(0)) #Code de fin de transfert
        ser.close()
